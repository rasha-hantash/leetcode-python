# Open Items

Tracker for deferred sprint-system work. Strike items through (`~~text~~`) when done; remove after 30 days.

## Pre-D1 (before Mon May 11)

- [ ] **Push branch to origin.** `gt submit` was blocked because `rasha-hantash/leetcode-python` isn't in Graphite's synced-repos list. Either add it at <https://app.graphite.com/settings/synced-repos> and re-run `gt submit --no-interactive --publish`, or fall back to `git push -u origin <branch>` for the live stack.
- [ ] **Verify mock dates against actual booking availability.** `prep-plan-daily.md` re-maps mock slots to Tue/Fri pairs (D2, D5, D9, D12, D16, D19, D23, D26, D30, D33, D37, D40, D44, D47, D51, D54). These are tentative — Pramp and Interviewing.io may not have those exact slots open. Book what's actually available; the recall engine doesn't depend on mock dates.

## Mid-sprint (when relevant)

- [ ] **Expand D59–D90 day-by-day.** Phase 7 + Phase 8 in `prep-plan-daily.md` describe daily-shape templates rather than day-by-day. Acceptable until you reach D58 and want to plan the mock-heavy + interview-mode phase in detail. Trigger: hit D55 with a plan to enumerate D59 onward.

## Reference

- Sprint window: Mon May 11 – Sat Aug 8, 2026
- Apply windows: D45 (stretch), D52 (target), D58 (safety)
- 163 problems · 18 NC150 patterns + 7 net-new patterns
