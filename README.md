# Interview Prep

A 90-day NeetCode 150 (+44 extras) + system design + behavioral prep system. **One master file** (`curriculum.md`) holds DSA + System Design + Mocks + Behavioral; a snapshot-mode SM-2 lite engine (SuperMemo-2 spaced-repetition, simplified to fixed intervals — see _Spaced repetition_ below) regenerates `today.md` each morning, and you drain it.

- **Day 1 – Day 45** — all 164 Easy/Medium NC/LC problems solved (Phases 1–6 → Fallback-ready)
- **Day 1 – Day 60** — all 194 DSA problems solved (Phase 7 Hards added → ready for hard-tier screens)
- **Coverage:** 194 DSA problems = 150 canonical NC150 + 44 extras (21 NC-150+, 15 LC-only, 8 company-asked) · DDIA Ch 5–9 · Alex Xu Vol 1 (16 ch) + Vol 2 (Ch 1–7) · ~24 mocks · ~10 behavioral stories

## Sequencing

- Easies before Mediums within each pattern
- E+M before Hards across patterns; **no Hards until phase 7**
- Phases: 1–6 (E+M acquisition) → 7 (Hards) → 8 (Fallback-ready Reinforcement) → 9 (Target-ready Mock-heavy) → 10 (Interview Mode). Phases 1–7 advance by problem-count budgets; Phases 8–10 have **no new acquisition** and advance by readiness tier (ledger-gated, not calendar-gated).
- Engine picks the lowest-numbered phase with eligible untouched problems
- Phase budgets live in `curriculum.md`'s `### Phase N — Name (X new/day)` headings; edit if your retention diagnostic says so. **Chronically behind (1+ week of slip)?** Drop the budget by 1/day for the rest of the phase.

**Everything is ledger-driven, not calendar-driven.** Phase advancement, the Recall queue, and **application-readiness gates** (Fallback / Target / Stretch — surfaced in `today.md`'s readiness banner) all fire from ledger state. Mock dates booked on the calendar are user bookkeeping; the engine counts _completed_ mocks toward Target-ready, not their dates.

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

Same daily structure as Acquisition; pace drops to 2 New/day (per Phase 7's budget). Hards take longer to acquire — give each one the full 90 min that the Recall budget reserves for H, even on first solve.

### Phase 8 — Reinforcement Window (Fallback-ready) · M–F

- Zero new acquisition; every problem already touched (curriculum phases 1–7 done). This is the **application gate**: start submitting to fallback-tier companies.
- Morning is all Recall
- Afternoon: extra mocks + behavioral story practice + fallback-tier company applications (the safety-net rung — companies you'd accept an offer from if higher tiers don't pan out)
- **Anki joins here** (~15 min/day) — fact-level cards complement the SM-2 problem queue (see _Where Anki fits_ above)

### Phase 9 — Mock-heavy Reinforcement (Target-ready) · M–F

- Mornings: real-clock re-solve + Pythonic refactor (rewrite the working solution using Python idioms — `Counter`, `defaultdict`, comprehensions, `enumerate`, `zip`, `bisect` — to compress code, surface stdlib fluency in screens, and double the retrieval value of each re-solve) + Recall
- Afternoons: real screens / paid mocks; SD anchored on DDIA Ch 8–9 deep-dives
- Daily STAR (Situation / Task / Action / Result) story drill; Anki sustains spaced-recall outside the morning block

| Time        | Block                                                    |
| ----------- | -------------------------------------------------------- |
| 9:00–13:00  | 30-min clock re-solve + Pythonic refactor + Recall drain |
| 14:00–16:00 | Real screens / paid mocks (SD writeup if empty)          |
| 16:00–17:00 | SD anchor (DDIA Ch 8–9 deep-dive)                        |
| 17:00–18:30 | Behavioral practice — 1 STAR story/day                   |
| 18:30–19:15 | Anki                                                     |

_Mid-Mock-heavy onward: add a 1-problem random retention check (15–20 min, ~20% E / 65% M / 15% H, drawn from "solved >14d ago") to the morning block._

### Saturdays during Phases 9–10 — Behavioral Intensive

| Time        | Block                                                                                 |
| ----------- | ------------------------------------------------------------------------------------- |
| 9:00–12:00  | DSA — 1 weakness re-solve on 30-min clock                                             |
| 12:00–13:00 | SD — Alex Xu Vol 2 chapter                                                            |
| 14:00–15:00 | Recall (anchored, 1 hr) + this-week's-hardest section                                 |
| 15:00–18:00 | Behavioral Intensive — story drafting + recording + 5-story drill (60s → 90s → 3-min) |

### Phase 10 — Interview Mode (when real screens start) · M–F

- Mornings simulate real screens (timed, blank file, 1 problem)
- Afternoons are real interviews or paid mocks
- Recall drops to anchored 30 min — goal is performance, not coverage

| Time        | Block                                                        |
| ----------- | ------------------------------------------------------------ |
| 9:00–10:30  | DSA mock (1 problem timed, Pramp / Interviewing.io / friend) |
| 10:30–12:00 | Mock notes + Anki                                            |
| 14:00–16:00 | Real screens / paid mocks (SD whiteboard if empty)           |
| 16:00–17:30 | Mock notes + Recall drain + 1 random retention check         |

## Spaced repetition (SM-2 lite)

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
- ~24 total · weekly cadence in Phases 1–6 (acquisition) · every-other-day from Phase 7 (Hards) through Phase 9 (Mock-heavy) · daily in Phase 10 (real interviews)
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
- **Phase** — one entry in `curriculum.md`'s `### Phase N — Name (X new/day)` headings. Advancement is ledger-driven.
- **NC-150+** — problems outside NeetCode's canonical 150 list but **inside** NeetCode's full 450-problem dataset (links to neetcode.io). **21 in the curriculum** — gap-fillers from the NC450 coverage analysis (minimax DP, prefix sum + hashmap, cyclic sort, etc — see `coverage-analysis.md`) plus selected heavy patterns (Segment Tree, Bitmask DP, Sweep Line). Distributed by difficulty across phases 1–7 — Es and Ms in their pattern's natural phase, Hs in Phase 7.
- **LC-only** — problems outside NeetCode's full 450 entirely (links to leetcode.com). **15 in the curriculum** — popular interview practice in two flavors: (1) the **String Transformation** cluster (Valid Word Abbreviation, String Compression, Basic Calculator II, atoi, Count Binary Substrings) which NeetCode underrepresents, and (2) heavy-pattern coverage NeetCode doesn't curate at all (Segment Tree, Sweep Line, BIT, Bitmask DP, Reservoir Sampling, Bit-Trie, Difference Array, Boyer-Moore Majority).
- **`(variant of: X)` tag** — relationship marker only: "this problem is a follow-up of canonical problem X." Does NOT mean the problem is outside NC150 — most "II" variants (e.g. Combination Sum II, Coin Change II) are themselves on the canonical 150. Combine with `(nc-150+)` or `(lc-only)` for variants that ARE outside it (e.g. Majority Element II is `(lc-only)`).
- **Snapshot mode** — today's queue is frozen at recompute time. Clicking checkboxes through the day does NOT re-rank. Tomorrow's recompute reflects what you did today.
- **Readiness tiers** — surfaced in `today.md`. **Fallback-ready** = all E+M touched. **Target-ready** = above + ≥20 SD + ≥8 mocks. **Stretch-ready** = every problem + all SD + all mocks.
