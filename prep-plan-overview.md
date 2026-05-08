# Interview Prep Sprint — Overview

_System-level reference (dashboard, routine, spaced-repetition rules, mock cadence, risks). For day-by-day execution see [`prep-plan-daily.md`](./prep-plan-daily.md)._

## Sprint Dashboard

- **Window:** Mon May 11 – Sat Aug 8, 2026 (90 days, ~77 working days, 13 Sundays off)
  - **E+M acquisition (D1–D39):** all NC150 Easies + Mediums by pattern, zero Hards. ~3.3/day average.
  - **Hard sprint (D40–D53):** all 22 NC150 Hards drilled fresh, ~1.5/day at 90 min each.
  - **Net-new (D54–D58):** 5 core + 2 optional from the 13 net-new (6 enrichment deferred to engine fallback).
  - **Mock-heavy reinforcement (D59–D78):** zero new, daily clocked re-solves + mocks + SD depth.
  - **Interview mode (D79–D90):** real-screen simulation, daily mocks, polished behaviorals.
- **Daily ceiling:** 9 hrs focused work
- **Coverage:** 150 NeetCode + 13 net-new + 9 String Transformation + 1 Sliding Window variant + 9 company-tagged variants (= 182 problems across 19 patterns) · DDIA Ch 5–9 · Alex Xu Vol 1 (16 ch) + Vol 2 (Ch 1–7) · ~10 polished behavioral stories · ~24 mocks
- **System artifacts:** `patterns/` notes (Mistakes nested) · `anki/` (4 decks: code-templates, pattern-recognition, python-gotchas, complexity — ~90 cards total) · `python-gotchas.md`
- **Difficulty-first sequencing:** within each pattern, Easies before Mediums. Across all patterns, E+M before H. **No Hards touched until D40.**

| Phase  | Days      | What                                                                                                                                                                   | Problems          | Cadence                       | WD  |
| ------ | --------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------- | ----------------------------- | --- |
| P1     | 1–7       | Linear: Arrays/Hashing → Two Pointers → SW → Stack → Binary Search start (E+M) + 6 String Transformation (E) + 1 SW variant + 2 company variants (lightning-ai, traba) | 36                | 5–6/day (4 on Sat)            | 6   |
| P2     | 8–17      | Binary Search rest → Linked List → Trees (E+M) + 4 String Transformation (M) on D8–D11 + 2 company variants (suno, zingage)                                            | 42                | 5–6/day on D8–D11, then 4/day | 9   |
| P3     | 18–24     | Backtracking → Tries → Graphs → Adv Graphs (M) + 2 company variants (chariot, credal)                                                                                  | 29                | 4–5/day                       | 6   |
| P4     | 25–39     | 1D DP → 2D DP → Greedy → Intervals → Math → Bit (E+M) + 1 company variant (january)                                                                                    | 39                | 3-4/day                       | 13  |
| **P5** | **40–53** | **🔥 Hard sprint — all 22 NC150 Hards** + 1 company variant (siro Employee Free Time)                                                                                  | 23                | 1.5-2/day                     | 12  |
| P6     | 54–58     | Net-new core (5) + optional (2) + 1 company variant (ngrok Wordler)                                                                                                    | 8+                | 2/day                         | 4   |
| P7     | 59–78     | Mock-heavy reinforcement (no new)                                                                                                                                      | 0 new (re-solves) | 1 weakness/day clocked        | 17  |
| P8     | 79–90     | Interview mode (full simulation)                                                                                                                                       | 0 new             | daily mock cadence            | 10  |

Total: **182** problems · 18 NC150 patterns + 7 net-new patterns + 1 String Transformation pattern · ~77 working days. The 6 enrichment net-new problems live in the curriculum but the engine deprioritizes them — they only surface if all core+optional is drained.

**Company-tagged variants (Track 1):** 9 problems pulled from your past interview list (`~/workspace/personal/interviews/` + Notion `Technical Interview Questions`). Each is slotted under the most natural NC150 pattern as a variant — engine treats them like any other curriculum problem with `(M) (core)` priority (or `(H) (core)` for the lone Hard). Mapping: lightning-ai → A&H D1, traba → A&H D3, suno → A&H D8, chariot (LC 2115) → Graphs D22, credal (BFS grid w/ time) → Graphs D23, zingage (char-freq tree) → Trees D13, january (prorated billing) → Intervals D34, ngrok (Wordler random+mutation, ~LC 380 flavor) → Reservoir Sampling D57, siro (Employee Free Time, LC 759 H) → Intervals D53 in Hard sprint.

**[String Transformation]** — frequency-driven addition (curriculum gap closed). NC150 has plenty of string problems but all wrap them in other patterns (sliding window, two-pointer, DP, tries). Real interviews ask raw char-by-char state-machine transformations: snake↔camel (ramp), atoi (LC 8), Decode String (LC 394, freq rank 14), Basic Calculator II (LC 227, freq rank 18), Roman to Integer (LC 13, freq rank 12), Add Binary (LC 67, freq rank 17), String Compression (LC 443), Longest Common Prefix (LC 14), Valid Word Abbreviation (LC 408 — Meta classic). 9 problems · 5E + 4M · slotted into D1–D6 (E warm-ups) and D8–D11 (M canonicals). Plus LC 696 Count Binary Substrings (E) added to Sliding Window pattern as a variant on D5.

**Apply window mapping:**

- D45 (Wed Jun 24): stretch tier (FAANG, top startups — slow recruiter pipelines)
- D52 (Wed Jul 1): target tier
- D58 (Tue Jul 7): safety tier
- First-round screens land Jul 8 onward; onsites Jul 21 onward.

**Hard sprint pattern decay mitigation:** when a Hard's pattern hasn't been touched in 2+ weeks (typical by D40), do a 5-min E+M canonical re-solve as warm-up before attempting the Hard.

---

## Daily Routine

Schedule shape shifts across phases: **E+M acquisition (D1–D39)** → **Hard sprint (D40–D53)** → **net-new (D54–D58)** → **mock-heavy reinforcement (D59–D78)** → **interview mode (D79–D90)**. Saturdays in D59+ restructure to fit a Behavioral Intensive block. Sundays are off across all phases.

The "Recall queue" below is the **`prep-data/today.md`** snapshot generated each morning by `recall_engine`. Open it during the morning Recall block; drain top-down. Whatever doesn't get done is folded into tomorrow's queue with higher overdue-ness. No manual scheduling.

### D1–D58 — Mon–Sat (Acquisition + Hard sprint + net-new)

**Why Recall in the morning:** Recall is the highest-leverage work — knowledge already paid for, decaying on an exponential curve. Putting it in the protected 9:00–13:00 slot guarantees it happens; deferring it to the afternoon means it gets dropped first when the day runs long. New problems demand novel pattern recognition but are deferrable; if you skip a New, it bubbles up to tomorrow's queue automatically.

| Time        | Block                      | Activity                                                                                                                                            |
| ----------- | -------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| 7:00–8:00   | Workout                    | Fixed (BDNF prime)                                                                                                                                  |
| 8:00–9:00   | Shower + breakfast         | Read tomorrow's first problem 10 min (incubation)                                                                                                   |
| 9:00–13:00  | **Recall (4 hr · peak)**   | Open `prep-data/today.md` → drain Recall top-down at standard time (E 20m / M 40m / H 90m) → yesterday's hardest re-solve → editorial → Anki        |
| 13:00–14:00 | Lunch + walk               | Off-screen                                                                                                                                          |
| 14:00–15:30 | **System Design (1.5 hr)** | Today's chapter writeup in Obsidian (mock days swap to 14:00-16:00 mock + 16:00-17:30 SD)                                                           |
| 15:30–19:30 | **DSA New (4 hr)**         | Today's fresh problems from `prep-plan-daily.md` (D1-D39: 3-4 E+M/day · D40-D53: 1.5-2 Hards/day · D54-D58: 2 net-new/day). Mock days: 17:30-19:30. |
| 19:30+      | Free                       | Pre-bed: read tomorrow's first problem 10 min                                                                                                       |

**Saturday note (D6, D13, D20, D27, D34, D41, D48, D55).** Same time blocks. The 4 hr morning Recall block opens with **This week's hardest — your pick**: open `prep-data/today.md` (Saturday's render adds the section automatically) and re-solve 2-3 problems you flagged hardest from your Mon-Fri "today's hardest" notes. Then drain Recall. New (3) intake on Saturdays drops to 3 problems instead of 4 to fit the reinforcement block.

**Daily ceiling note.** 4 hr Recall + 1.5 hr SD + 4 hr DSA New = 9.5 focused-work hours, 0.5 hr over the 9-hr dashboard ceiling. Acceptable on weekdays; if drift starts compounding, shrink the SD slot to 1 hr or end Recall 30 min early on light-queue days (rare — queue grows to 30-50 items by D40+).

### D59–D90 — Mon–Fri (Reinforcement + Interview Mode)

Workout (7:00–8:00) and breakfast / incubation (8:00–9:00) carry over to every working day. Each sub-phase shifts the rest of the day:

**P7 (D59–D78) — Mock-heavy reinforcement + SD Deep Dive**

| Time        | Block                              | Activity                                                                                                                              |
| ----------- | ---------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| 9:00–13:00  | Re-solve clock + Pythonic refactor | One problem on a 30-min clock narrating aloud, then 3 hrs Pythonic refactor + writeup. Drain Recall queue top-down within this block. |
| 13:00–14:00 | Lunch + walk                       | Off-screen                                                                                                                            |
| 14:00–16:00 | **Interview / Mock slot**          | Paid mocks scheduled. Real first-round screens land here from D59 onward. When empty: SD writeup.                                     |
| 16:00–17:00 | **SD anchor**                      | DDIA Ch 8–9 deep-dive or SD writeup continuation                                                                                      |
| 17:00–18:30 | **Behavioral practice**            | Refine 1 of the 10 STAR stories per day                                                                                               |
| 18:30–19:15 | Anki                               | Review the day's takeaways                                                                                                            |

_From D71 onward: add a 1-problem random retention check (15–20 min, weighted ~20% easy / 65% medium / 15% hard) to the morning block._

**P8 (D79–D90) — Interview Mode**

| Time        | Block                                  | Activity                                                                                                            |
| ----------- | -------------------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| 9:00–10:30  | DSA mock                               | 1 problem timed (Pramp / Interviewing.io / friend)                                                                  |
| 10:30–12:00 | Mock retro + Anki                      | Capture takeaways                                                                                                   |
| 12:00–14:00 | Lunch + walk                           | Off-screen                                                                                                          |
| 14:00–16:00 | **Interview / Mock slot**              | Real screens, paid mocks. When empty: SD mock (whiteboard-style on a fresh Alex Xu V2 problem).                     |
| 16:00–17:30 | **Mock retro + Recall + random check** | Whichever mock ran in the slot. Drain Recall queue top-down + 1 random retention check from "solved >14d ago" pool. |

### D59–D90 Saturdays — D62, D69, D76, D83, D90

Restructured for **Behavioral Intensive** (3 hr afternoon block).

| Time        | Block                           | Activity                                                                                                 |
| ----------- | ------------------------------- | -------------------------------------------------------------------------------------------------------- |
| 9:00–12:00  | DSA                             | 1 weakness re-solve on 30-min clock                                                                      |
| 12:00–13:00 | System Design                   | Alex Xu Vol 2 chapter                                                                                    |
| 13:00–14:00 | Lunch + walk                    | Off-screen                                                                                               |
| 14:00–15:00 | **Recall (anchored, 1 hr)**     | Recall queue drain + this-week's-hardest section in `prep-data/today.md` (P8: + random retention check). |
| 15:00–18:00 | **Behavioral Intensive (3 hr)** | Story drafting / refinement, recording + listen-back, 5-story drill (60-sec → 90-sec → 3-min versions).  |
| 18:00       | Done                            |                                                                                                          |

### Sundays — OFF (all phases)

D7, D14, D21, D28, D35, D42, D49, D56, D63, D70, D77, D84. Light _Fluent Python_ or DDIA reading allowed. No DSA, no SD, no behavioral.

---

**Protect the morning block ruthlessly** (9:00–13:00 in P1–P9; 9:00–12:00 in P10). No phone, email, Slack. Single-session attention residue is the most under-priced cost in the literature.

**Easy-day fallback:** if yesterday was all easy and the daily-hardest slot has nothing meaty, ask Claude for a 10–14d-stale problem to re-solve (skipping anything scheduled for the next Saturday).

---

## Spaced Repetition

Four layers, four different jobs:

**Anki (~10–25 min/day, mobile during downtime):** four decks under `anki/` — **code-templates** (~30 cards, code skeletons), **pattern-recognition** (~30 cards, problem→pattern smell), **python-gotchas** (~15 cards, language traps), **complexity** (~15 cards, big-O lookup). ~90 cards total. NOT full problems. Anki picks frequency via its built-in algorithm.

**Daily hardest re-solve (~30 min, start of morning Recall block):** yesterday's hardest, from a blank file. Mistake-driven (not pattern-coverage). Slot is in every day's Recall block.

**This week's hardest (Saturday morning, Recall block):** open `prep-data/today.md` — Saturday's render adds a `## This week's hardest — your pick` section automatically. Pick 2-3 problems you flagged hardest from your Mon-Fri "today's hardest" notes, write their canonical names into the empty bullets, re-solve from blank file, tick to log a touch.

**Recall queue (morning Recall block, every working day):** snapshot-mode SM-2 lite queue rendered into `prep-data/today.md` by `recall_engine`. Frozen at morning recompute time; clicking checkboxes does not reshuffle.

### How the Recall queue works

- An append-only JSONL ledger at `prep-data/completions.jsonl` records every (problem, date) touch.
- The engine aggregates the ledger by problem → `(touch_count, latest_date)`, applies SM-2 lite to compute a due date, and ranks items most-overdue first (capped at 10).
- During the morning Recall block: open `prep-data/today.md`, drain Recall top-down at standard times (Easy 20 min · Medium 40 min · Hard 90 min) until the block ends. Whatever doesn't get done is folded into tomorrow's queue with higher overdue-ness — no manual rescheduling.
- Snapshot mode means the visible list is fixed for the day. Manual `prep recompute` regenerates it any time (e.g., if you forgot to tick yesterday's items).

### Intervals (SM-2 lite)

| Touches | Next due interval |
| ------- | ----------------- |
| 1       | +1 day            |
| 2       | +3 days           |
| 3       | +7 days           |
| 4       | +21 days          |
| 5+      | +60 days          |

### Why this replaces tiering and horizons

The static D+3 / D+7 / D+21 schedule produced 41 of 45 working days where the Recall block ran 60–760 minutes over budget — a structural capacity problem that T1/T2 tiering couldn't fix. Self-pacing solves it directly: difficulty mix and capacity are absorbed by the block, and the queue floor is set by what you actually finish, not by an idealized calendar.

**Self-correcting behavior:**

- Easy-heavy day (3 E + 2 M up top, ~140 min) → 5–6 items cleared, queue slides further.
- Hard-heavy day (2 H + 1 M, ~220 min) → 3 items cleared, the rest stay at top of tomorrow's list with even higher overdue scores.
- Skip a day entirely → everything just gets more overdue. No catch-up logic needed.

**Random retention check (D71–D90, last 20 days, ~15–20 min/day):** unchanged. Random draw from the "solved >14d ago" pool tests cold-start retention. Distribution: ~20% easy / 65% medium / 15% hard. Time-boxed; if unsolved, the next solve auto-stamps a fresh completion date and the item bubbles back to the top via the standard query.

**Mistakes are nested inside `patterns/*.md`** — after every wrong/peeked problem, append a 1–2 sentence entry under the relevant problem in its pattern file (problem → "Stuck on", "Unlock", "Pattern"). Saturday weekly review reads these cross-pattern to surface gaps. Non-pattern Python stumbles go in `python-gotchas.md`.

**By Day 39 via this system:** every NC150 E+M problem touched at least once (128 problems, fully drilled within their source-day pattern blocks). Plus daily +1d/+3d/+7d Recall revisits (no separate scheduling needed). Plus ~39 daily hardest re-solves (mistake-driven). Plus daily Anki on templates. **Hard sprint opens D40.**

---

## Mock Cadence (book all on Day 0 where possible — pre-commitment beats willpower)

### Acquisition + Hard sprint (D1–D58): 13 mocks, weekly cadence

| Week | Days             | Platform                | Focus                                 |
| ---- | ---------------- | ----------------------- | ------------------------------------- |
| 1    | Tue D2, Fri D5   | Pramp                   | Easy/Med DSA                          |
| 2    | Tue D9, Fri D12  | Pramp                   | Trees DSA                             |
| 3    | Tue D16, Fri D19 | Pramp + Interviewing.io | Mixed; one verbal-only                |
| 4    | Tue D23, Fri D26 | Interviewing.io         | Graphs (hardest verbal)               |
| 5    | Tue D30, Fri D33 | Interviewing.io         | DP + intervals                        |
| 6    | Tue D37, Fri D40 | Interviewing.io         | E+M dress rehearsal → first Hard mock |
| 7    | Tue D44, Fri D47 | Interviewing.io         | Hard sprint mid-point                 |
| 8    | Tue D51, Fri D54 | Interviewing.io         | Hard end + net-new mocks              |
| 8    | Tue D58          | Interviewing.io         | Full real-screen simulation           |

### Reinforcement + interview mode (D59–D90): ~11 mocks, ramping cadence

| Week | Days             | Platform                  | Focus                                           |
| ---- | ---------------- | ------------------------- | ----------------------------------------------- |
| 9    | Tue D65, Fri D68 | Interviewing.io           | Re-solve weakness areas                         |
| 10   | Tue D72, Thu D74 | Interviewing.io           | Mock-heavy, full simulation                     |
| 11   | Tue D79, Thu D81 | Interviewing.io + paid    | Full-loop simulation                            |
| 12   | Tue D86, Thu D88 | Interviewing.io + friends | Final stretch (daily mocks D85–D89 if possible) |

**~24 mocks total across 90 days.** Front-loaded weekly during acquisition + Hard sprint, ramped up to every-other-day in P7-P8.

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
