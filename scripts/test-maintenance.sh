#!/bin/bash
# Usage: bash scripts/test-maintenance.sh
#
# Builds a synthetic ledger where every E/M problem has 4 touches, runs
# `prep recompute` in a /tmp sandbox, and prints the Maintenance section of
# the resulting today.md. Your real curriculum.md, prep-data/, and today.md
# are not touched — everything happens under a fresh mktemp dir.

set -euo pipefail

REPO="$(pwd)"
SANDBOX="$(mktemp -d -t prep-maintenance-XXXX)"
echo "→ Sandbox: $SANDBOX"

cp "$REPO/curriculum.template.md" "$SANDBOX/"
cd "$SANDBOX"

# Seed working curriculum.md from template.
uv run --project "$REPO" --no-sync prep init >/dev/null

# Synthetic ledger: every E/M problem touched 4x, spaced so SM-2 looks real.
python3 - <<'PY'
import json, re
from datetime import date, timedelta
from pathlib import Path

md = Path("curriculum.md").read_text()

# Walk like recall_engine.parse_curriculum: track Phase + Pattern, emit one
# entry per "- ..." line under a Pattern heading.
in_dsa = False
pattern = None
problems = []  # (pattern, name, difficulty)
for line in md.splitlines():
    if line.startswith("## NeetCode 150"):
        in_dsa = True
        continue
    if line.startswith("## ") and in_dsa:
        in_dsa = False
        pattern = None
        continue
    if not in_dsa:
        continue
    if line.startswith("#### "):
        pattern = line[5:].strip()
        continue
    if pattern is None:
        continue
    m = re.match(r"^- \[([^\]]+)\]\([^)]+\)\s*\(([EMH])\)", line)
    if not m:
        continue
    name, diff = m.group(1), m.group(2)
    problems.append((pattern, name, diff))

today = date(2026, 7, 30)
ledger_lines = []
for pat, name, diff in problems:
    if diff == "H":
        continue
    canonical = f"[{pat}] -> {name}"
    # Four touches spaced 1, 3, 7, 21 day intervals back from "5 days ago",
    # so nothing is currently overdue. The exact spacing doesn't affect the
    # trigger — only the touch count does.
    for n in range(4):
        on = today - timedelta(days=5 + (3 - n) * 7)
        ledger_lines.append(json.dumps({"problem": canonical, "on": on.isoformat()}))

Path("prep-data").mkdir(exist_ok=True)
Path("prep-data/completions.jsonl").write_text("\n".join(ledger_lines) + "\n")
em_count = len([p for p in problems if p[2] != "H"])
print(f"  wrote {len(ledger_lines)} touch events across {em_count} E/M problems")
PY

uv run --project "$REPO" --no-sync python - <<'PY'
from datetime import date
from pathlib import Path
from recall_engine import recompute
r = recompute(
    Path("curriculum.md"),
    Path("today.md"),
    Path("prep-data/completions.jsonl"),
    today=date(2026, 7, 30),
    hardest_ledger_path=Path("prep-data/hardest.jsonl"),
)
print(
    f"  result: recall={r.recall_size} "
    f"new={r.new_size} maintenance={r.maintenance_size}"
)
PY

echo
echo "─── Maintenance section in today.md ───"
sed -n '/## Maintenance/,/^## /p' today.md | sed '$d'
echo
echo "─── Sandbox preserved at: $SANDBOX ───"
