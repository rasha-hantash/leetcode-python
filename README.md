# Interview Prep Sprint — README

A 90-day NeetCode 150 + system design + behavioral prep system built on top of a snapshot-mode SM-2 lite recall queue. Each morning a Python script generates today's queue into `prep-data/today.md`. You drain it. Tomorrow morning the script regenerates based on what you checked.

## Daily flow

1. **Morning (one-time, automatic at 8:30 AM):** the LaunchAgent runs `uv run python -m recall_engine recompute`. This logs yesterday's completions into the ledger, then writes a fresh `prep-data/today.md` with today's **Recall** + **New** sections. _If the cron didn't fire, run the command manually — same result._
2. **Morning Recall block (9:00–13:00):** open `prep-data/today.md`. Drain **Recall** top-down — click the checkbox of each problem as you re-solve it. Tasks plugin auto-stamps `✅ DATE`. Recall is the highest-leverage work — protecting it with the morning slot keeps it from getting dropped when the day runs long.
3. **Afternoon System Design (14:00–15:30):** today's chapter in `prep-plan-daily.md` names what to read. Tick the box there.
4. **DSA New block (15:30–19:30):** open `prep-plan-daily.md` to find today's `### Day N` curriculum. Solve those problems. _Don't tick the source-day boxes — tick today's New section in `prep-data/today.md` instead._
5. **End the day:** fill in the inline "today's hardest" note in today's `prep-plan-daily.md` Day section. That's tomorrow morning's first re-solve.

That's it. The list you wake up to is the list for the day — it does not reshuffle as you check items off. Whatever you don't finish gets folded into tomorrow's queue with more days overdue.

### Forgot to check things yesterday?

Run `uv run python -m recall_engine recompute` any time. It scans `today.md` for new `✅` stamps, appends them to the ledger, then regenerates `today.md` with a fresh queue.

## How Recall works

**Single source of truth:** an append-only JSONL ledger at `prep-data/completions.jsonl`. Each line is `{"problem": "[Arrays & Hashing] -> Two Sum", "on": "2026-05-06"}`. One line per touch. The ledger only grows.

**Each recompute call:**

1. Reads `today.md`, finds checked-and-dated lines, appends them to the ledger (deduped by `(problem, date)` so reruns are safe).
2. Aggregates the ledger by problem → `(touch_count, latest_date)`.
3. Computes due-ness with SM-2 lite (table below). Items at or past their due date go into Recall, sorted most-overdue first, capped at 10.
4. Picks the first 3 never-touched problems from `prep-plan-daily.md` (in document order) for New.
5. Rewrites `today.md`.

**Intervals (SM-2 lite):**

| Touches | Next due |
| ------- | -------- |
| 1       | +1 day   |
| 2       | +3 days  |
| 3       | +7 days  |
| 4       | +21 days |
| 5+      | +60 days |

A problem you've solved once is due 1 day later. Solved twice → 3 days. Solved five times → 60 days, and stays there forever. The more you've drilled it, the longer it can wait.

**Why not Dataview / Tasks-plugin only?** Tasks plugin keeps only one `✅ DATE` stamp per line. To count _touches_ across the sprint you need a history that grows — that's what the JSONL ledger is for. The Python engine does what Dataview can't: accumulate completion history across re-solves.

## When you fall behind

**Recall always wins over New.** A recall item is knowledge you've already paid for; the forgetting curve is exponential. A skipped new problem is just deferred scope; nothing degrades.

| Situation                            | What to do                                                                                                                                      |
| ------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| Skipped yesterday                    | Drain Recall in the morning. Skip the afternoon DSA New block. Tomorrow morning the engine surfaces yesterday's leftovers in New automatically. |
| 4+ recall items aging fast           | Extend the morning Recall block past 13:00 and skip DSA New entirely. Yesterday's leftovers will surface in tomorrow's New automatically.       |
| Chronically behind (1+ week of slip) | Stop trying to catch up intake. Drop your daily new-problem rate by 1/day for the rest of the phase.                                            |

**Caveat:** if a mock this week needs a specific pattern you haven't covered yet (e.g., Friday Pramp = Trees), prioritize that pattern over recall for one day.

## One-time setup

**Full step-by-step guide:** see [`setup.md`](./setup.md). Covers Obsidian + Tasks plugin, Anki desktop/mobile, Python toolchain (`uv`), the recall engine + LaunchAgent, book indexing, mock booking, GCal recurring blocks, the Claude `/hint` command, and the Day-0 diagnostic re-solve.

**Minimum viable setup** (if you only do one thing today):

1. `uv sync` from the repo root — installs the recall engine and pytest.
2. Install Obsidian's **Tasks** plugin → enable "Set done date on task completion." (Rendered checkboxes are clickable by default — no separate toggle.)
3. `uv run python -m recall_engine recompute` — generates the first `prep-data/today.md`.
4. (Optional but recommended) Copy `launchd/com.rasha.recall-engine.plist` to `~/Library/LaunchAgents/` and `launchctl load` it. Now `recompute` runs daily at 8:30 AM.

## Tests

```sh
uv run pytest
```

The test names ARE the spec — read them top to bottom for a complete description of how the engine behaves.

## Files

| File                                    | What's in it                                                                                  |
| --------------------------------------- | --------------------------------------------------------------------------------------------- |
| `recall_engine.py`                      | Snapshot-mode SM-2 lite engine. Run via `uv run python -m recall_engine recompute`.           |
| `tests/test_recall_engine.py`           | Narrative tests — also serve as the spec.                                                     |
| `pyproject.toml`                        | Python project metadata + uv lock. `click` (CLI) + `pytest` (dev).                            |
| `launchd/com.rasha.recall-engine.plist` | LaunchAgent template that runs `recompute` daily at 8:30 AM.                                  |
| `prep-data/today.md`                    | _(generated)_ Today's frozen Recall + New queue. Tick boxes here.                             |
| `prep-data/completions.jsonl`           | _(generated)_ Append-only completion ledger. Source of truth.                                 |
| `setup.md`                              | Day-0 setup guide — Obsidian, Anki, Python, books, mocks, GCal, slash commands.               |
| `prep-plan-daily.md`                    | Day-by-day curriculum reference. Each Day's New problems and afternoon SD chapter.            |
| `prep-plan-overview.md`                 | System reference: routine shape per phase, mock cadence, spaced-repetition rules, risks.      |
| `dynamic-recall-system-plan.md`         | History of the dynamic-recall system evolution.                                               |
| `neetcode-150.md`                       | Original NC150 list (reference).                                                              |
| `python-gotchas.md`                     | Append-only log of Python language stumbles you hit during the sprint.                        |
| `patterns/*.md`                         | One file per pattern (e.g., `arrays-and-hashing.md`). Mistakes nested under each problem.     |
| `anki/`                                 | Four decks: code-templates, pattern-recognition, python-gotchas, complexity. ~90 cards total. |
| `problems/<pattern>/<diff>-<n>.py`      | Your actual solution code, organized by pattern + difficulty.                                 |

## Glossary

- **Recall block** — the 4 hr morning slot (9:00–13:00) for draining the Recall queue + yesterday's-hardest re-solve. Highest-leverage work; protected by the morning slot so it doesn't get dropped when the day runs long.
- **DSA New** — the 4 hr afternoon slot (15:30–19:30) for fresh problems from today's curriculum. On mock days shifts to 17:30–19:30.
- **Recall (10)** — the most-overdue 10 items in `prep-data/today.md`, frozen at recompute time.
- **New (3)** — the next 3 never-touched curriculum problems in `prep-data/today.md`, frozen at recompute time.
- **Touch** — one successful (re-)solve event. One line in `completions.jsonl`.
- **Ledger** — `prep-data/completions.jsonl`. Append-only history of every touch.
- **Recompute** — running `uv run python -m recall_engine recompute`. Logs new touches, regenerates `today.md`.
- **Snapshot mode** — today's queue is frozen at recompute time. Clicking checkboxes through the day does NOT re-rank. Tomorrow morning's recompute reflects what you did today.
- **`T2`** — vestigial low-priority marker on a few problems. The engine strips it when computing canonical text.
- **`M`** — mock-interview day.
- **Sprint phases** — P1–P10 across 90 days. P1–P7 = acquisition (NC150 net-new), P8 = pattern mastery + 7 net-new patterns, P9–P10 = mock-heavy + interview mode.
