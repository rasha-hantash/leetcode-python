# Open Items

Tracker for deferred prep-system work. Strike items through (`~~text~~`) when done; remove after 30 days.

## Pre-D1 (before Mon May 11)

- [x] ~~Push branch to origin.~~ Done 2026-05-07 — 4 PRs created via `gt submit` after repo synced. Stack: <https://app.graphite.com/submit/rasha-hantash/leetcode-python/2>.
- [ ] **Book mocks as Pramp/Interviewing.io availability lets you.** The recall engine doesn't depend on calendar mock dates — it just tracks `pending → scheduled (with date) → completed` from the `## Mocks` section in `curriculum.md`. Each mock line can carry `prereq: 15 E+M, 2 SD` (count thresholds) or `prereq: axu1-4, axu1-5, axu1-6` (specific chapter IDs); the engine surfaces met/unmet status. Book what's actually available; the readiness gates and prereq checks will tell you when each one is in scope.
- [x] ~~**Seed your tracking files.**~~ Done 2026-05-09 — superseded by the unified-curriculum refactor. Mocks, SD chapters, and behavioral prompts now live as inline sections of `curriculum.md`. No JSON files to copy.

## Mid-prep (when relevant)

- [x] ~~**Expand D59–D90 day-by-day.**~~ Done 2026-05-09 — dropped twice over. First superseded by ledger-derived dates, then by the phase-driven refactor (phase budgets live inline in `curriculum.md`'s `### Phase N` headings, engine advances ledger-driven, no calendar dates anywhere).
- [x] ~~**Build interview-coverage tool.**~~ Done 2026-05-08, then collapsed 2026-05-09 — `coverage.md` was superseded by the unified `curriculum.md`. Readiness lives in today.md; the master list IS the dashboard.

## Reference

- Prep window: Mon May 11 – Sat Aug 8, 2026 (full-time pace; the engine projects your actual end date in `today.md`).
- Job application gates (computed from ledger state, surfaced in today.md Readiness banner):
  - **Fallback-ready**: all E+M problems touched.
  - **Target-ready**: above + ≥20 SD chapters complete + ≥8 mocks completed.
  - **Stretch-ready**: every curriculum problem touched + all SD complete + all mocks complete.
- 163 problems · 18 NC150 patterns + 7 NC-150+ patterns
- 28 SD chapters seeded (Alex Xu Vol 1+2 + DDIA Ch 5–9)
- 13 behavioral prompts seeded (excluded from readiness gates — you can knock these out in a weekend)
