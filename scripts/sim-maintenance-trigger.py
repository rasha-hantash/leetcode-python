"""Day-by-day simulation: find the calendar day when the Maintenance
trigger fires (`min_touches_in_scope` reaches `_SLOT_LIMIT` for every E/M).

Models the daily loop under perfect adherence:
  - Mon-Sat working, Sunday off
  - Each working day: do today's New (phase rate) + Recall (most overdue, up to 10)
  - Each "do" event is a touch dated today
  - SM-2 schedules next due via INTERVALS_DAYS

The output is the BEST-CASE timing. Real adherence with skipped reviews,
mock-day pressure, or context switches pushes the actual trigger later.

Usage:
    uv run --no-sync python scripts/sim-maintenance-trigger.py
"""
from __future__ import annotations

import sys
from datetime import date, timedelta
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

from recall_engine import (  # noqa: E402
    INTERVALS_DAYS,
    Touch,
    aggregate_touches,
    due_date,
    min_touches_in_scope,
    parse_curriculum,
    parse_phases,
)

curriculum_md = (REPO / "curriculum.template.md").read_text()
curriculum = parse_curriculum(curriculum_md)
phases = parse_phases(curriculum_md)

# Build the New-acquisition queue per phase. compute_new picks E before M
# within a phase, then by document order.
em_curriculum = [p for p in curriculum if p.difficulty in ("E", "M")]
phase_problems: dict[int, list] = {phase.number: [] for phase in phases}
for p in em_curriculum:
    if p.phase is not None:
        phase_problems[p.phase].append(p)


def difficulty_rank(p) -> int:
    return {"E": 0, "M": 1, "H": 2}.get(p.difficulty or "M", 1)


for n in phase_problems:
    phase_problems[n].sort(key=difficulty_rank)

phase_pace = {phase.number: phase.new_per_day for phase in phases}

# Phases that have any E/M acquisition work (skip Phase 7 — Hards-only).
em_phase_numbers = sorted(
    n for n in phase_pace if any(p.difficulty != "H" for p in phase_problems[n])
)

ledger: list[Touch] = []
phase_cursors: dict[int, int] = {n: 0 for n in phase_problems}
day = date(2026, 5, 11)  # Day 1: a Monday
day_n = 1
fired_on = None
RECALL_LIMIT = 10


def current_em_phase() -> int | None:
    for n in em_phase_numbers:
        if phase_cursors[n] < len(phase_problems[n]):
            return n
    return None


while day_n <= 200:
    if day.weekday() == 6:  # Sunday — off
        day += timedelta(days=1)
        day_n += 1
        continue

    summary = aggregate_touches(ledger)
    overdue: list[tuple[str, int]] = []
    for text, (touches, last) in summary.items():
        if touches >= len(INTERVALS_DAYS):
            continue
        due = due_date(touches, last)
        if day >= due:
            overdue.append((text, (day - due).days))
    overdue.sort(key=lambda x: -x[1])
    for text, _ in overdue[:RECALL_LIMIT]:
        ledger.append(Touch(text, day))

    phase = current_em_phase()
    if phase is not None:
        pace = phase_pace[phase]
        cursor = phase_cursors[phase]
        for p in phase_problems[phase][cursor : cursor + pace]:
            ledger.append(Touch(p.text, day))
        phase_cursors[phase] += pace

    if min_touches_in_scope(curriculum, ledger, ("E", "M")) >= len(INTERVALS_DAYS):
        fired_on = (day_n, day)
        break

    day += timedelta(days=1)
    day_n += 1

if fired_on is None:
    final_min = min_touches_in_scope(curriculum, ledger, ("E", "M"))
    print(f"  trigger did NOT fire within {day_n} days "
          f"(current min_touches = {final_min})")
else:
    n, d = fired_on
    print(f"  trigger fires: Day {n} ({d.isoformat()}, {d.strftime('%a')})")

print()
print("  Phase acquisition completion (best case, no skipped reviews):")
cum = 0
for n in em_phase_numbers:
    count = len(phase_problems[n])
    pace = phase_pace[n]
    days = -(-count // pace)
    cum += days
    print(f"    Phase {n}: {count} problems @ {pace}/day = +{days} working days "
          f"(cumulative: {cum})")
