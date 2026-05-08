# Open Items

Tracker for deferred prep-system work. Strike items through (`~~text~~`) when done; remove after 30 days.

## Pre-D1 (before Mon May 11)

- [x] ~~Push branch to origin.~~ Done 2026-05-07 — 4 PRs created via `gt submit` after repo synced. Stack: <https://app.graphite.com/submit/rasha-hantash/leetcode-python/2>.
- [ ] **Book mocks as Pramp/Interviewing.io availability lets you.** The recall engine doesn't depend on calendar mock dates — it just tracks `pending → scheduled (with date) → completed` from `prep-data/mocks.json`. Each mock can carry `prerequisites: {em_problems, sd_chapters}` thresholds; the engine surfaces met/unmet status under each mock. Book what's actually available; the readiness gates and prereq checks will tell you when each one is in scope.
- [ ] **Seed your tracking files.** Copy `prep-data/mocks.example.json` → `mocks.json`, `sd-chapters.example.json` → `sd-chapters.json`, `behavioral.example.json` → `behavioral.json`. Edit as you progress. The example files stay in git as reference templates; the active files are gitignored as personal state.

## Mid-prep (when relevant)

- [x] ~~**Expand D59–D90 day-by-day.**~~ Done 2026-05-08 — dropped instead of expanded. Phase 7/8 in `prep-plan-daily.md` now use a Calendar milestones list anchored to dates rather than Day-N markers. Pace varies per user; calendar dates remain useful as full-time-pace reference.
- [x] ~~**Build interview-coverage tool.**~~ Done 2026-05-08 — superseded by `prep-data/coverage.md` (Readiness → Behavioral → Mocks → SD → DSA-by-pattern). Same source set as the engine, grouped by pattern, variants nested, boxes auto-checked from ledger.

## Reference

- Prep window: Mon May 11 – Sat Aug 8, 2026 (full-time pace; the engine projects your actual end date in `today.md`).
- Job application gates (computed from ledger state, surfaced in today.md Readiness banner):
  - **Fallback-ready**: all E+M problems touched.
  - **Target-ready**: above + ≥20 SD chapters complete + ≥8 mocks completed.
  - **Stretch-ready**: every curriculum problem touched + all SD complete + all mocks complete.
- 163 problems · 18 NC150 patterns + 7 NC-150+ patterns
- 28 SD chapters seeded (Alex Xu Vol 1+2 + DDIA Ch 5–9)
- 13 behavioral prompts seeded (excluded from readiness gates — you can knock these out in a weekend)
