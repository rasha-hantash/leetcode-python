"""Recall engine: snapshot-mode SM-2 lite scheduler for the NeetCode 150 sprint.

Reads `prep-plan-daily.md` (curriculum) and the previous `today.md` (yesterday's
checked-off items), folds new completions into an append-only JSONL ledger, then
regenerates `today.md` with today's Recall and New sections.

Designed to run once per morning (LaunchAgent) or on-demand (`prep recompute`).
There is no live daemon — today's set is frozen until the next recompute call.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path
from typing import Iterable

import click


# ─── Constants ────────────────────────────────────────────────────────────────

INTERVALS_DAYS: list[int] = [1, 3, 7, 21, 60]
"""SM-2 lite: interval after the Nth touch (1-indexed). 5+ touches stay at 60."""

DEFAULT_RECALL_LIMIT = 10
DEFAULT_NEW_LIMIT = 3


# ─── Data types ──────────────────────────────────────────────────────────────


@dataclass(frozen=True)
class Problem:
    """A curriculum entry: the canonical problem text and which Day N it lives in."""

    text: str
    source_day: int


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
    ledger: list[Touch], today: date, limit: int = DEFAULT_RECALL_LIMIT
) -> list[RecallItem]:
    """Items at or past their SM-2 due date, sorted most-overdue first, capped."""
    items = []
    for problem, (touches, last) in aggregate_touches(ledger).items():
        overdue = overdue_days(touches, last, today)
        if overdue >= 0:
            items.append(
                RecallItem(
                    problem=problem,
                    touches=touches,
                    last_touched=last,
                    days_overdue=overdue,
                )
            )
    items.sort(key=lambda r: r.days_overdue, reverse=True)
    return items[:limit]


def compute_new(
    curriculum: list[Problem], ledger: list[Touch], limit: int = DEFAULT_NEW_LIMIT
) -> list[Problem]:
    """The first N never-touched problems, in curriculum (document) order."""
    touched = {t.problem for t in ledger}
    return [p for p in curriculum if p.text not in touched][:limit]


# ─── Parsers ─────────────────────────────────────────────────────────────────


_DAY_HEADING = re.compile(r"^###\s+Day\s+(\d+)\b")
_PROBLEM_LINE = re.compile(r"^\s*-\s+\[[ xX]\]\s+(.*)$")
_DONE_DATE = re.compile(r"\s*✅\s*(\d{4}-\d{2}-\d{2}).*$")
_T_MARKER = re.compile(r"\s*`[A-Z]\d?`\s*$")
_DAY_ANNOTATION = re.compile(r"\s*\(Day\s+\d+\)\s*$")
_METADATA_SUFFIX = re.compile(r"\s+—\s+.*$")
_PROBLEM_TEXT = re.compile(r"^\[[^\]]+\]\s*->\s*.+$")


def _canonicalize(text: str) -> str:
    """Strip everything that isn't part of the canonical problem identifier:
    done-date stamp, metadata em-dash suffix, T2/M-style markers, (Day N) annotation."""
    text = _DONE_DATE.sub("", text)
    text = _METADATA_SUFFIX.sub("", text)
    text = _DAY_ANNOTATION.sub("", text)
    text = _T_MARKER.sub("", text)
    return text.strip()


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
        canonical = _canonicalize(problem_match.group(1))
        if _PROBLEM_TEXT.match(canonical):
            problems.append(Problem(text=canonical, source_day=current_day))

    return problems


_CHECKED_LINE = re.compile(r"^\s*-\s+\[[xX]\]\s+(.*)$")


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


def _render_recall_line(item: RecallItem) -> str:
    overdue_text = (
        "due today" if item.days_overdue == 0 else f"{item.days_overdue}d overdue"
    )
    return (
        f"- [ ] {item.problem} — {overdue_text} · "
        f"{item.touches}× · last {_format_date(item.last_touched)}"
    )


def _render_new_line(problem: Problem) -> str:
    return f"- [ ] {problem.text} (Day {problem.source_day})"


def render_today(today: date, recall: list[RecallItem], new: list[Problem]) -> str:
    """Produce the markdown that gets written to today.md."""
    weekday = today.strftime("%a")
    header = f"# Today — {weekday} {_format_date(today)}, {today.year}"

    lines = [
        header,
        "",
        "_Generated by `prep recompute`. Re-run anytime to refresh._",
        "",
        "## Recall — most overdue first",
        "",
    ]
    if recall:
        lines.extend(_render_recall_line(item) for item in recall)
    else:
        lines.append("_Empty — no problems are overdue yet._")
    lines.extend(["", "## New — next from the curriculum", ""])
    if new:
        lines.extend(_render_new_line(p) for p in new)
    else:
        lines.append("_Empty — every curriculum problem has been touched at least once._")
    lines.append("")
    return "\n".join(lines)


# ─── Orchestration ───────────────────────────────────────────────────────────


def recompute(
    daily_md_path: Path,
    today_md_path: Path,
    ledger_path: Path,
    today: date,
    recall_limit: int = DEFAULT_RECALL_LIMIT,
    new_limit: int = DEFAULT_NEW_LIMIT,
) -> RecomputeResult:
    """One full cycle: log yesterday's completions, then regenerate today.md."""
    curriculum = parse_curriculum(daily_md_path.read_text())

    new_touches: list[Touch] = []
    if today_md_path.exists():
        new_touches = parse_completions(today_md_path.read_text())
    logged = append_to_ledger(ledger_path, new_touches)

    ledger = load_ledger(ledger_path)
    recall = compute_recall(ledger, today=today, limit=recall_limit)
    new = compute_new(curriculum, ledger, limit=new_limit)

    today_md_path.write_text(render_today(today=today, recall=recall, new=new))

    return RecomputeResult(
        new_touches_logged=logged, recall_size=len(recall), new_size=len(new)
    )


# ─── CLI ─────────────────────────────────────────────────────────────────────


@click.group()
def cli() -> None:
    """Snapshot-mode recall engine for the NeetCode 150 sprint."""


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
def recompute_cmd(daily: Path, today_md: Path, ledger: Path) -> None:
    """Fold yesterday's checks into the ledger, then regenerate today.md."""
    result = recompute(daily, today_md, ledger, today=date.today())
    click.echo(
        f"logged {result.new_touches_logged} new touch(es) · "
        f"recall: {result.recall_size} · new: {result.new_size}"
    )


if __name__ == "__main__":
    cli()
