# Interview Prep — README

A 90-day NeetCode 150 + system design + behavioral prep system built on top of a snapshot-mode SM-2 lite recall queue. One master file (`curriculum.md`) holds DSA + System Design + Mocks + Behavioral. Each morning a Python script generates today's queue into `prep-data/today.md`. You drain it. Tomorrow morning the script regenerates based on what you checked — and `curriculum.md` stays in sync with the ledger.

## Daily flow

1. **Morning (one-time, automatic at 8:30 AM):** the LaunchAgent runs `uv run prep recompute`. This logs yesterday's completions into the ledger, syncs `curriculum.md` ticks, then writes a fresh `prep-data/today.md` with today's **Recall** + **New** sections. _If the cron didn't fire, run the command manually — same result._
2. **Morning Recall block (9:00–13:00):** open `prep-data/today.md`. Drain **Recall** top-down — click the checkbox of each problem as you re-solve it. Tasks plugin auto-stamps `✅ DATE`. Recall is the highest-leverage work — protecting it with the morning slot keeps it from getting dropped when the day runs long.
3. **Afternoon System Design (14:00–15:30):** today's chapter is surfaced as `## Today's SD reading` in `prep-data/today.md`. Tick the box in either today.md OR directly in curriculum.md's `## System Design` section.
4. **DSA New block (15:30–19:30):** today's New problems are listed in `prep-data/today.md` under `## New`. Solve them and tick the boxes there (or in `curriculum.md`). Phase + budget come from the heading in curriculum.md (`### Phase 1 — Linear Patterns E+M (5 new/day)`); `curriculum.md` is the master reference if you want to look ahead.
5. **End the day:** the engine doesn't need anything from you besides the ticked boxes. Pick tomorrow's first re-solve from your private "today's hardest" notes.

That's it. The list you wake up to is the list for the day — it does not reshuffle as you check items off. Whatever you don't finish gets folded into tomorrow's queue with more days overdue.

### Forgot to check things yesterday?

Run `uv run prep recompute` any time. It scans `today.md` for new `✅` stamps, appends them to the ledger, then regenerates `today.md` with a fresh queue.

## How Recall works

**Single source of truth:** an append-only JSONL ledger at `prep-data/completions.jsonl`. Each line is `{"problem": "[Arrays & Hashing] -> Two Sum", "on": "2026-05-06"}`. One line per touch. The ledger only grows.

**Each recompute call:**

1. Reads `today.md`, finds checked-and-dated lines, appends them to the ledger (deduped by `(problem, date)` so reruns are safe).
2. Reads `curriculum.md`'s DSA sub-bullet state. Each ticked sub-bullet `- [x] ✅ YYYY-MM-DD` is one logged touch. New sub-bullets (or hand-typed backdated ones) → log a touch on that date. Removed sub-bullets → purge that specific `(problem, date)` from the ledger. Other touches preserved. Removing every sub-bullet for a problem is the destructive "full purge" path (warned on stderr; preview with `--dry-run`).
3. Aggregates the ledger by problem → `(touch_count, latest_date)`.
4. Computes due-ness with SM-2 lite (table below). Items at or past their due date go into Recall, sorted most-overdue first, capped at 10.
5. Picks `phase.new_per_day` never-touched problems from the current phase in `curriculum.md`, ordered by source-rank → difficulty → document order.
6. Atomically writes `curriculum.md` — re-renders every DSA problem with the new counter (`· N/5`), `(next due DATE)` / `(overdue Nd)` annotation, and one ticked sub-bullet per logged touch + empty padding to 5 slots.
7. Rewrites `today.md`.

**DSA visual format in `curriculum.md`:** each problem is rendered as a parent line with up to 5 sub-bullet "mastery slots":

```markdown
- Two Sum (E) · 4/5 (next due 2026-06-25)
  - [x] ✅ 2026-05-11
  - [x] ✅ 2026-05-14
  - [x] ✅ 2026-05-21
  - [x] ✅ 2026-06-04
  - [ ]
- 3Sum (M) · 0/5
```

Each `[x]` = one logged touch. Empty `[ ]` = padding to 5 slots so the visible box count matches the `X/5` counter. Untouched problems render with no sub-bullets. After 5 touches, the counter saturates at `5/5`; additional touches still render (no truncation), so full history is preserved. Tick an empty padding slot in Obsidian → the Tasks plugin auto-stamps today's date → the next recompute logs the touch. To log a forgotten solve, hand-type `- [x] ✅ 2026-04-15` under the parent — the engine accepts backdated dates. Malformed dates are skipped with a stderr warning, never silently dropped.

**Intervals (SM-2 lite):**

| Touches | Next due |
| ------- | -------- |
| 1       | +1 day   |
| 2       | +3 days  |
| 3       | +7 days  |
| 4       | +21 days |
| 5+      | +60 days |

A problem you've solved once is due 1 day later. Solved twice → 3 days. Solved five times → 60 days, and stays there forever. The more you've drilled it, the longer it can wait.

**Why not Dataview / Tasks-plugin only?** Tasks plugin keeps only one `✅ DATE` stamp per line. To count _touches_ across the curriculum you need a history that grows — that's what the JSONL ledger is for. The Python engine does what Dataview can't: accumulate completion history across re-solves.

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
3. `uv run prep recompute` — generates the first `prep-data/today.md`.
4. (Optional but recommended) Copy `launchd/com.rasha.recall-engine.plist` to `~/Library/LaunchAgents/` and `launchctl load` it. Now `recompute` runs daily at 8:30 AM.

## Tests

```sh
uv run pytest
```

The test names ARE the spec — read them top to bottom for a complete description of how the engine behaves.

## Files

| File                                    | What's in it                                                                                                    |
| --------------------------------------- | --------------------------------------------------------------------------------------------------------------- |
| `curriculum.md`                         | **Master list** — DSA (by phase → pattern), System Design, Mocks, Behavioral. Tick boxes here OR in `today.md`. |
| `recall_engine.py`                      | Snapshot-mode SM-2 lite engine. Run via `uv run prep recompute`.                                                |
| `tests/test_recall_engine.py`           | Narrative tests — also serve as the spec.                                                                       |
| `pyproject.toml`                        | Python project metadata + uv lock. `click` (CLI) + `pytest` (dev).                                              |
| `launchd/com.rasha.recall-engine.plist` | LaunchAgent template that runs `recompute` daily at 8:30 AM.                                                    |
| `prep-data/today.md`                    | _(generated, bidirectionally synced)_ Today's frozen Recall + New queue. Tick boxes here OR in curriculum.md.   |
| `prep-data/completions.jsonl`           | _(generated)_ Append-only completion ledger. Source of truth for DSA touches.                                   |
| `setup.md`                              | Day-0 setup guide — Obsidian, Anki, Python, books, mocks, GCal, slash commands.                                 |
| `prep-plan-overview.md`                 | System reference: routine shape per phase, mock cadence, spaced-repetition rules, risks.                        |
| `neetcode-150.md`                       | Original NC150 list (reference).                                                                                |
| `python-gotchas.md`                     | Append-only log of Python language stumbles you hit during the prep.                                            |
| `patterns/*.md`                         | One file per pattern (e.g., `arrays-and-hashing.md`). Mistakes nested under each problem.                       |
| `anki/`                                 | Four decks: code-templates, pattern-recognition, python-gotchas, complexity. ~90 cards total.                   |
| `problems/<pattern>/<diff>-<n>.py`      | Your actual solution code, organized by pattern + difficulty.                                                   |
| `plans/`                                | Plan files for major refactors — living documents that document what's planned and what's done.                 |

## Glossary

- **Recall block** — the 4 hr morning slot (9:00–13:00) for draining the Recall queue + yesterday's-hardest re-solve. Highest-leverage work; protected by the morning slot so it doesn't get dropped when the day runs long.
- **DSA New** — the 4 hr afternoon slot (15:30–19:30) for fresh problems from today's curriculum. On mock days shifts to 17:30–19:30.
- **Recall (10)** — the most-overdue 10 items in `prep-data/today.md`, frozen at recompute time.
- **New (3)** — the next 3 never-touched curriculum problems in `prep-data/today.md`, frozen at recompute time.
- **Touch** — one successful (re-)solve event. One line in `completions.jsonl`.
- **Ledger** — `prep-data/completions.jsonl`. Append-only history of every touch.
- **Recompute** — running `uv run prep recompute`. Logs new touches, regenerates `today.md`.
- **Snapshot mode** — today's queue is frozen at recompute time. Clicking checkboxes through the day does NOT re-rank. Tomorrow morning's recompute reflects what you did today.
- **`(mock)`** — mock-interview day. Appears after the date in the day header.
- **Phase** — one entry in `phases.json` (pattern allowlist + `new_per_day` budget + difficulty cap/floor). Advancement is ledger-driven: the engine picks the lowest-numbered phase that still has untouched eligible problems. Phase 8 (Reinforcement) sets `new_per_day=0` and only surfaces Recall.
