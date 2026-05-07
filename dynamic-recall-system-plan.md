# Dynamic Recall System — Self-Pacing Queue via Obsidian Dataview

Replace the static D+3 / D+7 / D+21 queue schedule with a Dataview-driven dynamic queue. Tomorrow's problem set is computed live from yesterday's checkmarks via the Tasks plugin's completion timestamps + a DataviewJS overdue-ranking query.

## Why

- The static schedule produced **41 of 45** working days where the Consolidation block overran its budget — some by 3+ hours.
- T1/T2 tiering can't fix it: that's a value problem, not a capacity problem. Slowing intake doesn't fix it either: the queue floor is set by intake rate, and Saturday's pattern-rotation budget is structurally too small for any non-trivial queue.
- The user prioritizes **recall over new problems** and wants full re-solves (no horizon downgrade to "sketch" or "1-min recall").
- A self-pacing queue absorbs all of that: drain top-down until the block ends; whatever didn't get done becomes more overdue and bubbles higher tomorrow.

## How it works

1. Each problem appears **once** in `prep-plan-daily.md` — in its source-day's DSA New block. No more `(from Dn)` queue duplicates.
2. The Tasks plugin auto-stamps `✅ YYYY-MM-DD` on every checkbox toggle.
3. Re-solving = re-checking the same line; each toggle generates a new completion timestamp under it.
4. A DataviewJS query at the top of the file computes `priority = today - (last_completion + interval(touch_count))` and sorts descending.
5. During the Consolidation block, the user opens the "Today" dashboard and drains top-down until time runs out.

## Intervals (SM-2 lite)

| Touches | Next due interval |
| ------- | ----------------- |
| 1       | +1 day            |
| 2       | +3 days           |
| 3       | +7 days           |
| 4       | +21 days          |
| 5+      | +60 days          |

## Two queries, both at top of `prep-plan-daily.md`

**New (3):** first 3 unchecked source-day tasks, in document order. Self-rescheduling — leftover from yesterday surfaces first.

**Recall (10):** top 10 most-overdue review items via DataviewJS, ranked by overdue-ness with touch-count weighting.

## File changes

1. **`prep-plan-daily.md`**
   - Add `## Today (live)` dashboard at the top with the two Dataview queries.
   - Strip all `Queue items due today` blocks from each day's Consolidation section (header + indented children).
   - Replace each stripped block with a single bullet pointing to the Today dashboard.
   - Update Day 0 setup checklist to install Tasks + Dataview plugins (DataviewJS enabled).

2. **`prep-plan-overview.md`**
   - Replace the T1/T2 tier table + narrow/multi-subtype pattern lists + D+3/D+7/D+21 spacing rules with a description of the dynamic system.
   - Remove the queue-load math (no longer relevant — capacity is now self-bounded by the block).
   - Update the Daily Routine activity column to point at the Today dashboard.
   - Update the Saturday note (still acknowledge density; no longer talks about T2 skip order).

## Progress

- [x] Save this plan file
- [x] Build Python script to transform `prep-plan-daily.md` (`/tmp/build_dynamic_queue.py`)
- [x] Run script on `prep-plan-daily.md` — stripped 45 populated + 4 empty queue blocks; inserted Today dashboard; updated Day 0 setup line. File shrank 1502 → 1060 lines.
- [x] Hand-edit `prep-plan-overview.md` — replaced T1/T2 tier table, D+3/D+7/D+21 spacing rules, queue-load math; added SM-2 interval table; updated Daily Routine activity columns (D1–D50 + P8 + P9 + P10 + Saturday); updated Saturday note + risks/buffers list.
- [x] Update prose references in `prep-plan-daily.md` (P8/P9/P10 daily-shape sections + the legend line about T2 markers)
- [ ] Verify (manual user step): open Obsidian → install Tasks + Dataview plugins → enable JS queries → confirm Recall (10) and New (3) blocks render. First Recall items will appear after a few checkboxes are toggled (no completion stamps yet means empty list).

## Backup

Pre-transformation backup of daily file: `/tmp/prep-plan-daily.md.bak.pre-dynamic` (kept locally for rollback if needed).
