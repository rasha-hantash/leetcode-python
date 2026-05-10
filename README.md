# Interview Prep

A 90-day NeetCode 150 (+44 extras) + system design + behavioral prep system. **One master file** (`curriculum.md`) holds DSA + System Design + Mocks + Behavioral; a snapshot-mode SM-2 lite engine (SuperMemo-2 spaced-repetition, simplified to fixed intervals — see _Spaced repetition_ below) regenerates `today.md` each morning, and you drain it.

- **Day 1 – Day 45** — all 164 Easy/Medium NC/LC problems solved
- **Day 1 – Day 60** — all 194 DSA problems solved
- **Coverage:** 194 DSA problems = 150 canonical NC150 + 44 extras (21 NC-150+, 15 LC-only, 8 company-asked) · DDIA Ch 5–9 · Alex Xu Vol 1 (16 ch) + Vol 2 (Ch 1–7) · ~24 mocks · ~10 behavioral stories (career anecdotes drilled in STAR format for non-technical screening rounds)

## Sequencing

- Easies before Mediums within each pattern
- E+M before Hards across patterns; **no Hards until phase 7**
- Phases: 1–6 (E+M acquisition) → 7 (Hards; applications begin when Fallback-ready triggers) → 8 (Post-Acquisition with three internal bands: Decompression → Mock-heavy → Interview). Phases 1–7 advance by problem-count budgets; Phase 8 has no new acquisition and bands escalate by readiness state + external calendar, not problem count. The engine parks on Phase 7 once all problems are touched — Phase 8 band advancement is your call, not the engine's.
- Engine picks the lowest-numbered phase with eligible untouched problems
- Phase budgets live in `curriculum.md`'s `### Phase N — Name (X new/day)` headings; edit if your retention diagnostic says so. **Chronically behind (1+ week of slip)?** Drop the budget by 1/day for the rest of the phase.

**Everything is ledger-driven, not calendar-driven.** Phase advancement, the Recall queue, and **application-readiness gates** (Fallback / Target / Stretch — surfaced in `today.md`'s readiness banner) all fire from ledger state. Mock dates booked on the calendar are user bookkeeping; the engine counts _completed_ mocks toward Target-ready, not their dates.

**Application timing — keyed to readiness tiers, not phases:**

- **Fallback-ready** (~Day 45, start of Phase 7) → fallback-tier applications open (the safety-net rung — companies you'd accept an offer from if higher tiers don't pan out)
- **Target-ready** (typically mid-Phase 7: all E+M + ≥20 SD chapters + ≥8 mocks) → target-tier applications open
- **Stretch-ready** (end of Phase 8 mock-heavy band: every problem + all SD + all mocks) → stretch-tier applications

## Daily flow

**Sundays off** — across all phases. Light _Fluent Python_ or DDIA reading is fine.

**Recall always wins over New.** Recall is knowledge you've already paid for, decaying on an exponential curve — skip a day and the cost compounds (you re-learn from scratch). New is just deferred scope; nothing degrades. When the day runs short, drain **all** of Recall first; let New slip into tomorrow. If even Recall is too long for the morning block, get partway down it — the most-overdue items are at the top, so partial draining still rescues the highest-priority knowledge.

**Why split Recall and New?** Spaced retrieval (Recall) fights Ebbinghaus's forgetting curve — each gap between reviews is a "desirable difficulty" (Bjork) that strengthens the memory trace more than tight clustering would. Blocked acquisition (New, one pattern at a time) keeps working memory focused on first exposure; interleaving belongs to retention, not initial learning. **Acquire blocked, retain spaced.**

**Where Anki fits.** The SM-2 queue in `today.md` handles **problem-level** spaced retrieval. Anki handles **fact-level** retrieval — code templates, pattern cues, Python gotchas, complexity tables (the four decks under `anki/`). Same Ebbinghaus/Bjork foundation, different granularity. Anki stays out of Phases 1–7 on purpose: first-exposure acquisition already saturates working memory, and stacking fact drills on top would crowd out the pattern you're trying to internalize. From **Phase 8 onward** acquisition is done, so Anki joins the daily mix to keep fact-level recall alive while the SM-2 queue keeps problem-level recall alive.

_Mock-week pivot: if a scheduled mock needs an uncovered pattern, prioritize that pattern over Recall for one day._

### Phases 1–6 — Acquisition · M–F

- **Acquisition** = first-time exposure to new problems, blocked by pattern. Working memory holds one pattern's structure; spaced Recall locks it in over weeks
- Recall first thing; SD then DSA New in the afternoon
- Recall time budget: Easy 20m / Medium 40m / Hard 90m
- **End of day:** jot down your "today's hardest" — feeds Saturday's re-solve sub-block
- Saturday: morning Recall starts with a "this week's hardest" sub-block — re-solve 2–3 problems flagged hardest from Mon–Fri's notes (engine adds the section to `today.md`)

| Time        | Block                                           |
| ----------- | ----------------------------------------------- |
| 9:00–13:00  | Recall drain                                    |
| 14:00–15:30 | System Design (today's chapter from `today.md`) |
| 15:30–19:30 | DSA New                                         |

_Mock days: afternoon shifts to `14:00–16:00 mock + 16:00–17:30 SD + 17:30–19:30 DSA New`._

### Phase 7 — Hards · M–F

**Start applying here.** Phase 7 begins after all 164 E+M are acquired — Fallback-ready triggers at Day 45. Submit to fallback-tier companies on Day 1 of Phase 7. Hards are mostly an onsite-round signal, not a screen one; the ~15-day Phase 7 run + scheduling buffer gives you time to finish acquiring while early-round screens land on the calendar. Pre-commitment beats willpower — booked screens force the prep to converge.

Same daily structure as Acquisition; pace drops to 2 New/day (per Phase 7's budget). Hards take longer to acquire — give each one the full 90 min that the Recall budget reserves for H, even on first solve.

### Phase 8 — Post-Acquisition · M–F

All 194 problems touched. **Zero new acquisition.** Same daily skeleton as Acquisition, minus the DSA New afternoon block — that slot becomes mocks + behavioral + applications. What changes between bands is _intensity_ and _what fills each block_, not the structure.

| Time        | Block                                           |
| ----------- | ----------------------------------------------- |
| 9:00–13:00  | Recall drain                                    |
| 14:00–15:30 | System Design (today's chapter from `today.md`) |
| 15:30–18:00 | Mocks + behavioral practice + applications      |
| 18:00–19:00 | Anki                                            |

**Bands escalate in order, gated by readiness state + external calendar:**

- **Decompression** — first ~3–7 days (skip entirely if you're already Target-ready when Phase 7 ends). Morning Recall is passive maintenance; mocks are free Pramp peer; apps target fallback-tier. **Anki joins here** (~15 min/day) — fact-level cards complement the SM-2 problem queue (see _Where Anki fits_ above).
- **Mock-heavy** — Target-ready confirmed (≥20 SD + ≥8 mocks done). Morning Recall extends with a 30-min clock re-solve + Pythonic refactor (rewrite using `Counter`, `defaultdict`, comprehensions, `enumerate`, `zip`, `bisect` — compress code, signal stdlib fluency in screens, double the retrieval value of each re-solve). Afternoon mocks become paid Interviewing.io; SD anchors on DDIA Ch 8–9 deep-dives; daily STAR (Situation / Task / Action / Result) drill replaces casual story practice. Add a 1-problem random retention check (15–20 min, ~20% E / 65% M / 15% H, drawn from "solved >14d ago") to the morning block. Anki sustains.
- **Interview** — real screens are landing on the calendar. Morning shifts from full Recall drain to a single 1-problem timed mock (blank file) + mock-notes; Recall shrinks to anchored 30 min. Afternoon = whatever the calendar dictates (real screens / paid mocks). Performance over coverage.

### Saturdays after Phase 8 mock-heavy band begins — Behavioral Intensive

(Phase 8 decompression-band Saturdays inherit the Phase 1–7 format.)

| Time        | Block                                                                                 |
| ----------- | ------------------------------------------------------------------------------------- |
| 9:00–12:00  | DSA — 1 weakness re-solve on 30-min clock                                             |
| 12:00–13:00 | SD — Alex Xu Vol 2 chapter                                                            |
| 14:00–15:00 | Recall (anchored, 1 hr) + this-week's-hardest section                                 |
| 15:00–18:00 | Behavioral Intensive — story drafting + recording + 5-story drill (60s → 90s → 3-min) |

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
- Pramp (free, peer) for first half; Interviewing.io (paid, mid/late) for second
- ~24 total · weekly through Phase 6 · every-other-day in Phase 7 + Phase 8 mock-heavy band · daily in Phase 8 interview band
- State lives in `curriculum.md`'s `## Mocks` section: `pending → scheduled (📅 DATE) → completed (✅ DATE)`
- Each mock can carry a `prereq:` clause (count thresholds like `15 E+M, 2 SD` or specific chapter IDs); the engine surfaces met/unmet status in `today.md`

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
- **Readiness tiers** — surfaced in `today.md`. **Fallback-ready** = all E+M touched. **Target-ready** = above + ≥20 SD + ≥8 mocks. **Stretch-ready** = every problem + all SD + all mocks.
