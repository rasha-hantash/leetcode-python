# Interview Readiness Coverage Tool — Per-Company Decision Support

A private CLI that answers: **"Given my touch ledger, do I have enough coverage of company X's interview style to spend a mock slot or submit an application?"**

Built on top of the existing recall engine. Not public, not for recruiters — strictly a personal decision-support tool.

## The decision being made

Before applying to or scheduling a mock with company X, three signals matter:

| Signal            | What it measures                                                                                  | Strength                                                |
| ----------------- | ------------------------------------------------------------------------------------------------- | ------------------------------------------------------- |
| Touched coverage  | % of company's expected problems ever solved                                                      | Weak — touched ≠ remembered                             |
| Retained coverage | % of company's expected problems at touch count ≥3 (engine interval ≥+7d, recall without warm-up) | Strong — this is the actual readiness signal            |
| Pattern coverage  | % of patterns company asks where you have ≥1 retained rep                                         | Strong — generalizable knowledge, not memorized answers |

**Output:** a markdown report. Not a "% ready" number. Concrete coverage maps + gap list.

## Data model

```
companies/
├── meta.md
├── google.md
├── stripe.md
└── ...
```

Each company file:

```markdown
---
tier: target # stretch | target | safety
applied: false
last_updated: 2026-05-23
sources: [LC Premium company tag, Glassdoor anecdata, my interview history]
---

# Meta

## Expected problems

- [Arrays & Hashing] -> Two Sum
- [Arrays & Hashing] -> Group Anagrams
- [Trees] -> Lowest Common Ancestor of a Binary Tree
- [Sliding Window] -> Longest Substring Without Repeating Characters
- ...
```

**Why this format works:** the canonical key `[Pattern] -> Problem Name` is identical to the curriculum format. Engine canonicalization (em-dash stripping, difficulty/priority tag stripping) already handles it. Zero new parsing infra needed.

## CLI design

```sh
uv run python -m recall_engine coverage meta
```

Output (markdown to stdout):

```
=== Meta — coverage report (as of 2026-05-23) ===

Expected: 18 problems · 6 patterns
Touched:    14/18 (78%)
Retained:    9/18 (50%)   ← signal you actually care about

Pattern coverage (retained reps only):
  Arrays & Hashing  ████████ 100%  (5/5)
  Trees             █████░░░  60%  (3/5)
  Sliding Window    ██░░░░░░  20%  (1/5)
  Dynamic Prog.     ░░░░░░░░   0%  (0/3)
  ...

Gaps — not yet touched:
  - [Trees] -> Subtree of Another Tree
  - [Sliding Window] -> Longest Substring K Distinct
  - ...

Unretained — touched but <3 touches:
  - [DP] -> Longest Common Subsequence (1 touch)
  - ...

Recommendation: drill 4 gaps + 5 unretained before applying.
```

Optional flags:

- `--patterns-only` — skip per-problem detail, just pattern bars
- `--gaps-only` — just the punch list of what to drill

## Build plan — 4 diffs in a stack

| Diff | Scope                                                                         | Risk | LOC |
| ---- | ----------------------------------------------------------------------------- | ---- | --- |
| 1    | Company file parser (pure function: path → list of canonical keys + metadata) | low  | ~50 |
| 2    | Coverage computation (pure function: company keys + ledger → coverage report) | low  | ~80 |
| 3    | CLI subcommand `coverage <name>` + markdown renderer                          | low  | ~80 |
| 4    | Seed 3-5 initial company files from past-interview history + LC Premium tags  | data | ~0  |

Each diff has tests. Total ~250 LOC + tests. Engine canonical-text invariants stay intact (no changes to existing parser).

## Timing — defer to D14 (Sat May 23, 2026)

**Building now is technically cheap.** Deferring is the right call because:

1. **The tool produces zero useful output until ~D14.** Ledger needs ~2 weeks of data before "retained" % means anything. D1–D7 = ~25 touches → all signals are noise.
2. **D0 setup is already 4-5 hours.** Sprint launch is the high-leverage moment; pre-build distracts from that.
3. **You may decide you don't need it.** If P1 goes well and your application strategy clarifies, this might be a YAGNI build. Easier to skip than to undo.

**D14 trigger** (Sat May 23, 2026): on that morning, decide whether to spend the Saturday afternoon (post-Recall, post-SD reading) building Diff 1+2. Add to `TODO.md`.

## Sequencing once we start

1. **D14 morning:** decide go/no-go. If no-go, defer to D21 and revisit.
2. **D14 afternoon (if go):** Diff 1 (parser + tests).
3. **D15:** OFF (Sunday).
4. **D21 (next Saturday):** Diff 2 (coverage compute + tests).
5. **D22 OFF or D27 Sat:** Diffs 3+4 (CLI + seed data). End-to-end working tool.

Net build time: ~6-8 hours spread across 2-3 Saturdays. Doesn't intrude on weekday Recall/DSA blocks.

## Open questions (decide at D14)

- **Where does company data come from?** Best sources: your past-interviews dirs (`~/workspace/personal/interviews/`, `~/workspace/personal/python-practice-interviews/`), Notion `Technical Interview Questions` page, LC Premium company tags. Pick the 3-5 highest-priority companies and seed manually.
- **How fresh does company data need to be?** Probably stale-OK — interview question banks change slowly. Manual upkeep at ~1 file/month is fine.
- **Do we need a "trend" view?** Coverage over time (e.g., "Meta retention went from 30% on D14 to 60% on D28") is nice but YAGNI for v1.
- **Output format: stdout only or also `prep-data/coverage/<company>.md`?** Probably stdout-only for v1; add file output if you start sharing reports with yourself across sessions.

## Progress

- [ ] D14 (Sat May 23, 2026): go/no-go decision
- [ ] Diff 1: company file format + parser (~50 LOC + tests)
- [ ] Diff 2: coverage computation function (~80 LOC + tests)
- [ ] Diff 3: CLI subcommand + markdown renderer (~80 LOC + tests)
- [ ] Diff 4: seed 3-5 initial company files (data, no code)
- [ ] Validate end-to-end: `uv run python -m recall_engine coverage <name>` returns sensible output
- [ ] Add `coverage` to README's CLI section + glossary

## Notes / deviations

_(Append here as the plan is executed. Date entries.)_
