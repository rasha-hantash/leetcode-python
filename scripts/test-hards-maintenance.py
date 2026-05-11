"""Verify the Hards behavior of compute_maintenance:

  (a) Default scope is ("E", "M") — Hards stay out even when they're at
      the 4-touch mastery cap. Maintenance is post-acquisition for the
      E/M corpus only.
  (b) Opt-in scope ("E", "M", "H") includes mastered Hards in the
      round-robin. The exclusion is a parameter, not a hard rule.

Usage:
    uv run --no-sync python scripts/test-hards-maintenance.py
"""
from __future__ import annotations

import sys
from datetime import date, timedelta
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

from recall_engine import (  # noqa: E402
    Touch,
    compute_maintenance,
    parse_curriculum,
)

curriculum = parse_curriculum((REPO / "curriculum.template.md").read_text())

today = date(2026, 7, 30)
ledger: list[Touch] = []
for p in curriculum:
    if p.difficulty is None:
        continue
    for n in range(4):
        ledger.append(Touch(p.text, today - timedelta(days=5 + (3 - n) * 7)))

total_problems = sum(1 for p in curriculum if p.difficulty)
print(f"  fixture: 4 touches per problem, all difficulties (E/M/H)")
print(f"           {len(ledger)} touch events across {total_problems} problems\n")

items_default = compute_maintenance(curriculum, ledger, today=today, limit=300)
hards_default = [it for it in items_default if it.difficulty == "H"]
print(f"  (a) compute_maintenance(curriculum, ledger, today)  # default scope ('E','M')")
print(f"      → {len(items_default)} items, {len(hards_default)} Hards")
assert len(hards_default) == 0, "BUG: Hards leaked into default Maintenance"
print(f"      ✓ no Hards in default output\n")

items_all = compute_maintenance(
    curriculum, ledger, today=today, limit=300, difficulties=("E", "M", "H")
)
hards_all = [it for it in items_all if it.difficulty == "H"]
total_hards = sum(1 for p in curriculum if p.difficulty == "H")
print(f"  (b) compute_maintenance(..., difficulties=('E','M','H'))")
print(f"      → {len(items_all)} items, {len(hards_all)} Hards "
      f"({total_hards} Hards exist in the curriculum)")
assert len(hards_all) > 0, "BUG: Hards missing under explicit scope"
hard_patterns = {it.problem.split("]")[0] + "]" for it in hards_all}
print(f"      ✓ Hards surface across {len(hard_patterns)} pattern buckets")
print(f"\n  Both claims hold.")
