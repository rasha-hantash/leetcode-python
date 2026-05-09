"""Recall engine: snapshot-mode SM-2 lite scheduler for the NeetCode 150 curriculum.

Reads `curriculum.md` (single master list — DSA grouped by phase → pattern,
plus System Design / Mocks / Behavioral sections) and the previous `today.md`
(yesterday's checked-off items), folds new completions into an append-only
JSONL ledger, then regenerates `today.md` with today's Recall and New sections.
Phase advancement is ledger-driven: the current phase is the lowest-numbered
one with eligible untouched problems.

Designed to run once per morning (LaunchAgent) or on-demand (`prep recompute`).
There is no live daemon — today's set is frozen until the next recompute call.
"""

from __future__ import annotations

import calendar
import json
import math
import re
from dataclasses import dataclass, replace
from datetime import date, timedelta
from pathlib import Path
from typing import Any, Iterable, Literal

import click


# ─── Constants ────────────────────────────────────────────────────────────────

INTERVALS_DAYS: list[int] = [1, 3, 7, 21, 60]
"""SM-2 lite: interval after the Nth touch (1-indexed). 5+ touches stay at 60."""

DEFAULT_RECALL_LIMIT = 10
DEFAULT_NEW_LIMIT = 3

Difficulty = Literal["E", "M", "H"]
Source = Literal["nc-150", "nc-150+", "company question"]

_SOURCE_RANK: dict[str, int] = {"nc-150": 0, "nc-150+": 1, "company question": 2}
_DIFFICULTY_RANK: dict[str, int] = {"E": 0, "M": 1, "H": 2}


# ─── Data types ──────────────────────────────────────────────────────────────


@dataclass(frozen=True)
class Problem:
    """A curriculum entry: canonical problem text + optional metadata tags.

    `phase` is the phase number this problem was placed under in
    `curriculum.md` (set by `parse_curriculum`). None means the problem was
    parsed from a file without phase headings (legacy or test fixtures)."""

    text: str
    difficulty: Difficulty | None = None
    source: Source = "nc-150"
    variant_of: str | None = None
    phase: int | None = None

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
class Phase:
    """A curriculum phase: an ordinal section in `curriculum.md` with a
    daily new-problem budget. Phase membership lives on the Problem itself
    (set by `parse_curriculum` from the `### Phase N — Name (X new/day)`
    headings). `new_per_day=0` puts the phase in recall-only mode."""

    number: int
    name: str
    new_per_day: int


MockStatus = Literal["pending", "scheduled", "completed"]


@dataclass(frozen=True)
class MockPrereq:
    """Per-mock readiness thresholds. `sd_chapter_ids` (when set) overrides
    `sd_chapters` — the count then derives from the list length."""

    em_problems: int = 0
    sd_chapters: int = 0
    sd_chapter_ids: tuple[str, ...] = ()

    @property
    def has_any(self) -> bool:
        return bool(self.em_problems or self.sd_chapters or self.sd_chapter_ids)


@dataclass(frozen=True)
class PrereqRow:
    """One row of a prereq summary line; `detail` is an optional inline breakdown."""

    label: str
    met: bool
    current: int
    threshold: int
    detail: str | None = None


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
        """Per-mock override wins; otherwise the platform default. None if neither."""
        return self.booking_url or _PLATFORM_BOOKING_URLS.get(self.platform or "")

    @property
    def descriptor(self) -> str:
        """Human-readable label: `platform · topic`, or the id as fallback."""
        return " · ".join(b for b in (self.platform, self.topic) if b) or self.id


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
    """Completion of one prep category (E+M, SD, mocks). Drives bars and gates."""

    name: str
    done: int
    total: int

    @property
    def fraction(self) -> float:
        return self.done / self.total if self.total > 0 else 0.0

    @property
    def complete(self) -> bool:
        return self.total > 0 and self.done == self.total


@dataclass(frozen=True)
class Readiness:
    """Three category bars + tiers (ordered fallback → target → stretch)."""

    em: CategoryProgress
    sd: CategoryProgress
    mocks: CategoryProgress
    tiers: list["ReadinessTier"]


@dataclass(frozen=True)
class ReadinessTier:
    """One application-readiness gate as a list of (label, met) criteria."""

    name: str
    criteria: list[tuple[str, bool]]

    @property
    def met(self) -> bool:
        return all(ok for _, ok in self.criteria)


@dataclass(frozen=True)
class RecomputeResult:
    """Summary of one `recompute()` call, surfaced via the CLI."""

    new_touches_logged: int
    recall_size: int
    new_size: int


# ─── SM-2 lite arithmetic ────────────────────────────────────────────────────


def interval_for(touches: int) -> int:
    """Days from last touch to next due. Saturates at the last entry."""
    return INTERVALS_DAYS[min(touches, len(INTERVALS_DAYS)) - 1]


def due_date(touches: int, last_touched: date) -> date:
    return last_touched + timedelta(days=interval_for(touches))


def overdue_days(touches: int, last_touched: date, today: date) -> int:
    """Positive = past due. Zero = exactly due. Negative = not yet due."""
    return (today - due_date(touches, last_touched)).days


# ─── Sprint day math ─────────────────────────────────────────────────────────


def start_date(ledger: list[Touch]) -> date | None:
    """Earliest touch in the ledger; None if empty. Anchors Day 1."""
    return min((t.on for t in ledger), default=None)


def day_n_for(today: date, start: date) -> int:
    """Day number relative to start. start_date itself is Day 1."""
    return (today - start).days + 1


# ─── Pace projection ─────────────────────────────────────────────────────────


def avg_new_per_day(ledger: list[Touch], today: date) -> float | None:
    """Distinct problems per day since start_date. None if ledger is empty."""
    start = start_date(ledger)
    if start is None:
        return None
    return len({t.problem for t in ledger}) / day_n_for(today, start)


def projected_end_date(
    ledger: list[Touch],
    curriculum: list[Problem],
    today: date,
) -> date | None:
    """Calendar date when every curriculum problem has ≥1 touch at current pace.
    None if the ledger is empty; `today` if curriculum is already complete."""
    rate = avg_new_per_day(ledger, today)
    if not rate:
        return None
    touched = {t.problem for t in ledger}
    untouched = sum(1 for p in curriculum if p.text not in touched)
    if untouched == 0:
        return today
    return today + timedelta(days=math.ceil(untouched / rate))


# ─── Touch aggregation ───────────────────────────────────────────────────────


def aggregate_touches(ledger: Iterable[Touch]) -> dict[str, tuple[int, date]]:
    """Roll the ledger up to {problem: (touch_count, latest_completion_date)}."""
    summary: dict[str, tuple[int, date]] = {}
    for t in ledger:
        count, latest = summary.get(t.problem, (0, t.on))
        summary[t.problem] = (count + 1, max(latest, t.on))
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
    curriculum: list[Problem],
    ledger: list[Touch],
    limit: int = DEFAULT_NEW_LIMIT,
    phase: Phase | None = None,
) -> list[Problem]:
    """The next N never-touched problems, ordered by source provenance
    (nc-150 > nc-150+ > company question), then difficulty (E → M → H),
    then document order. When `phase` is given, the pool is filtered to
    problems assigned to that phase number in curriculum.md and the limit
    defaults to `phase.new_per_day` (so `new_per_day=0` returns nothing)."""
    touched = {t.problem for t in ledger}
    pool = [p for p in curriculum if p.text not in touched]
    if phase is not None:
        pool = [p for p in pool if p.phase == phase.number]
        limit = phase.new_per_day
    return sorted(
        pool,
        key=lambda p: (
            _SOURCE_RANK.get(p.source, 0),
            _DIFFICULTY_RANK.get(p.difficulty or "M", 1),
        ),
    )[:limit]


def current_phase(
    curriculum: list[Problem], ledger: list[Touch], phases: list[Phase]
) -> Phase | None:
    """The lowest-numbered phase that still has untouched problems assigned to
    it. Falls through to the last phase when every prior phase is drained.
    Returns None if `phases` is empty."""
    if not phases:
        return None
    touched = {t.problem for t in ledger}
    ordered = sorted(phases, key=lambda ph: ph.number)
    return next(
        (
            ph for ph in ordered
            if any(p.phase == ph.number and p.text not in touched for p in curriculum)
        ),
        ordered[-1],
    )


# ─── Parsers ─────────────────────────────────────────────────────────────────


_DSA_HEADING = re.compile(r"^##\s+DSA\s*$")
_PHASE_HEADING = re.compile(r"^###\s+Phase\s+(\d+)\s+—\s+(.+?)\s+\((\d+)\s+new/day\)\s*$")
_PATTERN_SUBHEADING = re.compile(r"^####\s+(.+?)\s*$")
_OTHER_H2 = re.compile(r"^##\s+(.+?)\s*$")
_PROBLEM_LINE = re.compile(r"^\s*-\s+\[[ xX]\]\s+(.*)$")
_CHECKED_LINE = re.compile(r"^\s*-\s+\[[xX]\]\s+(.*)$")
_DONE_DATE = re.compile(r"\s*✅\s*(\d{4}-\d{2}-\d{2}).*$")
_T_MARKER = re.compile(r"\s*`[A-Z]\d?`\s*")
_DAY_ANNOTATION = re.compile(r"\s*\(Day\s+\d+\)\s*")
_METADATA_SUFFIX = re.compile(r"\s+—\s+.*$")
_DIFFICULTY_TAG = re.compile(r"\s*\((E|M|H)\)\s*")
_SOURCE_TAG = re.compile(r"\s*\((nc-150\+|company question)\)\s*")
_VARIANT_TAG = re.compile(r"\s*\(variant of:\s*([^)]+)\)\s*")
_PROBLEM_TEXT = re.compile(r"^\[[^\]]+\]\s*->\s*.+$")


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


def parse_curriculum(curriculum_md: str) -> list[Problem]:
    """Walk the `## DSA` section of `curriculum.md`, emit one Problem per
    checkbox line under `### Phase N — Name (X new/day)` → `#### Pattern`
    headings. Canonical text is reconstructed as `[Pattern] -> Name`."""
    problems: list[Problem] = []
    in_dsa = False
    phase_num: int | None = None
    pattern: str | None = None

    for line in curriculum_md.splitlines():
        if _DSA_HEADING.match(line):
            in_dsa = True
            phase_num = None
            pattern = None
            continue
        # Any other top-level heading exits the DSA section.
        h2 = _OTHER_H2.match(line)
        if h2 and not _DSA_HEADING.match(line):
            in_dsa = False
            phase_num = None
            pattern = None
            continue
        if not in_dsa:
            continue
        if (m := _PHASE_HEADING.match(line)):
            phase_num = int(m.group(1))
            pattern = None
            continue
        if (m := _PATTERN_SUBHEADING.match(line)):
            pattern = m.group(1).strip()
            continue
        if pattern is None:
            continue
        problem_match = _PROBLEM_LINE.match(line)
        if not problem_match:
            continue
        raw = problem_match.group(1)
        diff_m = _DIFFICULTY_TAG.search(raw)
        src_m = _SOURCE_TAG.search(raw)
        var_m = _VARIANT_TAG.search(raw)
        name = _DIFFICULTY_TAG.sub(" ", raw)
        name = _SOURCE_TAG.sub(" ", name)
        name = _VARIANT_TAG.sub(" ", name)
        name = _T_MARKER.sub(" ", name)
        name = _DONE_DATE.sub("", name)
        name = re.sub(r"\s+", " ", name).strip()
        if not name:
            continue
        problems.append(
            Problem(
                text=f"[{pattern}] -> {name}",
                difficulty=diff_m.group(1) if diff_m else None,  # type: ignore[arg-type]
                source=src_m.group(1) if src_m else "nc-150",  # type: ignore[arg-type]
                variant_of=var_m.group(1).strip() if var_m else None,
                phase=phase_num,
            )
        )

    return problems


def parse_phases(curriculum_md: str) -> list[Phase]:
    """Walk the `## DSA` section, return one Phase per `### Phase N — Name (X new/day)` heading."""
    phases: list[Phase] = []
    in_dsa = False
    for line in curriculum_md.splitlines():
        if _DSA_HEADING.match(line):
            in_dsa = True
            continue
        h2 = _OTHER_H2.match(line)
        if h2 and not _DSA_HEADING.match(line):
            in_dsa = False
            continue
        if not in_dsa:
            continue
        if (m := _PHASE_HEADING.match(line)):
            phases.append(Phase(
                number=int(m.group(1)),
                name=m.group(2).strip(),
                new_per_day=int(m.group(3)),
            ))
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


def _opt_date(s: str | None) -> date | None:
    return date.fromisoformat(s) if s else None


def load_ledger(path: Path) -> list[Touch]:
    """Read the JSONL ledger. Empty list if the file does not exist."""
    if not path.exists():
        return []
    touches: list[Touch] = []
    for line in path.read_text().splitlines():
        if not line.strip():
            continue
        r = json.loads(line)
        touches.append(Touch(problem=r["problem"], on=date.fromisoformat(r["on"])))
    return touches


def next_sd_chapter(chapters: list[SDChapter]) -> SDChapter | None:
    """First pending chapter, or None if all complete."""
    return next((ch for ch in chapters if ch.status == "pending"), None)


# ─── Curriculum-MD section parsers (SD / Mocks / Behavioral) ──────────────────


_ID_PREFIX = re.compile(r"^\[([^\]]+)\]\s+(.*)$")
_BOOK_LINK = re.compile(r"\[book\]\([^)]+\)")
_BOOKING_URL = re.compile(r"\[book\]\(([^)]+)\)")
_PREREQ = re.compile(r"prereq:\s*(.*)")
_NOTE = re.compile(r"note:\s*(.*)")
_PENDING = re.compile(r"_pending_")
_SECTION_H2 = re.compile(r"^##\s+(.+?)\s*$")


def _section_lines(md: str, name: str) -> list[str]:
    """Lines under `## <name>` up to the next `## ` heading or EOF."""
    out: list[str] = []
    in_section = False
    for line in md.splitlines():
        h = _SECTION_H2.match(line)
        if h:
            in_section = h.group(1).strip() == name
            continue
        if in_section:
            out.append(line)
    return out


def parse_sd_chapters(md: str) -> list[SDChapter]:
    """Parse the `## System Design` section of curriculum.md.
    Format: `- [ ] [id] Book · Title [✅ DATE]`."""
    out: list[SDChapter] = []
    for line in _section_lines(md, "System Design"):
        m = _PROBLEM_LINE.match(line)
        if not m:
            continue
        body = m.group(1)
        is_done = bool(_CHECKED_LINE.match(line))
        date_m = _DONE_DATE.search(body)
        body = _DONE_DATE.sub("", body).strip()
        id_m = _ID_PREFIX.match(body)
        if not id_m:
            continue
        cid, rest = id_m.group(1), id_m.group(2)
        if " · " in rest:
            book, title = rest.split(" · ", 1)
        else:
            book, title = "", rest
        out.append(SDChapter(
            id=cid,
            book=book.strip(),
            title=title.strip(),
            status="completed" if is_done else "pending",
            completed_date=date.fromisoformat(date_m.group(1)) if date_m else None,
        ))
    return out


def parse_behavioral(md: str) -> list[BehavioralTopic]:
    """Parse the `## Behavioral` section. Format: `- [ ] [id] prompt [✅ DATE] [· note: ...]`."""
    out: list[BehavioralTopic] = []
    for line in _section_lines(md, "Behavioral"):
        m = _PROBLEM_LINE.match(line)
        if not m:
            continue
        body = m.group(1)
        is_done = bool(_CHECKED_LINE.match(line))
        date_m = _DONE_DATE.search(body)
        # Extract optional note suffix.
        note: str | None = None
        if " · note: " in body:
            body, note = body.split(" · note: ", 1)
            note = note.strip()
        body = _DONE_DATE.sub("", body).strip()
        id_m = _ID_PREFIX.match(body)
        if not id_m:
            continue
        out.append(BehavioralTopic(
            id=id_m.group(1),
            prompt=id_m.group(2).strip(),
            status="completed" if is_done else "pending",
            completed_date=date.fromisoformat(date_m.group(1)) if date_m else None,
            notes=note,
        ))
    return out


def parse_mocks(md: str) -> list[Mock]:
    """Parse the `## Mocks` section.
    Format: `- [ ] [mock-id] Platform · Topic · {📅 DATE | _pending_ | ✅ DATE} · [book](url) · prereq: ... · note: ...`
    Segments after the first two are ` · `-delimited and order-independent."""
    out: list[Mock] = []
    for line in _section_lines(md, "Mocks"):
        m = _PROBLEM_LINE.match(line)
        if not m:
            continue
        body = m.group(1).strip()
        id_m = _ID_PREFIX.match(body)
        if not id_m:
            continue
        mock_id = id_m.group(1)
        rest = id_m.group(2)
        segments = [s.strip() for s in rest.split(" · ")]
        # First two segments are platform · topic (when present and not metadata).
        platform: str | None = None
        topic: str | None = None
        booking_url: str | None = None
        prereq_text: str | None = None
        note: str | None = None
        scheduled_date: date | None = None
        completed_date: date | None = None

        def is_meta(seg: str) -> bool:
            return bool(
                _BOOKING_URL.search(seg) or _DONE_DATE.search(seg) or
                _BOOKED_DATE.search(seg) or _PREREQ.match(seg) or
                _NOTE.match(seg) or _PENDING.search(seg)
            )

        head: list[str] = []
        for seg in segments:
            if not is_meta(seg) and len(head) < 2:
                head.append(seg)
                continue
            if (mh := _BOOKING_URL.search(seg)):
                booking_url = mh.group(1)
                continue
            if (dm := _DONE_DATE.search(seg)):
                completed_date = date.fromisoformat(dm.group(1))
                continue
            if (sm := _BOOKED_DATE.search(seg)):
                scheduled_date = date.fromisoformat(sm.group(1))
                continue
            if (pm := _PREREQ.match(seg)):
                prereq_text = pm.group(1).strip()
                continue
            if (nm := _NOTE.match(seg)):
                note = nm.group(1).strip()
                continue

        platform = head[0] if head else None
        topic = head[1] if len(head) > 1 else None

        is_done = bool(_CHECKED_LINE.match(line))
        if is_done:
            status: MockStatus = "completed"
        elif scheduled_date is not None:
            status = "scheduled"
        else:
            status = "pending"

        prereq = _parse_inline_prereq(prereq_text) if prereq_text else None

        out.append(Mock(
            id=mock_id,
            status=status,
            platform=platform,
            topic=topic,
            scheduled_date=scheduled_date,
            completed_date=completed_date,
            notes=note,
            prerequisites=prereq,
            booking_url=booking_url,
        ))
    return out


_INLINE_EM = re.compile(r"^(\d+)\s+E\+M$")
_INLINE_SD_COUNT = re.compile(r"^(\d+)\s+SD$")


def _parse_inline_prereq(text: str) -> MockPrereq | None:
    """Parse `15 E+M, 2 SD` or `25 E+M, axu1-4, axu1-5` into a MockPrereq."""
    em = 0
    sd_count = 0
    sd_ids: list[str] = []
    for raw in (s.strip() for s in text.split(",")):
        if not raw:
            continue
        if (m := _INLINE_EM.match(raw)):
            em = int(m.group(1))
        elif (m := _INLINE_SD_COUNT.match(raw)):
            sd_count = int(m.group(1))
        else:
            sd_ids.append(raw)
    pre = MockPrereq(em_problems=em, sd_chapters=sd_count, sd_chapter_ids=tuple(sd_ids))
    return pre if pre.has_any else None


def _render_mock_line(m: Mock) -> str:
    """One bullet for the `## Mocks` section."""
    if m.status == "completed":
        check = "x"
    else:
        check = " "
    head_bits = [f"[{m.id}]"]
    if m.platform:
        head_bits.append(m.platform)
    if m.topic:
        head_bits.append(m.topic)
    if len(head_bits) == 1:
        head = head_bits[0]
    else:
        head = f"{head_bits[0]} {' · '.join(head_bits[1:])}"
    suffix: list[str] = []
    if m.status == "scheduled" and m.scheduled_date:
        suffix.append(f"📅 {m.scheduled_date.isoformat()}")
    elif m.status == "pending":
        suffix.append("_pending_")
    elif m.status == "completed" and m.completed_date:
        suffix.append(f"✅ {m.completed_date.isoformat()}")
    if m.status != "completed" and (url := m.effective_booking_url):
        suffix.append(f"[book]({url})")
    if m.prerequisites and m.prerequisites.has_any:
        bits: list[str] = []
        if m.prerequisites.em_problems:
            bits.append(f"{m.prerequisites.em_problems} E+M")
        if m.prerequisites.sd_chapter_ids:
            bits.append(", ".join(m.prerequisites.sd_chapter_ids))
        elif m.prerequisites.sd_chapters:
            bits.append(f"{m.prerequisites.sd_chapters} SD")
        if bits:
            suffix.append(f"prereq: {', '.join(bits)}")
    if m.notes:
        suffix.append(f"note: {m.notes}")
    line = f"- [{check}] {head}"
    if suffix:
        line += " · " + " · ".join(suffix)
    return line


def write_curriculum_mocks(md: str, mocks: list[Mock]) -> str:
    """Surgically replace each mock line in curriculum.md by id (preserves any
    user-added headers/notes outside the bullet lines)."""
    by_id = {m.id: m for m in mocks}
    out: list[str] = []
    in_mocks = False
    for line in md.splitlines():
        h = _SECTION_H2.match(line)
        if h:
            in_mocks = h.group(1).strip() == "Mocks"
            out.append(line)
            continue
        if in_mocks:
            pm = _PROBLEM_LINE.match(line)
            if pm:
                body = pm.group(1).strip()
                idm = _ID_PREFIX.match(body)
                if idm and idm.group(1) in by_id:
                    out.append(_render_mock_line(by_id[idm.group(1)]))
                    continue
        out.append(line)
    return "\n".join(out)


def _atomic_write(path: Path, content: str) -> None:
    """Write via a sibling tmp file + os.replace — atomic on POSIX."""
    import os
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(content)
    os.replace(tmp, path)


_MOCK_LINE = re.compile(r"^\s*-\s+\[([ xX])\]\s+\[([^\]]+)\]\s+(.*)$")
_BOOKED_DATE = re.compile(r"📅\s*(\d{4}-\d{2}-\d{2})")


def parse_mock_updates(
    today_md: str, known_ids: set[str]
) -> list[tuple[str, MockStatus, date]]:
    """Extract user edits to `[mock-id]` checkbox lines in today.md. ✅ → completed,
    📅 → scheduled. Lines whose id isn't in `known_ids` are skipped."""
    updates: list[tuple[str, MockStatus, date]] = []
    for line in today_md.splitlines():
        m = _MOCK_LINE.match(line)
        if not m or m.group(2) not in known_ids:
            continue
        mock_id, body = m.group(2), m.group(3)
        if hit := _DONE_DATE.search(body):
            updates.append((mock_id, "completed", date.fromisoformat(hit.group(1))))
        elif hit := _BOOKED_DATE.search(body):
            updates.append((mock_id, "scheduled", date.fromisoformat(hit.group(1))))
    return updates


def apply_mock_updates(
    mocks: list[Mock],
    updates: list[tuple[str, MockStatus, date]],
) -> tuple[list[Mock], int]:
    """Fold parsed today.md updates into the mock list. Completed status is
    sticky — a stale 📅 cannot downgrade an already-completed mock."""
    by_id = {m.id: m for m in mocks}
    changes = 0
    for mock_id, new_status, dt in updates:
        existing = by_id.get(mock_id)
        if existing is None or existing.status == "completed":
            continue
        if new_status == "completed" and existing.completed_date != dt:
            by_id[mock_id] = replace(existing, status="completed", completed_date=dt)
            changes += 1
        elif new_status == "scheduled" and (
            existing.status != "scheduled" or existing.scheduled_date != dt
        ):
            by_id[mock_id] = replace(existing, status="scheduled", scheduled_date=dt)
            changes += 1
    return list(by_id.values()), changes


def mock_prereq_status(
    mock: Mock,
    em_done: int,
    sd_done: int,
    sd_chapters: list[SDChapter] | None = None,
) -> list[PrereqRow]:
    """One `PrereqRow` per dimension a mock pins. Empty if no prereqs.
    When `sd_chapter_ids` is set, the SD row counts only those chapters and
    lists them inline — otherwise it uses the count threshold."""
    pre = mock.prerequisites
    if not pre or not pre.has_any:
        return []

    rows: list[PrereqRow] = []
    if pre.em_problems > 0:
        rows.append(PrereqRow(
            "E/M problems", em_done >= pre.em_problems, em_done, pre.em_problems
        ))

    if pre.sd_chapter_ids:
        lookup = {ch.id: ch for ch in (sd_chapters or [])}
        chapters = [(cid, lookup.get(cid)) for cid in pre.sd_chapter_ids]
        done = sum(1 for _, ch in chapters if ch and ch.status == "completed")
        detail = ", ".join(
            f"{ch.title} ✓" if ch and ch.status == "completed" else (ch.title if ch else cid)
            for cid, ch in chapters
        )
        rows.append(PrereqRow(
            "SD chapters", done >= len(chapters), done, len(chapters), detail
        ))
    elif pre.sd_chapters > 0:
        rows.append(PrereqRow(
            "SD chapters", sd_done >= pre.sd_chapters, sd_done, pre.sd_chapters
        ))

    return rows


def _check(ok: bool) -> str:
    return "✓" if ok else "❌"


def _format_prereq_line(rows: list[PrereqRow]) -> str:
    """`  - Prereqs: ✓ 5/4 E/M problems, ❌ 1/3 SD chapters: Ch 4 ✓, Ch 5, Ch 6`"""
    def fmt(r: PrereqRow) -> str:
        head = f"{_check(r.met)} {r.current}/{r.threshold} {r.label}"
        return f"{head}: {r.detail}" if r.detail else head
    return f"  - Prereqs: {', '.join(fmt(r) for r in rows)}"


def _format_urgency(delta: int) -> str:
    if delta < 0:
        return f"{abs(delta)}d ago — mark complete or reschedule"
    return {0: "today", 1: "tomorrow"}.get(delta, f"in {delta}d")




def _render_next_mock_block(
    mock: Mock,
    today: date,
    em_done: int = 0,
    sd_done: int = 0,
    sd_chapters: list[SDChapter] | None = None,
) -> list[str]:
    """Editable checkbox for the next mock, tagged `[mock-id]`.
    Pending: user appends `📅 DATE` after booking. Scheduled: user ticks box on
    completion (Tasks plugin auto-stamps ✅). Recompute folds either edit back
    into the `## Mocks` section of curriculum.md."""
    if mock.status == "scheduled" and mock.scheduled_date is not None:
        delta = (mock.scheduled_date - today).days
        line = (
            f"- [ ] [{mock.id}] {mock.descriptor} · 📅 {mock.scheduled_date.isoformat()} "
            f"({_format_date(mock.scheduled_date, weekday=True)}, {_format_urgency(delta)})"
        )
    else:
        line = f"- [ ] [{mock.id}] {mock.descriptor} — _pending_"

    lines = [line]
    prereqs = mock_prereq_status(mock, em_done, sd_done, sd_chapters)
    if prereqs:
        lines.append(_format_prereq_line(prereqs))

    if mock.status == "pending":
        if url := mock.effective_booking_url:
            lines.append(f"  - Book: [{mock.platform or 'link'}]({url})")
        lines.append(
            "  - _When booked, append `📅 YYYY-MM-DD` to the line above. "
            "Recompute folds it into `mock_interviews.json`._"
        )
    elif mock.status == "scheduled":
        lines.append(
            "  - _When done, check the box above. The Tasks plugin auto-stamps "
            "`✅ DATE` and recompute marks this completed._"
        )
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


def _format_date(d: date, *, weekday: bool = False) -> str:
    """`May 11` or `Mon May 11` (weekday=True). Day is never zero-padded."""
    fmt = "%a %b " if weekday else "%b "
    return d.strftime(fmt).replace(" 0", " ") + str(d.day)


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
    return f"- [ ] {problem.text}{_diff_suffix(problem.difficulty)}"


def _render_time_blocks(mock_today: bool) -> list[str]:
    """`## Time blocks` section. On mock days, the SD slot shifts after the mock."""
    blocks = (
        [
            "- 9:00–13:00  Recall",
            "- 14:00–16:00 Mock",
            "- 16:00–17:30 System Design",
            "- 17:30–19:30 DSA New",
        ]
        if mock_today
        else [
            "- 9:00–13:00  Recall",
            "- 14:00–15:30 System Design",
            "- 15:30–19:30 DSA New",
        ]
    )
    return ["## Time blocks", "", *blocks, ""]


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
    phase: Phase | None = None,
    total_phases: int | None = None,
    projection: date | None = None,
    projection_rate: float | None = None,
    projection_untouched: int | None = None,
    sd_next: SDChapter | None = None,
    readiness: Readiness | None = None,
    next_up_mock: Mock | None = None,
    em_done: int = 0,
    sd_done: int = 0,
    sd_chapters: list[SDChapter] | None = None,
    mock_today: bool = False,
) -> str:
    """Produce the markdown for today.md."""
    base = f"# Today — {_format_date(today, weekday=True)}, {today.year}"
    if day_n is None:
        header = f"{base} · Pre-prep"
    elif phase is None:
        header = f"{base} · Day {day_n}"
    else:
        progress = f"{phase.number}/{total_phases}" if total_phases else str(phase.number)
        header = (
            f"{base} · Phase {progress} — {phase.name} · "
            f"Day {day_n} · {phase.new_per_day} new/day"
        )

    lines = [header, ""]
    if projection and projection_rate and projection_untouched:
        lines += [
            _format_projection_line(projection, projection_rate, projection_untouched, today),
            "",
        ]
    lines += ["_Generated by `prep recompute`. Re-run anytime to refresh._", ""]
    if readiness is not None:
        lines += render_readiness_block(readiness)
    if next_up_mock is not None:
        lines += ["## Next mock", ""]
        lines += _render_next_mock_block(next_up_mock, today, em_done, sd_done, sd_chapters)
        lines.append("")

    lines += _render_time_blocks(mock_today)

    lines += ["## Recall — most overdue first", ""]
    lines += (
        [_render_recall_line(i) for i in recall]
        if recall else ["_Empty — no problems are overdue yet._"]
    )
    lines += ["", "## New — next from the curriculum", ""]
    lines += (
        [_render_new_line(p) for p in new]
        if new else ["_Empty — every curriculum problem has been touched at least once._"]
    )

    if sd_next is not None:
        lines += ["", "## Today's SD reading", "", f"- [ ] {sd_next.book} · {sd_next.title}"]

    if today.weekday() == calendar.SATURDAY:
        lines += [
            "",
            "## This week's hardest — your pick",
            "",
            "_Re-solve 2-3 problems you found hardest this week (from your daily \"today's hardest\" notes Mon–Fri). Write the canonical `[Pattern] -> Name` form between the brackets so ticking logs a real touch._",
            "",
            "- [ ] [Pattern] -> Problem Name",
            "- [ ] [Pattern] -> Problem Name",
            "- [ ] [Pattern] -> Problem Name",
        ]

    lines.append("")
    return "\n".join(lines)


# ─── Mock progress + upcoming ────────────────────────────────────────────────


def _progress_bar(done: int, total: int, width: int = 13) -> str:
    """Unicode block bar. Empty if total <= 0."""
    filled = round((done / total) * width) if total > 0 else 0
    return f"[{'█' * filled}{'░' * (width - filled)}]"


def _section_header(name: str, done: int, total: int, extra: str = "") -> list[str]:
    """`## Name (X/Y complete[ · extra])` + blank + progress bar + blank."""
    summary = f"{done}/{total} complete" + (f" · {extra}" if extra else "")
    return [
        f"## {name} ({summary})",
        "",
        f"{_progress_bar(done, total)} {done}/{total}",
        "",
    ]


def next_mock(mocks: list[Mock]) -> Mock | None:
    """First non-completed mock, or None if all completed."""
    return next((m for m in mocks if m.status != "completed"), None)


def _format_mock_line(mock: Mock) -> str:
    """One bullet describing a single mock — its status, date, platform, topic."""
    if mock.status == "completed" and mock.completed_date:
        return f"- [x] {mock.descriptor}{_stamp(mock.completed_date)}"
    if mock.status == "scheduled" and mock.scheduled_date:
        return f"- [ ] {mock.descriptor} · 📅 {mock.scheduled_date.isoformat()}"
    return f"- [ ] {mock.descriptor} · _pending_"


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
    """Roll up the three ledgers into category bars + tiered application gates."""
    touched = {t.problem for t in ledger}
    em_curr = [p for p in curriculum if p.difficulty in ("E", "M")]
    em = CategoryProgress("E+M problems", sum(1 for p in em_curr if p.text in touched), len(em_curr))
    sd = CategoryProgress("System Design", sum(1 for c in sd_chapters if c.status == "completed"), len(sd_chapters))
    mp = CategoryProgress("Mocks", sum(1 for m in mocks if m.status == "completed"), len(mocks))
    all_done = bool(curriculum) and all(p.text in touched for p in curriculum)

    tiers = [
        ReadinessTier("Fallback-ready", [("All E+M problems touched", em.complete)]),
        ReadinessTier("Target-ready", [
            ("All E+M problems touched", em.complete),
            (f"≥{_TARGET_READY_MIN_SD_CHAPTERS} SD chapters complete",
             sd.done >= _TARGET_READY_MIN_SD_CHAPTERS),
            (f"≥{_TARGET_READY_MIN_MOCKS} mocks completed",
             mp.done >= _TARGET_READY_MIN_MOCKS),
        ]),
        ReadinessTier("Stretch-ready", [
            ("All curriculum problems touched", all_done),
            ("All SD chapters complete", sd.complete),
            ("All mocks completed", mp.complete),
        ]),
    ]
    return Readiness(em=em, sd=sd, mocks=mp, tiers=tiers)


def _render_category_line(cat: CategoryProgress) -> str:
    pct = round(cat.fraction * 100)
    return f"- {cat.name:<14} {_progress_bar(cat.done, cat.total)} {pct}% ({cat.done}/{cat.total})"


def render_readiness_block(readiness: Readiness) -> list[str]:
    """`## Readiness` block: three category bars + per-tier criteria."""
    lines = ["## Readiness", ""]
    lines += [_render_category_line(c) for c in (readiness.em, readiness.sd, readiness.mocks)]
    lines.append("")
    for tier in readiness.tiers:
        lines.append(f"**{tier.name}: {_check(tier.met)}**")
        for label, ok in tier.criteria:
            lines.append(f"  - {_check(ok)} {label}")
        lines.append("")
    return lines


# ─── Mocks view (dedicated) ──────────────────────────────────────────────────


def _render_mocks_section(
    mocks: list[Mock],
    today: date,
    em_done: int = 0,
    sd_done: int = 0,
    sd_chapters: list[SDChapter] | None = None,
) -> list[str]:
    """`## Mocks` section in coverage.md: summary + Next + Completed history."""
    completed = sum(1 for m in mocks if m.status == "completed")
    scheduled = sum(1 for m in mocks if m.status == "scheduled")
    pending = sum(1 for m in mocks if m.status == "pending")
    lines = _section_header(
        "Mocks", completed, len(mocks),
        f"{scheduled} scheduled · {pending} pending",
    )
    if not mocks:
        lines += [
            "_No mocks tracked yet. Add entries to `prep-data/mock_interviews.json` "
            "(see `mock_interviews.example.json` for the schema)._",
            "",
        ]
        return lines

    lines += ["### Next", ""]
    if nxt := next_mock(mocks):
        lines += _render_next_mock_block(nxt, today, em_done, sd_done, sd_chapters)
    else:
        lines.append("_All mocks completed._")
    lines.append("")

    completed_mocks = [m for m in mocks if m.status == "completed"]
    if completed_mocks:
        lines += ["### Completed", ""]
        for m in completed_mocks:
            note = f" — _{m.notes}_" if m.notes else ""
            lines.append(f"{_format_mock_line(m)}{note}")
        lines.append("")

    return lines


# ─── Coverage view ───────────────────────────────────────────────────────────


def _stamp(d: date | None) -> str:
    return f" · ✅ {d.isoformat()}" if d else ""


def _render_behavioral_section(topics: list[BehavioralTopic]) -> list[str]:
    completed = sum(1 for t in topics if t.status == "completed")
    lines = _section_header("Behavioral", completed, len(topics))
    if not topics:
        lines += ["_Empty — add prompts to `prep-data/behavioral_prompts.json`._", ""]
        return lines
    for t in topics:
        box = "x" if t.status == "completed" else " "
        note = f" — _{t.notes}_" if t.notes else ""
        lines.append(f"- [{box}] {t.prompt}{_stamp(t.completed_date)}{note}")
    lines.append("")
    return lines


def _render_sd_section(sd_chapters: list[SDChapter]) -> list[str]:
    completed = sum(1 for c in sd_chapters if c.status == "completed")
    lines = _section_header("System Design", completed, len(sd_chapters))
    if not sd_chapters:
        lines += ["_Empty — add chapters to `prep-data/system_design_chapters.json`._", ""]
        return lines
    for ch in sd_chapters:
        box = "x" if ch.status == "completed" else " "
        lines.append(f"- [{box}] {ch.book} · {ch.title}{_stamp(ch.completed_date)}")
    lines.append("")
    return lines


def _render_dsa_by_pattern(
    curriculum: list[Problem], ledger: list[Touch]
) -> list[str]:
    touched = {t.problem for t in ledger}

    def box(p: Problem, indent: str = "") -> str:
        mark = "x" if p.text in touched else " "
        return f"{indent}- [{mark}] {p.name}{_diff_suffix(p.difficulty)}"

    sorted_items = sorted(
        enumerate(curriculum), key=lambda i: (_SOURCE_RANK.get(i[1].source, 0), i[0])
    )
    by_pattern: dict[str, list[Problem]] = {}
    for _, p in sorted_items:
        by_pattern.setdefault(p.pattern, []).append(p)

    lines = ["## DSA — by pattern", ""]
    for pattern, items in by_pattern.items():
        canonicals = {p.name for p in items if p.variant_of is None}
        variants: dict[str, list[Problem]] = {}
        loose: list[Problem] = []
        for p in items:
            if p.variant_of is None:
                continue
            if p.variant_of in canonicals:
                variants.setdefault(p.variant_of, []).append(p)
            else:
                loose.append(p)

        lines.append(f"### {pattern}")
        for p in items:
            if p.variant_of is not None:
                continue
            lines.append(box(p))
            lines.extend(box(v, "  ") for v in variants.get(p.name, []))
        for v in loose:
            lines.append(f"{box(v)} _(variant of {v.variant_of})_")
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
    """Coverage overview: Readiness → Behavioral → Mocks → SD → DSA-by-pattern."""
    lines = [
        "# Coverage",
        "",
        "_Generated by `prep recompute`. Comprehensive overview — readiness, behavioral, mocks, system design, and the full DSA curriculum by pattern. Boxes auto-check from the ledger and per-category JSON files._",
        "",
    ]
    if readiness is not None:
        lines += render_readiness_block(readiness)
    if behavioral is not None:
        lines += _render_behavioral_section(behavioral)
    if mocks is not None:
        lines += _render_mocks_section(
            mocks, today or date.today(), em_done, sd_done, sd_chapters
        )
    if sd_chapters is not None:
        lines += _render_sd_section(sd_chapters)
    lines += _render_dsa_by_pattern(curriculum, ledger)
    return "\n".join(lines)


# ─── Orchestration ───────────────────────────────────────────────────────────


def recompute(
    curriculum_md_path: Path,
    today_md_path: Path,
    ledger_path: Path,
    today: date,
    recall_limit: int = DEFAULT_RECALL_LIMIT,
    coverage_md_path: Path | None = None,
) -> RecomputeResult:
    """One full cycle: log new completions, fold mock edits, regenerate today.md + coverage.md.

    Reads everything (DSA, SD, Mocks, Behavioral) from curriculum.md. When
    today.md ticks update mock state, the change is written back to
    curriculum.md atomically."""
    curriculum_md = curriculum_md_path.read_text()
    curriculum = parse_curriculum(curriculum_md)
    phases = parse_phases(curriculum_md)
    sd_chapters = parse_sd_chapters(curriculum_md)
    mocks = parse_mocks(curriculum_md)
    behavioral = parse_behavioral(curriculum_md)

    today_md = today_md_path.read_text() if today_md_path.exists() else ""
    logged = append_to_ledger(ledger_path, parse_completions(today_md))

    ledger = load_ledger(ledger_path)
    recall = compute_recall(ledger, today=today, limit=recall_limit, curriculum=curriculum)
    phase = current_phase(curriculum, ledger, phases) if phases else None
    new = (
        compute_new(curriculum, ledger, phase=phase) if phase
        else compute_new(curriculum, ledger)
    )

    start = start_date(ledger)
    day_n = day_n_for(today, start) if start else None

    rate = avg_new_per_day(ledger, today)
    end = projected_end_date(ledger, curriculum, today)
    touched = {t.problem for t in ledger}
    untouched = sum(1 for p in curriculum if p.text not in touched)

    if mocks:
        updates = parse_mock_updates(today_md, {m.id for m in mocks})
        if updates:
            mocks, changed = apply_mock_updates(mocks, updates)
            if changed:
                _atomic_write(
                    curriculum_md_path,
                    write_curriculum_mocks(curriculum_md, mocks),
                )

    readiness = compute_readiness(curriculum, ledger, sd_chapters, mocks)
    em_done, sd_done = readiness.em.done, readiness.sd.done

    mock_today = any(m.scheduled_date == today for m in mocks)
    today_md_path.write_text(render_today(
        today=today,
        recall=recall,
        new=new,
        day_n=day_n,
        phase=phase,
        total_phases=len(phases) if phases else None,
        projection=end,
        projection_rate=rate,
        projection_untouched=untouched,
        sd_next=next_sd_chapter(sd_chapters),
        readiness=readiness,
        next_up_mock=next_mock(mocks),
        em_done=em_done,
        sd_done=sd_done,
        sd_chapters=sd_chapters,
        mock_today=mock_today,
    ))

    if coverage_md_path is not None:
        coverage_md_path.parent.mkdir(parents=True, exist_ok=True)
        coverage_md_path.write_text(render_coverage(
            curriculum,
            ledger,
            today=today,
            mocks=mocks,
            sd_chapters=sd_chapters,
            readiness=readiness,
            behavioral=behavioral,
            em_done=em_done,
            sd_done=sd_done,
        ))

    return RecomputeResult(
        new_touches_logged=logged, recall_size=len(recall), new_size=len(new)
    )


# ─── CLI ─────────────────────────────────────────────────────────────────────


@click.group()
def cli() -> None:
    """Snapshot-mode recall engine for the NeetCode 150 curriculum."""


@cli.command(name="recompute")
@click.option(
    "--curriculum",
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
    default=Path("curriculum.md"),
    show_default=True,
    help="Master curriculum markdown (DSA by phase + SD/Mocks/Behavioral).",
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
def recompute_cmd(
    curriculum: Path,
    today_md: Path,
    ledger: Path,
    coverage_md: Path,
) -> None:
    """Fold yesterday's checks into the ledger, then regenerate today.md and coverage.md."""
    result = recompute(
        curriculum,
        today_md,
        ledger,
        today=date.today(),
        coverage_md_path=coverage_md,
    )
    click.echo(
        f"logged {result.new_touches_logged} new touch(es) · "
        f"recall: {result.recall_size} · new: {result.new_size}"
    )


@cli.command(name="reset")
@click.option("--yes", is_flag=True, help="Skip the confirmation prompt.")
@click.option(
    "--ledger-dir",
    type=click.Path(file_okay=False, path_type=Path),
    default=Path("prep-data"),
    show_default=True,
    help="Directory containing the ledger.",
)
def reset_cmd(yes: bool, ledger_dir: Path) -> None:
    """Delete the DSA completion ledger. Next recompute treats you as pre-prep."""
    path = ledger_dir / "completions.jsonl"
    existence = "exists" if path.exists() else "does not exist (no-op)"
    click.echo(f"Will delete: {path} ({existence})")
    if not yes and not click.confirm("Proceed?", default=False):
        click.echo("Aborted.")
        return
    if path.exists():
        path.unlink()
    click.echo("Reset complete. Run `prep recompute` to regenerate today.md.")


if __name__ == "__main__":
    cli()
