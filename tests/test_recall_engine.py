"""Tests for the recall engine.

These tests double as the spec: each test name is a complete sentence describing
a user-visible behavior of the snapshot-mode SM-2 lite recall queue.
"""

from __future__ import annotations

from datetime import date
from pathlib import Path

import pytest

from recall_engine import (
    CategoryProgress,
    CurriculumPhase,
    Mock,
    Problem,
    Readiness,
    ReadinessTier,
    SDChapter,
    Touch,
    aggregate_touches,
    append_to_ledger,
    avg_new_per_day,
    compute_new,
    compute_readiness,
    compute_recall,
    day_n_for,
    due_date,
    interval_for,
    load_ledger,
    load_mocks,
    load_sd_chapters,
    next_sd_chapter,
    overdue_days,
    parse_completions,
    parse_curriculum,
    parse_phases,
    phase_for,
    projected_end_date,
    recompute,
    render_coverage,
    render_readiness_block,
    render_today,
    start_date,
    upcoming_mocks,
)


# ─── SM-2 lite interval expansion ──────────────────────────────────────────────


@pytest.mark.parametrize(
    "touches,expected_interval_days",
    [(1, 1), (2, 3), (3, 7), (4, 21), (5, 60), (6, 60), (10, 60)],
    ids=[
        "a problem solved once is due 1 day later",
        "a problem solved twice is due 3 days later",
        "a problem solved three times is due 7 days later",
        "a problem solved four times is due 21 days later",
        "a problem solved five times is due 60 days later",
        "the sixth solve does not extend the interval beyond 60 days",
        "extra solves past five never push the interval beyond 60 days",
    ],
)
def test_sm2_lite_interval_expansion(touches: int, expected_interval_days: int) -> None:
    assert interval_for(touches) == expected_interval_days


# ─── Overdue arithmetic ────────────────────────────────────────────────────────


@pytest.mark.parametrize(
    "touches,last_touched,today,expected_overdue",
    [
        (1, date(2026, 5, 6), date(2026, 5, 6), -1),
        (1, date(2026, 5, 6), date(2026, 5, 7), 0),
        (1, date(2026, 5, 6), date(2026, 5, 8), 1),
        (5, date(2026, 4, 1), date(2026, 5, 31), 0),
        (5, date(2026, 4, 1), date(2026, 6, 30), 30),
    ],
    ids=[
        "a problem solved today is not yet due tomorrow",
        "a problem due today reads as zero days overdue",
        "a once-solved problem skipped one day reads as one day overdue",
        "a five-times-solved problem becomes due exactly sixty days later",
        "a five-times-solved problem can be ignored two months before going overdue",
    ],
)
def test_overdue_days_calculation(
    touches: int, last_touched: date, today: date, expected_overdue: int
) -> None:
    assert overdue_days(touches, last_touched, today) == expected_overdue


def test_due_date_is_last_touched_plus_sm2_interval() -> None:
    assert due_date(1, date(2026, 5, 6)) == date(2026, 5, 7)
    assert due_date(3, date(2026, 5, 6)) == date(2026, 5, 13)


# ─── Touch aggregation ─────────────────────────────────────────────────────────


def test_aggregate_touches_counts_completions_per_problem() -> None:
    ledger = [
        Touch("[A] Two Sum", date(2026, 5, 1)),
        Touch("[A] Two Sum", date(2026, 5, 4)),
        Touch("[A] Group Anagrams", date(2026, 5, 6)),
    ]
    assert aggregate_touches(ledger) == {
        "[A] Two Sum": (2, date(2026, 5, 4)),
        "[A] Group Anagrams": (1, date(2026, 5, 6)),
    }


def test_aggregate_touches_tracks_only_the_latest_completion_date() -> None:
    """If the user solves the same problem twice on different days, the schedule
    should reset from the most recent completion, not the first."""
    ledger = [
        Touch("[A] Two Sum", date(2026, 5, 1)),
        Touch("[A] Two Sum", date(2026, 5, 8)),
        Touch("[A] Two Sum", date(2026, 5, 4)),  # out-of-order entry
    ]
    aggregated = aggregate_touches(ledger)
    assert aggregated["[A] Two Sum"] == (3, date(2026, 5, 8))


# ─── Recall ranking and filtering ──────────────────────────────────────────────


def test_recall_ranks_the_most_overdue_problem_first() -> None:
    ledger = [
        Touch("[A] Two Sum", date(2026, 5, 1)),  # 1× → due May 2 → 5d overdue on May 7
        Touch("[A] Group Anagrams", date(2026, 5, 5)),  # 1× → due May 6 → 1d overdue
        Touch("[A] Valid Anagram", date(2026, 5, 6)),  # 1× → due May 7 → 0d overdue
    ]
    recall = compute_recall(ledger, today=date(2026, 5, 7), limit=10)
    assert [r.problem for r in recall] == [
        "[A] Two Sum",
        "[A] Group Anagrams",
        "[A] Valid Anagram",
    ]


def test_recall_caps_at_the_requested_limit_when_more_items_are_overdue() -> None:
    ledger = [Touch(f"[X] P{i}", date(2026, 5, 1)) for i in range(15)]
    recall = compute_recall(ledger, today=date(2026, 5, 7), limit=10)
    assert len(recall) == 10


def test_recall_excludes_problems_whose_due_date_has_not_yet_arrived() -> None:
    ledger = [
        Touch("[A] Two Sum", date(2026, 5, 4)),
        Touch("[A] Two Sum", date(2026, 5, 6)),  # 2× → 3d interval → due May 9
    ]
    recall = compute_recall(ledger, today=date(2026, 5, 7), limit=10)
    assert recall == []


def test_recall_is_empty_when_no_problem_has_ever_been_touched() -> None:
    assert compute_recall(ledger=[], today=date(2026, 5, 7), limit=10) == []


def test_recall_item_carries_metadata_for_rendering() -> None:
    ledger = [Touch("[A] Two Sum", date(2026, 5, 1))]
    recall = compute_recall(ledger, today=date(2026, 5, 7), limit=10)
    [item] = recall
    assert item.problem == "[A] Two Sum"
    assert item.touches == 1
    assert item.last_touched == date(2026, 5, 1)
    assert item.days_overdue == 5


# ─── New (next-up) selection ───────────────────────────────────────────────────


CURRICULUM = [
    Problem("[A] P1", source_day=1),
    Problem("[A] P2", source_day=1),
    Problem("[A] P3", source_day=2),
    Problem("[A] P4", source_day=2),
    Problem("[A] P5", source_day=3),
]


def test_new_picks_the_first_three_unchecked_source_day_problems_in_order() -> None:
    new = compute_new(CURRICULUM, ledger=[], limit=3)
    assert [p.text for p in new] == ["[A] P1", "[A] P2", "[A] P3"]


def test_new_advances_past_problems_already_in_the_ledger() -> None:
    ledger = [
        Touch("[A] P1", date(2026, 5, 6)),
        Touch("[A] P3", date(2026, 5, 6)),
    ]
    new = compute_new(CURRICULUM, ledger, limit=3)
    assert [p.text for p in new] == ["[A] P2", "[A] P4", "[A] P5"]


def test_new_surfaces_yesterdays_skipped_problems_first_in_document_order() -> None:
    """If you skip Day 1 problems, the next morning they appear in New ahead of
    Day 2 — no manual rescheduling needed."""
    ledger = [Touch("[A] P1", date(2026, 5, 6))]
    new = compute_new(CURRICULUM, ledger, limit=3)
    assert [p.text for p in new] == ["[A] P2", "[A] P3", "[A] P4"]


def test_new_returns_fewer_than_limit_when_curriculum_is_exhausted() -> None:
    ledger = [Touch(p.text, date(2026, 5, 6)) for p in CURRICULUM[:-1]]
    new = compute_new(CURRICULUM, ledger, limit=3)
    assert [p.text for p in new] == ["[A] P5"]


# ─── Curriculum parser ─────────────────────────────────────────────────────────


SAMPLE_DAILY_MD = """\
# Header

## Today (live)

- [ ] this checkbox is in the dashboard, ignore

## Day 0 — Setup (Tue May 5)

- [ ] Anki desktop installed
- [ ] uv installed

## Phase 1 — Arrays/Hashing (Days 1–6, 4/day)

### Day 1 — Wed May 6 (4)

- **9:00–13:00 DSA New (4):**
  - [ ] [Arrays & Hashing] -> Contains Duplicate
  - [ ] [Arrays & Hashing] -> Valid Anagram
- **14:00–15:30 System Design:**
  - [ ] Grokking SD Fundamentals — intro
- **15:30–19:30 Consolidation:**
  - **Recall queue:** open the [Today](#today-live) dashboard.
  - [ ] today's hardest: ___

### Day 2 — Thu May 7 (4)

- **9:00–13:00 DSA New (4):**
  - [ ] [Arrays & Hashing] -> Two Sum
  - [ ] [Two Pointers] -> Trapping Rain Water `T2`
"""


def test_curriculum_parser_extracts_every_dsa_new_problem() -> None:
    problems = parse_curriculum(SAMPLE_DAILY_MD)
    assert [p.text for p in problems] == [
        "[Arrays & Hashing] -> Contains Duplicate",
        "[Arrays & Hashing] -> Valid Anagram",
        "[Arrays & Hashing] -> Two Sum",
        "[Two Pointers] -> Trapping Rain Water",
    ]


def test_curriculum_parser_tags_each_problem_with_its_source_day() -> None:
    problems = parse_curriculum(SAMPLE_DAILY_MD)
    assert [(p.text, p.source_day) for p in problems] == [
        ("[Arrays & Hashing] -> Contains Duplicate", 1),
        ("[Arrays & Hashing] -> Valid Anagram", 1),
        ("[Arrays & Hashing] -> Two Sum", 2),
        ("[Two Pointers] -> Trapping Rain Water", 2),
    ]


def test_curriculum_parser_strips_the_T2_marker_from_canonical_text() -> None:
    """The vestigial `T2` marker on a few problems must not contaminate the
    canonical key — otherwise the same problem would appear twice in the ledger."""
    problems = parse_curriculum(SAMPLE_DAILY_MD)
    trapping = next(p for p in problems if "Trapping" in p.text)
    assert trapping.text == "[Two Pointers] -> Trapping Rain Water"


def test_curriculum_parser_ignores_non_problem_checkboxes() -> None:
    problems = parse_curriculum(SAMPLE_DAILY_MD)
    texts = {p.text for p in problems}
    assert "Anki desktop installed" not in texts
    assert "Grokking SD Fundamentals — intro" not in texts
    assert "today's hardest: ___" not in texts


def test_curriculum_parser_ignores_problems_outside_a_day_section() -> None:
    """Day 0 setup checkboxes look like tasks but aren't curriculum problems."""
    problems = parse_curriculum(SAMPLE_DAILY_MD)
    assert all(p.source_day >= 1 for p in problems)


# ─── Completion parser ────────────────────────────────────────────────────────


def test_completion_parser_captures_problems_with_a_done_date_stamp() -> None:
    md = (
        "- [x] [A] -> Two Sum ✅ 2026-05-06\n"
        "- [x] [A] -> Group Anagrams ✅ 2026-05-06\n"
        "- [ ] [A] -> Valid Anagram\n"
    )
    assert parse_completions(md) == [
        Touch("[A] -> Two Sum", date(2026, 5, 6)),
        Touch("[A] -> Group Anagrams", date(2026, 5, 6)),
    ]


def test_completion_parser_ignores_unchecked_lines() -> None:
    assert parse_completions("- [ ] [A] -> P1") == []


def test_completion_parser_ignores_checked_lines_without_a_date_stamp() -> None:
    """Without a date we cannot schedule the next review — better to skip silently
    than to invent a date."""
    assert parse_completions("- [x] [A] -> P1") == []


def test_completion_parser_strips_metadata_suffix_from_canonical_text() -> None:
    """today.md adds an em-dash annotation like ` — 1d overdue · 1× · last May 6`.
    The canonical key must match the curriculum form, not the annotated render."""
    md = "- [x] [A] -> Two Sum — 1d overdue · 1× · last May 6 ✅ 2026-05-07"
    assert parse_completions(md) == [Touch("[A] -> Two Sum", date(2026, 5, 7))]


def test_completion_parser_strips_source_day_annotation() -> None:
    """The New section appends ` (Day N)` for context — strip it for the ledger."""
    md = "- [x] [A] -> Valid Anagram (Day 1) ✅ 2026-05-06"
    assert parse_completions(md) == [Touch("[A] -> Valid Anagram", date(2026, 5, 6))]


def test_completion_parser_strips_T2_marker() -> None:
    md = "- [x] [Two Pointers] -> Trapping Rain Water `T2` ✅ 2026-05-09"
    assert parse_completions(md) == [
        Touch("[Two Pointers] -> Trapping Rain Water", date(2026, 5, 9))
    ]


# ─── Ledger I/O ──────────────────────────────────────────────────────────────


def test_ledger_round_trips_a_single_touch(tmp_path: Path) -> None:
    path = tmp_path / "completions.jsonl"
    append_to_ledger(path, [Touch("[A] Two Sum", date(2026, 5, 6))])
    assert load_ledger(path) == [Touch("[A] Two Sum", date(2026, 5, 6))]


def test_ledger_records_separate_touches_on_different_days(tmp_path: Path) -> None:
    """Two valid completions of the same problem on different days must both land
    in the ledger so the touch counter can grow."""
    path = tmp_path / "completions.jsonl"
    append_to_ledger(
        path,
        [
            Touch("[A] Two Sum", date(2026, 5, 6)),
            Touch("[A] Two Sum", date(2026, 5, 9)),
        ],
    )
    assert len(load_ledger(path)) == 2


def test_ledger_dedupes_a_repeated_completion_on_the_same_day(tmp_path: Path) -> None:
    """Re-running recompute on a today.md that hasn't changed should not double-log
    yesterday's completions."""
    path = tmp_path / "completions.jsonl"
    append_to_ledger(path, [Touch("[A] Two Sum", date(2026, 5, 6))])
    appended = append_to_ledger(path, [Touch("[A] Two Sum", date(2026, 5, 6))])
    assert appended == 0
    assert load_ledger(path) == [Touch("[A] Two Sum", date(2026, 5, 6))]


def test_ledger_returns_empty_list_when_no_file_exists(tmp_path: Path) -> None:
    """First-run case — no completions yet, no file yet."""
    assert load_ledger(tmp_path / "does-not-exist.jsonl") == []


# ─── End-to-end recompute ────────────────────────────────────────────────────


THREE_DAY_CURRICULUM_MD = """\
## Phase 1

### Day 1 — Mon May 6

- **9:00–13:00 DSA New:**
  - [ ] [A] -> P1
  - [ ] [A] -> P2

### Day 2 — Tue May 7

- **9:00–13:00 DSA New:**
  - [ ] [A] -> P3
  - [ ] [A] -> P4

### Day 3 — Wed May 8

- **9:00–13:00 DSA New:**
  - [ ] [A] -> P5
"""


def test_recompute_creates_today_md_on_first_run(tmp_path: Path) -> None:
    """Day 1 morning: nothing exists yet. Recompute generates today's set."""
    daily = tmp_path / "prep-plan-daily.md"
    daily.write_text(THREE_DAY_CURRICULUM_MD)
    today_md = tmp_path / "today.md"
    ledger = tmp_path / "completions.jsonl"

    result = recompute(daily, today_md, ledger, today=date(2026, 5, 6))

    assert today_md.exists()
    text = today_md.read_text()
    assert "[A] -> P1" in text
    assert "[A] -> P2" in text
    assert result.new_size >= 1
    assert result.recall_size == 0
    assert result.new_touches_logged == 0


def test_recompute_logs_yesterday_completions_into_the_ledger(tmp_path: Path) -> None:
    """Tomorrow morning: previous today.md has a checked, dated item. Recompute
    folds that touch into the ledger before regenerating today.md."""
    daily = tmp_path / "prep-plan-daily.md"
    daily.write_text(THREE_DAY_CURRICULUM_MD)
    ledger = tmp_path / "completions.jsonl"
    today_md = tmp_path / "today.md"
    today_md.write_text("- [x] [A] -> P1 (Day 1) ✅ 2026-05-06\n")

    result = recompute(daily, today_md, ledger, today=date(2026, 5, 7))

    assert result.new_touches_logged == 1
    assert load_ledger(ledger) == [Touch("[A] -> P1", date(2026, 5, 6))]


def test_recompute_surfaces_yesterdays_completion_into_recall_the_next_day(
    tmp_path: Path,
) -> None:
    """A problem solved on May 6 with 1 touch is due May 7 — it should appear in
    the May 7 Recall section after recompute folds the touch into the ledger."""
    daily = tmp_path / "prep-plan-daily.md"
    daily.write_text(THREE_DAY_CURRICULUM_MD)
    ledger = tmp_path / "completions.jsonl"
    today_md = tmp_path / "today.md"
    today_md.write_text("- [x] [A] -> P1 (Day 1) ✅ 2026-05-06\n")

    recompute(daily, today_md, ledger, today=date(2026, 5, 7))

    text = today_md.read_text()
    assert "## Recall" in text
    # P1 is now overdue 0 days (due exactly today) and should appear in Recall.
    recall_section = text.split("## New")[0]
    assert "[A] -> P1" in recall_section


def test_recompute_does_not_relog_when_run_twice_with_no_new_completions(
    tmp_path: Path,
) -> None:
    """Snapshot semantics: rerunning recompute mid-day must not corrupt the
    ledger. Each completion gets logged exactly once regardless of how many
    times the user triggers a refresh."""
    daily = tmp_path / "prep-plan-daily.md"
    daily.write_text(THREE_DAY_CURRICULUM_MD)
    ledger = tmp_path / "completions.jsonl"
    today_md = tmp_path / "today.md"
    today_md.write_text("- [x] [A] -> P1 (Day 1) ✅ 2026-05-06\n")

    first = recompute(daily, today_md, ledger, today=date(2026, 5, 7))
    # User did not check anything else; a manual mid-day re-run should be a no-op
    # for the ledger. (today.md is rewritten but contains the same canonical set.)
    second = recompute(daily, today_md, ledger, today=date(2026, 5, 7))

    assert first.new_touches_logged == 1
    assert second.new_touches_logged == 0
    assert len(load_ledger(ledger)) == 1


def test_recompute_advances_new_section_past_completed_curriculum_problems(
    tmp_path: Path,
) -> None:
    """After P1 is logged as solved, today's New section should not surface P1
    again — it advances to the next unsolved curriculum problem."""
    daily = tmp_path / "prep-plan-daily.md"
    daily.write_text(THREE_DAY_CURRICULUM_MD)
    ledger = tmp_path / "completions.jsonl"
    today_md = tmp_path / "today.md"
    today_md.write_text("- [x] [A] -> P1 (Day 1) ✅ 2026-05-06\n")

    recompute(daily, today_md, ledger, today=date(2026, 5, 7))

    text = today_md.read_text()
    new_section = text.split("## New")[1] if "## New" in text else ""
    assert "[A] -> P1" not in new_section


# ─── Renderer ────────────────────────────────────────────────────────────────


def test_renderer_produces_an_empty_recall_message_when_nothing_is_overdue() -> None:
    out = render_today(today=date(2026, 5, 6), recall=[], new=[Problem("[A] P1", 1)])
    assert "## Recall" in out
    assert "## New" in out
    # Some explicit empty-state copy so the user knows the section is intentionally empty.
    assert "Empty" in out or "empty" in out


def test_renderer_includes_a_dated_header_for_orientation() -> None:
    out = render_today(today=date(2026, 5, 6), recall=[], new=[])
    assert "May 6" in out or "2026-05-06" in out


# ─── Difficulty + source tags ─────────────────────────────────────────────────


_TAGGED_DAILY_MD = """\
### Day 1 — Mon May 11

- **9:00–13:00 DSA New:**
  - [ ] [Arrays & Hashing] -> Contains Duplicate (E)
  - [ ] [Arrays & Hashing] -> Group Anagrams (M)

### Day 40 — Hard problems

- **9:00–13:00 DSA New:**
  - [ ] [Two Pointers] -> Trapping Rain Water (H)

### Day 54 — Beyond-NC150 patterns

- **9:00–13:00 DSA New:**
  - [ ] [Boyer-Moore] -> Majority Element II (M) (nc-150+)
  - [ ] [Segment Tree] -> Count of Smaller After Self (H) (nc-150+)
  - [ ] [Arrays & Hashing] -> Customers With 2-Day 2-Page Visits (M) (company question)
"""


def test_curriculum_parser_extracts_difficulty_marker() -> None:
    problems = parse_curriculum(_TAGGED_DAILY_MD)
    by_text = {p.text: p for p in problems}
    assert by_text["[Arrays & Hashing] -> Contains Duplicate"].difficulty == "E"
    assert by_text["[Arrays & Hashing] -> Group Anagrams"].difficulty == "M"
    assert by_text["[Two Pointers] -> Trapping Rain Water"].difficulty == "H"


def test_curriculum_parser_defaults_source_to_nc_150_when_no_source_tag() -> None:
    """NC150 problems carry only a difficulty marker; their source is implicitly 'nc-150'."""
    problems = parse_curriculum(_TAGGED_DAILY_MD)
    by_text = {p.text: p for p in problems}
    assert by_text["[Arrays & Hashing] -> Contains Duplicate"].source == "nc-150"


def test_curriculum_parser_extracts_explicit_source_marker() -> None:
    problems = parse_curriculum(_TAGGED_DAILY_MD)
    by_text = {p.text: p for p in problems}
    assert by_text["[Boyer-Moore] -> Majority Element II"].source == "nc-150+"
    assert by_text["[Segment Tree] -> Count of Smaller After Self"].source == "nc-150+"
    assert (
        by_text["[Arrays & Hashing] -> Customers With 2-Day 2-Page Visits"].source
        == "company question"
    )


def test_curriculum_parser_canonical_text_omits_difficulty_and_source_tags() -> None:
    """Ledger keys must match across renders, so the canonical text excludes
    annotations the renderer might add or drop."""
    problems = parse_curriculum(_TAGGED_DAILY_MD)
    texts = {p.text for p in problems}
    for t in texts:
        assert "(E)" not in t and "(M)" not in t and "(H)" not in t
        assert "(nc-150+)" not in t and "(company question)" not in t


def test_completion_parser_strips_difficulty_tag_from_canonical() -> None:
    """A checked line in today.md carries `(E) (Day 1)`-style annotations that the
    parser must strip to produce a ledger key matching the curriculum."""
    md = "- [x] [Arrays & Hashing] -> Contains Duplicate (E) (Day 1) ✅ 2026-05-11"
    assert parse_completions(md) == [
        Touch("[Arrays & Hashing] -> Contains Duplicate", date(2026, 5, 11))
    ]


def test_completion_parser_strips_source_tag_from_canonical() -> None:
    md = "- [x] [Segment Tree] -> Count of Smaller After Self (H) (nc-150+) (Day 54) ✅ 2026-07-03"
    assert parse_completions(md) == [
        Touch("[Segment Tree] -> Count of Smaller After Self", date(2026, 7, 3))
    ]


def test_completion_parser_strips_variant_of_tag_from_canonical() -> None:
    """`(variant of: X)` is human-readable lineage info; ledger keys must
    match the same problem text whether the tag is present or not."""
    md = "- [x] [1-D DP] -> House Robber II (M) (variant of: House Robber) (Day 31) ✅ 2026-06-10"
    assert parse_completions(md) == [
        Touch("[1-D DP] -> House Robber II", date(2026, 6, 10))
    ]


def test_curriculum_parser_canonical_text_omits_variant_of_tag() -> None:
    md = """\
### Day 31 — Wed Jun 10

- **9:00–13:00 DSA New:**
  - [ ] [1-D DP] -> House Robber II (M) (variant of: House Robber)
"""
    problems = parse_curriculum(md)
    assert len(problems) == 1
    assert problems[0].text == "[1-D DP] -> House Robber II"


# ─── compute_new source-tier ordering ─────────────────────────────────────────


def test_compute_new_prefers_nc_150_over_nc_150_plus_in_same_day() -> None:
    """The engine surfaces NC150 problems before non-NC150 patterns regardless
    of document position within a day."""
    curriculum = [
        Problem("[X] beyond-1", source_day=54, difficulty="M", source="nc-150+"),
        Problem("[X] core-nc-1", source_day=54, difficulty="M", source="nc-150"),
        Problem("[X] beyond-2", source_day=54, difficulty="H", source="nc-150+"),
        Problem("[X] core-nc-2", source_day=54, difficulty="M", source="nc-150"),
    ]
    new = compute_new(curriculum, ledger=[], limit=2)
    assert [p.text for p in new] == ["[X] core-nc-1", "[X] core-nc-2"]


def test_compute_new_falls_through_to_nc_150_plus_then_company_when_nc_150_is_drained() -> None:
    curriculum = [
        Problem("[X] nc-only", source_day=54, difficulty="M", source="nc-150"),
        Problem("[X] beyond-thing", source_day=54, difficulty="M", source="nc-150+"),
        Problem("[X] company-thing", source_day=54, difficulty="H", source="company question"),
    ]
    ledger = [Touch("[X] nc-only", date(2026, 7, 3))]
    new = compute_new(curriculum, ledger, limit=2)
    assert [p.text for p in new] == ["[X] beyond-thing", "[X] company-thing"]


def test_compute_new_within_a_source_tier_preserves_document_order() -> None:
    curriculum = [
        Problem("[X] P3", source_day=2, difficulty="M", source="nc-150"),
        Problem("[X] P1", source_day=1, difficulty="M", source="nc-150"),
        Problem("[X] P2", source_day=1, difficulty="M", source="nc-150"),
    ]
    new = compute_new(curriculum, ledger=[], limit=3)
    assert [p.text for p in new] == ["[X] P3", "[X] P1", "[X] P2"]


# ─── Difficulty surfaced in renderer ───────────────────────────────────────────


def test_recall_item_carries_difficulty_when_curriculum_is_provided() -> None:
    curriculum = [
        Problem("[A] Two Sum", source_day=1, difficulty="E", source="nc-150"),
    ]
    ledger = [Touch("[A] Two Sum", date(2026, 5, 1))]
    recall = compute_recall(ledger, today=date(2026, 5, 7), limit=10, curriculum=curriculum)
    assert recall[0].difficulty == "E"


def test_renderer_displays_difficulty_in_recall_lines() -> None:
    from recall_engine import RecallItem

    out = render_today(
        today=date(2026, 5, 7),
        recall=[
            RecallItem(
                problem="[A] Two Sum",
                touches=1,
                last_touched=date(2026, 5, 1),
                days_overdue=5,
                difficulty="E",
            )
        ],
        new=[],
    )
    # Difficulty is visible somewhere on the recall line
    recall_section = out.split("## New")[0]
    assert "(E)" in recall_section


def test_renderer_displays_difficulty_in_new_lines() -> None:
    out = render_today(
        today=date(2026, 5, 11),
        recall=[],
        new=[Problem("[A] Two Sum", source_day=1, difficulty="E", source="nc-150")],
    )
    new_section = out.split("## New")[1]
    assert "(E)" in new_section


# ─── Saturday "this week's hardest" section ────────────────────────────────────


def test_renderer_includes_this_weeks_hardest_section_on_saturdays() -> None:
    """Saturday is reinforcement day — render an empty checklist where the user
    writes 2-3 problems they found hardest from this week's daily-hardest notes."""
    saturday = date(2026, 5, 16)
    assert saturday.weekday() == 5
    out = render_today(today=saturday, recall=[], new=[])
    assert "This week's hardest" in out


def test_renderer_omits_this_weeks_hardest_section_on_weekdays() -> None:
    monday = date(2026, 5, 11)
    assert monday.weekday() == 0
    out = render_today(today=monday, recall=[], new=[])
    assert "This week's hardest" not in out


def test_saturday_hardest_section_renders_empty_checkboxes_for_user_to_fill_in() -> None:
    """User writes problem names into the empty boxes; ticking them logs touches.
    The empty boxes themselves must be skipped by the completion parser."""
    saturday = date(2026, 5, 16)
    out = render_today(today=saturday, recall=[], new=[])
    # Section has writable bullet lines for the user
    section = out.split("This week's hardest")[1]
    assert section.count("- [ ]") >= 2


def test_completion_parser_ignores_empty_writable_checkboxes_on_saturday(tmp_path: Path) -> None:
    """The Saturday `- [ ]` empty bullets should never produce ledger entries
    even after Tasks plugin auto-stamps them when the user ticks them blank."""
    md = (
        "## This week's hardest — your pick\n\n"
        "- [x]  ✅ 2026-05-16\n"
        "- [x]  (just whitespace) ✅ 2026-05-16\n"
    )
    assert parse_completions(md) == []


# ─── Sprint day + phase math ──────────────────────────────────────────────────


_PHASE_MD = """\
## Phase 1 — Linear Patterns E+M (Days 1–7)

intro

### Day 1 — Mon May 11

- [ ] [A] Foo (E)

## Phase 2 — Search + Trees (Days 8–17)

### Day 8 — Mon May 18

- [ ] [B] Bar (M)

## Phase 5 — Hard Problems (Days 40–53) — mock-heavy

### Day 40 — Thu Jun 18

- [ ] [C] Baz (H)
"""


def test_parse_phases_extracts_each_phase_heading() -> None:
    phases = parse_phases(_PHASE_MD)
    assert len(phases) == 3
    assert phases[0] == CurriculumPhase(
        number=1, name="Linear Patterns E+M", days_start=1, days_end=7
    )
    assert phases[1] == CurriculumPhase(
        number=2, name="Search + Trees", days_start=8, days_end=17
    )
    # Phase 5 has trailing "— mock-heavy" after the days range; parser ignores it.
    assert phases[2] == CurriculumPhase(
        number=5, name="Hard Problems", days_start=40, days_end=53
    )


def test_phase_for_returns_phase_containing_the_day() -> None:
    phases = parse_phases(_PHASE_MD)
    assert phase_for(1, phases).number == 1
    assert phase_for(7, phases).number == 1  # inclusive end
    assert phase_for(8, phases).number == 2  # next phase begins
    assert phase_for(40, phases).number == 5
    assert phase_for(53, phases).number == 5


def test_phase_for_returns_none_when_day_falls_outside_known_phases() -> None:
    phases = parse_phases(_PHASE_MD)
    assert phase_for(0, phases) is None  # before Day 1
    assert phase_for(20, phases) is None  # gap between Phase 2 and Phase 5
    assert phase_for(100, phases) is None  # past last phase


def test_curriculum_phase_slug_matches_github_anchor_conventions() -> None:
    phase = CurriculumPhase(
        number=1, name="Linear Patterns E+M", days_start=1, days_end=7
    )
    # GitHub: lowercase, drop punctuation (— em-dash, +, parens), spaces → hyphens
    assert phase.slug == "phase-1--linear-patterns-em-days-17"


def test_start_date_returns_none_for_empty_ledger() -> None:
    assert start_date([]) is None


def test_start_date_is_the_earliest_touch_in_the_ledger() -> None:
    """A friend running their own prep with a different start date will get
    Day 1 anchored to whenever they first checked something off."""
    ledger = [
        Touch("[A] Bar", date(2026, 5, 13)),
        Touch("[A] Foo", date(2026, 5, 11)),  # earliest
        Touch("[A] Baz", date(2026, 5, 14)),
    ]
    assert start_date(ledger) == date(2026, 5, 11)


def test_day_n_for_treats_start_date_as_day_one() -> None:
    start = date(2026, 5, 11)
    assert day_n_for(date(2026, 5, 11), start) == 1
    assert day_n_for(date(2026, 5, 12), start) == 2
    assert day_n_for(date(2026, 5, 18), start) == 8


# ─── Header rendering with phase + day ────────────────────────────────────────


def test_renderer_header_says_pre_prep_when_no_day_n() -> None:
    out = render_today(today=date(2026, 5, 8), recall=[], new=[])
    first_line = out.splitlines()[0]
    assert "Pre-prep" in first_line


def test_renderer_header_includes_day_n_when_provided() -> None:
    phase = CurriculumPhase(
        number=1, name="Linear Patterns E+M", days_start=1, days_end=7
    )
    out = render_today(
        today=date(2026, 5, 11), recall=[], new=[], day_n=1, phase=phase
    )
    first_line = out.splitlines()[0]
    assert "Day 1" in first_line


def test_renderer_header_includes_linked_phase_heading_with_anchor() -> None:
    phase = CurriculumPhase(
        number=1, name="Linear Patterns E+M", days_start=1, days_end=7
    )
    out = render_today(
        today=date(2026, 5, 11), recall=[], new=[], day_n=1, phase=phase
    )
    first_line = out.splitlines()[0]
    # Markdown link to the daily file with the phase slug as anchor
    assert "[Phase 1 — Linear Patterns E+M (Days 1–7)]" in first_line
    assert "#phase-1--linear-patterns-em-days-17" in first_line


def test_renderer_header_falls_back_to_day_only_when_phase_is_none() -> None:
    """If day_n is past the last phase (e.g., Day 95 in a 90-day curriculum),
    render the day number without a phase link rather than crashing."""
    out = render_today(
        today=date(2026, 8, 15), recall=[], new=[], day_n=95, phase=None
    )
    first_line = out.splitlines()[0]
    assert "Day 95" in first_line
    assert "Phase" not in first_line


# ─── Pace projection ──────────────────────────────────────────────────────────


def test_avg_new_per_day_returns_none_for_empty_ledger() -> None:
    assert avg_new_per_day([], today=date(2026, 5, 11)) is None


def test_avg_new_per_day_is_distinct_problems_over_days_elapsed() -> None:
    """Day 1 with 3 distinct touches → 3.0/day. Day 2 with 5 distinct → 2.5/day."""
    ledger = [
        Touch("[A] Foo", date(2026, 5, 11)),
        Touch("[A] Bar", date(2026, 5, 11)),
        Touch("[A] Baz", date(2026, 5, 11)),
    ]
    assert avg_new_per_day(ledger, today=date(2026, 5, 11)) == 3.0

    ledger.extend(
        [
            Touch("[A] Qux", date(2026, 5, 12)),
            Touch("[A] Quux", date(2026, 5, 12)),
        ]
    )
    assert avg_new_per_day(ledger, today=date(2026, 5, 12)) == 2.5


def test_avg_new_per_day_counts_distinct_problems_not_touch_events() -> None:
    """Resolving the same problem twice does not inflate the acquisition rate."""
    ledger = [
        Touch("[A] Foo", date(2026, 5, 11)),
        Touch("[A] Foo", date(2026, 5, 12)),  # re-solve, not a new acquisition
        Touch("[A] Bar", date(2026, 5, 12)),
    ]
    # 2 distinct problems / 2 days elapsed = 1.0/day
    assert avg_new_per_day(ledger, today=date(2026, 5, 12)) == 1.0


def test_projected_end_date_returns_none_for_empty_ledger() -> None:
    curriculum = [Problem("[A] Foo", source_day=1, difficulty="E")]
    assert projected_end_date([], curriculum, today=date(2026, 5, 11)) is None


def test_projected_end_date_returns_today_when_curriculum_is_fully_touched() -> None:
    curriculum = [Problem("[A] Foo", source_day=1, difficulty="E")]
    ledger = [Touch("[A] Foo", date(2026, 5, 11))]
    assert projected_end_date(ledger, curriculum, today=date(2026, 5, 11)) == date(
        2026, 5, 11
    )


def test_projected_end_date_extrapolates_remaining_problems_at_current_pace() -> None:
    """Day 1, solved 3 of 9 → rate 3.0/day, 6 untouched → +2 days = May 13."""
    curriculum = [
        Problem(f"[A] P{i}", source_day=1, difficulty="E") for i in range(9)
    ]
    ledger = [
        Touch("[A] P0", date(2026, 5, 11)),
        Touch("[A] P1", date(2026, 5, 11)),
        Touch("[A] P2", date(2026, 5, 11)),
    ]
    assert projected_end_date(
        ledger, curriculum, today=date(2026, 5, 11)
    ) == date(2026, 5, 13)


def test_projected_end_date_self_corrects_as_pace_data_accrues() -> None:
    """Pace projections in early days swing wildly — that's OK as long as the
    function honestly reflects what the ledger says today."""
    curriculum = [
        Problem(f"[A] P{i}", source_day=1, difficulty="E") for i in range(20)
    ]
    fast_day_one = [Touch(f"[A] P{i}", date(2026, 5, 11)) for i in range(5)]
    end_after_fast_day = projected_end_date(
        fast_day_one, curriculum, today=date(2026, 5, 11)
    )
    # 5/day pace, 15 left → 3 days
    assert end_after_fast_day == date(2026, 5, 14)

    slow_day_two = fast_day_one + [Touch("[A] P5", date(2026, 5, 12))]
    end_after_slow_day = projected_end_date(
        slow_day_two, curriculum, today=date(2026, 5, 12)
    )
    # 6 distinct over 2 days = 3.0/day, 14 left → ceil(14/3) = 5 days
    assert end_after_slow_day == date(2026, 5, 17)


def test_renderer_omits_projection_line_when_no_projection_provided() -> None:
    out = render_today(today=date(2026, 5, 8), recall=[], new=[])
    assert "Projected" not in out


def test_renderer_includes_projection_line_below_header_when_data_present() -> None:
    out = render_today(
        today=date(2026, 5, 11),
        recall=[],
        new=[],
        day_n=1,
        projection=date(2026, 8, 15),
        projection_rate=3.0,
        projection_untouched=160,
    )
    lines = out.splitlines()
    assert "Day 1" in lines[0]
    # Projection sits on line 2 (zero-indexed: line index 2 after header + blank)
    assert "Projected acquisition complete" in lines[2]
    assert "Aug 15" in lines[2]
    assert "3.0 new/day" in lines[2]
    assert "160 left" in lines[2]


def test_renderer_omits_projection_line_when_curriculum_already_fully_touched() -> None:
    """Once everything is touched, the projection collapses to today — don't
    render a noisy '0 left' line; just suppress it."""
    out = render_today(
        today=date(2026, 8, 15),
        recall=[],
        new=[],
        day_n=97,
        projection=date(2026, 8, 15),
        projection_rate=2.0,
        projection_untouched=0,
    )
    assert "Projected" not in out


# ─── Coverage view (by-pattern) ───────────────────────────────────────────────


def test_curriculum_parser_captures_variant_of_relationship() -> None:
    md = (
        "## Phase 1 — X (Days 1–7)\n"
        "### Day 1\n"
        "- [ ] [1-D DP] -> House Robber (M)\n"
        "- [ ] [1-D DP] -> House Robber II (M) (variant of: House Robber)\n"
    )
    problems = parse_curriculum(md)
    assert problems[0].variant_of is None
    assert problems[1].variant_of == "House Robber"


def test_problem_pattern_and_name_split_on_arrow() -> None:
    p = Problem("[Arrays & Hashing] -> Two Sum", source_day=1, difficulty="E")
    assert p.pattern == "Arrays & Hashing"
    assert p.name == "Two Sum"


def test_render_coverage_groups_problems_by_pattern() -> None:
    curriculum = [
        Problem("[Arrays & Hashing] -> Two Sum", source_day=1, difficulty="E"),
        Problem("[Two Pointers] -> Valid Palindrome", source_day=2, difficulty="E"),
        Problem("[Arrays & Hashing] -> Group Anagrams", source_day=1, difficulty="M"),
    ]
    out = render_coverage(curriculum, ledger=[])
    assert "### Arrays & Hashing" in out
    assert "### Two Pointers" in out
    # Both Arrays & Hashing problems land under their shared heading
    section = out.split("### Arrays & Hashing", 1)[1].split("###", 1)[0]
    assert "Two Sum" in section
    assert "Group Anagrams" in section


def test_render_coverage_checks_box_when_problem_is_in_ledger() -> None:
    curriculum = [
        Problem("[Arrays & Hashing] -> Two Sum", source_day=1, difficulty="E"),
        Problem("[Arrays & Hashing] -> Group Anagrams", source_day=1, difficulty="M"),
    ]
    ledger = [Touch("[Arrays & Hashing] -> Two Sum", date(2026, 5, 11))]
    out = render_coverage(curriculum, ledger)
    assert "- [x] Two Sum (E)" in out
    assert "- [ ] Group Anagrams (M)" in out


def test_render_coverage_nests_variants_under_their_canonical() -> None:
    curriculum = [
        Problem("[1-D DP] -> House Robber", source_day=1, difficulty="M"),
        Problem(
            "[1-D DP] -> House Robber II",
            source_day=1,
            difficulty="M",
            variant_of="House Robber",
        ),
    ]
    out = render_coverage(curriculum, ledger=[])
    assert "- [ ] House Robber (M)" in out
    # Variant is indented (two-space prefix) under canonical
    assert "  - [ ] House Robber II (M)" in out


def test_render_coverage_orders_patterns_by_source_tier() -> None:
    """nc-150 patterns surface before nc-150+ ones, regardless of doc order."""
    curriculum = [
        Problem(
            "[Beyond] -> X",
            source_day=54,
            difficulty="M",
            source="nc-150+",
        ),
        Problem(
            "[Core] -> Y",
            source_day=54,
            difficulty="M",
            source="nc-150",
        ),
    ]
    out = render_coverage(curriculum, ledger=[])
    core_pos = out.find("### Core")
    beyond_pos = out.find("### Beyond")
    assert 0 <= core_pos < beyond_pos


def test_render_coverage_handles_variant_whose_canonical_is_not_in_curriculum() -> None:
    """Some II-suffix problems (Basic Calculator II, My Calendar III) have no
    canonical in the curriculum — render them at top level with a footnote
    rather than dropping them or crashing."""
    curriculum = [
        Problem(
            "[Stack] -> Basic Calculator II",
            source_day=10,
            difficulty="M",
            variant_of="Basic Calculator",
        ),
    ]
    out = render_coverage(curriculum, ledger=[])
    assert "Basic Calculator II" in out
    assert "(variant of Basic Calculator)" in out


def test_recompute_writes_coverage_md_when_path_provided(tmp_path: Path) -> None:
    daily_md = tmp_path / "prep-plan-daily.md"
    daily_md.write_text(
        "## Phase 1 — X (Days 1–7)\n"
        "### Day 1\n"
        "- [ ] [Arrays & Hashing] -> Two Sum (E)\n"
    )
    today_md = tmp_path / "today.md"
    ledger = tmp_path / "completions.jsonl"
    coverage_md = tmp_path / "coverage.md"
    recompute(
        daily_md,
        today_md,
        ledger,
        today=date(2026, 5, 11),
        coverage_md_path=coverage_md,
    )
    assert coverage_md.exists()
    assert "### Arrays & Hashing" in coverage_md.read_text()


# ─── Mock tracking ────────────────────────────────────────────────────────────


def test_load_mocks_returns_empty_list_when_file_does_not_exist(
    tmp_path: Path,
) -> None:
    assert load_mocks(tmp_path / "nope.json") == []


def test_load_mocks_parses_pending_scheduled_completed_states(
    tmp_path: Path,
) -> None:
    path = tmp_path / "mocks.json"
    path.write_text(
        '[{"id": "m1", "status": "pending"}, '
        '{"id": "m2", "status": "scheduled", "platform": "Pramp", '
        '"topic": "Trees", "scheduled_date": "2026-05-20"}, '
        '{"id": "m3", "status": "completed", "completed_date": "2026-05-08", '
        '"notes": "weak on memo"}]'
    )
    mocks = load_mocks(path)
    assert mocks[0].status == "pending"
    assert mocks[1].scheduled_date == date(2026, 5, 20)
    assert mocks[1].platform == "Pramp"
    assert mocks[2].completed_date == date(2026, 5, 8)
    assert mocks[2].notes == "weak on memo"


def test_load_mocks_rejects_a_non_list_payload(tmp_path: Path) -> None:
    path = tmp_path / "mocks.json"
    path.write_text('{"id": "m1", "status": "pending"}')
    with pytest.raises(ValueError, match="must contain a JSON list"):
        load_mocks(path)


def test_upcoming_mocks_filters_to_scheduled_only_within_window() -> None:
    today = date(2026, 5, 11)
    mocks = [
        Mock(id="m1", status="pending"),
        Mock(
            id="m2",
            status="scheduled",
            platform="Pramp",
            scheduled_date=date(2026, 5, 13),
        ),
        Mock(
            id="m3",
            status="scheduled",
            platform="Interviewing.io",
            scheduled_date=date(2026, 6, 1),  # 21 days out — past 14-day window
        ),
        Mock(
            id="m4", status="completed", completed_date=date(2026, 5, 8)
        ),
    ]
    upcoming = upcoming_mocks(mocks, today)
    assert [m.id for m in upcoming] == ["m2"]


def test_upcoming_mocks_surfaces_past_due_scheduled_mocks_so_user_notices() -> None:
    """A scheduled mock whose date is already past — likely the user forgot
    to mark it complete. Surface it rather than hiding it."""
    today = date(2026, 5, 15)
    mocks = [
        Mock(
            id="m1",
            status="scheduled",
            platform="Pramp",
            scheduled_date=date(2026, 5, 10),  # 5 days ago
        ),
    ]
    upcoming = upcoming_mocks(mocks, today)
    assert [m.id for m in upcoming] == ["m1"]


def test_upcoming_mocks_sorts_soonest_first() -> None:
    today = date(2026, 5, 11)
    mocks = [
        Mock(
            id="later",
            status="scheduled",
            scheduled_date=date(2026, 5, 18),
        ),
        Mock(
            id="sooner",
            status="scheduled",
            scheduled_date=date(2026, 5, 13),
        ),
    ]
    assert [m.id for m in upcoming_mocks(mocks, today)] == ["sooner", "later"]


def test_render_coverage_includes_mock_section_with_progress_bar() -> None:
    curriculum = [Problem("[A] Foo", source_day=1, difficulty="E")]
    mocks = [
        Mock(id="m1", status="completed", completed_date=date(2026, 5, 8)),
        Mock(id="m2", status="scheduled", scheduled_date=date(2026, 5, 20)),
        Mock(id="m3", status="pending"),
    ]
    out = render_coverage(curriculum, ledger=[], mocks=mocks)
    assert "## Mocks (1/3 complete · 1 scheduled · 1 pending)" in out
    # Progress bar present (Unicode block characters)
    assert "█" in out and "░" in out


def test_render_coverage_omits_mocks_section_when_mocks_arg_is_none() -> None:
    """Backwards-compatible: callers that don't pass mocks get the bare
    by-pattern view, no Mocks header."""
    out = render_coverage(
        [Problem("[A] Foo", source_day=1)], ledger=[], mocks=None
    )
    assert "Mocks" not in out


def test_recompute_renders_upcoming_mocks_in_today_and_summary_in_coverage(
    tmp_path: Path,
) -> None:
    """today.md gets the next-up Upcoming mocks block (between Readiness and
    Recall) — daily attention. coverage.md still has the full Mocks section,
    and mocks.md has the standalone view."""
    daily_md = tmp_path / "prep-plan-daily.md"
    daily_md.write_text(
        "## Phase 1 — X (Days 1–7)\n"
        "### Day 1\n"
        "- [ ] [A] -> Foo (E)\n"
    )
    today_md = tmp_path / "today.md"
    ledger = tmp_path / "completions.jsonl"
    coverage_md = tmp_path / "coverage.md"
    mocks_path = tmp_path / "mocks.json"
    mocks_path.write_text(
        '[{"id": "m1", "status": "scheduled", "platform": "Pramp", '
        '"topic": "Trees", "scheduled_date": "2026-05-13"}]'
    )
    recompute(
        daily_md,
        today_md,
        ledger,
        today=date(2026, 5, 11),
        coverage_md_path=coverage_md,
        mocks_path=mocks_path,
    )
    today_text = today_md.read_text()
    assert "## Upcoming mocks" in today_text
    # Upcoming mocks sits between Readiness and Recall
    readiness_pos = today_text.find("## Readiness")
    upcoming_pos = today_text.find("## Upcoming mocks")
    recall_pos = today_text.find("## Recall")
    assert 0 <= readiness_pos < upcoming_pos < recall_pos
    assert "## Mocks" in coverage_md.read_text()


# ─── System Design chapter tracking ───────────────────────────────────────────


def test_load_sd_chapters_returns_empty_list_when_file_does_not_exist(
    tmp_path: Path,
) -> None:
    assert load_sd_chapters(tmp_path / "nope.json") == []


def test_load_sd_chapters_parses_pending_and_completed_states(
    tmp_path: Path,
) -> None:
    path = tmp_path / "sd.json"
    path.write_text(
        '[{"id": "ch-1", "title": "Scale from Zero to Millions", '
        '"book": "Alex Xu Vol 1", "status": "completed", '
        '"completed_date": "2026-05-12"},'
        ' {"id": "ch-2", "title": "Back-of-envelope estimation", '
        '"book": "Alex Xu Vol 1", "status": "pending"}]'
    )
    chapters = load_sd_chapters(path)
    assert chapters[0].status == "completed"
    assert chapters[0].completed_date == date(2026, 5, 12)
    assert chapters[1].status == "pending"
    assert chapters[1].completed_date is None


def test_load_sd_chapters_rejects_a_non_list_payload(tmp_path: Path) -> None:
    path = tmp_path / "sd.json"
    path.write_text('{"id": "ch-1"}')
    with pytest.raises(ValueError, match="must contain a JSON list"):
        load_sd_chapters(path)


def test_next_sd_chapter_returns_first_pending_in_document_order() -> None:
    chapters = [
        SDChapter(
            id="ch-1",
            title="Ch 1",
            book="Alex Xu Vol 1",
            status="completed",
            completed_date=date(2026, 5, 11),
        ),
        SDChapter(id="ch-2", title="Ch 2", book="Alex Xu Vol 1", status="pending"),
        SDChapter(id="ch-3", title="Ch 3", book="Alex Xu Vol 1", status="pending"),
    ]
    nxt = next_sd_chapter(chapters)
    assert nxt is not None and nxt.id == "ch-2"


def test_next_sd_chapter_returns_none_when_all_complete() -> None:
    chapters = [
        SDChapter(
            id="ch-1",
            title="Ch 1",
            book="Alex Xu Vol 1",
            status="completed",
            completed_date=date(2026, 5, 11),
        ),
    ]
    assert next_sd_chapter(chapters) is None


def test_render_today_surfaces_next_pending_sd_chapter_until_checked() -> None:
    nxt = SDChapter(
        id="ch-1",
        title="Scale from Zero to Millions",
        book="Alex Xu Vol 1",
        status="pending",
    )
    out = render_today(today=date(2026, 5, 11), recall=[], new=[], sd_next=nxt)
    assert "## Today's SD reading" in out
    assert "Alex Xu Vol 1" in out
    assert "Scale from Zero to Millions" in out


def test_render_today_omits_sd_section_when_no_pending_chapters() -> None:
    out = render_today(today=date(2026, 5, 11), recall=[], new=[], sd_next=None)
    assert "Today's SD reading" not in out


def test_render_coverage_includes_system_design_section_with_progress_bar() -> None:
    chapters = [
        SDChapter(
            id="ch-1",
            title="Ch 1",
            book="Alex Xu Vol 1",
            status="completed",
            completed_date=date(2026, 5, 11),
        ),
        SDChapter(id="ch-2", title="Ch 2", book="Alex Xu Vol 1", status="pending"),
    ]
    out = render_coverage(
        [Problem("[A] Foo", source_day=1)], ledger=[], sd_chapters=chapters
    )
    assert "## System Design (1/2 complete)" in out
    assert "█" in out and "░" in out
    assert "- [x] Alex Xu Vol 1 · Ch 1 · ✅ 2026-05-11" in out
    assert "- [ ] Alex Xu Vol 1 · Ch 2" in out


def test_recompute_reads_sd_chapters_and_renders_in_both_views(
    tmp_path: Path,
) -> None:
    daily_md = tmp_path / "prep-plan-daily.md"
    daily_md.write_text(
        "## Phase 1 — X (Days 1–7)\n"
        "### Day 1\n"
        "- [ ] [A] -> Foo (E)\n"
    )
    today_md = tmp_path / "today.md"
    ledger = tmp_path / "completions.jsonl"
    coverage_md = tmp_path / "coverage.md"
    sd_path = tmp_path / "sd.json"
    sd_path.write_text(
        '[{"id": "ch-1", "title": "Scale from Zero to Millions", '
        '"book": "Alex Xu Vol 1", "status": "pending"}]'
    )
    recompute(
        daily_md,
        today_md,
        ledger,
        today=date(2026, 5, 11),
        coverage_md_path=coverage_md,
        sd_chapters_path=sd_path,
    )
    assert "## Today's SD reading" in today_md.read_text()
    assert "## System Design" in coverage_md.read_text()


# ─── Application-readiness gates ──────────────────────────────────────────────


def _em(text: str) -> Problem:
    return Problem(text, source_day=1, difficulty="M")


def _h(text: str) -> Problem:
    return Problem(text, source_day=1, difficulty="H")


def test_readiness_fallback_tier_clears_when_all_em_problems_touched() -> None:
    curriculum = [_em("[A] x"), _em("[A] y"), _h("[A] z")]
    ledger = [Touch("[A] x", date(2026, 5, 11)), Touch("[A] y", date(2026, 5, 12))]
    r = compute_readiness(curriculum, ledger, sd_chapters=[], mocks=[])
    fallback = next(t for t in r.tiers if t.name == "Fallback-ready")
    assert fallback.met is True
    # Hard ledger gap doesn't block fallback
    stretch = next(t for t in r.tiers if t.name == "Stretch-ready")
    assert stretch.met is False


def test_readiness_target_tier_requires_em_plus_partial_sd_plus_partial_mocks() -> None:
    curriculum = [_em("[A] x")]
    ledger = [Touch("[A] x", date(2026, 5, 11))]
    sd = [
        SDChapter(id=f"ch-{i}", title=f"T{i}", book="B", status="completed",
                  completed_date=date(2026, 5, 11)) for i in range(20)
    ]
    mocks = [Mock(id=f"m{i}", status="completed",
                  completed_date=date(2026, 5, 11)) for i in range(8)]
    r = compute_readiness(curriculum, ledger, sd, mocks)
    target = next(t for t in r.tiers if t.name == "Target-ready")
    assert target.met is True


def test_readiness_target_tier_blocks_when_below_sd_threshold() -> None:
    curriculum = [_em("[A] x")]
    ledger = [Touch("[A] x", date(2026, 5, 11))]
    too_few_sd = [
        SDChapter(id=f"ch-{i}", title=f"T{i}", book="B", status="completed",
                  completed_date=date(2026, 5, 11)) for i in range(10)
    ]
    enough_mocks = [
        Mock(id=f"m{i}", status="completed", completed_date=date(2026, 5, 11))
        for i in range(8)
    ]
    r = compute_readiness(curriculum, ledger, too_few_sd, enough_mocks)
    target = next(t for t in r.tiers if t.name == "Target-ready")
    assert target.met is False


def test_readiness_stretch_tier_clears_only_when_everything_complete() -> None:
    curriculum = [_em("[A] x"), _h("[A] z")]
    ledger = [
        Touch("[A] x", date(2026, 5, 11)),
        Touch("[A] z", date(2026, 5, 11)),
    ]
    sd_full = [
        SDChapter(id="ch-1", title="T", book="B", status="completed",
                  completed_date=date(2026, 5, 11))
    ]
    mocks_full = [
        Mock(id="m1", status="completed", completed_date=date(2026, 5, 11))
    ]
    r = compute_readiness(curriculum, ledger, sd_full, mocks_full)
    stretch = next(t for t in r.tiers if t.name == "Stretch-ready")
    assert stretch.met is True


def test_readiness_category_progress_reports_done_over_total() -> None:
    curriculum = [_em("[A] x"), _em("[A] y")]
    ledger = [Touch("[A] x", date(2026, 5, 11))]
    r = compute_readiness(curriculum, ledger, sd_chapters=[], mocks=[])
    assert r.em.done == 1 and r.em.total == 2
    assert r.em.fraction == 0.5


def test_render_readiness_block_shows_three_category_bars_and_three_tiers() -> None:
    em = CategoryProgress(name="E+M problems", done=4, total=8)
    sd = CategoryProgress(name="System Design", done=2, total=10)
    mocks = CategoryProgress(name="Mocks", done=1, total=3)
    tiers = [
        ReadinessTier(name="Fallback-ready", criteria=[("All E+M done", False)]),
        ReadinessTier(name="Target-ready", criteria=[("All E+M done", False)]),
        ReadinessTier(name="Stretch-ready", criteria=[("All curriculum done", False)]),
    ]
    out = "\n".join(render_readiness_block(Readiness(em, sd, mocks, tiers)))
    assert "## Readiness" in out
    assert "E+M problems" in out and "50%" in out and "(4/8)" in out
    assert "System Design" in out and "20%" in out
    assert "Mocks" in out
    assert "**Fallback-ready: ❌**" in out
    assert "**Target-ready: ❌**" in out
    assert "**Stretch-ready: ❌**" in out


def test_render_today_renders_readiness_block_above_recall_section() -> None:
    """Readiness sits at the top so the user sees apply-state before scrolling."""
    em = CategoryProgress(name="E+M problems", done=0, total=1)
    sd = CategoryProgress(name="System Design", done=0, total=1)
    mocks = CategoryProgress(name="Mocks", done=0, total=1)
    tiers = [
        ReadinessTier(name="Fallback-ready", criteria=[("x", False)]),
        ReadinessTier(name="Target-ready", criteria=[("x", False)]),
        ReadinessTier(name="Stretch-ready", criteria=[("x", False)]),
    ]
    readiness = Readiness(em=em, sd=sd, mocks=mocks, tiers=tiers)
    out = render_today(
        today=date(2026, 5, 11), recall=[], new=[], readiness=readiness
    )
    readiness_pos = out.find("## Readiness")
    recall_pos = out.find("## Recall")
    assert 0 <= readiness_pos < recall_pos


# ─── Coverage.md mocks subsections (folded in from old mocks.md) ──────────────


def test_render_coverage_mocks_section_has_upcoming_completed_to_schedule_subsections() -> None:
    today = date(2026, 5, 11)
    mocks = [
        Mock(
            id="m1",
            platform="Pramp",
            topic="DP",
            status="completed",
            completed_date=date(2026, 5, 8),
            notes="weak on memo",
        ),
        Mock(
            id="m2",
            platform="Interviewing.io",
            topic="Trees",
            status="scheduled",
            scheduled_date=date(2026, 5, 13),
        ),
        Mock(id="m3", platform="Pramp", topic="Backtracking", status="pending"),
    ]
    out = render_coverage(
        [Problem("[A] Foo", source_day=1, difficulty="E")],
        ledger=[],
        today=today,
        mocks=mocks,
    )
    assert "## Mocks (1/3 complete · 1 scheduled · 1 pending)" in out
    assert "### Upcoming" in out
    assert "### Completed" in out
    assert "weak on memo" in out
    assert "### To schedule" in out
    assert "Backtracking" in out


def test_render_coverage_orders_sections_readiness_then_mocks_then_sd_then_dsa() -> None:
    """User asked for coverage.md to surface readiness/mocks/SD ABOVE the
    DSA pattern walk — high-level state first, then drill-down."""
    em = CategoryProgress(name="E+M problems", done=0, total=1)
    sd_progress = CategoryProgress(name="System Design", done=0, total=1)
    mocks_progress = CategoryProgress(name="Mocks", done=0, total=1)
    readiness = Readiness(
        em=em,
        sd=sd_progress,
        mocks=mocks_progress,
        tiers=[ReadinessTier(name="Fallback-ready", criteria=[("x", False)])],
    )
    out = render_coverage(
        [Problem("[Trees] -> Foo", source_day=1)],
        ledger=[],
        today=date(2026, 5, 11),
        mocks=[Mock(id="m1", status="pending")],
        sd_chapters=[
            SDChapter(id="ch-1", title="T", book="B", status="pending")
        ],
        readiness=readiness,
    )
    readiness_pos = out.find("## Readiness")
    mocks_pos = out.find("## Mocks")
    sd_pos = out.find("## System Design")
    dsa_pos = out.find("## DSA — by pattern")
    assert 0 <= readiness_pos < mocks_pos < sd_pos < dsa_pos
