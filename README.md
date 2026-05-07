# Interview Prep Sprint — README

A 90-day NeetCode 150 + system design + behavioral prep system built on top of a self-pacing recall queue. Open `prep-plan-daily.md` in Obsidian — that's where you live.

## Daily flow

1. **Open `prep-plan-daily.md` in Obsidian.** The `## Today (live)` section at the top renders two live queries: **Recall (10)** and **New (3)**.
2. **Morning DSA block (9:00–13:00):** scroll to today's `### Day N` section. Solve the problems in the **DSA New** list. Tick the boxes as you go — Tasks plugin auto-stamps the date.
3. **Afternoon System Design (14:00–15:30):** today's chapter in `prep-plan-daily.md` names what to read. Tick the box.
4. **Consolidation block (15:30–19:30):** scroll back to **Today → Recall (10)**. Solve the top item, find it in its source-day section, tick the box. The dashboard recomputes — next item rises to the top. Repeat until the block ends.
5. **End the day:** fill in the inline "today's hardest" note in today's section. That's tomorrow's first re-solve.

That's it. No daily setup, no manual rescheduling. Whatever you don't finish becomes more overdue and bubbles higher tomorrow.

## How Recall works

Each problem appears **once** in the file (in its source-day's DSA New block). Every time you re-solve it, you re-tick the same checkbox; Tasks plugin records a new completion timestamp. The Recall query computes:

```
priority = today − (last_completion + interval(touch_count))
```

…and sorts by that, descending. Most overdue floats to the top.

**Intervals (SM-2 lite):**

| Touches | Next due |
| ------- | -------- |
| 1       | +1 day   |
| 2       | +3 days  |
| 3       | +7 days  |
| 4       | +21 days |
| 5+      | +60 days |

So a problem you've solved once is due 1 day later. Solved twice → 3 days. Solved three times → 7 days. The more you've drilled it, the longer it can wait.

## When you fall behind

**Recall always wins over New.** A recall item is knowledge you've already paid for; the forgetting curve is exponential. A skipped new problem is just deferred scope; nothing degrades.

| Situation                            | What to do                                                                                                                              |
| ------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------- |
| Skipped yesterday                    | Drain Recall (10) end-to-end today. Skip New. Tomorrow morning, do today's New + 1–2 leftovers.                                         |
| 4+ recall items aging fast           | Spend the morning DSA block on Recall too — push New out a day. Yesterday's leftovers will surface in tomorrow's New (3) automatically. |
| Chronically behind (1+ week of slip) | Stop trying to catch up intake. Drop your daily new-problem rate by 1/day for the rest of the phase.                                    |

**Caveat:** if a mock this week needs a specific pattern you haven't covered yet (e.g., Friday Pramp = Trees), prioritize that pattern over recall for one day.

## One-time setup

**Full step-by-step guide:** see [`setup.md`](./setup.md). Covers Obsidian + plugins, Anki desktop/mobile, Python toolchain (`uv`), book indexing, mock booking, GCal recurring blocks, the Claude `/hint` command, and the Day-0 diagnostic re-solve.

**Minimum viable Obsidian setup** (if you only do one thing today):

1. Install **Tasks** plugin → enable "Set done date on task completion." (Rendered task checkboxes are clickable by default — no separate toggle.)
2. Install **Dataview** plugin → enable "Enable JavaScript Queries" + "Enable Inline JavaScript Queries."
3. Open `prep-plan-daily.md`. The Today dashboard at the top should render. The first time, Recall (10) will be empty — it populates after you tick a few boxes.

> **Heads-up:** both **Recall (10)** and **New (3)** render as clickable task lists — tick directly from the dashboard. Recall items embed metadata in the line itself (`— Xd overdue · Y× · last May 4`).

## Files

| File                               | What's in it                                                                                    |
| ---------------------------------- | ----------------------------------------------------------------------------------------------- |
| `setup.md`                         | Day-0 setup guide — Obsidian, Anki, Python, books, mocks, GCal, slash commands.                 |
| `prep-plan-daily.md`               | Day-by-day execution. Today dashboard + every working day's DSA New / SD / Consolidation slots. |
| `prep-plan-overview.md`            | System reference: routine shape per phase, mock cadence, spaced-repetition rules, risks.        |
| `dynamic-recall-system-plan.md`    | Plan + history of the dynamic recall system change (kept as a record, not a daily doc).         |
| `neetcode-150.md`                  | Original NC150 list (reference).                                                                |
| `python-gotchas.md`                | Append-only log of Python language stumbles you hit during the sprint.                          |
| `patterns/*.md`                    | One file per pattern (e.g., `arrays-and-hashing.md`). Mistakes nested under each problem.       |
| `anki/`                            | Four decks: code-templates, pattern-recognition, python-gotchas, complexity. ~90 cards total.   |
| `problems/<pattern>/<diff>-<n>.py` | Your actual solution code, organized by pattern + difficulty.                                   |

## Glossary

- **Cons / Consolidation block** — the 4 hr afternoon slot (15:30–19:30) for re-solves and review.
- **DSA New** — the 4 hr morning slot for fresh problems.
- **Recall (10)** — the live dashboard table at the top of `prep-plan-daily.md`. Top 10 most-overdue review items.
- **New (3)** — the live dashboard table for the next 3 unchecked source-day problems.
- **Touch** — one solve attempt of a problem. Each checkbox tick = 1 touch.
- **Source line / source-day block** — the canonical entry for a problem in its original `Day N` DSA New section. The single source of truth for completion timestamps.
- **`T2`** — vestigial low-priority marker on a few problems. Kept on source lines for historical reference; ignored by the Recall query.
- **`M`** — mock-interview day.
- **Sprint phases** — P1–P10 across 90 days. P1–P7 = acquisition (NC150 net-new), P8 = pattern mastery + 7 net-new patterns, P9–P10 = mock-heavy + interview mode.
