# Interview Prep

A 90-day NeetCode 150 (+44 extras) + system design + behavioral prep system. **One master file** (`curriculum.md`) holds DSA + System Design + Mocks + Behavioral; a snapshot-mode SM-2 lite engine (SuperMemo-2 spaced-repetition, simplified to fixed intervals — see _Spaced repetition_ below) regenerates `today.md` each morning, and you drain it.

- **Day 1 – Day 45** — all 164 Easy/Medium NC/LC problems solved
- **Day 1 – Day 60** — all 194 DSA problems solved
- **Coverage:** 194 DSA problems = 150 canonical NC150 + 44 extras (21 NC-150+, 15 LC-only, 8 company-asked) · DDIA Ch 5–9 · Alex Xu Vol 1 (16 ch) + Vol 2 (Ch 1–7) · ~24 mocks · ~10 behavioral stories (career anecdotes drilled in STAR format for non-technical screening rounds)

## Sequencing

- Easies before Mediums within each pattern
- E+M before Hards across patterns; **no Hards until phase 7**
- **Phases:**
  - **1–6** — E+M acquisition (Easies + Mediums, blocked by pattern)
  - **7** — Hards. **Start applying to new roles / jobs here.**
  - **8** — Post-Acquisition (zero new problems; bands: Decompression → Mock-heavy → Interview)

**Everything is ledger-driven, not calendar-driven.** Phase advancement, the Recall queue, and **mock interview unlocks** (each mock's `prereq:` clause is checked against ledger state and surfaced as met/unmet in `today.md`) all fire from ledger state.

**When to apply:** Phase 7 onward — start with safety-net companies on Day 45. Open up to target companies once you hit the Phase 8 Mock-heavy band, and dream / aspirational picks once you're in the Interview band. (See Phase 8 sections below for trigger conditions.)

## Daily flow

**Sundays off** — across all phases. Light _Fluent Python_ or DDIA reading is fine.

**Recall always wins over New.** Recall is knowledge you've already paid for, decaying on an exponential curve — skip a day and the cost compounds (you re-learn from scratch). New is just deferred scope; nothing degrades. When the day runs short, drain **all** of Recall first; let New slip into tomorrow. If even Recall is too long for the morning block, get partway down it — the most-overdue items are at the top, so partial draining still rescues the highest-priority knowledge.

**Why split Recall and New?** Spaced retrieval (Recall) fights Ebbinghaus's forgetting curve — each gap between reviews is a "desirable difficulty" (Bjork) that strengthens the memory trace more than tight clustering would. Blocked acquisition (New, one pattern at a time) keeps working memory focused on first exposure; interleaving belongs to retention, not initial learning. **Acquire blocked, retain spaced.**

**Where Anki fits.** The SM-2 queue in `today.md` handles **problem-level** spaced retrieval. Anki handles **fact-level** retrieval — code templates, pattern cues, Python gotchas, complexity tables (the four decks under `anki/`). Same Ebbinghaus/Bjork foundation, different granularity. Anki stays out of Phases 1–7 on purpose: first-exposure acquisition already saturates working memory, and stacking fact drills on top would crowd out the pattern you're trying to internalize. From **Phase 8 onward** acquisition is done, so Anki joins the daily mix to keep fact-level recall alive while the SM-2 queue keeps problem-level recall alive.

_Mock-week pivot: if a scheduled mock needs an uncovered pattern, prioritize that pattern over Recall for one day._

### Phases 1–6 — Acquisition · Mon–Sat

- **Acquisition** = first-time exposure to new problems, blocked by pattern. Working memory holds one pattern's structure; spaced Recall locks it in over weeks
- Recall first thing; SD then DSA New in the afternoon
- Recall time budget: Easy 20m / Medium 40m (no Hards in Recall during 1–6 — they don't enter the queue until Phase 7)
- **End of day:** tick the problem you found hardest in today.md's `## Today's hardest` section. Engine logs to `prep-data/hardest.jsonl` on next recompute and pre-fills Saturday's re-solve sub-block — no typing, no spelling, links auto-included.
- **Phase 7 uses the same two schedules below** (Mon–Fri table for weekdays, Saturday table for Saturdays). Sundays off across all phases.

**Mon–Fri schedule:**

| Time        | Block                                           |
| ----------- | ----------------------------------------------- |
| 9:00–13:00  | Recall drain                                    |
| 14:00–15:30 | System Design (today's chapter from `today.md`) |
| 15:30–19:30 | DSA New                                         |

_Mock days: afternoon shifts to `14:00–16:00 mock + 16:00–17:30 SD + 17:30–19:30 DSA New`._

**Saturday schedule:**

| Time        | Block                                                                                              |
| ----------- | -------------------------------------------------------------------------------------------------- |
| 9:00–13:00  | Recall drain — starts with **"this-week's-hardest"** sub-block (re-solve 2–3 hardest from Mon–Fri) |
| 14:00–15:30 | System Design (today's chapter from `today.md`)                                                    |
| 15:30–19:30 | DSA New                                                                                            |

_Engine pre-fills the "this-week's-hardest" sub-block from your weekday hardest flags (auto-resolved to live problem links from the curriculum). Falls back to a 3-slot blank template if you didn't flag anything that week._

### Phase 7 — Hards · Mon–Sat

**Start applying to new roles / jobs here.** Phase 7 begins after all 164 E+M are acquired (~Day 45). Submit to safety-net companies on Day 1. Hards are mostly an onsite-round signal, not a screen one; the ~15-day Phase 7 run + scheduling buffer gives you time to finish acquiring while early-round screens land on the calendar. Pre-commitment beats willpower — booked screens force the prep to converge.

Same daily structure as Acquisition; pace drops to 2 New/day (per Phase 7's budget). Recall budget for H: **90 min** — give each Hard the full 90 even on first solve.

### Phase 8 — Post-Acquisition · Mon–Sat

All 194 problems touched. **Zero new acquisition.** Three bands escalate in order; each column in the table below is one band.

- **Decompression** — _first 3–7 days of Phase 8_
- **Mock-heavy** — _trigger: ≥20 SD chapters + ≥8 mocks done_
- **Interview** — _trigger: real screens landing on the calendar_

**Mon–Fri schedule (read columns left-to-right as you escalate through the bands):**

| Block (time)                                | Decompression                     | Mock-heavy                                                               | Interview                                                             |
| ------------------------------------------- | --------------------------------- | ------------------------------------------------------------------------ | --------------------------------------------------------------------- |
| **Recall** (9:00–13:00)                     | Passive maintenance, no extras    | + 30-min timed re-solve + Pythonic refactor¹ + retention spot-check²     | Shrinks: 1 timed mock (blank file, no notes) + 30 min anchored Recall |
| **SD** (14:00–15:30)                        | Today's chapter from `today.md`   | DDIA Ch 8–9 deep-dives                                                   | Per calendar                                                          |
| **Mocks / Behavioral / Apps** (15:30–18:00) | Free Pramp peer · safety-net apps | Paid Interviewing.io / Hello Interview · daily STAR drill³ · target apps | Real screens / paid mocks · dream apps                                |
| **Anki** (18:00–19:00)                      | **Joins here** · 15 min/day       | Sustains                                                                 | Sustains                                                              |

¹ _Pythonic refactor: rewrite using `Counter`, `defaultdict`, comprehensions, `enumerate`, `zip`, `bisect`. Doubles each re-solve's value (memory + stdlib fluency)._
² _Retention spot-check: 1 random problem (15–20 min, drawn from "solved >14d ago")._
³ _STAR drill: Situation / Task / Action / Result — replaces casual story practice._

Interview-band ethos: **performance over coverage** — you've already drilled the volume.

**Saturday schedule (Mock-heavy / Interview bands — Behavioral Intensive):**

_Decompression-band Saturdays inherit the Phase 1–7 Saturday format above._

| Time        | Block                                                                                  |
| ----------- | -------------------------------------------------------------------------------------- |
| 9:00–12:00  | Recall (anchored) + this-week's-hardest sub-block (weakness re-solves on 30-min clock) |
| 12:00–13:00 | SD — Alex Xu Vol 2 chapter                                                             |
| 14:00–17:00 | Behavioral Intensive — story drafting + recording + 5-story drill (60s → 90s → 3-min)  |

## Spaced repetition (SM-2 lite)

**SM-2** = SuperMemo-2 (Wozniak, 1980s) — the spaced-repetition algorithm underpinning Anki and most SRS tools. The original adapts each card's interval via a per-card _ease factor_ updated by your 0–5 difficulty grade after every review. **The "lite" version this engine uses drops the ease factor entirely** — every successful touch just advances the card one rung on a fixed ladder. Same Ebbinghaus/Bjork foundation, simpler engine.

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

Each `[x]` is a logged touch; `[ ]` is empty padding to 5 slots. Untouched problems render with no sub-bullets (the first tick from `today.md` unlocks them). The annotation flips to `(overdue Nd)` once today passes the due date.

## Mocks

- Pre-commitment beats willpower — book early-sprint mocks on Day 0
- ~24 total · weekly through Phase 6 · every-other-day in Phase 7 + Phase 8 mock-heavy band · daily in Phase 8 interview band
- State lives in `curriculum.md`'s `## Mocks` section: `pending → scheduled (📅 DATE) → completed (✅ DATE)`
- Each mock carries a `prereq:` clause (count thresholds like `15 E+M, 2 SD` or specific chapter IDs); the engine evaluates it against ledger state and surfaces met/unmet in `today.md`. **Suggested mocks are unlocked by ledger state, not the calendar.**

**Platforms — algo mocks sequenced by signal quality and cost; SD mocks gated on chapter coverage:**

- **Pramp** (free, peer-to-peer · algo) — your "interviewer" is another candidate, so feedback quality varies. Use **first half** to get cheap reps, normalize live coding under another person's eyes, and surface low-hanging weaknesses before paying for stronger feedback.
- **Interviewing.io** (paid, vetted ex-FAANG interviewers · algo) — higher-fidelity feedback at a price. Use **second half** when you need realistic difficulty and actionable critique closer to real screens, after Pramp has cleared the obvious gaps. Skip for SD — peer/algo platforms can't reliably grade a system design.
- **Hello Interview** (paid, ex-FAANG SD specialists · SD-only) — curated SD curriculum (Design Twitter / Uber / Top-K, etc.) plus mocks with interviewers who do nothing but SD. **Gate: ≥10 Alex Xu chapters before your first booking** — earlier and you'll discover you can't talk through a design yet, wasting the slot.

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

**Anki (~10–25 min/day, mobile during downtime, Phase 8 onward):** four decks under `anki/` — code-templates, pattern-recognition, python-gotchas, complexity. ~90 cards total. Handles **fact-level** spaced repetition (distinct from `today.md`'s SM-2 queue, which handles problem-level). NOT for full problem re-solves — those live in Obsidian. Rationale for the late entry: see _Where Anki fits_ in Daily flow.

**Books:** DDIA (Ch 5–9), Alex Xu Vol 1 (16 ch) + Vol 2 (Ch 1–7), Fluent Python (Sunday reading). Index DDIA + Alex Xu in `technical-rag` MCP for fast lookup.

**Day-0 diagnostic:** pick 3 random problems you've already solved, re-solve each on a 30-min clock from a blank file. Got <2/3? Drop Phase 1's budget — edit `curriculum.md`'s `### Phase 1 — Linear Patterns E+M (5 new/day)` heading to `(3 new/day)`.

## CLI

`uv run prep recompute` — the engine entrypoint. Reads `today.md` ticks and `curriculum.md`'s DSA sub-bullets, appends new touches to the ledger, regenerates `today.md`. Atomic and idempotent — safe to re-run any time.

- LaunchAgent runs it daily at 8:30 AM
- Run manually if you wake up to a sleeping Mac (no fresh `today.md`)
- Forgot to tick yesterday? Add `✅ DATE` to the matching sub-bullet in `curriculum.md` and recompute
- Removing every sub-bullet for a problem is the destructive "full purge" path — loud stderr warning; preview with `--dry-run`

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
| `prep-data/hardest.jsonl`               | _(generated)_ Append-only "hardest of the day" flag ledger. Pre-fills Saturday's re-solve list.                                                                               |
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
- **Phase** — one entry in `curriculum.md`'s `### Phase N — Name (X new/day)` headings (Phases 1–7). Advancement is ledger-driven via the engine's `current_phase`. Phase 8 is README-only (post-acquisition; no engine-tracked budget); the engine parks on Phase 7 once all problems are touched, and Phase 8's bands escalate manually.
- **NC-150+** — problems outside NeetCode's canonical 150 list but **inside** NeetCode's full 450-problem dataset (links to neetcode.io). **21 in the curriculum** — gap-fillers from the NC450 coverage analysis (minimax DP, prefix sum + hashmap, cyclic sort, etc — see `coverage-analysis.md`) plus selected heavy patterns (Segment Tree, Bitmask DP, Sweep Line). Distributed by difficulty across phases 1–7 — Es and Ms in their pattern's natural phase, Hs in Phase 7.
- **LC-only** — problems outside NeetCode's full 450 entirely (links to leetcode.com). **15 in the curriculum** — popular interview practice in two flavors: (1) the **String Transformation** cluster (Valid Word Abbreviation, String Compression, Basic Calculator II, atoi, Count Binary Substrings) which NeetCode underrepresents, and (2) heavy-pattern coverage NeetCode doesn't curate at all (Segment Tree, Sweep Line, BIT, Bitmask DP, Reservoir Sampling, Bit-Trie, Difference Array, Boyer-Moore Majority).
- **`(variant of: X)` tag** — relationship marker only: "this problem is a follow-up of canonical problem X." Does NOT mean the problem is outside NC150 — most "II" variants (e.g. Combination Sum II, Coin Change II) are themselves on the canonical 150. Combine with `(nc-150+)` or `(lc-only)` for variants that ARE outside it (e.g. Majority Element II is `(lc-only)`).
- **Snapshot mode** — today's queue is frozen at recompute time. Clicking checkboxes through the day does NOT re-rank. Tomorrow's recompute reflects what you did today.
- **Readiness banner** — engine-rendered checkpoints in `today.md`: **Fallback-ready** = all E+M touched (~Day 45). **Target-ready** = +≥20 SD chapters +≥8 mocks. **Stretch-ready** = every problem + all SD + all mocks. Use as informal milestones; application timing is your call (see _When to apply_ in Sequencing).
