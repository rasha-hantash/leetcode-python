"""Tests for the recall engine.

These tests double as the spec: each test name is a complete sentence describing
a user-visible behavior of the snapshot-mode SM-2 lite recall queue.
"""

from __future__ import annotations

from datetime import date
from pathlib import Path

import pytest

from recall_engine import (
    Problem,
    Touch,
    aggregate_touches,
    append_to_ledger,
    compute_new,
    compute_recall,
    due_date,
    interval_for,
    load_ledger,
    overdue_days,
    parse_completions,
    parse_curriculum,
    recompute,
    render_today,
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


# ─── Difficulty + priority tags ────────────────────────────────────────────────


_TAGGED_DAILY_MD = """\
### Day 1 — Mon May 11

- **9:00–13:00 DSA New:**
  - [ ] [Arrays & Hashing] -> Contains Duplicate (E)
  - [ ] [Arrays & Hashing] -> Group Anagrams (M)

### Day 40 — Hard sprint

- **9:00–13:00 DSA New:**
  - [ ] [Two Pointers] -> Trapping Rain Water (H)

### Day 54 — Net-new

- **9:00–13:00 DSA New:**
  - [ ] [Boyer-Moore] -> Majority Element II (M) (core)
  - [ ] [Segment Tree] -> Count of Smaller After Self (H) (enrichment)
  - [ ] [Bit-Trie] -> Maximum XOR (M) (optional)
"""


def test_curriculum_parser_extracts_difficulty_marker() -> None:
    problems = parse_curriculum(_TAGGED_DAILY_MD)
    by_text = {p.text: p for p in problems}
    assert by_text["[Arrays & Hashing] -> Contains Duplicate"].difficulty == "E"
    assert by_text["[Arrays & Hashing] -> Group Anagrams"].difficulty == "M"
    assert by_text["[Two Pointers] -> Trapping Rain Water"].difficulty == "H"


def test_curriculum_parser_defaults_priority_to_core_when_no_priority_tag() -> None:
    """NC150 problems carry only a difficulty marker; their priority is implicitly 'core'."""
    problems = parse_curriculum(_TAGGED_DAILY_MD)
    by_text = {p.text: p for p in problems}
    assert by_text["[Arrays & Hashing] -> Contains Duplicate"].priority == "core"


def test_curriculum_parser_extracts_explicit_priority_marker() -> None:
    problems = parse_curriculum(_TAGGED_DAILY_MD)
    by_text = {p.text: p for p in problems}
    assert by_text["[Boyer-Moore] -> Majority Element II"].priority == "core"
    assert by_text["[Segment Tree] -> Count of Smaller After Self"].priority == "enrichment"
    assert by_text["[Bit-Trie] -> Maximum XOR"].priority == "optional"


def test_curriculum_parser_canonical_text_omits_difficulty_and_priority_tags() -> None:
    """Ledger keys must match across renders, so the canonical text excludes
    annotations the renderer might add or drop."""
    problems = parse_curriculum(_TAGGED_DAILY_MD)
    texts = {p.text for p in problems}
    # No "(E)", "(M)", "(H)", "(core)", "(enrichment)", "(optional)" anywhere
    for t in texts:
        assert "(E)" not in t and "(M)" not in t and "(H)" not in t
        assert "(core)" not in t and "(enrichment)" not in t and "(optional)" not in t


def test_completion_parser_strips_difficulty_tag_from_canonical() -> None:
    """A checked line in today.md carries `(E) (Day 1)`-style annotations that the
    parser must strip to produce a ledger key matching the curriculum."""
    md = "- [x] [Arrays & Hashing] -> Contains Duplicate (E) (Day 1) ✅ 2026-05-11"
    assert parse_completions(md) == [
        Touch("[Arrays & Hashing] -> Contains Duplicate", date(2026, 5, 11))
    ]


def test_completion_parser_strips_priority_tag_from_canonical() -> None:
    md = "- [x] [Segment Tree] -> Count of Smaller After Self (H) (enrichment) (Day 54) ✅ 2026-07-03"
    assert parse_completions(md) == [
        Touch("[Segment Tree] -> Count of Smaller After Self", date(2026, 7, 3))
    ]


# ─── compute_new priority tiebreaker ───────────────────────────────────────────


def test_compute_new_prefers_core_problems_over_enrichment_in_same_day() -> None:
    """When falling behind, the engine should never offer an enrichment problem
    while a core problem of the same day is still untouched."""
    curriculum = [
        Problem("[X] enrichment-1", source_day=54, difficulty="H", priority="enrichment"),
        Problem("[X] core-1", source_day=54, difficulty="M", priority="core"),
        Problem("[X] enrichment-2", source_day=54, difficulty="H", priority="enrichment"),
        Problem("[X] core-2", source_day=54, difficulty="M", priority="core"),
    ]
    new = compute_new(curriculum, ledger=[], limit=2)
    assert [p.text for p in new] == ["[X] core-1", "[X] core-2"]


def test_compute_new_falls_through_to_optional_then_enrichment_when_core_is_drained() -> None:
    curriculum = [
        Problem("[X] core-only", source_day=54, difficulty="M", priority="core"),
        Problem("[X] optional-thing", source_day=54, difficulty="M", priority="optional"),
        Problem("[X] enrichment-thing", source_day=54, difficulty="H", priority="enrichment"),
    ]
    ledger = [Touch("[X] core-only", date(2026, 7, 3))]
    new = compute_new(curriculum, ledger, limit=2)
    assert [p.text for p in new] == ["[X] optional-thing", "[X] enrichment-thing"]


def test_compute_new_within_a_priority_tier_preserves_document_order() -> None:
    curriculum = [
        Problem("[X] P3", source_day=2, difficulty="M", priority="core"),
        Problem("[X] P1", source_day=1, difficulty="M", priority="core"),
        Problem("[X] P2", source_day=1, difficulty="M", priority="core"),
    ]
    new = compute_new(curriculum, ledger=[], limit=3)
    assert [p.text for p in new] == ["[X] P3", "[X] P1", "[X] P2"]


# ─── Difficulty surfaced in renderer ───────────────────────────────────────────


def test_recall_item_carries_difficulty_when_curriculum_is_provided() -> None:
    curriculum = [
        Problem("[A] Two Sum", source_day=1, difficulty="E", priority="core"),
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
        new=[Problem("[A] Two Sum", source_day=1, difficulty="E", priority="core")],
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
