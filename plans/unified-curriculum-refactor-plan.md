# Unified Curriculum — One Master File, Bidirectional Sync

Collapse the prep-system data model so `curriculum.md` is the single master list and `today.md` is a synced view. Drop `coverage.md` and the per-category JSON files. Tick a box in either file → both stay in sync after `recompute`.

## Why

Current shape has too many files: `curriculum.md` (DSA only), `coverage.md` (auto-generated dashboard), `mock_interviews.json`, `system_design_chapters.json`, `behavioral_prompts.json`, `phases.json`, `prep-data/today.md`. Touching mocks/SD/behavioral means hand-editing JSON. Coverage state can't be edited (un-ticking in `coverage.md` doesn't persist). The user has to track "where does this kind of thing live?" mentally.

Target: **one master file you edit, one daily view you drain, ledger as the append-only audit trail.**

## Target shape

### `curriculum.md` (master)

```markdown
# Curriculum

_The master list. Tick boxes here OR in `prep-data/today.md` — `prep recompute` keeps them in sync._

## DSA

### Phase 1 — Linear Patterns E+M (5 new/day)

#### Arrays & Hashing

- [ ] Contains Duplicate (E)
- [x] Valid Anagram (E) ✅ 2026-05-09
- [ ] Two Sum (E)
- [ ] Group Anagrams (M)
      ...

#### Two Pointers

- [ ] Valid Palindrome (E)
      ...

### Phase 2 — Linked List + Trees (4 new/day)

...

### Phase 5 — Hard Problems (2 new/day)

#### Arrays & Hashing

- [ ] First Missing Positive (H)
- [ ] Longest Consecutive Sequence (H — variant)
      ...

## System Design

- [ ] axu1-1 · Alex Xu Vol 1 · Ch 1 — Scale from Zero to Millions
- [x] axu1-2 · Alex Xu Vol 1 · Ch 2 — Back-of-envelope estimation ✅ 2026-05-08
      ...

## Mocks

- [ ] [mock-1] Pramp · Arrays & Hashing — pending · [book](https://www.pramp.com/dashboard) · prereq: 15 E+M, 2 SD
- [ ] [mock-2] Interviewing.io · Trees · 📅 2026-05-20 · [join](https://interviewing.io/your-call) · prereq: 25 E+M, axu1-4..6
- [x] [mock-3] Pramp · DP ✅ 2026-05-08 · note: Weak on memoization

## Behavioral

- [ ] [b1] Tell me about yourself / walk me through your background
- [x] [b2] Why this company / why are you looking ✅ 2026-05-05
      ...
```

**Key properties:**

- DSA section is grouped by phase first, then pattern. Same pattern can appear in multiple phases (e.g., Arrays & Hashing E/M in Phase 1, A&H H in Phase 5). Phase header carries the budget (`5 new/day`).
- SD/Mocks/Behavioral keep their stable IDs (`axu1-1`, `mock-1`, `b1`) inline so the engine can match them across edits.
- All status (checked/scheduled date/note) lives inline. No separate JSON.

### `today.md` (view)

Same as today, except:

- DSA Recall + New still come from the engine.
- SD chapter shown is "next pending in `curriculum.md`'s System Design section."
- Next mock shown is "next scheduled mock in `curriculum.md`'s Mocks section."
- Behavioral block (when surfaced) pulls next pending prompt.

## Sync rules

| Action                                        | Effect                                                                                                                   |
| --------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| Tick DSA box in `today.md`                    | `recompute` appends `(problem, date)` to ledger; on next render, curriculum.md DSA box gets `[x] … ✅ DATE` (touched ≥1) |
| Tick DSA box in `curriculum.md`               | Same — appends to ledger as a touch dated today                                                                          |
| Tick SD/Mock/Behavioral in `today.md`         | `recompute` rewrites the matching line in `curriculum.md` to `[x] … ✅ DATE`                                             |
| Tick SD/Mock/Behavioral in `curriculum.md`    | Already there — `recompute` is idempotent (no-op except parsing)                                                         |
| Uncheck DSA in `curriculum.md`                | Destructive: purges ALL ledger entries for that problem. Print a warning in `recompute` output naming the problem        |
| Uncheck SD/Mock/Behavioral in `curriculum.md` | Reverts to pending — strip the `✅ DATE`                                                                                 |
| Edit a mock's `📅 DATE`                       | `recompute` reads it as the new scheduled date                                                                           |

**Conflict policy:** If a DSA box is ticked in `today.md` and unchecked in `curriculum.md` in the same recompute window, ticked wins (user clearly drilled it; the uncheck was a typo). Print a warning.

## Files to delete

- `prep-data/coverage.md` — replaced by curriculum.md (it IS the dashboard)
- `prep-data/mock_interviews.json` + `.example.json` — replaced by `## Mocks` section
- `prep-data/system_design_chapters.json` + `.example.json` — replaced by `## System Design` section
- `prep-data/behavioral_prompts.json` + `.example.json` — replaced by `## Behavioral` section
- `phases.json` — phase budgets move into `## Phase N — Name (X new/day)` headings in curriculum.md

## Files preserved

- `prep-data/completions.jsonl` — ledger stays as audit trail
- `prep-data/today.md` — daily view (now a synced view, not the only place to tick)
- `recall_engine.py` — gains markdown-write capability + new parsers
- `tests/test_recall_engine.py` — full coverage of new sync behavior

## PR stack (4 diffs)

### PR 1 — Restructure `curriculum.md` (data only)

- Write a one-shot script that:
  - Reads current `curriculum.md` (flat by-pattern) + `phases.json`
  - For each phase, picks problems matching its pattern allowlist + difficulty bounds
  - Emits new `curriculum.md` with `## DSA` → `### Phase N — Name (X new/day)` → `#### Pattern` → problems
  - Migrates `system_design_chapters.example.json` → `## System Design` section
  - Migrates `mock_interviews.example.json` → `## Mocks` section
  - Migrates `behavioral_prompts.example.json` → `## Behavioral` section
- Run the script; commit the new `curriculum.md`. Engine still reads old format → tests still pass (no engine change in this PR).
- **Wait — that won't work.** Engine reads `## Pattern` headers; new file has `## DSA` → `### Phase N` → `#### Pattern`. So PR 1 must include the parser change too. Combine PR 1 + PR 2.

### PR 1 — Restructure curriculum.md + parser updates (combined)

- Restructure `curriculum.md` as above.
- Update `parse_curriculum` to walk `## DSA` → `### Phase N — Name (X new/day)` → `#### Pattern` headings; capture phase per problem.
- Update `Phase` model: drop pattern allowlist + difficulty bounds (now implicit from curriculum.md membership). Keep `number`, `name`, `new_per_day`. Read from headings.
- Update `current_phase` to use the embedded phase membership.
- Delete `phases.json` + its loader.
- Update tests.

### PR 2 — Parse SD/Mocks/Behavioral from curriculum.md

- Add parsers for `## System Design`, `## Mocks`, `## Behavioral` sections.
- Replace JSON loaders for those three.
- Update `today.md` rendering to surface from the new parsed data.
- Delete the four JSON files (and `.example.json` siblings).

### PR 3 — Bidirectional sync (curriculum.md is writable)

- Add `write_curriculum(curriculum_path, ledger, today_md_state)`:
  - For each DSA problem, set `[x] … ✅ DATE` if touched (use latest_date), `[ ]` otherwise.
  - For SD/Mocks/Behavioral, copy state from in-memory parse (which already reflects today.md ticks).
- `recompute` now writes back to `curriculum.md` after parsing.
- Implement uncheck-as-purge for DSA (strip ledger entries for unchecked problems; print warning).
- Tests for round-trip sync (tick today.md → curriculum.md updated; tick curriculum.md → today.md reflects on next recompute).

### PR 4 — Cleanup + docs

- Delete `prep-data/coverage.md` (engine no longer generates it).
- Update `README.md`, `setup.md`, `TODO.md` to drop coverage/JSON references; document bidirectional sync.
- Mark this plan file Progress complete.

## Decisions (resolved 2026-05-09)

1. **Phases.json killed.** Budgets move into headings (`### Phase 1 — Linear Patterns E+M (5 new/day)`). Single source of truth.
2. **Phase indicator surfaces in today.md** as `Phase 2/7` (current/total non-Reinforcement phases) so you can see progress at a glance. Reinforcement (final phase, `new_per_day=0`) is excluded from the denominator.
3. **Mock metadata kept inline:** `booking_url` rendered as `[book](url)` (clickable in both today.md and curriculum.md); `notes` kept in curriculum.md (not surfaced in today.md). `prereq` inline as `prereq: 15 E+M, 2 SD` or `prereq: 25 E+M, axu1-4..6`.
4. **Atomic write:** `curriculum.md.tmp` → `os.replace`. Warn if mtime advanced during recompute.
5. **Curriculum order preserved.** Engine never reorders user-edited curriculum.md.
6. **`prep recompute --dry-run` flag** before destructive uncheck-as-purge actually mutates the ledger.
7. **Anchors in today.md → curriculum.md** out of scope for this stack.

## Risks

- **Big diff in curriculum.md.** Reviewing the migrated layout takes care. The script should be deterministic and re-runnable so we can validate against the old file.
- **Engine writes user-edited files.** Mitigations: atomic write, mtime check, plus the existing `prep recompute` ergonomic of "run when you're done editing."
- **Unchecking DSA destroys ledger history.** This is the user's request, but warn loudly. Consider a `--dry-run` flag for recompute to preview destructive changes.

## Progress

- [ ] PR 1 — Restructure curriculum.md + parser updates
- [ ] PR 2 — Parse SD/Mocks/Behavioral from curriculum.md
- [ ] PR 3 — Bidirectional sync (curriculum.md writable)
- [ ] PR 4 — Cleanup + docs
