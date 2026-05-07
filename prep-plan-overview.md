# Interview Prep Sprint — Overview

_System-level reference (dashboard, routine, spaced-repetition rules, mock cadence, risks). For day-by-day execution see [`prep-plan-daily.md`](./prep-plan-daily.md)._

## Sprint Dashboard

- **Window:** Wed May 6 – Wed Aug 5, 2026 (90 days, ~78 working days, 13 Sundays off)
  - **Acquisition phase (D1–D50):** finish NC150
  - **Consolidation phase (D51–D90):** depth, mocks, system design — gains compound here
- **Daily ceiling:** 9 hrs focused work
- **Coverage:** 150 NeetCode + 13 net-new (= 163 problems across 25 patterns) · DDIA Ch 5–9 · Alex Xu Vol 1 (16 ch) + Vol 2 (Ch 1–7) · ~10 polished behavioral stories · ~24 mocks
- **System artifacts:** `patterns/` (25 pattern notes, Mistakes nested) · `anki/` (4 decks: code-templates, pattern-recognition, python-gotchas, complexity — ~90 cards total) · `python-gotchas.md` (language stumbles log, append-only)
- **Cadence:** every phase has a single integer cadence (no fractional days)

| Phase | Days  | Categories                                   | Problems               | Cadence                    | WD  |
| ----- | ----- | -------------------------------------------- | ---------------------- | -------------------------- | --- |
| P1    | 1–6   | A&H + 2P + Sliding Window                    | 20                     | 4/day                      | 5   |
| P2    | 7–13  | Stack + Binary Search + Linked List          | 24                     | 4/day                      | 6   |
| P3    | 14–18 | Trees + Tries + 2 Heap (intro)               | 20                     | 4/day                      | 5   |
| P4    | 20–24 | rest Heap + Backtracking                     | 15                     | 3/day                      | 5   |
| P5    | 25–30 | Graphs + Adv Graphs + Climbing Stairs        | 20                     | **4/day (aggressive)**     | 5   |
| P6    | 31–38 | rest 1D DP + most 2D DP                      | 21                     | 3/day                      | 7   |
| P7    | 39–50 | last 2D DP + Greedy + Intervals + Math + Bit | 30                     | 3/day                      | 10  |
| P8    | 51–65 | Pattern Mastery + 7 net-new patterns         | 13 net-new + re-solves | ~1/day new, heavy re-solve | 13  |
| P9    | 66–78 | Mock-heavy + System Design Deep Dive         | 0 new (re-solves only) | 1 problem/day on clock     | 11  |
| P10   | 79–90 | Interview Mode (full simulation)             | 0 new (mock-paced)     | daily mock cadence         | 10  |

Total: **163** problems (150 NC150 + 13 net-new), **~78** working days, 25 patterns. Cross-phase moves to maintain 50-day consistency: 2 easy Heap problems lifted into P3, 1 1D DP (Climbing Stairs) lifted into P5, 1 2D DP (Regex Matching T2) pushed into P7.

**P8 net-new problems:** Segment Tree (Range Sum Query - Mutable + Count of Smaller After Self), Bitmask DP (Shortest Path Visiting All Nodes + Partition K Equal Subsets), Bit-Trie (Maximum XOR), Sweep Line (My Calendar III + Skyline), Reservoir Sampling (LL Random Node + Random Pick with Weight), Boyer-Moore (Majority Element + Majority Element II), Difference Array (Corporate Flight Bookings + Car Pooling).

**P5 cadence note:** Graphs at 4/day = ~1 hr/problem, dense. If you fall behind here, slip 1–2 problems into start of P6 — the dynamic Recall queue absorbs the slip without rescheduling.

---

## Daily Routine

Schedule shape shifts between the **acquisition phase (D1–D50)** — finishing NC150 — and the **consolidation phase (D51–D90)** — mocks, depth, system design. Saturdays in D51–D90 also restructure to fit a Behavioral Intensive block. Sundays are off across all phases.

The "queue" referenced below is the **dynamic Recall (10) dashboard** at the top of `prep-plan-daily.md` — a live Dataview query that re-ranks every solved problem by overdue-ness each time the file opens. Drain top-down during the Consolidation block; whatever doesn't get done becomes more overdue and bubbles higher tomorrow. No manual scheduling.

### D1–D50 — Mon–Sat (Acquisition)

| Time        | Block                      | Activity                                                                                                                                                                |
| ----------- | -------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 7:00–8:00   | Workout                    | Fixed (BDNF prime)                                                                                                                                                      |
| 8:00–9:00   | Shower + breakfast         | Read tomorrow's first problem 10 min (incubation)                                                                                                                       |
| 9:00–13:00  | **DSA New (4 hr · peak)**  | Today's fresh problems (count varies by phase)                                                                                                                          |
| 13:00–14:00 | Lunch + walk               | Off-screen                                                                                                                                                              |
| 14:00–15:30 | **System Design (1.5 hr)** | Today's chapter writeup in Obsidian                                                                                                                                     |
| 15:30–19:30 | **Consolidation (4 hr)**   | Open Recall (10) dashboard → drain top-down at standard time (E 20m / M 40m / H 90m) until the block ends → yesterday's hardest → Pythonic refactor → editorial → Anki. |
| 19:30+      | Free                       | Pre-bed: read tomorrow's first problem 10 min                                                                                                                           |

**Saturday note (D4, D11, D18, D25, D32, D39, D46).** Same time blocks. The 4 hr Consolidation block absorbs **Pattern coverage rotation** (~2 hr re-solving canonical problems from `patterns/`) + Recall queue + yesterday's hardest + (from D25) the +21d batch. Saturdays are the densest day — pattern rotation eats half the block, so Recall drain may only fit 2–3 items. Items that don't fit auto-bubble higher next Monday.

**Daily ceiling note.** Extending Consolidation to 4 hr brings focused-work hours to 9.5 (4 DSA + 1.5 SD + 4 Cons), 0.5 hr over the 9-hr dashboard ceiling. Acceptable on weekdays; if drift starts compounding, shrink the SD slot to 1 hr or end Consolidation 30 min early on light-queue days.

### D51–D90 — Mon–Fri (Consolidation)

Workout (7:00–8:00) and breakfast / incubation (8:00–9:00) carry over to every working day. Each sub-phase shifts the rest of the day:

**P8 (D51–D65) — Pattern Mastery + Net-New**

| Time        | Block                        | Activity                                                                         |
| ----------- | ---------------------------- | -------------------------------------------------------------------------------- |
| 9:00–13:00  | DSA New                      | ~1 net-new problem/day                                                           |
| 13:00–14:00 | Lunch + walk                 | Off-screen                                                                       |
| 14:00–16:00 | **Interview / Mock slot**    | Real screens, paid mocks, peer Pramp. When empty: 2 weakness re-solves.          |
| 16:00–17:30 | System Design                | DDIA Ch 7 + Alex Xu Vol 2                                                        |
| 17:30–18:30 | **Consolidation (anchored)** | Recall (10) drain top-down → 1 weakness re-solve OR cross-pattern mistake-mining |

**P9 (D66–D78) — Mock-heavy + SD Deep Dive**

| Time        | Block                              | Activity                                                                                                                             |
| ----------- | ---------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| 9:00–13:00  | Re-solve clock + Pythonic refactor | One problem on a 30-min clock narrating aloud, then 3 hrs Pythonic refactor + writeup. Drain Recall (10) top-down within this block. |
| 13:00–14:00 | Lunch + walk                       | Off-screen                                                                                                                           |
| 14:00–16:00 | **Interview / Mock slot**          | Paid mocks scheduled. When empty: SD writeup.                                                                                        |
| 16:00–17:00 | **SD anchor**                      | DDIA Ch 8–9 reading or SD writeup continuation                                                                                       |
| 18:30–19:15 | Anki                               | Review the day's takeaways                                                                                                           |

_From D71 onward: add a 1-problem random retention check (15–20 min, weighted ~20% easy / 65% medium / 15% hard) to the morning block._

**P10 (D79–D90) — Interview Mode**

| Time        | Block                                  | Activity                                                                                                           |
| ----------- | -------------------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| 9:00–10:30  | DSA mock                               | 1 problem timed (Pramp / Interviewing.io / friend)                                                                 |
| 10:30–12:00 | Mock retro + Anki                      | Capture takeaways                                                                                                  |
| 12:00–14:00 | Lunch + walk                           | Off-screen                                                                                                         |
| 14:00–16:00 | **Interview / Mock slot**              | Real screens, paid mocks. When empty: SD mock (whiteboard-style on a fresh Alex Xu V2 problem).                    |
| 16:00–17:30 | **Mock retro + Recall + random check** | Whichever mock ran in the slot. Drain Recall (10) top-down + 1 random retention check from "solved >14d ago" pool. |

### D51–D90 Saturdays — D53, D60, D67, D74, D81, D88

Restructured for **Behavioral Intensive** (3 hr afternoon block).

| Time        | Block                              | Activity                                                                                                 |
| ----------- | ---------------------------------- | -------------------------------------------------------------------------------------------------------- |
| 9:00–12:00  | DSA                                | P8: 1 net-new problem · P9/P10: 1 weakness re-solve on 30-min clock                                      |
| 12:00–13:00 | System Design                      | Alex Xu Vol 2 chapter                                                                                    |
| 13:00–14:00 | Lunch + walk                       | Off-screen                                                                                               |
| 14:00–15:00 | **Consolidation (anchored, 1 hr)** | Recall (10) drain top-down + previous-day hardest re-solve. (P10: + random retention check on D81, D88.) |
| 15:00–18:00 | **Behavioral Intensive (3 hr)**    | Story drafting / refinement, recording + listen-back, 5-story drill (60-sec → 90-sec → 3-min versions).  |
| 18:00       | Done                               |                                                                                                          |

### Sundays — OFF (all phases)

D5, D12, D19, D26, D33, D40, D47, D54, D61, D68, D75, D82, D89. Light _Fluent Python_ or DDIA reading allowed. No DSA, no SD, no behavioral.

---

**Protect the morning block ruthlessly** (9:00–13:00 in P1–P9; 9:00–12:00 in P10). No phone, email, Slack. Single-session attention residue is the most under-priced cost in the literature.

**Easy-day fallback:** if yesterday was all easy and the daily-hardest slot has nothing meaty, ask Claude for a 10–14d-stale problem to re-solve (skipping anything scheduled for the next Saturday).

---

## Spaced Repetition

Four layers, four different jobs:

**Anki (~10–25 min/day, mobile during downtime):** four decks under `anki/` — **code-templates** (~30 cards, code skeletons), **pattern-recognition** (~30 cards, problem→pattern smell), **python-gotchas** (~15 cards, language traps), **complexity** (~15 cards, big-O lookup). ~90 cards total. NOT full problems. Anki picks frequency via its built-in algorithm.

**Daily hardest re-solve (~30 min, start of consolidation block):** yesterday's hardest, from a blank file. Mistake-driven (not pattern-coverage). Slot is in every day's Consolidation line.

**Pattern coverage rotation (Saturday afternoon, ~2 hrs):** re-solve 2–3 canonical problems from `patterns/` rotation. Spans 13 Saturdays across the 90-day window — every pattern hit at least once, hot patterns 2x. Specific patterns are pre-named in each Saturday's entry.

**Recall queue (Cons block, every working day):** dynamic Dataview-driven priority queue at the top of `prep-plan-daily.md`. Replaces the old D+3 / D+7 / D+21 schedule.

### How the Recall queue works

- Each problem appears **once** in `prep-plan-daily.md` — in its source-day's DSA New block. Re-solving = re-checking the same line; the Tasks plugin auto-stamps a new completion timestamp on every toggle.
- A DataviewJS query computes `priority = today − (last_completion + interval(touch_count))` for every checked task and sorts descending. The top 10 most-overdue items render live as the **Recall (10)** dashboard.
- During the Cons block: open the dashboard, drain top-down at standard times (Easy 20 min · Medium 40 min · Hard 90 min) until the block ends. Whatever doesn't get done becomes more overdue and bubbles higher tomorrow — no manual rescheduling.

### Intervals (SM-2 lite)

| Touches | Next due interval |
| ------- | ----------------- |
| 1       | +1 day            |
| 2       | +3 days           |
| 3       | +7 days           |
| 4       | +21 days          |
| 5+      | +60 days          |

### Why this replaces tiering and horizons

The static D+3 / D+7 / D+21 schedule produced 41 of 45 working days where the Cons block ran 60–760 minutes over budget — a structural capacity problem that T1/T2 tiering couldn't fix. Self-pacing solves it directly: difficulty mix and capacity are absorbed by the block, and the queue floor is set by what you actually finish, not by an idealized calendar.

**Self-correcting behavior:**

- Easy-heavy day (3 E + 2 M up top, ~140 min) → 5–6 items cleared, queue slides further.
- Hard-heavy day (2 H + 1 M, ~220 min) → 3 items cleared, the rest stay at top of tomorrow's list with even higher overdue scores.
- Skip a day entirely → everything just gets more overdue. No catch-up logic needed.

**Random retention check (D71–D90, last 20 days, ~15–20 min/day):** unchanged. Random draw from the "solved >14d ago" pool tests cold-start retention. Distribution: ~20% easy / 65% medium / 15% hard. Time-boxed; if unsolved, the next solve auto-stamps a fresh completion date and the item bubbles back to the top via the standard query.

**Mistakes are nested inside `patterns/*.md`** — after every wrong/peeked problem, append a 1–2 sentence entry under the relevant problem in its pattern file (problem → "Stuck on", "Unlock", "Pattern"). Saturday weekly review reads these cross-pattern to surface gaps. Non-pattern Python stumbles go in `python-gotchas.md`.

**By Day 50 via this system:** 15 of 18 NC150 patterns hit by canonical re-solve once each (Intervals, Math, Bit get first hit on D53). Plus weekly +21d revisits via the Recall query (no separate scheduling needed). Plus ~50 daily hardest re-solves (mistake-driven). Plus daily Anki on templates.

---

## Mock Cadence (book all on Day 0 where possible — pre-commitment beats willpower)

### Acquisition phase (D1–D50): 13 mocks, weekly cadence

| Week | Days             | Platform                | Focus                     |
| ---- | ---------------- | ----------------------- | ------------------------- |
| 2    | Tue D7, Fri D10  | Pramp                   | Easy/Med DSA              |
| 3    | Tue D14, Fri D17 | Pramp                   | Trees DSA                 |
| 4    | Tue D21, Fri D24 | Pramp + Interviewing.io | Mixed; one verbal-only    |
| 5    | Tue D28, Fri D31 | Interviewing.io         | Graphs (hardest verbal)   |
| 6    | Tue D35, Fri D38 | Interviewing.io         | DP + system design        |
| 7    | Tue D42, Fri D45 | Interviewing.io         | Mixed full-loop           |
| 8    | Tue D49          | Interviewing.io         | NC150-end dress rehearsal |

### Consolidation phase (D51–D90): ~11 mocks, ramping cadence

| Week | Days                               | Platform                  | Focus                                           |
| ---- | ---------------------------------- | ------------------------- | ----------------------------------------------- |
| 9    | Tue D56                            | Interviewing.io           | Net-new pattern recognition                     |
| 10   | Tue D63, Fri D66                   | Interviewing.io           | Re-solve weakness areas                         |
| 11   | Tue D67, Thu D69, Tue D74, Thu D76 | Interviewing.io           | Mock-heavy, full simulation                     |
| 12   | Tue D79, Thu D81                   | Interviewing.io + paid    | Full-loop simulation                            |
| 13   | Tue D86, Thu D88                   | Interviewing.io + friends | Final stretch (daily mocks D85–D89 if possible) |

**~24 mocks total across 90 days.** Front-loaded weekly in acquisition, ramped up to every-other-day in P9-P10.

**After each mock:** 30-min retro. What stalled — communication, pattern recognition, syntax, complexity? Append insights to relevant `patterns/*/Mistakes` section. Add 1-2 Anki cards if there's a takeaway.

---

## Stretch List (when extra time, top→bottom)

1. Extra mock interview
2. Re-solve a previously-done problem on a 30-min clock, narrating out loud
3. System design problem from Alex Xu (write/whiteboard, don't just read)
4. Record a behavioral story, play back, refine
5. DDIA chapter + Anki cards
6. Engineering Q&A bank card authoring
7. Pre-bed problem preview (extra)
8. **Last:** extra fresh LeetCode problem

---

## Risks & Buffers

- **Falling behind?** The dynamic Recall queue absorbs slips automatically — items just become more overdue and bubble higher next day. If consistently 4+ days behind on intake, drop the new-problem cadence by 1/day for the rest of the phase rather than skipping reviews.
- **9-hr ceiling:** if you push past and morning block degrades, you've already lost the day. Quit on time.
- **Tool drift:** Anki/Obsidian tweaks only on Sundays.
- **Burnout signal:** day-3 of grind without retention → half-day off, no negotiation.

---

## Known Unknowns

- True retention from Day 0 diagnostic — if <50%, slow Phase 1 to 3/day
- Mock difficulty calibration — first 2 mocks reveal Pramp medium = LeetCode medium for you?
- DDIA pace — adjust based on prior DB knowledge
- Senior SD depth — varies wildly by company; revisit after first interview

---
