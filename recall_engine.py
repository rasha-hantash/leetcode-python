"""Recall engine: snapshot-mode SM-2 lite scheduler for the NeetCode 150 curriculum.

Reads `prep-plan-daily.md` (curriculum) and the previous `today.md` (yesterday's
checked-off items), folds new completions into an append-only JSONL ledger, then
regenerates `today.md` with today's Recall and New sections.

Designed to run once per morning (LaunchAgent) or on-demand (`prep recompute`).
There is no live daemon — today's set is frozen until the next recompute call.
"""

from __future__ import annotations

import json
import math
import re
from dataclasses import dataclass, field
from datetime import date, timedelta
from pathlib import Path
from typing import Iterable, Literal

import click


# ─── Constants ────────────────────────────────────────────────────────────────

INTERVALS_DAYS: list[int] = [1, 3, 7, 21, 60]
"""SM-2 lite: interval after the Nth touch (1-indexed). 5+ touches stay at 60."""

DEFAULT_RECALL_LIMIT = 10
DEFAULT_NEW_LIMIT = 3

Difficulty = Literal["E", "M", "H"]
Source = Literal["nc-150", "nc-150+", "company question"]

_SOURCE_RANK: dict[str, int] = {"nc-150": 0, "nc-150+": 1, "company question": 2}


# ─── Data types ──────────────────────────────────────────────────────────────


@dataclass(frozen=True)
class Problem:
    """A curriculum entry: canonical problem text, source day, and optional tags."""

    text: str
    source_day: int
    difficulty: Difficulty | None = None
    source: Source = "nc-150"
    variant_of: str | None = None

    @property
    def pattern(self) -> str:
        match = re.match(r"^\[([^\]]+)\]", self.text)
        return match.group(1) if match else ""

    @property
    def name(self) -> str:
        match = re.match(r"^\[[^\]]+\]\s*->\s*(.+)$", self.text)
        return match.group(1).strip() if match else self.text


@dataclass(frozen=True)
class Touch:
    """One successful (re-)solve event. The ledger is a list of these."""

    problem: str
    on: date


@dataclass(frozen=True)
class RecallItem:
    """A problem ranked into the Recall section, with metadata for rendering."""

    problem: str
    touches: int
    last_touched: date
    days_overdue: int
    difficulty: Difficulty | None = None


@dataclass(frozen=True)
class CurriculumPhase:
    """A `## Phase N — Name (Days A–B)` section header parsed from the curriculum."""

    number: int
    name: str
    days_start: int
    days_end: int

    @property
    def heading(self) -> str:
        return f"Phase {self.number} — {self.name} (Days {self.days_start}–{self.days_end})"

    @property
    def slug(self) -> str:
        """GitHub-flavored markdown anchor for the phase header.

        GitHub strips punctuation but preserves the *number* of spaces — a
        run of `space em-dash space` becomes `--` (the em-dash is dropped
        but the two surrounding spaces survive as two hyphens)."""
        s = self.heading.lower()
        s = re.sub(r"[^\w\s-]", "", s, flags=re.UNICODE)
        # Each whitespace char → one hyphen (no collapsing)
        s = re.sub(r"\s", "-", s).strip("-")
        return s


MockStatus = Literal["pending", "scheduled", "completed"]


@dataclass(frozen=True)
class MockPrereq:
    """Per-mock readiness threshold the user wants to clear before sitting it.
    Both fields default to 0, meaning 'no threshold' for that dimension."""

    em_problems: int = 0
    sd_chapters: int = 0

    @property
    def has_any(self) -> bool:
        return self.em_problems > 0 or self.sd_chapters > 0


_PLATFORM_BOOKING_URLS: dict[str, str] = {
    "Pramp": "https://www.pramp.com/dashboard/upcoming-sessions",
    "Interviewing.io": "https://interviewing.io/dashboard",
}


@dataclass(frozen=True)
class Mock:
    """A planned, scheduled, or completed mock interview. State machine:
    pending → scheduled (with date) → completed (with date)."""

    id: str
    status: MockStatus
    platform: str | None = None
    topic: str | None = None
    scheduled_date: date | None = None
    completed_date: date | None = None
    notes: str | None = None
    prerequisites: MockPrereq | None = None
    booking_url: str | None = None

    @property
    def effective_booking_url(self) -> str | None:
        """Per-mock override wins; otherwise fall back to the platform default
        for Pramp / Interviewing.io. Returns None for unknown platforms."""
        if self.booking_url:
            return self.booking_url
        if self.platform and self.platform in _PLATFORM_BOOKING_URLS:
            return _PLATFORM_BOOKING_URLS[self.platform]
        return None


SDChapterStatus = Literal["pending", "completed"]


@dataclass(frozen=True)
class SDChapter:
    """One System Design reading unit (a book chapter). Two states: pending
    and completed. Sequential — order in the JSON file is the read order."""

    id: str
    title: str
    book: str
    status: SDChapterStatus
    completed_date: date | None = None


BehavioralStatus = Literal["pending", "completed"]


@dataclass(frozen=True)
class BehavioralTopic:
    """One behavioral interview prep unit (a story or question to prepare).
    Two states: pending and completed. The user excludes behavioral from the
    application-readiness gates — this is a self-paced checklist surfaced for
    visibility, not blocking."""

    id: str
    prompt: str
    status: BehavioralStatus
    completed_date: date | None = None
    notes: str | None = None


@dataclass(frozen=True)
class CategoryProgress:
    """Completion progress within one prep category (E+M problems, SD chapters,
    or mocks). Used to render percentage bars and feed readiness gates."""

    name: str
    done: int
    total: int

    @property
    def fraction(self) -> float:
        return self.done / self.total if self.total > 0 else 0.0


@dataclass(frozen=True)
class Readiness:
    """Aggregate prep state — three category progresses + which application
    tiers the user has cleared. Tier thresholds are hardcoded in `compute_readiness`.

    The `tiers` list is ordered easiest-first (fallback → target → stretch);
    each entry's `met` flag reflects whether all criteria for that tier are
    currently satisfied."""

    em: CategoryProgress
    sd: CategoryProgress
    mocks: CategoryProgress
    tiers: list["ReadinessTier"]


@dataclass(frozen=True)
class ReadinessTier:
    """One application-readiness gate. `criteria` is a list of (label, met)
    pairs that compose the tier — e.g., 'All E+M problems touched'."""

    name: str
    criteria: list[tuple[str, bool]]

    @property
    def met(self) -> bool:
        return all(ok for _, ok in self.criteria)


@dataclass(frozen=True)
class RecomputeResult:
    """Summary of what a single recompute() call did. Useful for CLI output."""

    new_touches_logged: int
    recall_size: int
    new_size: int


# ─── SM-2 lite arithmetic ────────────────────────────────────────────────────


def interval_for(touches: int) -> int:
    """Days from last touch to next due. Past the table, the interval saturates."""
    if touches < 1:
        raise ValueError(f"touches must be >= 1, got {touches}")
    return INTERVALS_DAYS[min(touches, len(INTERVALS_DAYS)) - 1]


def due_date(touches: int, last_touched: date) -> date:
    return last_touched + timedelta(days=interval_for(touches))


def overdue_days(touches: int, last_touched: date, today: date) -> int:
    """Positive = past due. Zero = exactly due today. Negative = not yet due."""
    return (today - due_date(touches, last_touched)).days


# ─── Sprint day + phase math ─────────────────────────────────────────────────


def start_date(ledger: list[Touch]) -> date | None:
    """The earliest touch in the ledger, or None if the ledger is empty.

    This anchors Day 1 to the first DSA completion — friend-portable and
    independent of any pre-configured calendar."""
    return min((t.on for t in ledger), default=None)


def day_n_for(today: date, start: date) -> int:
    """Day number relative to the user's first touch. start_date itself is Day 1."""
    return (today - start).days + 1


def phase_for(
    day_n: int, phases: list[CurriculumPhase]
) -> CurriculumPhase | None:
    """Find the curriculum phase containing the given day number, or None
    if the day falls outside every phase's range (e.g., past Day 90)."""
    for phase in phases:
        if phase.days_start <= day_n <= phase.days_end:
            return phase
    return None


# ─── Pace projection ─────────────────────────────────────────────────────────


def avg_new_per_day(ledger: list[Touch], today: date) -> float | None:
    """Cumulative rate of distinct problems acquired per day, anchored to
    the ledger's start_date. Returns None if the ledger is empty.

    Uses cumulative average from Day 1 — recomputed on every recompute call,
    so the projection self-corrects as more data accrues."""
    start = start_date(ledger)
    if start is None:
        return None
    distinct = {t.problem for t in ledger}
    days_elapsed = day_n_for(today, start)
    return len(distinct) / days_elapsed


def projected_end_date(
    ledger: list[Touch],
    curriculum: list[Problem],
    today: date,
) -> date | None:
    """Projected calendar date when every curriculum problem will have ≥1 touch,
    based on the user's cumulative pace. Returns None when no projection is
    possible (empty ledger, or pace is zero); returns `today` if the curriculum
    is already fully touched."""
    rate = avg_new_per_day(ledger, today)
    if rate is None or rate <= 0:
        return None
    touched = {t.problem for t in ledger}
    untouched = sum(1 for p in curriculum if p.text not in touched)
    if untouched == 0:
        return today
    days_remaining = math.ceil(untouched / rate)
    return today + timedelta(days=days_remaining)


# ─── Touch aggregation ───────────────────────────────────────────────────────


def aggregate_touches(ledger: Iterable[Touch]) -> dict[str, tuple[int, date]]:
    """Roll the ledger up to {problem: (touch_count, latest_completion_date)}."""
    summary: dict[str, tuple[int, date]] = {}
    for t in ledger:
        if t.problem in summary:
            count, latest = summary[t.problem]
            summary[t.problem] = (count + 1, max(latest, t.on))
        else:
            summary[t.problem] = (1, t.on)
    return summary


# ─── Recall and New computation ──────────────────────────────────────────────


def compute_recall(
    ledger: list[Touch],
    today: date,
    limit: int = DEFAULT_RECALL_LIMIT,
    curriculum: list[Problem] | None = None,
) -> list[RecallItem]:
    """Items at or past their SM-2 due date, sorted most-overdue first, capped.
    If `curriculum` is given, each RecallItem is annotated with its difficulty."""
    diff_lookup: dict[str, Difficulty | None] = {
        p.text: p.difficulty for p in (curriculum or [])
    }
    items: list[RecallItem] = []
    for problem, (touches, last) in aggregate_touches(ledger).items():
        overdue = overdue_days(touches, last, today)
        if overdue >= 0:
            items.append(
                RecallItem(
                    problem=problem,
                    touches=touches,
                    last_touched=last,
                    days_overdue=overdue,
                    difficulty=diff_lookup.get(problem),
                )
            )
    items.sort(key=lambda r: r.days_overdue, reverse=True)
    return items[:limit]


def compute_new(
    curriculum: list[Problem], ledger: list[Touch], limit: int = DEFAULT_NEW_LIMIT
) -> list[Problem]:
    """The next N never-touched problems, ordered by source provenance
    (nc-150 > nc-150+ > company question) then document order. NC150 problems
    always surface before non-NC150 patterns, and both before company-specific
    variants."""
    touched = {t.problem for t in ledger}
    indexed = [
        (i, p) for i, p in enumerate(curriculum) if p.text not in touched
    ]
    indexed.sort(key=lambda item: (_SOURCE_RANK.get(item[1].source, 0), item[0]))
    return [p for _, p in indexed[:limit]]


# ─── Parsers ─────────────────────────────────────────────────────────────────


_DAY_HEADING = re.compile(r"^###\s+Day\s+(\d+)\b")
_PHASE_HEADING = re.compile(
    r"^##\s+Phase\s+(\d+)\s+[—-]\s+(.+?)\s+\(Days?\s+(\d+)[–-](\d+)\)"
)
_PROBLEM_LINE = re.compile(r"^\s*-\s+\[[ xX]\]\s+(.*)$")
_CHECKED_LINE = re.compile(r"^\s*-\s+\[[xX]\]\s+(.*)$")
_DONE_DATE = re.compile(r"\s*✅\s*(\d{4}-\d{2}-\d{2}).*$")
_T_MARKER = re.compile(r"\s*`[A-Z]\d?`\s*")
_DAY_ANNOTATION = re.compile(r"\s*\(Day\s+\d+\)\s*")
_METADATA_SUFFIX = re.compile(r"\s+—\s+.*$")
_DIFFICULTY_TAG = re.compile(r"\s*\((E|M|H)\)\s*")
_SOURCE_TAG = re.compile(r"\s*\((nc-150\+|company question)\)\s*")
_VARIANT_TAG = re.compile(r"\s*\(variant of:\s*[^)]+\)\s*")
_PROBLEM_TEXT = re.compile(r"^\[[^\]]+\]\s*->\s*.+$")


def _extract_difficulty(text: str) -> Difficulty | None:
    match = _DIFFICULTY_TAG.search(text)
    if match is None:
        return None
    return match.group(1)  # type: ignore[return-value]


def _extract_source(text: str) -> Source:
    match = _SOURCE_TAG.search(text)
    if match is None:
        return "nc-150"
    return match.group(1)  # type: ignore[return-value]


def _extract_variant_of(text: str) -> str | None:
    match = re.search(r"\(variant of:\s*([^)]+)\)", text)
    return match.group(1).strip() if match else None


def _canonicalize(text: str) -> str:
    """Strip every non-canonical annotation: done-date stamp, em-dash metadata
    suffix, (Day N), (E)/(M)/(H), (nc-150+)/(company question), (variant of: X),
    `T2`/`M`."""
    text = _DONE_DATE.sub("", text)
    text = _METADATA_SUFFIX.sub("", text)
    text = _DAY_ANNOTATION.sub(" ", text)
    text = _DIFFICULTY_TAG.sub(" ", text)
    text = _SOURCE_TAG.sub(" ", text)
    text = _VARIANT_TAG.sub(" ", text)
    text = _T_MARKER.sub(" ", text)
    return re.sub(r"\s+", " ", text).strip()


def parse_curriculum(daily_md: str) -> list[Problem]:
    """Walk the daily schedule file, emit one Problem per checkbox line that
    matches the `[Category] -> Name` form under a `### Day N` heading."""
    problems: list[Problem] = []
    current_day: int | None = None

    for line in daily_md.splitlines():
        day_match = _DAY_HEADING.match(line)
        if day_match:
            current_day = int(day_match.group(1))
            continue
        if current_day is None:
            continue
        problem_match = _PROBLEM_LINE.match(line)
        if not problem_match:
            continue
        raw = problem_match.group(1)
        difficulty = _extract_difficulty(raw)
        source = _extract_source(raw)
        variant_of = _extract_variant_of(raw)
        canonical = _canonicalize(raw)
        if _PROBLEM_TEXT.match(canonical):
            problems.append(
                Problem(
                    text=canonical,
                    source_day=current_day,
                    difficulty=difficulty,
                    source=source,
                    variant_of=variant_of,
                )
            )

    return problems


def parse_phases(daily_md: str) -> list[CurriculumPhase]:
    """Walk the daily schedule file, emit one CurriculumPhase per `## Phase N — Name (Days A–B)` heading."""
    phases: list[CurriculumPhase] = []
    for line in daily_md.splitlines():
        match = _PHASE_HEADING.match(line)
        if match:
            phases.append(
                CurriculumPhase(
                    number=int(match.group(1)),
                    name=match.group(2).strip(),
                    days_start=int(match.group(3)),
                    days_end=int(match.group(4)),
                )
            )
    return phases


def parse_completions(today_md: str) -> list[Touch]:
    """Pull every checked, dated, problem-shaped line out of a today.md file."""
    touches: list[Touch] = []
    for line in today_md.splitlines():
        match = _CHECKED_LINE.match(line)
        if not match:
            continue
        body = match.group(1)
        date_match = _DONE_DATE.search(body)
        if not date_match:
            continue
        canonical = _canonicalize(body)
        if _PROBLEM_TEXT.match(canonical):
            touches.append(
                Touch(problem=canonical, on=date.fromisoformat(date_match.group(1)))
            )
    return touches


# ─── Ledger I/O ──────────────────────────────────────────────────────────────


def load_ledger(path: Path) -> list[Touch]:
    """Read the JSONL ledger. Empty list if the file does not exist yet."""
    if not path.exists():
        return []
    touches: list[Touch] = []
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        record = json.loads(line)
        touches.append(
            Touch(problem=record["problem"], on=date.fromisoformat(record["on"]))
        )
    return touches


def load_sd_chapters(path: Path) -> list[SDChapter]:
    """Read the user-editable SD chapter list. Empty list if the file does not
    exist yet. Each line is the latest state of one chapter; the file is
    edited in place rather than appended to."""
    if not path.exists():
        return []
    raw = json.loads(path.read_text())
    if not isinstance(raw, list):
        raise ValueError(f"{path} must contain a JSON list of SD chapters")
    chapters: list[SDChapter] = []
    for record in raw:
        completed = record.get("completed_date")
        chapters.append(
            SDChapter(
                id=record["id"],
                title=record["title"],
                book=record["book"],
                status=record["status"],
                completed_date=date.fromisoformat(completed) if completed else None,
            )
        )
    return chapters


def next_sd_chapter(chapters: list[SDChapter]) -> SDChapter | None:
    """First pending chapter in document order, or None if all complete."""
    for ch in chapters:
        if ch.status == "pending":
            return ch
    return None


def load_behavioral(path: Path) -> list[BehavioralTopic]:
    """Read the user-editable behavioral prep list. Empty list if the file
    does not exist yet."""
    if not path.exists():
        return []
    raw = json.loads(path.read_text())
    if not isinstance(raw, list):
        raise ValueError(f"{path} must contain a JSON list of behavioral topics")
    topics: list[BehavioralTopic] = []
    for record in raw:
        completed = record.get("completed_date")
        topics.append(
            BehavioralTopic(
                id=record["id"],
                prompt=record["prompt"],
                status=record["status"],
                completed_date=date.fromisoformat(completed) if completed else None,
                notes=record.get("notes"),
            )
        )
    return topics


def load_mocks(path: Path) -> list[Mock]:
    """Read the user-editable mocks JSON file. Empty list if the file does not
    exist yet. Unlike the ledger, mocks are mutable — each entry is the latest
    state of one mock interview, edited in place rather than appended to."""
    if not path.exists():
        return []
    raw = json.loads(path.read_text())
    if not isinstance(raw, list):
        raise ValueError(f"{path} must contain a JSON list of mocks")
    mocks: list[Mock] = []
    for record in raw:
        scheduled = record.get("scheduled_date")
        completed = record.get("completed_date")
        prereq_data = record.get("prerequisites")
        prerequisites: MockPrereq | None = None
        if isinstance(prereq_data, dict):
            prerequisites = MockPrereq(
                em_problems=int(prereq_data.get("em_problems", 0)),
                sd_chapters=int(prereq_data.get("sd_chapters", 0)),
            )
        mocks.append(
            Mock(
                id=record["id"],
                status=record["status"],
                platform=record.get("platform"),
                topic=record.get("topic"),
                scheduled_date=date.fromisoformat(scheduled) if scheduled else None,
                completed_date=date.fromisoformat(completed) if completed else None,
                notes=record.get("notes"),
                prerequisites=prerequisites,
                booking_url=record.get("booking_url"),
            )
        )
    return mocks


def mock_prereq_status(
    mock: Mock, em_done: int, sd_done: int
) -> list[tuple[str, bool, int, int]]:
    """For a mock with prerequisites, return list of (label, met, current, threshold).
    Empty list if the mock has no prereqs defined."""
    if mock.prerequisites is None or not mock.prerequisites.has_any:
        return []
    rows: list[tuple[str, bool, int, int]] = []
    if mock.prerequisites.em_problems > 0:
        rows.append(
            (
                "E/M problems",
                em_done >= mock.prerequisites.em_problems,
                em_done,
                mock.prerequisites.em_problems,
            )
        )
    if mock.prerequisites.sd_chapters > 0:
        rows.append(
            (
                "SD chapters",
                sd_done >= mock.prerequisites.sd_chapters,
                sd_done,
                mock.prerequisites.sd_chapters,
            )
        )
    return rows


def _format_prereq_line(rows: list[tuple[str, bool, int, int]]) -> str:
    """Single-line summary of prereq rows for use as a sub-bullet."""
    parts: list[str] = []
    for label, met, current, threshold in rows:
        marker = "✓" if met else "❌"
        parts.append(f"{marker} {threshold} {label} (have {current})")
    return f"  - Prereqs: {', '.join(parts)}"


def _render_next_mock_block(
    mock: Mock, today: date, em_done: int = 0, sd_done: int = 0
) -> list[str]:
    """One-mock display: status descriptor (scheduled date or pending), platform/topic,
    prereq sub-bullet if defined, and a booking link if pending. Used in today.md
    and coverage.md to surface the single mock the user should focus on next."""
    bits = [mock.platform or "", mock.topic or ""]
    descriptor = " · ".join(b for b in bits if b) or mock.id
    if mock.status == "scheduled" and mock.scheduled_date is not None:
        delta = (mock.scheduled_date - today).days
        if delta < 0:
            urgency = f"{abs(delta)}d ago — mark complete or reschedule"
        elif delta == 0:
            urgency = "today"
        elif delta == 1:
            urgency = "tomorrow"
        else:
            urgency = f"in {delta}d"
        date_str = (
            mock.scheduled_date.strftime("%a %b ").replace(" 0", " ")
            + str(mock.scheduled_date.day)
        )
        line = f"- {descriptor} · {date_str} ({urgency})"
    else:
        line = f"- {descriptor} · _pending — book this next_"
    lines = [line]
    prereqs = mock_prereq_status(mock, em_done, sd_done)
    if prereqs:
        lines.append(_format_prereq_line(prereqs))
    if mock.status == "pending":
        url = mock.effective_booking_url
        if url:
            lines.append(f"  - Book: [{mock.platform or 'link'}]({url})")
    return lines


def append_to_ledger(path: Path, new_touches: list[Touch]) -> int:
    """Append touches to the ledger, deduping against existing entries by
    (problem, date). Returns the number of touches actually written."""
    existing = {(t.problem, t.on) for t in load_ledger(path)}
    written = 0
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a") as f:
        for t in new_touches:
            key = (t.problem, t.on)
            if key in existing:
                continue
            existing.add(key)
            f.write(json.dumps({"problem": t.problem, "on": t.on.isoformat()}) + "\n")
            written += 1
    return written


# ─── Renderer ────────────────────────────────────────────────────────────────


def _format_date(d: date) -> str:
    return d.strftime("%b ").replace(" 0", " ") + str(d.day)


def _diff_suffix(d: Difficulty | None) -> str:
    return f" ({d})" if d else ""


def _render_recall_line(item: RecallItem) -> str:
    overdue_text = (
        "due today" if item.days_overdue == 0 else f"{item.days_overdue}d overdue"
    )
    return (
        f"- [ ] {item.problem}{_diff_suffix(item.difficulty)} — {overdue_text} · "
        f"{item.touches}× · last {_format_date(item.last_touched)}"
    )


def _render_new_line(problem: Problem) -> str:
    return f"- [ ] {problem.text}{_diff_suffix(problem.difficulty)} (Day {problem.source_day})"


def _format_projection_line(
    end: date, rate: float, untouched: int, today: date
) -> str:
    days_remaining = (end - today).days
    return (
        f"_Projected acquisition complete: ~{_format_date(end)}, {end.year} "
        f"({rate:.1f} new/day · {untouched} left · ~{days_remaining}d remaining)_"
    )


def render_today(
    today: date,
    recall: list[RecallItem],
    new: list[Problem],
    *,
    day_n: int | None = None,
    phase: CurriculumPhase | None = None,
    daily_md_link: str = "./prep-plan-daily.md",
    projection: date | None = None,
    projection_rate: float | None = None,
    projection_untouched: int | None = None,
    sd_next: SDChapter | None = None,
    readiness: Readiness | None = None,
    next_up_mock: Mock | None = None,
    em_done: int = 0,
    sd_done: int = 0,
) -> str:
    """Produce the markdown that gets written to today.md.

    The header reflects sprint state:
    - No ledger yet → `· Pre-prep`
    - Ledger exists, no matching phase → `· Day N`
    - Ledger exists and inside a known phase → `· [Phase X — Name](link) · Day N`

    If `projection` is provided, an italic line below the header shows the
    estimated complete date, current pace, and remaining problem count.
    """
    weekday = today.strftime("%a")
    base_header = f"# Today — {weekday} {_format_date(today)}, {today.year}"
    if day_n is None:
        header = f"{base_header} · Pre-prep"
    elif phase is None:
        header = f"{base_header} · Day {day_n}"
    else:
        link = f"[{phase.heading}]({daily_md_link}#{phase.slug})"
        header = f"{base_header} · {link} · Day {day_n}"

    lines = [header, ""]
    if (
        projection is not None
        and projection_rate is not None
        and projection_untouched is not None
        and projection_untouched > 0
    ):
        lines.append(
            _format_projection_line(
                projection, projection_rate, projection_untouched, today
            )
        )
        lines.append("")
    lines.extend(
        [
            "_Generated by `prep recompute`. Re-run anytime to refresh._",
            "",
        ]
    )
    if readiness is not None:
        lines.extend(render_readiness_block(readiness))
    if next_up_mock is not None:
        lines.extend(["## Next mock", ""])
        lines.extend(
            _render_next_mock_block(next_up_mock, today, em_done, sd_done)
        )
        lines.append("")
    lines.extend(["## Recall — most overdue first", ""])
    if recall:
        lines.extend(_render_recall_line(item) for item in recall)
    else:
        lines.append("_Empty — no problems are overdue yet._")
    lines.extend(["", "## New — next from the curriculum", ""])
    if new:
        lines.extend(_render_new_line(p) for p in new)
    else:
        lines.append(
            "_Empty — every curriculum problem has been touched at least once._"
        )

    if sd_next is not None:
        lines.extend(
            [
                "",
                "## Today's SD reading",
                "",
                f"- [ ] {sd_next.book} · {sd_next.title}",
            ]
        )

    if today.weekday() == 5:  # Saturday
        lines.extend(
            [
                "",
                "## This week's hardest — your pick",
                "",
                "_Re-solve 2-3 problems you found hardest this week (from your daily \"today's hardest\" notes Mon–Fri). Write the canonical `[Pattern] -> Name` form between the brackets so ticking logs a real touch._",
                "",
                "- [ ] [Pattern] -> Problem Name",
                "- [ ] [Pattern] -> Problem Name",
                "- [ ] [Pattern] -> Problem Name",
            ]
        )

    lines.append("")
    return "\n".join(lines)


# ─── Mock progress + upcoming ────────────────────────────────────────────────


def _progress_bar(done: int, total: int, width: int = 13) -> str:
    """Unicode block bar for inline visualization. Always renders even if total
    is 0 (returns an empty bar)."""
    if total <= 0:
        return f"[{'░' * width}]"
    filled = round((done / total) * width)
    return f"[{'█' * filled}{'░' * (width - filled)}]"


def next_mock(mocks: list[Mock]) -> Mock | None:
    """The first non-completed mock in document order — the one the user
    should focus on next, whether it's scheduled or still pending. Returns
    None if every mock is completed."""
    for m in mocks:
        if m.status != "completed":
            return m
    return None


def upcoming_mocks(
    mocks: list[Mock], today: date, window_days: int = 14
) -> list[Mock]:
    """Mocks that are scheduled and due to happen within the next `window_days`,
    sorted soonest first. Past-dated scheduled mocks (forgotten to mark complete)
    also surface so the user notices."""
    soon: list[Mock] = []
    for m in mocks:
        if m.status != "scheduled" or m.scheduled_date is None:
            continue
        delta = (m.scheduled_date - today).days
        if delta <= window_days:
            soon.append(m)
    soon.sort(key=lambda m: m.scheduled_date or today)
    return soon


def _format_mock_line(mock: Mock) -> str:
    """One bullet describing a single mock — its status, date, platform, topic."""
    bits: list[str] = []
    if mock.platform:
        bits.append(mock.platform)
    if mock.topic:
        bits.append(mock.topic)
    descriptor = " · ".join(bits) if bits else mock.id
    if mock.status == "completed" and mock.completed_date:
        return f"- [x] {descriptor} · ✅ {mock.completed_date.isoformat()}"
    if mock.status == "scheduled" and mock.scheduled_date:
        return f"- [ ] {descriptor} · 📅 {mock.scheduled_date.isoformat()}"
    return f"- [ ] {descriptor} · _pending_"


def _render_upcoming_mocks_block(
    mocks: list[Mock],
    today: date,
    em_done: int = 0,
    sd_done: int = 0,
) -> list[str]:
    """The 'Upcoming mocks' block that surfaces in today.md when scheduled
    mocks are within the look-ahead window. Each mock with prerequisites
    gets a sub-bullet showing whether its thresholds are met."""
    lines: list[str] = []
    for m in mocks:
        assert m.scheduled_date is not None  # filtered by upcoming_mocks
        delta = (m.scheduled_date - today).days
        if delta < 0:
            urgency = f"{abs(delta)}d ago — mark complete or reschedule"
        elif delta == 0:
            urgency = "today"
        elif delta == 1:
            urgency = "tomorrow"
        else:
            urgency = f"in {delta}d"
        bits = [m.platform or "", m.topic or ""]
        descriptor = " · ".join(b for b in bits if b) or m.id
        lines.append(
            f"- {descriptor} · {m.scheduled_date.strftime('%a %b ').replace(' 0', ' ')}"
            f"{m.scheduled_date.day} ({urgency})"
        )
        prereqs = mock_prereq_status(m, em_done, sd_done)
        if prereqs:
            lines.append(_format_prereq_line(prereqs))
    return lines


# ─── Application-readiness gates ─────────────────────────────────────────────


# Target-ready partial thresholds. Stretch-ready demands everything (no constant
# needed). Tweak in code if you want a stricter target gate.
_TARGET_READY_MIN_MOCKS = 8
_TARGET_READY_MIN_SD_CHAPTERS = 20


def compute_readiness(
    curriculum: list[Problem],
    ledger: list[Touch],
    sd_chapters: list[SDChapter],
    mocks: list[Mock],
) -> Readiness:
    """Roll up the three ledgers into a Readiness summary with three tiered
    application gates: Fallback-ready (E+M done), Target-ready (E+M + partial
    SD + partial mocks), Stretch-ready (everything)."""
    touched = {t.problem for t in ledger}
    em_curriculum = [p for p in curriculum if p.difficulty in ("E", "M")]
    em_done = sum(1 for p in em_curriculum if p.text in touched)
    em = CategoryProgress(
        name="E+M problems", done=em_done, total=len(em_curriculum)
    )
    em_complete = em.done == em.total and em.total > 0

    sd_done = sum(1 for c in sd_chapters if c.status == "completed")
    sd = CategoryProgress(
        name="System Design", done=sd_done, total=len(sd_chapters)
    )
    sd_complete = sd.done == sd.total and sd.total > 0

    mocks_done = sum(1 for m in mocks if m.status == "completed")
    mock_progress = CategoryProgress(
        name="Mocks", done=mocks_done, total=len(mocks)
    )
    mocks_complete = mock_progress.done == mock_progress.total and mock_progress.total > 0

    all_curriculum_done = all(p.text in touched for p in curriculum) and curriculum

    tiers = [
        ReadinessTier(
            name="Fallback-ready",
            criteria=[("All E+M problems touched", em_complete)],
        ),
        ReadinessTier(
            name="Target-ready",
            criteria=[
                ("All E+M problems touched", em_complete),
                (
                    f"≥{_TARGET_READY_MIN_SD_CHAPTERS} SD chapters complete",
                    sd.done >= _TARGET_READY_MIN_SD_CHAPTERS,
                ),
                (
                    f"≥{_TARGET_READY_MIN_MOCKS} mocks completed",
                    mock_progress.done >= _TARGET_READY_MIN_MOCKS,
                ),
            ],
        ),
        ReadinessTier(
            name="Stretch-ready",
            criteria=[
                ("All curriculum problems touched", bool(all_curriculum_done)),
                ("All SD chapters complete", sd_complete),
                ("All mocks completed", mocks_complete),
            ],
        ),
    ]

    return Readiness(em=em, sd=sd, mocks=mock_progress, tiers=tiers)


def _render_category_line(cat: CategoryProgress) -> str:
    """One percentage-bar line for the readiness block."""
    pct = round(cat.fraction * 100)
    return (
        f"- {cat.name:<14} {_progress_bar(cat.done, cat.total)} "
        f"{pct}% ({cat.done}/{cat.total})"
    )


def render_readiness_block(readiness: Readiness) -> list[str]:
    """The Readiness section that appears at the top of today.md and coverage.md.
    Shows three category bars plus a status indicator per application tier."""
    lines = ["## Readiness", ""]
    lines.append(_render_category_line(readiness.em))
    lines.append(_render_category_line(readiness.sd))
    lines.append(_render_category_line(readiness.mocks))
    lines.append("")
    for tier in readiness.tiers:
        marker = "✓" if tier.met else "❌"
        lines.append(f"**{tier.name}: {marker}**")
        for label, ok in tier.criteria:
            sub = "✓" if ok else "❌"
            lines.append(f"  - {sub} {label}")
        lines.append("")
    return lines


# ─── Mocks view (dedicated) ──────────────────────────────────────────────────


def _render_mocks_section(
    mocks: list[Mock],
    today: date,
    em_done: int = 0,
    sd_done: int = 0,
) -> list[str]:
    """The `## Mocks` section in coverage.md. Summary line + Next (one entry,
    the first non-completed mock with prereqs) + Completed history. Future
    pending mocks aren't listed individually — the user works through them
    sequentially, so only the immediate next one matters."""
    completed_count = sum(1 for m in mocks if m.status == "completed")
    scheduled_count = sum(1 for m in mocks if m.status == "scheduled")
    pending_count = sum(1 for m in mocks if m.status == "pending")
    total = len(mocks)

    lines = [
        f"## Mocks ({completed_count}/{total} complete · {scheduled_count} scheduled · {pending_count} pending)",
        "",
        f"{_progress_bar(completed_count, total)} {completed_count}/{total}",
        "",
    ]

    if total == 0:
        lines.append(
            "_No mocks tracked yet. Add entries to `prep-data/mock_interviews.json` "
            "(see `mock_interviews.example.json` for the schema)._"
        )
        lines.append("")
        return lines

    nxt = next_mock(mocks)
    lines.append("### Next")
    lines.append("")
    if nxt is not None:
        lines.extend(_render_next_mock_block(nxt, today, em_done, sd_done))
    else:
        lines.append("_All mocks completed._")
    lines.append("")

    completed_mocks = [m for m in mocks if m.status == "completed"]
    if completed_mocks:
        lines.append("### Completed")
        lines.append("")
        for m in completed_mocks:
            note = f" — _{m.notes}_" if m.notes else ""
            lines.append(f"{_format_mock_line(m)}{note}")
        lines.append("")

    return lines


# ─── Coverage view ───────────────────────────────────────────────────────────


def _render_behavioral_section(topics: list[BehavioralTopic]) -> list[str]:
    completed = sum(1 for t in topics if t.status == "completed")
    total = len(topics)
    lines = [
        f"## Behavioral ({completed}/{total} complete)",
        "",
        f"{_progress_bar(completed, total)} {completed}/{total}",
        "",
    ]
    if topics:
        for t in topics:
            box = "x" if t.status == "completed" else " "
            stamp = (
                f" · ✅ {t.completed_date.isoformat()}"
                if t.completed_date
                else ""
            )
            note = f" — _{t.notes}_" if t.notes else ""
            lines.append(f"- [{box}] {t.prompt}{stamp}{note}")
    else:
        lines.append("_Empty — add prompts to `prep-data/behavioral_prompts.json`._")
    lines.append("")
    return lines


def _render_sd_section(sd_chapters: list[SDChapter]) -> list[str]:
    completed = sum(1 for c in sd_chapters if c.status == "completed")
    total = len(sd_chapters)
    lines = [
        f"## System Design ({completed}/{total} complete)",
        "",
        f"{_progress_bar(completed, total)} {completed}/{total}",
        "",
    ]
    if sd_chapters:
        for ch in sd_chapters:
            box = "x" if ch.status == "completed" else " "
            stamp = (
                f" · ✅ {ch.completed_date.isoformat()}"
                if ch.completed_date
                else ""
            )
            lines.append(f"- [{box}] {ch.book} · {ch.title}{stamp}")
    else:
        lines.append("_Empty — add chapters to `prep-data/system_design_chapters.json`._")
    lines.append("")
    return lines


def _render_dsa_by_pattern(
    curriculum: list[Problem], ledger: list[Touch]
) -> list[str]:
    touched = {t.problem for t in ledger}
    indexed = list(enumerate(curriculum))
    indexed.sort(key=lambda i: (_SOURCE_RANK.get(i[1].source, 0), i[0]))
    by_pattern: dict[str, list[Problem]] = {}
    for _, p in indexed:
        by_pattern.setdefault(p.pattern, []).append(p)

    lines = ["## DSA — by pattern", ""]
    for pattern, items in by_pattern.items():
        canonical_names = {p.name for p in items if p.variant_of is None}
        variants_by_canonical: dict[str, list[Problem]] = {}
        loose_variants: list[Problem] = []
        for p in items:
            if p.variant_of is None:
                continue
            if p.variant_of in canonical_names:
                variants_by_canonical.setdefault(p.variant_of, []).append(p)
            else:
                loose_variants.append(p)

        lines.append(f"### {pattern}")
        for p in items:
            if p.variant_of is not None:
                continue
            box = "x" if p.text in touched else " "
            lines.append(f"- [{box}] {p.name}{_diff_suffix(p.difficulty)}")
            for variant in variants_by_canonical.get(p.name, []):
                vbox = "x" if variant.text in touched else " "
                lines.append(
                    f"  - [{vbox}] {variant.name}{_diff_suffix(variant.difficulty)}"
                )
        for variant in loose_variants:
            vbox = "x" if variant.text in touched else " "
            lines.append(
                f"- [{vbox}] {variant.name}{_diff_suffix(variant.difficulty)} "
                f"_(variant of {variant.variant_of})_"
            )
        lines.append("")
    return lines


def render_coverage(
    curriculum: list[Problem],
    ledger: list[Touch],
    today: date | None = None,
    mocks: list[Mock] | None = None,
    sd_chapters: list[SDChapter] | None = None,
    readiness: Readiness | None = None,
    behavioral: list[BehavioralTopic] | None = None,
    em_done: int = 0,
    sd_done: int = 0,
) -> str:
    """Render the comprehensive overview file:
    Readiness → Behavioral → Mocks → System Design → DSA-by-pattern.

    One file for all comprehensive state — open it whenever you want a high-level
    view of progress, what's left, and what's coming up. The daily queue lives in today.md."""
    lines = [
        "# Coverage",
        "",
        "_Generated by `prep recompute`. Comprehensive overview — readiness, behavioral, mocks, system design, and the full DSA curriculum by pattern. Boxes auto-check from the ledger and per-category JSON files._",
        "",
    ]
    if readiness is not None:
        lines.extend(render_readiness_block(readiness))
    if behavioral is not None:
        lines.extend(_render_behavioral_section(behavioral))
    if mocks is not None:
        lines.extend(
            _render_mocks_section(
                mocks, today=today or date.today(), em_done=em_done, sd_done=sd_done
            )
        )
    if sd_chapters is not None:
        lines.extend(_render_sd_section(sd_chapters))
    lines.extend(_render_dsa_by_pattern(curriculum, ledger))
    return "\n".join(lines)


# ─── Orchestration ───────────────────────────────────────────────────────────


def recompute(
    daily_md_path: Path,
    today_md_path: Path,
    ledger_path: Path,
    today: date,
    recall_limit: int = DEFAULT_RECALL_LIMIT,
    new_limit: int = DEFAULT_NEW_LIMIT,
    coverage_md_path: Path | None = None,
    mocks_path: Path | None = None,
    sd_chapters_path: Path | None = None,
    behavioral_path: Path | None = None,
) -> RecomputeResult:
    """One full cycle: log yesterday's completions, then regenerate today.md
    (with the readiness banner at the top) and the comprehensive coverage.md
    overview — Readiness → Mocks → SD → DSA-by-pattern."""
    daily_md = daily_md_path.read_text()
    curriculum = parse_curriculum(daily_md)
    phases = parse_phases(daily_md)

    new_touches: list[Touch] = []
    if today_md_path.exists():
        new_touches = parse_completions(today_md_path.read_text())
    logged = append_to_ledger(ledger_path, new_touches)

    ledger = load_ledger(ledger_path)
    recall = compute_recall(
        ledger, today=today, limit=recall_limit, curriculum=curriculum
    )
    new = compute_new(curriculum, ledger, limit=new_limit)

    start = start_date(ledger)
    day_n = day_n_for(today, start) if start else None
    phase = phase_for(day_n, phases) if day_n is not None else None

    rate = avg_new_per_day(ledger, today)
    end = projected_end_date(ledger, curriculum, today)
    touched = {t.problem for t in ledger}
    untouched = sum(1 for p in curriculum if p.text not in touched)

    mocks: list[Mock] = []
    if mocks_path is not None and mocks_path.exists():
        mocks = load_mocks(mocks_path)
    next_up_mock = next_mock(mocks) if mocks else None

    sd_chapters: list[SDChapter] = []
    if sd_chapters_path is not None and sd_chapters_path.exists():
        sd_chapters = load_sd_chapters(sd_chapters_path)
    sd_next = next_sd_chapter(sd_chapters) if sd_chapters else None

    behavioral: list[BehavioralTopic] = []
    if behavioral_path is not None and behavioral_path.exists():
        behavioral = load_behavioral(behavioral_path)

    readiness = compute_readiness(curriculum, ledger, sd_chapters, mocks)

    em_done_count = readiness.em.done
    sd_done_count = readiness.sd.done

    today_md_path.write_text(
        render_today(
            today=today,
            recall=recall,
            new=new,
            day_n=day_n,
            phase=phase,
            projection=end,
            projection_rate=rate,
            projection_untouched=untouched,
            sd_next=sd_next,
            readiness=readiness,
            next_up_mock=next_up_mock,
            em_done=em_done_count,
            sd_done=sd_done_count,
        )
    )

    if coverage_md_path is not None:
        coverage_md_path.parent.mkdir(parents=True, exist_ok=True)
        coverage_md_path.write_text(
            render_coverage(
                curriculum,
                ledger,
                today=today,
                mocks=mocks if mocks_path else None,
                sd_chapters=sd_chapters if sd_chapters_path else None,
                readiness=readiness,
                behavioral=behavioral if behavioral_path else None,
                em_done=em_done_count,
                sd_done=sd_done_count,
            )
        )

    return RecomputeResult(
        new_touches_logged=logged, recall_size=len(recall), new_size=len(new)
    )


# ─── CLI ─────────────────────────────────────────────────────────────────────


@click.group()
def cli() -> None:
    """Snapshot-mode recall engine for the NeetCode 150 curriculum."""


@cli.command(name="recompute")
@click.option(
    "--daily",
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
    default=Path("prep-plan-daily.md"),
    show_default=True,
    help="Curriculum / schedule reference markdown.",
)
@click.option(
    "--today-md",
    type=click.Path(dir_okay=False, path_type=Path),
    default=Path("prep-data/today.md"),
    show_default=True,
    help="Generated daily list. Overwritten on every recompute.",
)
@click.option(
    "--ledger",
    type=click.Path(dir_okay=False, path_type=Path),
    default=Path("prep-data/completions.jsonl"),
    show_default=True,
    help="Append-only completion ledger.",
)
@click.option(
    "--coverage-md",
    type=click.Path(dir_okay=False, path_type=Path),
    default=Path("prep-data/coverage.md"),
    show_default=True,
    help="Generated by-pattern coverage view. Overwritten on every recompute.",
)
@click.option(
    "--mocks",
    type=click.Path(dir_okay=False, path_type=Path),
    default=Path("prep-data/mock_interviews.json"),
    show_default=True,
    help="User-editable list of mock interviews (pending/scheduled/completed).",
)
@click.option(
    "--sd-chapters",
    type=click.Path(dir_okay=False, path_type=Path),
    default=Path("prep-data/system_design_chapters.json"),
    show_default=True,
    help="User-editable list of System Design chapters (pending/completed).",
)
@click.option(
    "--behavioral",
    type=click.Path(dir_okay=False, path_type=Path),
    default=Path("prep-data/behavioral_prompts.json"),
    show_default=True,
    help="User-editable list of behavioral interview prompts (pending/completed).",
)
def recompute_cmd(
    daily: Path,
    today_md: Path,
    ledger: Path,
    coverage_md: Path,
    mocks: Path,
    sd_chapters: Path,
    behavioral: Path,
) -> None:
    """Fold yesterday's checks into the ledger, then regenerate today.md and coverage.md."""
    result = recompute(
        daily,
        today_md,
        ledger,
        today=date.today(),
        coverage_md_path=coverage_md,
        mocks_path=mocks,
        sd_chapters_path=sd_chapters,
        behavioral_path=behavioral,
    )
    click.echo(
        f"logged {result.new_touches_logged} new touch(es) · "
        f"recall: {result.recall_size} · new: {result.new_size}"
    )


@cli.command(name="reset")
@click.option("--dsa", is_flag=True, help="Delete the DSA completion ledger.")
@click.option(
    "--sd",
    is_flag=True,
    help="Delete the system-design ledger (reserved — no SD ledger exists yet).",
)
@click.option(
    "--all", "all_", is_flag=True, help="Delete every ledger this command knows about."
)
@click.option("--yes", is_flag=True, help="Skip the confirmation prompt.")
@click.option(
    "--ledger-dir",
    type=click.Path(file_okay=False, path_type=Path),
    default=Path("prep-data"),
    show_default=True,
    help="Directory containing the ledger files.",
)
def reset_cmd(dsa: bool, sd: bool, all_: bool, yes: bool, ledger_dir: Path) -> None:
    """Delete one or more ledgers. Deletion = the next recompute treats you as pre-prep."""
    targets: list[tuple[str, Path]] = []
    if dsa or all_:
        targets.append(("DSA ledger", ledger_dir / "completions.jsonl"))
    if sd or all_:
        targets.append(
            ("SD ledger (not yet in use)", ledger_dir / "sd-completions.jsonl")
        )
    if not targets:
        click.echo("Nothing to reset. Pass --dsa, --sd, or --all.")
        return
    click.echo("Will delete:")
    for label, path in targets:
        existence = "exists" if path.exists() else "does not exist (no-op)"
        click.echo(f"  - {label}: {path} ({existence})")
    if not yes and not click.confirm("Proceed?", default=False):
        click.echo("Aborted.")
        return
    for _label, path in targets:
        if path.exists():
            path.unlink()
    click.echo("Reset complete. Run `recompute` to regenerate today.md.")


if __name__ == "__main__":
    cli()
