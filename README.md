# Interview Prep

A 90-day NeetCode 150 + system design + behavioral prep system. One master file (`curriculum.md`) holds DSA + System Design + Mocks + Behavioral. A snapshot-mode SM-2 lite engine generates `today.md` each morning; you drain it; tomorrow's queue regenerates from what you ticked.

- **Window:** Mon May 11 – Sat Aug 8, 2026 · ~77 working days · 9 hr/day ceiling
- **Coverage:** 182 problems (NC150 + NC-150+ + 9 String Transformation + 9 company variants) · DDIA Ch 5–9 · Alex Xu Vol 1 (16 ch) + Vol 2 (Ch 1–7) · ~24 mocks · ~10 behavioral stories
- **Sequencing:** Easies before Mediums within each pattern; E+M before H across patterns; **no Hards until phase 5**

Phase advancement is ledger-driven — phase 1 (E+M acquisition) → 4 (still E+M) → 5 (Hards) → 6–8 (reinforcement / interview mode). The engine picks the lowest-numbered phase with eligible untouched problems. Phase budgets live inline in `curriculum.md`'s `### Phase N — Name (X new/day)` headings; edit the budget there if your retention diagnostic says so.

**Everything is ledger-driven, not calendar-driven.** Phase advancement, the Recall queue, and **application-readiness gates** (Fallback / Target / Stretch — surfaced in `today.md`'s readiness banner) all fire from ledger state, not from what day it is. The D-numbers in the schedule tables below (D1, D54, D79, etc.) are full-time-pace shorthand, not deadlines — if you slip, you just reach phase 5 later. Mock dates you book on the calendar are user-input bookkeeping; the engine counts _completed_ mocks toward Target-ready, not their dates.

## Daily flow

1. **Morning (auto, 8:30 AM):** LaunchAgent runs `uv run prep recompute` — logs yesterday's completions into the ledger, syncs `curriculum.md` ticks, regenerates `today.md`.
2. **Recall (9:00–13:00):** open `today.md`. Drain **Recall** top-down — Easy 20m / Medium 40m / Hard 90m. Tasks plugin auto-stamps `✅ DATE` on tick. Highest-leverage work; protected by the morning slot.
3. **System Design (14:00–15:30):** today's chapter is surfaced as `## Today's SD reading` in `today.md`. Tick the box there or in `curriculum.md`'s `## System Design` section.
4. **DSA New (15:30–19:30):** today's New problems live under `## New` in `today.md`. Solve them and tick.
5. **End of day:** the engine doesn't need anything else. Note tomorrow's first re-solve from your "today's hardest" notes.

The list you wake up to is the list for the day — it does not reshuffle as you check items off. Whatever you don't finish folds into tomorrow's queue with more days overdue.

**Recall always wins over New.** Recall is knowledge you've already paid for, decaying on an exponential curve — skip a day and the cost compounds (you re-learn from scratch). New is just deferred scope; nothing degrades. When the day runs short, drain **all** of Recall first; let New slip into tomorrow. If even Recall is too long for the morning block, get partway down it — the most-overdue items are at the top, so partial draining still rescues the highest-priority knowledge.

**Mock days:** afternoon shifts to `14:00–16:00 mock + 16:00–17:30 SD + 17:30–19:30 DSA New`.
**Sundays:** off across all phases. Light _Fluent Python_ or DDIA reading is fine.

### Phase-shift schedules

The shape above (Recall / SD / DSA New) is **phases 1–5 (D1–D53)**, when there's still acquisition to do. Saturday in this window adds a "this week's hardest — your pick" sub-block to the morning Recall: re-solve 2–3 problems you flagged hardest from your Mon–Fri "today's hardest" notes, write their canonical names into the Saturday-only section that the engine adds to `today.md`, then drain Recall.

**Phase 6 (D54–D58) — Reinforcement + job application window.** Zero new acquisition; every problem already touched. Morning is all Recall. Afternoon shifts to extra mocks + behavioral story practice + fallback-tier company applications. The 6 NC-150+ heavy patterns (Segment Tree, Bitmask DP, Sweep Line) are available as fallback if Recall fully drains.

**Phase 7 (D59–D78) — Mock-heavy reinforcement, M–F:**

| Time        | Block                                                    |
| ----------- | -------------------------------------------------------- |
| 9:00–13:00  | 30-min clock re-solve + Pythonic refactor + Recall drain |
| 14:00–16:00 | Real screens / paid mocks (SD writeup if empty)          |
| 16:00–17:00 | SD anchor (DDIA Ch 8–9 deep-dive)                        |
| 17:00–18:30 | Behavioral practice — 1 STAR story/day                   |
| 18:30–19:15 | Anki                                                     |

_From D71 onward: add a 1-problem random retention check (15–20 min, ~20% E / 65% M / 15% H, drawn from "solved >14d ago") to the morning block._

**Phase 8 (D79–D90) — Interview mode, M–F:**

| Time        | Block                                                        |
| ----------- | ------------------------------------------------------------ |
| 9:00–10:30  | DSA mock (1 problem timed, Pramp / Interviewing.io / friend) |
| 10:30–12:00 | Mock notes + Anki                                            |
| 14:00–16:00 | Real screens / paid mocks (SD whiteboard if empty)           |
| 16:00–17:30 | Mock notes + Recall drain + 1 random retention check         |

**Phase 7+ Saturdays (D62, D69, D76, D83, D90)** — restructured for Behavioral Intensive:

| Time        | Block                                                                                 |
| ----------- | ------------------------------------------------------------------------------------- |
| 9:00–12:00  | DSA — 1 weakness re-solve on 30-min clock                                             |
| 12:00–13:00 | SD — Alex Xu Vol 2 chapter                                                            |
| 14:00–15:00 | Recall (anchored, 1 hr) + this-week's-hardest section                                 |
| 15:00–18:00 | Behavioral Intensive — story drafting + recording + 5-story drill (60s → 90s → 3-min) |

## How Recall works

**Single source of truth:** `prep-data/completions.jsonl` — append-only JSONL, one line per touch: `{"problem": "[Arrays & Hashing] -> Two Sum", "on": "2026-05-06"}`. The ledger only grows.

**Intervals (SM-2 lite):**

| Touches | Next due |
| ------- | -------- |
| 1       | +1 day   |
| 2       | +3 days  |
| 3       | +7 days  |
| 4       | +21 days |
| 5+      | +60 days |

A problem solved once is due 1 day later. Solved 5 times → +60 days, locked there. The more you've drilled it, the longer it can wait.

**DSA visual format in `curriculum.md`** — each problem has a parent line and up to 5 mastery slots:

```markdown
- Two Sum (E) · 4/5 (next due 2026-06-25)
  - [x] ✅ 2026-05-11
  - [x] ✅ 2026-05-14
  - [x] ✅ 2026-05-21
  - [x] ✅ 2026-06-04
  - [ ]
- 3Sum (M) · 0/5
```

Each `[x]` is a logged touch; `[ ]` is empty padding to 5 slots. Untouched problems render with no sub-bullets (first tick from `today.md` unlocks them). After 5 touches, all touches still render — full history is preserved. The annotation flips to `(overdue Nd)` once today passes the due date.

**Each `prep recompute` call:**

1. Reads `today.md` — ticked-and-dated lines append to the ledger (deduped by `(problem, date)`).
2. Reads `curriculum.md`'s DSA sub-bullets. New ones (incl. hand-typed backdated dates) → log a touch. Removed ones → purge that specific `(problem, date)`. Other touches preserved. Removing every sub-bullet for a problem is the destructive "full purge" path — loud stderr warning; preview with `--dry-run`.
3. Computes due-ness, ranks Recall most-overdue first (cap 10).
4. Picks `phase.new_per_day` never-touched problems from the current phase, ordered by source-rank → difficulty → document order.
5. Atomically writes both files.

Run `uv run prep recompute` any time — safe to re-run. Forgot to tick yesterday? Add `✅ DATE` to a sub-bullet in `curriculum.md` and recompute.

## When you fall behind

| Situation                              | What to do                                                                                                                                |
| -------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| Skipped yesterday                      | Drain Recall in the morning. Skip DSA New. Yesterday's leftovers surface in tomorrow's queue automatically.                               |
| 4+ recall items aging fast             | Extend the morning Recall block past 13:00 and skip DSA New entirely.                                                                     |
| Chronically behind (1+ week of slip)   | Stop trying to catch up intake. Drop your daily new-problem rate by 1/day for the rest of the phase by editing `curriculum.md`'s heading. |
| Mock this week needs uncovered pattern | Prioritize that pattern over recall for one day.                                                                                          |

## Mocks

Pre-commitment beats willpower — book early-sprint mocks on Day 0. Pramp (free, peer) for the first half, Interviewing.io (paid, mid/late) for the second. ~24 mocks total, weekly cadence in phases 1–5 ramping to every-other-day in phases 7–8. Mock state lives in `curriculum.md`'s `## Mocks` section: `pending → scheduled (📅 DATE) → completed (✅ DATE)`. Each mock can carry a `prereq:` clause (count thresholds like `15 E+M, 2 SD` or specific chapter IDs); the engine surfaces met/unmet status in `today.md`.

## Setup (one-time, ~4 hr)

**Daily driver:** Obsidian — open this repo as a vault. Install **Tasks** plugin, enable "Set done date on task completion." That's the only setting.

**Python toolchain:**

```sh
# Python 3.11+ required
curl -LsSf https://astral.sh/uv/install.sh | sh
uv sync
uv run pytest                     # confirm engine wired up
uv run prep recompute             # generates first today.md
```

**LaunchAgent (daily auto-recompute at 8:30 AM):**

```sh
cp launchd/com.rasha.recall-engine.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.rasha.recall-engine.plist
```

Logs land in `~/Library/Logs/recall-engine.log`. The Mac must be awake at 8:30 to fire; if it sleeps through, run `uv run prep recompute` manually whenever you wake up.

**Anki (~10–25 min/day, mobile during downtime):** four decks under `anki/` — code-templates, pattern-recognition, python-gotchas, complexity. ~90 cards total. NOT for full problem re-solves — those live in Obsidian.

**Books:** DDIA (Ch 5–9), Alex Xu Vol 1 (16 ch) + Vol 2 (Ch 1–7), Fluent Python (Sunday reading). Index DDIA + Alex Xu in `technical-rag` MCP for fast lookup.

**Day-0 diagnostic:** pick 3 random problems you've already solved, re-solve each on a 30-min clock from a blank file. Got <2/3? Drop Phase 1's budget — edit `curriculum.md`'s `### Phase 1 — Linear Patterns E+M (5 new/day)` heading to `(3 new/day)`.

## Tests

```sh
uv run pytest
```

Test names ARE the spec — read them top to bottom for a complete description of how the engine behaves.

## Files

| File                                    | What's in it                                                                                                                                                                  |
| --------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `curriculum.md`                         | **Master list** — DSA (by phase → pattern), System Design, Mocks, Behavioral. Tick boxes here OR in `today.md`.                                                               |
| `today.md`                              | _(generated)_ Today's frozen Recall + New queue. Tick boxes here OR in `curriculum.md`.                                                                                       |
| `prep-data/completions.jsonl`           | _(generated)_ Append-only completion ledger. Source of truth for DSA touches.                                                                                                 |
| `recall_engine.py`                      | Snapshot-mode SM-2 lite engine. CLI: `uv run prep recompute`.                                                                                                                 |
| `tests/test_recall_engine.py`           | Narrative tests — also serve as the spec.                                                                                                                                     |
| `launchd/com.rasha.recall-engine.plist` | LaunchAgent template — daily recompute at 8:30 AM.                                                                                                                            |
| `python-gotchas.md`                     | Append-only log of Python language traps you hit during the prep (mutable defaults, late binding, etc).                                                                       |
| `random-problems.md`                    | 92 NeetCode 250 problems outside the curriculum — a draw pile for unscripted practice. **Untracked by the engine** — solve one when you want a problem outside today's queue. |
| `patterns/*.md`                         | One file per pattern. Per-problem "Mistakes" nested underneath; surface gaps during the Saturday weekly review.                                                               |
| `anki/`                                 | Four decks: code-templates, pattern-recognition, python-gotchas, complexity (~90 cards).                                                                                      |
| `problems/<pattern>/<diff>-<n>.py`      | Your actual solution code, organized by pattern + difficulty.                                                                                                                 |
| `plans/`                                | Living plan files for major refactors.                                                                                                                                        |

## Glossary

- **Touch** — one successful (re-)solve event. One line in `completions.jsonl`.
- **Recall** — the most-overdue 10 items in `today.md`, frozen at recompute time.
- **New** — the next `phase.new_per_day` never-touched problems from the current phase.
- **Phase** — one entry in `curriculum.md`'s `### Phase N — Name (X new/day)` headings. Advancement is ledger-driven.
- **Snapshot mode** — today's queue is frozen at recompute time. Clicking checkboxes through the day does NOT re-rank. Tomorrow's recompute reflects what you did today.
- **Readiness tiers** — surfaced in `today.md`. **Fallback-ready** = all E+M touched. **Target-ready** = above + ≥20 SD + ≥8 mocks. **Stretch-ready** = every problem + all SD + all mocks.
