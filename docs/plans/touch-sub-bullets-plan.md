# Touch sub-bullets — surface DSA touch history in curriculum.md, keep today.md compact

Add nested checkboxes under each touched DSA problem in `curriculum.md`, one per touch. An accidental uncheck of a sub-bullet removes only that specific touch from the ledger; the top-level uncheck still triggers a full purge (with warning + `--dry-run`). `today.md` stays compact — sub-bullets do NOT render there.

## Why

Current behavior: an accidental uncheck of a top-level DSA box in `curriculum.md` purges every ledger entry for that problem. After 4 weeks of drilling Two Sum, one stray click destroys the spaced-repetition history. The migration safeguard catches the bulk case but not single-problem accidents.

Visualizing each touch as its own sub-bullet gives:

- A visible history (you can see "I've drilled Two Sum 4 times")
- Per-touch granularity for accidental unchecks (peel back one date instead of nuking all)
- Natural fit with Obsidian Tasks plugin's first-class support for nested tasks

## Target shape

In `curriculum.md` — **no parent checkbox; counter `X/5` is the status indicator; 5 slots always rendered for touched problems (ticks + empty padding)**:

```markdown
## DSA

### Phase 1 — Linear Patterns E+M (5 new/day)

#### Arrays & Hashing

- Two Sum (E) · 4/5 (next due 2026-06-25)
  - [x] ✅ 2026-05-11
  - [x] ✅ 2026-05-14
  - [x] ✅ 2026-05-21
  - [x] ✅ 2026-06-04
  - [ ]
- Valid Anagram (E) · 5/5 (next due 2026-09-02)
  - [x] ✅ 2026-05-11
  - [x] ✅ 2026-05-14
  - [x] ✅ 2026-05-21
  - [x] ✅ 2026-06-04
  - [x] ✅ 2026-07-04
- 3Sum (M) · 0/5
```

Each ticked sub-bullet `[x] ✅ DATE` = one logged touch. Empty sub-bullets `[ ]` are visual padding to 5 slots — they carry no data until ticked.

Render rules:

- **0 touches**: counter `0/5`, no sub-bullets (clean — avoids 815 empty checkboxes across untouched problems).
- **1–4 touches**: counter `N/5`, ticks oldest → newest, then `(5-N)` empty padding slots = 5 sub-bullets total.
- **5 touches**: counter `5/5`, 5 ticked sub-bullets, no padding.
- **6+ touches**: counter saturates at `5/5`, all touches render as ticked sub-bullets (no padding, no truncation — full history preserved).

Touch count saturates at `5/5` — past 5 touches the spaced-rep interval is locked at +60d, but additional touches still log to the ledger and show as new ticks.

The `(next due YYYY-MM-DD)` annotation appears on touched problems only. Computed from `latest_touch_date + interval_for(N_touches)`. If today > next-due (i.e. user skipped past it), the annotation flips to `(overdue Nd)` so curriculum.md surfaces lapsed problems at a glance.

In `today.md` (unchanged from current):

```markdown
## Recall — most overdue first

- [ ] [Arrays & Hashing] -> Two Sum (E)

## New — next from the curriculum

- [ ] [Arrays & Hashing] -> 3Sum (M)
```

Today stays compact — sub-bullets do NOT render there.

## Sync rules

| Action                                                                       | Effect                                                                                                                                                      |
| ---------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Tick the box in today.md (Recall or New)                                     | Engine appends one touch dated today; next render shows it as a new ticked sub-bullet in curriculum.md and shrinks the empty-padding slot count by one      |
| Tick an empty padding sub-bullet `[ ]` in curriculum.md                      | Tasks plugin auto-stamps `✅ TODAY`; next recompute logs a touch dated today (same effect as ticking in today.md)                                           |
| Hand-add a sub-bullet `- [x] ✅ YYYY-MM-DD` in curriculum.md (any past date) | Engine appends a touch dated YYYY-MM-DD to the ledger (backdated touch). Useful for logging a forgotten solve.                                              |
| Untick an existing sub-bullet `[x] ✅ DATE` in curriculum.md                 | Engine removes that specific `(problem, date)` entry from the ledger. Other touches preserved. Next render shows it as an empty padding slot (or drops it). |
| Delete a sub-bullet line entirely in curriculum.md                           | Same as untick: that touch removed from the ledger.                                                                                                         |
| Hand-add a sub-bullet with malformed date (e.g. `2/2/26`)                    | Engine prints a stderr warning naming the line and the bad text; the line is ignored (no touch logged, no destructive action)                               |
| All ticked sub-bullets removed for a problem (counter goes from N/5 → 0/5)   | All ledger entries for that problem purged (this is the new "full uncheck" path; warning printed on stderr)                                                 |
| Skip a day past `(next due DATE)`                                            | No data change. Next render flips the annotation to `(overdue Nd)`. The problem also surfaces in today.md's Recall section, sorted most-overdue-first.      |

## Engine changes

1. **`write_curriculum_dsa(md, ledger)` rewrite**: for each problem, render `- {Name} ({difficulty}) · {min(N, 5)}/5{annotation}` where:
   - `N` = touches in ledger; counter saturates at `5/5`.
   - `annotation` = `(next due YYYY-MM-DD)` for touched problems with future due date; `(overdue Nd)` if past due; empty for untouched.
   - Sub-bullets: 0 touches → no sub-bullets. 1–4 touches → N ticked (oldest → newest) + `(5-N)` empty padding `- [ ]`. 5 touches → 5 ticked, no padding. 6+ touches → all ticked, no padding.
2. **`parse_curriculum_dsa_state(md)`**: return type `dict[problem_text, set[date]]` — the set of ticked sub-bullet dates per problem. Empty `[ ]` padding sub-bullets are skipped silently (no date, not a touch). Empty set = untouched.
3. **`diff_dsa_state(state, ledger, today)`**: per-touch additions and per-touch purges.
   - For each problem:
     - For each ledger entry whose date is NOT in `state[problem]` → purge that specific entry (user unticked or deleted that sub-bullet).
     - For each date in `state[problem]` not in ledger → log a touch dated that date (covers fresh ticks via today.md round-trip, ticked padding slots, AND hand-added backdated touches).
4. **Malformed-date handling**: when parsing sub-bullets, ticked lines whose date doesn't match `YYYY-MM-DD` are skipped with a stderr warning naming the problem + the bad text. Non-destructive. Empty `[ ]` padding sub-bullets are NOT malformed — they're skipped silently.
5. **Next-due annotation**: computed from `latest_touch_date + interval_for(N)`. SM-2 lite intervals `[1, 3, 7, 21, 60]`. If `today <= next_due`: render `(next due YYYY-MM-DD)`. If `today > next_due`: render `(overdue {today - next_due}d)`. Recomputed on every render — skipping a day flips the annotation but doesn't mutate the ledger.
6. **`render_today` doesn't change** — today.md never shows sub-bullets. The `[Pattern] -> Name` line in Recall/New keeps its current shape.

## Migration

First recompute after this PR ships:

- `write_curriculum_dsa` re-renders `curriculum.md` with sub-bullets where the ledger has entries.
- No data migration needed — existing ledger drives the new render.

## PR plan

- **PR 1**: Engine refactor (`write_curriculum_dsa` + `parse_curriculum_dsa_state` + `diff_dsa_state` + tests) — no user-visible behavior change yet because tests use sub-bullet fixtures.
- **PR 2**: Run-once render to upgrade real `curriculum.md` to the new format, plus docs update (README's "How Recall works" section explains sub-bullets).

Probably bundle into one PR — the engine + curriculum.md re-render are tightly coupled. Decide at build time.

## Decisions (resolved 2026-05-09)

### No parent checkbox; counter `X/5` is the status

- **Decision:** drop the parent `[ ]` / `[x]` on each problem; render `- {Name} (E) · 4/5` instead, with sub-bullets below.
- **Rejected:**
  - Parent `[x]` plus sub-bullets (counter ambiguous: "is the parent a touch?")
  - No counter, just sub-bullets (no quick visual on touched-vs-untouched without expanding)
- **Why:**
  - Sub-bullet count visibly matches the counter (4 sub-bullets ↔ `4/5`) — no mental subtraction.
  - User read `4/5` as `5/5` when the parent was visible; the convention failed the readability test.
  - Untouched problems still surface with `· 0/5` — sortable/scannable.

### Render 5 slots for touched problems (ticks + empty padding)

- **Decision:** touched problems always render 5 sub-bullets (or more, if past saturation): N ticked + `(5-N)` empty padding `- [ ]`. Untouched problems render no sub-bullets.
- **Rejected:**
  - One sub-bullet per touch only (4 touches = 4 sub-bullets): visual mismatch with the `4/5` counter — user expected to see 5 boxes.
  - 5 empty slots for every problem (touched and untouched): adds ~815 empty lines across 163 untouched problems; clutters scanning.
  - Truncate to latest 5 after saturation: loses history; conflicts with the ledger as source of truth.
- **Why:**
  - Sub-bullet count visually matches the `X/5` counter for touched problems — the progress bar and the number agree.
  - Untouched problems stay clean for scanning new-problem queues.
  - After 5/5, all ticks render (no truncation) — full history preserved; counter saturates at `5/5` since the spaced-rep interval is locked at +60d anyway.
  - Ticking an empty padding slot in Obsidian → Tasks plugin auto-stamps date → next recompute logs a touch. Same sync model as ticking in today.md.

### Next-due annotation flips overdue

- **Decision:** append `(next due YYYY-MM-DD)` after the counter on touched problems. If today is past the due date, flip to `(overdue Nd)`.
- **Rejected:**
  - No annotation: forces user to mentally compute next due from latest touch + interval — friction.
  - Static `(next due DATE)` even when overdue: the date becomes a stale future hint; user has no signal that it's lapsed.
  - Annotation written to ledger / persisted: no — recomputed every render; skipping a day must NOT mutate the ledger.
- **Why:**
  - curriculum.md becomes scannable for "what's lapsed" — complements today.md's most-overdue-first sort.
  - Skipping a day is non-destructive: the next render flips the annotation, no data lost.
  - Recomputing each render keeps a single source of truth (the ledger) — the annotation is a derived view.

### Counter denominator is 5

- **Decision:** counter is `X/5` where 5 is the SM-2 lite saturation point.
- **Rejected:**
  - `X×` (open-ended count): doesn't show progress toward "fully internalized."
  - `X/4` (intervals only): off-by-one — there are 5 intervals (1, 3, 7, 21, 60d).
- **Why:** 5 matches the engine's SM-2 lite array length; once you hit 5/5, the spaced-rep interval is locked at +60d permanently.

### Backdated touches accepted via hand-typed sub-bullets

- **Decision:** the engine accepts hand-typed `- [x] ✅ YYYY-MM-DD` sub-bullets and appends them to the ledger as backdated touches.
- **Rejected:** ignore hand-typed dates; require user to edit `prep-data/completions.jsonl`.
- **Why:**
  - The whole point of curriculum.md being editable is that it's a friendly UI.
  - Forgetting to log a solve is a real, recurring failure mode the user expects to fix without touching JSONL.

### Malformed dates: loud skip

- **Decision:** when a sub-bullet date doesn't match `YYYY-MM-DD`, print a stderr warning naming the problem + the bad text; ignore the line (no touch logged).
- **Rejected:** silent skip (line just doesn't register).
- **Why:** user-typed entries fail in ways the engine can detect — staying silent makes the user wonder why their entry vanished.

### Sub-bullet uncheck warnings: silent

- **Decision:** unticking or deleting a single sub-bullet does NOT print a warning. The single-touch remove is by design safe.
- **Rejected:** verbose (every removal gets an `ℹ️ removed N entries` line).
- **Why:** the new design makes single-touch removes routine and reversible (just re-add the sub-bullet). Warning noise on every recompute would be ignored.
- **Exception:** when ALL sub-bullets are removed for a problem (counter 0/5 + ledger had entries), still print the destructive warning — that's the new "full purge" path.

### today.md keeps its compact shape

- **Decision:** sub-bullets render only in curriculum.md. today.md's Recall and New sections stay one-line-per-problem.
- **Rejected:** mirror the sub-bullets into today.md.
- **Why:** today.md is the daily action surface; the user wants a clean queue, not a history view.

## Progress

- [x] PR 1 — Engine refactor + curriculum.md re-render — _bundled with docs into a single PR (2026-05-09); engine + curriculum.md migration + tests + README all moved together since they're tightly coupled._
- [x] PR 2 — Docs (bundled into PR 1)

## Pre-conditions

This stack depends on the unified-curriculum stack (PRs #50–#53) being merged first. Don't start until then.
