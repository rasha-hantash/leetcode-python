# Interview Prep Sprint — Mid-Level (Big Tech) + Senior (Startups)

## Sprint Dashboard

- **Window:** Wed May 6 – Wed Aug 5, 2026 (90 days, ~78 working days, 13 Sundays off)
  - **Acquisition phase (D1–D50):** finish NC150
  - **Consolidation phase (D51–D90):** depth, mocks, system design — gains compound here
- **Daily ceiling:** 9 hrs focused work
- **Coverage:** 150 NeetCode + 13 net-new (= 163 problems across 25 patterns) · DDIA Ch 5–9 · Alex Xu Vol 1 (16 ch) + Vol 2 (Ch 1–7) · ~10 polished behavioral stories · ~24 mocks
- **System artifacts:** `patterns/` (25 pattern notes, Mistakes nested) · `anki/` (4 decks: code-templates, pattern-recognition, python-gotchas, complexity — ~90 cards total) · `python-gotchas.md` (language stumbles log, append-only)
- **Cadence:** every phase has a single integer cadence (no fractional days)

| Phase | Days  | Categories                                   | Problems               | Cadence                    | WD  |
| ----- | ----- | -------------------------------------------- | ---------------------- | -------------------------- | --- |
| P1    | 1–6   | A&H + 2P + Sliding Window                    | 20                     | 4/day                      | 5   |
| P2    | 7–13  | Stack + Binary Search + Linked List          | 24                     | 4/day                      | 6   |
| P3    | 14–18 | Trees + Tries + 2 Heap (intro)               | 20                     | 4/day                      | 5   |
| P4    | 20–24 | rest Heap + Backtracking                     | 15                     | 3/day                      | 5   |
| P5    | 25–30 | Graphs + Adv Graphs + Climbing Stairs        | 20                     | **4/day (aggressive)**     | 5   |
| P6    | 31–38 | rest 1D DP + most 2D DP                      | 21                     | 3/day                      | 7   |
| P7    | 39–50 | last 2D DP + Greedy + Intervals + Math + Bit | 30                     | 3/day                      | 10  |
| P8    | 51–65 | Pattern Mastery + 7 net-new patterns         | 13 net-new + re-solves | ~1/day new, heavy re-solve | 13  |
| P9    | 66–78 | Mock-heavy + System Design Deep Dive         | 0 new (re-solves only) | 1 problem/day on clock     | 11  |
| P10   | 79–90 | Interview Mode (full simulation)             | 0 new (mock-paced)     | daily mock cadence         | 10  |

Total: **163** problems (150 NC150 + 13 net-new), **~78** working days, 25 patterns. Cross-phase moves to maintain 50-day consistency: 2 easy Heap problems lifted into P3, 1 1D DP (Climbing Stairs) lifted into P5, 1 2D DP (Regex Matching T2) pushed into P7.

**P8 net-new problems:** Segment Tree (Range Sum Query - Mutable + Count of Smaller After Self), Bitmask DP (Shortest Path Visiting All Nodes + Partition K Equal Subsets), Bit-Trie (Maximum XOR), Sweep Line (My Calendar III + Skyline), Reservoir Sampling (LL Random Node + Random Pick with Weight), Boyer-Moore (Majority Element + Majority Element II), Difference Array (Corporate Flight Bookings + Car Pooling).

**P5 cadence note:** Graphs at 4/day = ~1 hr/problem, dense. If you fall behind here, slip 1–2 problems into start of P6 (no T2 cuts needed yet).

---

## Day 0 — Setup (Tue May 5)

5-hour cap. After this, no more tool tweaking — start solving.

- [ ] Anki desktop + AnkiMobile (iOS) or AnkiDroid (Android), import the shared deck you found
- [ ] Obsidian — point vault at this repo folder; install Obsidian_to_Anki plugin (or standalone Python script); skip themes/customization
- [ ] Index DDIA + Alex Xu Vol 1 + Vol 2 in `technical-rag` MCP (PDF text extraction first; OCR via Gemini only if scans)
- [ ] Create `.claude/commands/hint.md` for graduated hints (L1=pattern category, L2=approach, L3=pseudocode, L4=code)
- [ ] GCal block: 7:00–8:00 workout · 9:00–13:00 DSA · 14:00–17:00 consolidation · 17:00–18:30 SD · 18:30–19:15 behavioral
- [ ] Push existing in-progress files (`problems/stack/easy-valid_parenthesis.py`, `problems/arrays-and-hashing/*`, `problems/sliding-window/*`)
- [ ] Initialize `notes/mistakes.md` and `notes/python-gotchas.md`
- [ ] `uv init` (~30 min skim of uv docs)
- [ ] Buy _Fluent Python_ (2nd ed, Ramalho) — Sunday reading material
- [ ] Book all 13 mocks (Pramp + Interviewing.io) on the dates in the Mock Cadence table — pre-commitment beats willpower
- [ ] **Diagnostic:** pick 3 random problems from your 27 already solved on neetcode.io. Re-solve each on a 30-min clock without looking. Retention baseline → feeds Phase 1 calibration.

---

## Daily Routine (fixed time blocks, Mon–Sat)

| Time        | Block                      | Activity                                                                                                            |
| ----------- | -------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| 7:00–8:00   | Workout                    | Fixed (BDNF prime)                                                                                                  |
| 8:00–9:00   | Shower + breakfast         | Read tomorrow's first problem 10 min (incubation)                                                                   |
| 9:00–13:00  | **DSA New (4 hr · peak)**  | Today's fresh problems (count varies by phase)                                                                      |
| 13:00–14:00 | Lunch + walk               | Off-screen                                                                                                          |
| 14:00–17:00 | **Consolidation (3 hr)**   | Re-solve yesterday's hardest as warm-up → Pythonic refactor pass → editorial reading → Anki cards (1–3/problem max) |
| 17:00–18:30 | **System Design (1.5 hr)** | Today's chapter writeup in Obsidian (topic per day below)                                                           |
| 18:30–19:15 | **Behavioral (45 min)**    | Today's story focus (per day below)                                                                                 |
| 19:15+      | Free                       | Pre-bed: read tomorrow's first problem 10 min                                                                       |

**Sundays:** off DSA + SD. Light Fluent Python reading allowed.

**Protect 9:00–13:00 ruthlessly.** No phone, email, Slack. Single-session attention residue is the most under-priced cost in the literature.

**Easy-day fallback:** if yesterday was all easy and the daily-hardest slot has nothing meaty, ask Claude for a 10–14d-stale problem to re-solve (skipping anything scheduled for the next Saturday).

---

## Spaced Repetition

Three layers, three different jobs:

**Anki (~10–25 min/day, mobile during downtime):** four decks under `anki/` — **code-templates** (~30 cards, code skeletons), **pattern-recognition** (~30 cards, problem→pattern smell), **python-gotchas** (~15 cards, language traps), **complexity** (~15 cards, big-O lookup). ~90 cards total. NOT full problems. Anki picks frequency via its built-in algorithm.

**Daily hardest re-solve (~30 min, start of consolidation block):** yesterday's hardest, from a blank file. Mistake-driven (not pattern-coverage). Slot is in every day's Consolidation line.

**Pattern coverage rotation (Saturday afternoon, ~2 hrs):** re-solve 2–3 canonical problems from `patterns/` rotation. Spans 13 Saturdays across the 90-day window — every pattern hit at least once, hot patterns 2x. Specific patterns are pre-named in each Saturday's entry.

**+21d batch (Saturday from D25):** re-solve 1–2 already-known patterns at long delay (the Wk-N batch named in each Saturday entry). Slot is in D25/D32/D39/D46 entries.

**Mistakes are nested inside `patterns/*.md`** — after every wrong/peeked problem, append a 1–2 sentence entry under the relevant problem in its pattern file (problem → "Stuck on", "Unlock", "Pattern"). Saturday weekly review reads these cross-pattern to surface gaps. Non-pattern Python stumbles go in `python-gotchas.md`.

**By Day 50 via this system:** 15 of 18 NC150 patterns hit by canonical re-solve once each (Intervals, Math, Bit get first hit on D53). Plus 8 +21d revisits. Plus ~50 daily hardest re-solves (mistake-driven). Plus daily Anki on templates.

---

## Mock Cadence (book all on Day 0 where possible — pre-commitment beats willpower)

### Acquisition phase (D1–D50): 13 mocks, weekly cadence

| Week | Days             | Platform                | Focus                     |
| ---- | ---------------- | ----------------------- | ------------------------- |
| 2    | Tue D7, Fri D10  | Pramp                   | Easy/Med DSA              |
| 3    | Tue D14, Fri D17 | Pramp                   | Trees DSA                 |
| 4    | Tue D21, Fri D24 | Pramp + Interviewing.io | Mixed; one verbal-only    |
| 5    | Tue D28, Fri D31 | Interviewing.io         | Graphs (hardest verbal)   |
| 6    | Tue D35, Fri D38 | Interviewing.io         | DP + system design        |
| 7    | Tue D42, Fri D45 | Interviewing.io         | Mixed full-loop           |
| 8    | Tue D49          | Interviewing.io         | NC150-end dress rehearsal |

### Consolidation phase (D51–D90): ~11 mocks, ramping cadence

| Week | Days                               | Platform                  | Focus                                           |
| ---- | ---------------------------------- | ------------------------- | ----------------------------------------------- |
| 9    | Tue D56                            | Interviewing.io           | Net-new pattern recognition                     |
| 10   | Tue D63, Fri D66                   | Interviewing.io           | Re-solve weakness areas                         |
| 11   | Tue D67, Thu D69, Tue D74, Thu D76 | Interviewing.io           | Mock-heavy, full simulation                     |
| 12   | Tue D79, Thu D81                   | Interviewing.io + paid    | Full-loop simulation                            |
| 13   | Tue D86, Thu D88                   | Interviewing.io + friends | Final stretch (daily mocks D85–D89 if possible) |

**~24 mocks total across 90 days.** Front-loaded weekly in acquisition, ramped up to every-other-day in P9-P10.

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

- **T2 cuts** (~30 problems tagged) = ~10 days buffer. Drop in T2 order if behind.
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

# Day-by-Day Schedule

`T2` = Tier-2 (drop first if behind). `M` = mock day. Each problem is prefixed with its NeetCode category in brackets.

## Phase 1 — Arrays/Hashing + Two Pointers + Sliding Window (Days 1–6, 4/day)

### Day 1 — Wed May 6 (4)

- **9:00–13:00 DSA New (4):**
  - [ ] [Arrays & Hashing] -> Contains Duplicate
  - [ ] [Arrays & Hashing] -> Valid Anagram
  - [ ] [Arrays & Hashing] -> Two Sum
  - [ ] [Arrays & Hashing] -> Group Anagrams
- **14:00–17:00 Consolidation:**
  - [ ] today's hardest: **_ • didn't click: _** (no warm-up — sprint start)
- **17:00–18:30 System Design:**
  - [ ] Grokking SD Fundamentals — intro + caching basics
- **18:30–19:15 Behavioral:**
  - [ ] draft "conflict" story (rough STAR — peer/manager disagreement)

---

### Day 2 — Thu May 7 (4)

- **9:00–13:00 DSA New (4):**
  - [ ] [Arrays & Hashing] -> Top K Frequent Elements
  - [ ] [Arrays & Hashing] -> Encode/Decode Strings
  - [ ] [Arrays & Hashing] -> Product of Array Except Self
  - [ ] [Arrays & Hashing] -> Valid Sudoku
- **14:00–17:00 Consolidation:**
  - [ ] D1 hardest re-solve: **_ • today's hardest: _** • didn't click: \_\_\_
- **17:00–18:30 System Design:**
  - [ ] Grokking SD Fundamentals — CDNs, load balancers
- **18:30–19:15 Behavioral:**
  - [ ] refine "conflict" story (tighten Situation + Action)

---

### Day 3 — Fri May 8 (4)

- **9:00–13:00 DSA New (4):**
  - [ ] [Arrays & Hashing] -> Longest Consecutive Sequence
  - [ ] [Two Pointers] -> Valid Palindrome
  - [ ] [Two Pointers] -> Two Sum II
  - [ ] [Two Pointers] -> 3Sum
- **14:00–17:00 Consolidation:**
  - [ ] D2 hardest re-solve: **_ • today's hardest: _** • didn't click: \_\_\_
- **17:00–18:30 System Design:**
  - [ ] Grokking SD Fundamentals — sharding + replication basics
- **18:30–19:15 Behavioral:**
  - [ ] draft "ownership" story (took initiative without being asked)

---

### Day 4 — Sat May 9 (4)

- **9:00–13:00 DSA New (4):**
  - [ ] [Two Pointers] -> Container With Most Water
  - [ ] [Two Pointers] -> Trapping Rain Water `T2`
  - [ ] [Sliding Window] -> Best Time to Buy/Sell Stock
  - [ ] [Sliding Window] -> Longest Substring Without Repeating Chars
- **14:00–17:00 Consolidation:**
  - [ ] D3 hardest re-solve: **_ • today's hardest: _** • didn't click: \_\_\_
  - **Pattern coverage rotation (Wk 1) — re-solve canonical from blank file:**
    - [ ] [Arrays & Hashing] -> Two Sum
    - [ ] [Sliding Window] -> Longest Substring Without Repeating Characters
    - [ ] (optional) Hardest from this week — own choice
- **17:00–18:30 System Design:**
  - [ ] Alex Xu Vol 1 Ch 1 (Scale from Zero to Millions) — start
- **18:30–19:15 Behavioral:**
  - [ ] refine "ownership" story

---

### Day 5 — Sun May 10 — OFF

Light reading: _Fluent Python_ Ch 1 (data model) — optional.

---

### Day 6 — Mon May 11 (4)

- **9:00–13:00 DSA New (4):**
  - [ ] [Sliding Window] -> Longest Repeating Character Replacement
  - [ ] [Sliding Window] -> Permutation in String
  - [ ] [Sliding Window] -> Minimum Window Substring
  - [ ] [Sliding Window] -> Sliding Window Maximum `T2`
- **14:00–17:00 Consolidation:**
  - [ ] D4 hardest re-solve: **_ • today's hardest: _** • didn't click: \_\_\_
- **17:00–18:30 System Design:**
  - [ ] Alex Xu Vol 1 Ch 1 (Scale to Millions) — finish
- **18:30–19:15 Behavioral:**
  - [ ] draft "ambiguity" story (operated without clear direction)

---

## Phase 2 — Stack + Binary Search + Linked List (Days 7–13, 4/day)

### Day 7 — Tue May 12 (4) `M`

- **9:00–13:00 DSA New (4):**
  - [ ] [Stack] -> Valid Parentheses
  - [ ] [Stack] -> Min Stack
  - [ ] [Stack] -> Evaluate RPN
  - [ ] [Stack] -> Daily Temperatures
- **14:00–17:00 Consolidation:**
  - [ ] D6 hardest re-solve: **_ • today's hardest: _** • didn't click: \_\_\_
- **17:00–18:30 System Design:**
  - [ ] Alex Xu Vol 1 Ch 2 (Back-of-envelope estimation) — part 1
- **18:30–19:15 Behavioral:**
  - [ ] record "conflict" story (audio, 2-min target)
- **Mock retro (Pramp easy/med DSA):**
  - [ ] what stalled? \_\_\_

---

### Day 8 — Wed May 13 (4)

- **9:00–13:00 DSA New (4):**
  - [ ] [Stack] -> Car Fleet
  - [ ] [Stack] -> Largest Rectangle in Histogram `T2`
  - [ ] [Binary Search] -> Binary Search
  - [ ] [Binary Search] -> Search 2D Matrix
- **14:00–17:00 Consolidation:**
  - [ ] D7 hardest re-solve: **_ • today's hardest: _** • didn't click: \_\_\_
- **17:00–18:30 System Design:**
  - [ ] Alex Xu Vol 1 Ch 2 (BoE estimation) — part 2 + practice 2 estimations
- **18:30–19:15 Behavioral:**
  - [ ] listen to "conflict" recording, note 2 issues, re-record

---

### Day 9 — Thu May 14 (4)

- **9:00–13:00 DSA New (4):**
  - [ ] [Binary Search] -> Koko Eating Bananas
  - [ ] [Binary Search] -> Find Minimum in Rotated Sorted Array
  - [ ] [Binary Search] -> Search in Rotated Sorted Array
  - [ ] [Binary Search] -> Time Based Key-Value Store
- **14:00–17:00 Consolidation:**
  - [ ] D8 hardest re-solve: **_ • today's hardest: _** • didn't click: \_\_\_
- **17:00–18:30 System Design:**
  - [ ] Alex Xu Vol 1 Ch 3 (Framework for SD interviews) — part 1
- **18:30–19:15 Behavioral:**
  - [ ] record "ownership" story (audio)

---

### Day 10 — Fri May 15 (4) `M`

- **9:00–13:00 DSA New (4):**
  - [ ] [Binary Search] -> Median of Two Sorted Arrays `T2`
  - [ ] [Linked List] -> Reverse Linked List
  - [ ] [Linked List] -> Merge Two Sorted Lists
  - [ ] [Linked List] -> Linked List Cycle
- **14:00–17:00 Consolidation:**
  - [ ] D9 hardest re-solve: **_ • today's hardest: _** • didn't click: \_\_\_
- **17:00–18:30 System Design:**
  - [ ] Alex Xu Vol 1 Ch 3 (Framework) — part 2 + write the 4-step framework on a card
- **18:30–19:15 Behavioral:**
  - [ ] listen "ownership", note issues
- **Mock retro:**
  - [ ] what stalled? \_\_\_

---

### Day 11 — Sat May 16 (4)

- **9:00–13:00 DSA New (4):**
  - [ ] [Linked List] -> Reorder List
  - [ ] [Linked List] -> Remove Nth Node From End
  - [ ] [Linked List] -> Copy List With Random Pointer
  - [ ] [Linked List] -> Add Two Numbers
- **14:00–17:00 Consolidation:**
  - [ ] D10 hardest re-solve: **_ • today's hardest: _** • didn't click: \_\_\_
  - **Pattern coverage rotation (Wk 2) — re-solve canonical from blank file:**
    - [ ] [Two Pointers] -> 3Sum
    - [ ] [Stack] -> Daily Temperatures
    - [ ] (optional) Hardest from this week — own choice
- **17:00–18:30 System Design:**
  - [ ] Alex Xu Vol 1 Ch 4 (Rate Limiter) — part 1
- **18:30–19:15 Behavioral:**
  - [ ] re-record "ownership" + record "ambiguity"

---

### Day 12 — Sun May 17 — OFF

_Fluent Python_ Ch 2 (sequences) or Ch 3 (dicts/sets).

---

### Day 13 — Mon May 18 (4)

- **9:00–13:00 DSA New (4):**
  - [ ] [Linked List] -> Find the Duplicate Number
  - [ ] [Linked List] -> LRU Cache
  - [ ] [Linked List] -> Merge K Sorted Lists `T2`
  - [ ] [Linked List] -> Reverse Nodes in K-Group `T2`
- **14:00–17:00 Consolidation:**
  - [ ] D11 hardest re-solve: **_ • today's hardest: _** • didn't click: \_\_\_
- **17:00–18:30 System Design:**
  - [ ] Alex Xu Vol 1 Ch 4 (Rate Limiter) — part 2 + token-bucket vs leaky-bucket card
- **18:30–19:15 Behavioral:**
  - [ ] all 3 stories pass-through review (60-sec each, timed)

---

## Phase 3 — Trees + Tries + Heap intro (Days 14–18, 4/day)

### Day 14 — Tue May 19 (4) `M`

- **9:00–13:00 DSA New (4):**
  - [ ] [Trees] -> Invert Binary Tree
  - [ ] [Trees] -> Maximum Depth Binary Tree
  - [ ] [Trees] -> Diameter of Binary Tree
  - [ ] [Trees] -> Balanced Binary Tree
- **14:00–17:00 Consolidation:**
  - [ ] D13 hardest re-solve: **_ • today's hardest: _** • didn't click: \_\_\_
- **17:00–18:30 System Design:**
  - [ ] Alex Xu Vol 1 Ch 5 (Consistent Hashing) — part 1
- **18:30–19:15 Behavioral:**
  - [ ] draft "leadership/influence" story (Senior priority — drove change through others)
- **Mock retro:**
  - [ ] what stalled? \_\_\_

---

### Day 15 — Wed May 20 (4)

- **9:00–13:00 DSA New (4):**
  - [ ] [Trees] -> Same Tree
  - [ ] [Trees] -> Subtree of Another Tree
  - [ ] [Trees] -> LCA of BST
  - [ ] [Trees] -> Binary Tree Level Order Traversal
- **14:00–17:00 Consolidation:**
  - [ ] D14 hardest re-solve: **_ • today's hardest: _** • didn't click: \_\_\_
- **17:00–18:30 System Design:**
  - [ ] Alex Xu Vol 1 Ch 5 (Consistent Hashing) — part 2 + virtual node card
- **18:30–19:15 Behavioral:**
  - [ ] refine "leadership" + draft "failure/lessons" story

---

### Day 16 — Thu May 21 (4)

- **9:00–13:00 DSA New (4):**
  - [ ] [Trees] -> Binary Tree Right Side View
  - [ ] [Trees] -> Count Good Nodes in Binary Tree
  - [ ] [Trees] -> Validate Binary Search Tree
  - [ ] [Trees] -> Kth Smallest Element in BST
- **14:00–17:00 Consolidation:**
  - [ ] D15 hardest re-solve: **_ • today's hardest: _** • didn't click: \_\_\_
- **17:00–18:30 System Design:**
  - [ ] Alex Xu Vol 1 Ch 6 (Key-Value Store) — part 1 (data partitioning, replication)
- **18:30–19:15 Behavioral:**
  - [ ] refine "failure" + draft "technical debate" story

---

### Day 17 — Fri May 22 (4) `M`

- **9:00–13:00 DSA New (4):**
  - [ ] [Trees] -> Construct Tree from Preorder/Inorder
  - [ ] [Trees] -> Binary Tree Maximum Path Sum `T2`
  - [ ] [Trees] -> Serialize and Deserialize Binary Tree `T2`
  - [ ] [Heap / Priority Queue] -> Kth Largest Element in Stream
- **14:00–17:00 Consolidation:**
  - [ ] D16 hardest re-solve: **_ • today's hardest: _** • didn't click: \_\_\_
- **17:00–18:30 System Design:**
  - [ ] Alex Xu Vol 1 Ch 6 (KV Store) — part 2 (consistency, gossip, anti-entropy)
- **18:30–19:15 Behavioral:**
  - [ ] refine "technical debate"
- **Mock retro:**
  - [ ] what stalled? \_\_\_

---

### Day 18 — Sat May 23 (4)

- **9:00–13:00 DSA New (4):**
  - [ ] [Tries] -> Implement Trie (Prefix Tree)
  - [ ] [Tries] -> Design Add and Search Words
  - [ ] [Tries] -> Word Search II `T2`
  - [ ] [Heap / Priority Queue] -> Last Stone Weight
- **14:00–17:00 Consolidation:**
  - [ ] D17 hardest re-solve: **_ • today's hardest: _** • didn't click: \_\_\_
  - **Pattern coverage rotation (Wk 3) — re-solve canonical from blank file:**
    - [ ] [Binary Search] -> Koko Eating Bananas
    - [ ] [Linked List] -> Reverse Linked List
    - [ ] (optional) Hardest from this week — own choice
- **17:00–18:30 System Design:**
  - [ ] Alex Xu Vol 1 Ch 7 (Unique ID Generator) — Snowflake breakdown
- **18:30–19:15 Behavioral:**
  - [ ] record audio for stories #4–6 (leadership, failure, technical debate)

---

### Day 19 — Sun May 24 — OFF

_Fluent Python_ Ch 7 (first-class functions) or Ch 9 (decorators preview).

---

## Phase 4 — Heap (rest) + Backtracking (Days 20–24, 3/day)

### Day 20 — Mon May 25 (3)

- **9:00–13:00 DSA New (3):**
  - [ ] [Heap / Priority Queue] -> K Closest Points to Origin
  - [ ] [Heap / Priority Queue] -> Kth Largest Element in Array
  - [ ] [Heap / Priority Queue] -> Task Scheduler
- **14:00–17:00 Consolidation:**
  - [ ] D18 hardest re-solve: **_ • today's hardest: _** • didn't click: \_\_\_
- **17:00–18:30 System Design:**
  - [ ] Alex Xu Vol 1 Ch 8 (URL Shortener)
- **18:30–19:15 Behavioral:**
  - [ ] listen back stories #4–6, identify weakest 2

---

### Day 21 — Tue May 26 (3) `M`

- **9:00–13:00 DSA New (3):**
  - [ ] [Heap / Priority Queue] -> Design Twitter
  - [ ] [Heap / Priority Queue] -> Find Median From Data Stream `T2`
  - [ ] [Backtracking] -> Subsets
- **14:00–17:00 Consolidation:**
  - [ ] D20 hardest re-solve: **_ • today's hardest: _** • didn't click: \_\_\_
- **17:00–18:30 System Design:**
  - [ ] Alex Xu Vol 1 Ch 9 (Web Crawler) — politeness, freshness, dedup
- **18:30–19:15 Behavioral:**
  - [ ] re-record weakest 2 from #4–6
- **Mock retro:**
  - [ ] what stalled? \_\_\_

---

### Day 22 — Wed May 27 (3)

- **9:00–13:00 DSA New (3):**
  - [ ] [Backtracking] -> Combination Sum
  - [ ] [Backtracking] -> Combination Sum II
  - [ ] [Backtracking] -> Permutations
- **14:00–17:00 Consolidation:**
  - [ ] D21 hardest re-solve: **_ • today's hardest: _** • didn't click: \_\_\_
- **17:00–18:30 System Design:**
  - [ ] DDIA Ch 5 part 1 (Replication: single-leader, sync vs async)
- **18:30–19:15 Behavioral:**
  - [ ] draft "mentorship" story (coached / leveled-up someone)

---

### Day 23 — Thu May 28 (3)

- **9:00–13:00 DSA New (3):**
  - [ ] [Backtracking] -> Subsets II
  - [ ] [Backtracking] -> Generate Parentheses
  - [ ] [Backtracking] -> Word Search
- **14:00–17:00 Consolidation:**
  - [ ] D22 hardest re-solve: **_ • today's hardest: _** • didn't click: \_\_\_
- **17:00–18:30 System Design:**
  - [ ] DDIA Ch 5 part 2 (multi-leader, leaderless, conflict resolution)
- **18:30–19:15 Behavioral:**
  - [ ] draft "cross-functional collab" story

---

### Day 24 — Fri May 29 (3) `M`

- **9:00–13:00 DSA New (3):**
  - [ ] [Backtracking] -> Palindrome Partitioning
  - [ ] [Backtracking] -> Letter Combinations of Phone Number
  - [ ] [Backtracking] -> N-Queens `T2`
- **14:00–17:00 Consolidation:**
  - [ ] D23 hardest re-solve: **_ • today's hardest: _** • didn't click: \_\_\_
- **17:00–18:30 System Design:**
  - [ ] DDIA Ch 6 part 1 (Partitioning by key range vs hash)
- **18:30–19:15 Behavioral:**
  - [ ] refine "mentorship" + "cross-functional" stories
- **Mock retro:**
  - [ ] what stalled? \_\_\_

---

## Phase 5 — Graphs + Adv Graphs + Climbing Stairs (Days 25–30, 4/day · aggressive)

### Day 25 — Sat May 30 (4)

- **9:00–13:00 DSA New (4):**
  - [ ] [Graphs] -> Number of Islands
  - [ ] [Graphs] -> Max Area of Island
  - [ ] [Graphs] -> Clone Graph
  - [ ] [Graphs] -> Walls and Gates
- **14:00–17:00 Consolidation:**
  - [ ] D24 hardest re-solve: **_ • today's hardest: _** • didn't click: \_\_\_
  - **Pattern coverage rotation (Wk 4) — re-solve canonical from blank file:**
    - [ ] [Trees] -> Maximum Depth of Binary Tree
    - [ ] [Tries] -> Implement Trie (Prefix Tree)
    - [ ] (optional) Hardest from this week — own choice
  - **+21d batch (from Wk 1, D1–D4):** re-solve 1–2 already-known patterns at long delay
    - [ ] +21d: [Arrays & Hashing] re-solve a Wk-1 problem on a 25-min clock
    - [ ] +21d: [Sliding Window] re-solve a Wk-1 problem on a 25-min clock
- **17:00–18:30 System Design:**
  - [ ] DDIA Ch 6 part 2 (Rebalancing, request routing)
- **18:30–19:15 Behavioral:**
  - [ ] record audio for #7 mentorship + #8 cross-functional

---

### Day 26 — Sun May 31 — OFF

_Fluent Python_ Ch 9 (decorators).

---

### Day 27 — Mon Jun 1 (4)

- **9:00–13:00 DSA New (4):**
  - [ ] [Graphs] -> Rotting Oranges
  - [ ] [Graphs] -> Pacific Atlantic Water Flow
  - [ ] [Graphs] -> Surrounded Regions
  - [ ] [Graphs] -> Course Schedule
- **14:00–17:00 Consolidation:**
  - [ ] D25 hardest re-solve: **_ • today's hardest: _** • didn't click: \_\_\_
- **17:00–18:30 System Design:**
  - [ ] Alex Xu Vol 1 Ch 10 (Notification System) — fanout patterns
- **18:30–19:15 Behavioral:**
  - [ ] draft "customer/user impact" story

---

### Day 28 — Tue Jun 2 (4) `M`

- **9:00–13:00 DSA New (4):**
  - [ ] [Graphs] -> Course Schedule II
  - [ ] [Graphs] -> Graph Valid Tree
  - [ ] [Graphs] -> Number of Connected Components
  - [ ] [Graphs] -> Redundant Connection
- **14:00–17:00 Consolidation:**
  - [ ] D27 hardest re-solve: **_ • today's hardest: _** • didn't click: \_\_\_
- **17:00–18:30 System Design:**
  - [ ] Alex Xu Vol 1 Ch 11 (News Feed) — pull vs push vs hybrid
- **18:30–19:15 Behavioral:**
  - [ ] draft "strategic thinking" story (proposed direction)
- **Mock retro:**
  - [ ] what stalled? \_\_\_

---

### Day 29 — Wed Jun 3 (4)

- **9:00–13:00 DSA New (4):**
  - [ ] [Graphs] -> Word Ladder `T2`
  - [ ] [Advanced Graphs] -> Network Delay Time
  - [ ] [Advanced Graphs] -> Reconstruct Itinerary
  - [ ] [Advanced Graphs] -> Min Cost to Connect All Points
- **14:00–17:00 Consolidation:**
  - [ ] D28 hardest re-solve: **_ • today's hardest: _** • didn't click: \_\_\_
- **17:00–18:30 System Design:**
  - [ ] Alex Xu Vol 1 Ch 12 (Chat System) — online presence, message storage
- **18:30–19:15 Behavioral:**
  - [ ] refine "customer impact" + "strategic" + record both

---

### Day 30 — Thu Jun 4 (4)

- **9:00–13:00 DSA New (4):**
  - [ ] [Advanced Graphs] -> Swim in Rising Water `T2`
  - [ ] [Advanced Graphs] -> Alien Dictionary
  - [ ] [Advanced Graphs] -> Cheapest Flights Within K Stops `T2`
  - [ ] [1-D DP] -> Climbing Stairs
- **14:00–17:00 Consolidation:**
  - [ ] D29 hardest re-solve: **_ • today's hardest: _** • didn't click: \_\_\_
- **17:00–18:30 System Design:**
  - [ ] DDIA Ch 7 part 1 (Transactions: ACID, weak isolation)
- **18:30–19:15 Behavioral:**
  - [ ] listen back all 10 stories — identify any junk stories to retire

---

## Phase 6 — DP (Days 31–38, 3/day)

### Day 31 — Fri Jun 5 (3) `M`

- **9:00–13:00 DSA New (3):**
  - [ ] [1-D DP] -> Min Cost Climbing Stairs
  - [ ] [1-D DP] -> House Robber
  - [ ] [1-D DP] -> House Robber II
- **14:00–17:00 Consolidation:**
  - [ ] D30 hardest re-solve: **_ • today's hardest: _** • didn't click: \_\_\_
- **17:00–18:30 System Design:**
  - [ ] DDIA Ch 7 part 2 (Snapshot isolation, serializability, SSI)
- **18:30–19:15 Behavioral:**
  - [ ] top 5 stories → 90-sec elevator versions
- **Mock retro:**
  - [ ] what stalled? \_\_\_

---

### Day 32 — Sat Jun 6 (3)

- **9:00–13:00 DSA New (3):**
  - [ ] [1-D DP] -> Longest Palindromic Substring
  - [ ] [1-D DP] -> Palindromic Substrings
  - [ ] [1-D DP] -> Decode Ways
- **14:00–17:00 Consolidation:**
  - [ ] D31 hardest re-solve: **_ • today's hardest: _** • didn't click: \_\_\_
  - **Pattern coverage rotation (Wk 5) — re-solve canonical from blank file:**
    - [ ] [Heap] -> Kth Largest Element in a Stream
    - [ ] [Backtracking] -> Subsets
    - [ ] (optional) Hardest from this week — own choice
  - **+21d batch (from Wk 2, D6–D11):** re-solve 1–2 already-known patterns at long delay
    - [ ] +21d: [Two Pointers] re-solve a Wk-2 problem on a 25-min clock
    - [ ] +21d: [Stack] re-solve a Wk-2 problem on a 25-min clock
- **17:00–18:30 System Design:**
  - [ ] Alex Xu Vol 1 Ch 13 (Search Autocomplete) — trie + ranking
- **18:30–19:15 Behavioral:**
  - [ ] top 5 → 3-min versions

---

### Day 33 — Sun Jun 7 — OFF

_Fluent Python_ Ch 17 (generators/coroutines).

---

### Day 34 — Mon Jun 8 (3)

- **9:00–13:00 DSA New (3):**
  - [ ] [1-D DP] -> Coin Change
  - [ ] [1-D DP] -> Maximum Product Subarray
  - [ ] [1-D DP] -> Word Break
- **14:00–17:00 Consolidation:**
  - [ ] D32 hardest re-solve: **_ • today's hardest: _** • didn't click: \_\_\_
- **17:00–18:30 System Design:**
  - [ ] Alex Xu Vol 1 Ch 14 (YouTube) — video upload, transcoding, CDN
- **18:30–19:15 Behavioral:**
  - [ ] mock behavioral round (5 stories back-to-back, simulate fatigue)

---

### Day 35 — Tue Jun 9 (3) `M`

- **9:00–13:00 DSA New (3):**
  - [ ] [1-D DP] -> Longest Increasing Subsequence
  - [ ] [1-D DP] -> Partition Equal Subset Sum
  - [ ] [2-D DP] -> Unique Paths
- **14:00–17:00 Consolidation:**
  - [ ] D34 hardest re-solve: **_ • today's hardest: _** • didn't click: \_\_\_
- **17:00–18:30 System Design:**
  - [ ] Alex Xu Vol 1 Ch 15 (Google Drive) — block-level dedup, sync conflicts
- **18:30–19:15 Behavioral:**
  - [ ] retro on yesterday's mock — re-script weak transitions
- **Mock retro:**
  - [ ] what stalled? \_\_\_

---

### Day 36 — Wed Jun 10 (3)

- **9:00–13:00 DSA New (3):**
  - [ ] [2-D DP] -> Longest Common Subsequence
  - [ ] [2-D DP] -> Best Time to Buy/Sell with Cooldown
  - [ ] [2-D DP] -> Coin Change II
- **14:00–17:00 Consolidation:**
  - [ ] D35 hardest re-solve: **_ • today's hardest: _** • didn't click: \_\_\_
- **17:00–18:30 System Design:**
  - [ ] Alex Xu Vol 1 Ch 16 (Search Engine summary)
- **18:30–19:15 Behavioral:**
  - [ ] practice "tell me about yourself" 60-sec pitch (5 reps)

---

### Day 37 — Thu Jun 11 (3)

- **9:00–13:00 DSA New (3):**
  - [ ] [2-D DP] -> Target Sum
  - [ ] [2-D DP] -> Interleaving String `T2`
  - [ ] [2-D DP] -> Longest Increasing Path in Matrix `T2`
- **14:00–17:00 Consolidation:**
  - [ ] D36 hardest re-solve: **_ • today's hardest: _** • didn't click: \_\_\_
- **17:00–18:30 System Design:**
  - [ ] DDIA Ch 8 part 1 (Trouble: faults, partial failures, lies)
- **18:30–19:15 Behavioral:**
  - [ ] practice "why this company / why now" — 3 target-company variants

---

### Day 38 — Fri Jun 12 (3) `M`

- **9:00–13:00 DSA New (3):**
  - [ ] [2-D DP] -> Distinct Subsequences `T2`
  - [ ] [2-D DP] -> Edit Distance
  - [ ] [2-D DP] -> Burst Balloons `T2`
- **14:00–17:00 Consolidation:**
  - [ ] D37 hardest re-solve: **_ • today's hardest: _** • didn't click: \_\_\_
- **17:00–18:30 System Design:**
  - [ ] DDIA Ch 8 part 2 (Knowledge, truth, lies of distributed systems)
- **18:30–19:15 Behavioral:**
  - [ ] prepare 5 "questions for me" (specific to top 3 target companies)
- **Mock retro:**
  - [ ] what stalled? \_\_\_

---

## Phase 7 — Last 2D DP + Greedy + Intervals + Math + Bit (Days 39–50, 3/day)

### Day 39 — Sat Jun 13 (3)

- **9:00–13:00 DSA New (3):**
  - [ ] [2-D DP] -> Regular Expression Matching `T2`
  - [ ] [Greedy] -> Maximum Subarray
  - [ ] [Greedy] -> Jump Game
- **14:00–17:00 Consolidation:**
  - [ ] D38 hardest re-solve: **_ • today's hardest: _** • didn't click: \_\_\_
  - **Pattern coverage rotation (Wk 6) — re-solve canonical from blank file:**
    - [ ] [Graphs] -> Number of Islands
    - [ ] [Advanced Graphs] -> Network Delay Time
    - [ ] (optional) Hardest from this week — own choice
  - **+21d batch (from Wk 3, D13–D18):** re-solve 1–2 already-known patterns at long delay
    - [ ] +21d: [Binary Search] re-solve a Wk-3 problem on a 25-min clock
    - [ ] +21d: [Linked List] re-solve a Wk-3 problem on a 25-min clock
- **17:00–18:30 System Design:**
  - [ ] Alex Xu Vol 2 Ch 1 (Proximity Service) — geohash, quadtree
- **18:30–19:15 Behavioral:**
  - [ ] all 10 stories → 90-sec versions, timed

---

### Day 40 — Sun Jun 14 — OFF

_Fluent Python_ Ch 19 (concurrency overview).

---

### Day 41 — Mon Jun 15 (3)

- **9:00–13:00 DSA New (3):**
  - [ ] [Greedy] -> Jump Game II
  - [ ] [Greedy] -> Gas Station
  - [ ] [Greedy] -> Hand of Straights
- **14:00–17:00 Consolidation:**
  - [ ] D39 hardest re-solve: **_ • today's hardest: _** • didn't click: \_\_\_
- **17:00–18:30 System Design:**
  - [ ] Alex Xu Vol 2 Ch 2 (Nearby Friends) — pub-sub, location updates
- **18:30–19:15 Behavioral:**
  - [ ] all 10 → 3-min versions, timed

---

### Day 42 — Tue Jun 16 (3) `M`

- **9:00–13:00 DSA New (3):**
  - [ ] [Greedy] -> Merge Triplets to Form Target
  - [ ] [Greedy] -> Partition Labels
  - [ ] [Greedy] -> Valid Parenthesis String
- **14:00–17:00 Consolidation:**
  - [ ] D41 hardest re-solve: **_ • today's hardest: _** • didn't click: \_\_\_
- **17:00–18:30 System Design:**
  - [ ] Alex Xu Vol 2 Ch 3 (Google Maps) — routing, ETA, road network graph
- **18:30–19:15 Behavioral:**
  - [ ] map stories → Big Tech leadership principles (Amazon LP, etc.)
- **Mock retro:**
  - [ ] what stalled? \_\_\_

---

### Day 43 — Wed Jun 17 (3)

- **9:00–13:00 DSA New (3):**
  - [ ] [Intervals] -> Insert Interval
  - [ ] [Intervals] -> Merge Intervals
  - [ ] [Intervals] -> Non-overlapping Intervals
- **14:00–17:00 Consolidation:**
  - [ ] D42 hardest re-solve: **_ • today's hardest: _** • didn't click: \_\_\_
- **17:00–18:30 System Design:**
  - [ ] Alex Xu Vol 2 Ch 4 (Distributed Message Queue) — Kafka-style design
- **18:30–19:15 Behavioral:**
  - [ ] map stories → startup Senior values (ownership, scope, ambiguity)

---

### Day 44 — Thu Jun 18 (3)

- **9:00–13:00 DSA New (3):**
  - [ ] [Intervals] -> Meeting Rooms
  - [ ] [Intervals] -> Meeting Rooms II
  - [ ] [Intervals] -> Minimum Interval to Include Each Query `T2`
- **14:00–17:00 Consolidation:**
  - [ ] D43 hardest re-solve: **_ • today's hardest: _** • didn't click: \_\_\_
- **17:00–18:30 System Design:**
  - [ ] Alex Xu Vol 2 Ch 5 (Metrics Monitoring) — time-series DB
- **18:30–19:15 Behavioral:**
  - [ ] practice transitions between stories (interviewer follow-up probes)

---

### Day 45 — Fri Jun 19 (3) `M`

- **9:00–13:00 DSA New (3):**
  - [ ] [Math & Geometry] -> Rotate Image
  - [ ] [Math & Geometry] -> Spiral Matrix
  - [ ] [Math & Geometry] -> Set Matrix Zeroes
- **14:00–17:00 Consolidation:**
  - [ ] D44 hardest re-solve: **_ • today's hardest: _** • didn't click: \_\_\_
- **17:00–18:30 System Design:**
  - [ ] Alex Xu Vol 2 Ch 6 (Ad Click Aggregation) — exactly-once, idempotency
- **18:30–19:15 Behavioral:**
  - [ ] practice handling interruptions / "tell me more about X"
- **Mock retro:**
  - [ ] what stalled? \_\_\_

---

### Day 46 — Sat Jun 20 (3)

- **9:00–13:00 DSA New (3):**
  - [ ] [Math & Geometry] -> Happy Number
  - [ ] [Math & Geometry] -> Plus One
  - [ ] [Math & Geometry] -> Pow(x, n)
- **14:00–17:00 Consolidation:**
  - [ ] D45 hardest re-solve: **_ • today's hardest: _** • didn't click: \_\_\_
  - **Pattern coverage rotation (Wk 7) — re-solve canonical from blank file:**
    - [ ] [1-D DP] -> House Robber
    - [ ] [2-D DP] -> Unique Paths
    - [ ] [Greedy] -> Maximum Subarray (Kadane's)
  - **+21d batch (from Wk 4, D20–D25):** re-solve 1–2 already-known patterns at long delay
    - [ ] +21d: [Trees] re-solve a Wk-4 problem on a 25-min clock
    - [ ] +21d: [Tries] re-solve a Wk-4 problem on a 25-min clock
- **17:00–18:30 System Design:**
  - [ ] Alex Xu Vol 2 Ch 7 (Hotel Reservation) — locking, double-booking prevention
- **18:30–19:15 Behavioral:**
  - [ ] mock behavioral with friend or self-video

---

### Day 47 — Sun Jun 21 — OFF

_Fluent Python_ — re-read weakest chapter from the sprint.

---

### Day 48 — Mon Jun 22 (3)

- **9:00–13:00 DSA New (3):**
  - [ ] [Math & Geometry] -> Multiply Strings `T2`
  - [ ] [Math & Geometry] -> Detect Squares `T2`
  - [ ] [Bit Manipulation] -> Single Number
- **14:00–17:00 Consolidation:**
  - [ ] D46 hardest re-solve: **_ • today's hardest: _** • didn't click: \_\_\_
- **17:00–18:30 System Design:**
  - [ ] DDIA Ch 9 part 1 (Linearizability, total order broadcast)
- **18:30–19:15 Behavioral:**
  - [ ] final dress rehearsal — full 45-min behavioral round (record)

---

### Day 49 — Tue Jun 23 (3) `M`

- **9:00–13:00 DSA New (3):**
  - [ ] [Bit Manipulation] -> Number of 1 Bits
  - [ ] [Bit Manipulation] -> Counting Bits
  - [ ] [Bit Manipulation] -> Reverse Bits
- **14:00–17:00 Consolidation:**
  - [ ] D48 hardest re-solve: **_ • today's hardest: _** • didn't click: \_\_\_
- **17:00–18:30 System Design:**
  - [ ] DDIA Ch 9 part 2 (Quorum, consensus, Raft/Paxos sketch)
- **18:30–19:15 Behavioral:**
  - [ ] final dress rehearsal — combined behavioral + system design
- **Mock retro (final dress):**
  - [ ] what stalled? \_\_\_

---

### Day 50 — Wed Jun 24 (3) — NC150 ACQUISITION COMPLETE (mid-sprint checkpoint)

- **9:00–13:00 DSA New (3):**
  - [ ] [Bit Manipulation] -> Missing Number
  - [ ] [Bit Manipulation] -> Sum of Two Integers
  - [ ] [Bit Manipulation] -> Reverse Integer `T2`
- **14:00–17:00 Consolidation:**
  - [ ] D49 hardest re-solve: **_ • today's hardest: _** • didn't click: \_\_\_
- **17:00–18:30 System Design:**
  - [ ] Final review — re-read weakest chapter + Anki cards on shaky concepts
- **18:30–19:15 Behavioral:**
  - [ ] light review + early sleep

**50-Day Mid-Sprint Checkpoint** (sprint continues to D90):

- Total NC150 problems completed: \_\_\_ / 150
- T2 problems dropped: \_\_\_
- Strongest pattern category (so far): \_\_\_
- Weakest pattern category (target P8 re-solves): \_\_\_
- Mocks at "would hire": \_\_\_ / 13
- Behavioral stories drafted: \_\_\_ / 10
- DDIA chapters covered: \_\_\_ / 5 (Ch 5–9)
- Alex Xu Vol 1 chapters: \_\_\_ / 16
- Pattern notes with non-empty Mistakes section: \_\_\_ / 18 (NC150 patterns only — net-new start P8)
- **Plan adjustments for P8–P10 based on this checkpoint:** \_\_\_

---

## Phase Totals (auto-tally)

- [ ] P1 — 20/20 (Days 1–6)
- [ ] P2 — 24/24 (Days 7–13)
- [ ] P3 — 20/20 (Days 14–18)
- [ ] P4 — 15/15 (Days 20–24)
- [ ] P5 — 20/20 (Days 25–30)
- [ ] P6 — 21/21 (Days 31–38)
- [ ] P7 — 30/30 (Days 39–50)
- [ ] P8 — 13/13 net-new (Days 51–65)
- [ ] P9 — re-solves + 8 mocks (Days 66–78)
- [ ] P10 — daily mocks + final review (Days 79–90)

---

# 90-Day Extension — Phases 8 / 9 / 10

The first 50 days finish NC150. Days 51–90 are **consolidation** — depth, mocks, system design. The day-by-day for these phases is intentionally NOT pre-filled — the right content depends on which patterns turn out to be your weakest by D50. Expand to per-day during the **D50 mid-sprint checkpoint**.

Saturdays in the 90-day window: D4, D11, D18, D25, D32, D39, D46 (acquisition) + **D53, D60, D67, D74, D81, D88** (consolidation) = 13 total.

---

## Phase 8 — Pattern Mastery + 7 Net-New Patterns (Days 51–65, 13 wd)

**Goal:** Introduce all 7 net-new patterns (13 problems total) AND start using the consolidation block exclusively for re-solving from your accumulated weakness list.

**Daily shape (Mon–Fri):**

- **9:00–13:00** DSA New: ~1 net-new problem/day (some days 2 if you fly through)
- **13:00–14:00** Lunch + walk
- **14:00–16:00 Interview / Mock slot**: real screen, paid mock, or peer Pramp when scheduled. Lunch is done, brain is rested, anxiety window is short. When empty: 2 weakness re-solves from `patterns/*/Mistakes`. Default availability for recruiters.
- **16:00–17:00 Consolidation (anchored)**: 1 weakness re-solve OR cross-pattern mistake-mining — runs even on interview days so consolidation never fully drops out.
- **17:00–18:30** System Design: DDIA Ch 7 + Alex Xu Vol 2 chapters
- **18:30–19:15** Behavioral: refine 2 weakest stories

**Net-new problem schedule across P8 (13 wd, 13 problems):**

| Day range | Pattern                | Canonical                           | Variant                             |
| --------- | ---------------------- | ----------------------------------- | ----------------------------------- |
| D51–D52   | Segment Tree / Fenwick | Range Sum Query - Mutable           | Count of Smaller Numbers After Self |
| D53–D54   | Bitmask DP             | Shortest Path Visiting All Nodes    | Partition to K Equal Sum Subsets    |
| D55       | Bit-Trie               | Maximum XOR of Two Numbers in Array | (canonical only)                    |
| D56–D57   | Sweep Line             | My Calendar III                     | The Skyline Problem                 |
| D58–D59   | Reservoir Sampling     | Linked List Random Node             | Random Pick with Weight             |
| D60–D61   | Boyer-Moore Voting     | Majority Element                    | Majority Element II                 |
| D62–D63   | Difference Array       | Corporate Flight Bookings           | Car Pooling                         |
| D64–D65   | Buffer                 | weakness re-solves                  | weakness re-solves                  |

### Saturdays in P8

#### Day 53 — Sat Jun 27 (1 net-new)

- **9:00–13:00 DSA New (1):**
  - [ ] [Bitmask DP] -> Shortest Path Visiting All Nodes (canonical)
- **13:00–14:00** Lunch + walk
- **14:00–16:00 Interview slot OR Pattern coverage rotation (Wk 8):** Saturday interviews rare, so defaults to rotation. If a screen lands here, push rotation to 16:00–18:00 and shift SD/behavioral later.
  - **Pattern coverage rotation — re-solve canonical from blank file (catching up missed P7 patterns):**
    - [ ] [Intervals] -> Merge Intervals
    - [ ] [Math & Geometry] -> Spiral Matrix
    - [ ] [Bit Manipulation] -> Single Number
- **16:00–17:00 Consolidation (anchored):**
  - [ ] D52 hardest re-solve: **_ • today's hardest: _** • didn't click: \_\_\_
- **17:00–18:30 System Design:** Alex Xu Vol 2 Ch 1 (Proximity Service) — start
- **18:30–19:15 Behavioral:** stories not yet polished — record + listen-back

#### Day 60 — Sat Jul 4 (1 net-new) — independence day, lower intensity OK

- **9:00–13:00 DSA New (1):**
  - [ ] [Boyer-Moore] -> Majority Element (canonical)
- **13:00–14:00** Lunch + walk
- **14:00–16:00 Interview slot OR Pattern coverage rotation (Wk 9):** Saturday default is rotation. If interview scheduled, push rotation to 16:00–18:00.
  - **Pattern coverage rotation — re-solve canonical from blank file:**
    - [ ] [Segment Tree] -> Range Sum Query - Mutable
    - [ ] [Bitmask DP] -> Shortest Path Visiting All Nodes
    - [ ] [Bit-Trie] -> Maximum XOR of Two Numbers in Array
- **16:00–17:00 Consolidation (anchored):**
  - [ ] D59 hardest re-solve: **_ • today's hardest: _** • didn't click: \_\_\_
- **17:00–18:30 System Design:** Alex Xu Vol 2 Ch 2 (Nearby Friends)
- **18:30–19:15 Behavioral:** mock-style story drill (45-second versions)

#### Day 67 — Sat Jul 11 (P9 starts D66)

- **9:00–13:00 DSA Re-solve (1 on the clock, 30 min):**
  - [ ] Pick from weakness list — solve narrating out loud as if in interview
- **13:00–14:00** Lunch + walk
- **14:00–16:00 Interview slot OR Pattern coverage rotation (Wk 10):** Saturday default is rotation. If interview scheduled, push rotation to 16:00–18:00.
  - **Pattern coverage rotation — re-solve canonical from blank file:**
    - [ ] [Sweep Line] -> My Calendar III
    - [ ] [Reservoir Sampling] -> Linked List Random Node
    - [ ] [Boyer-Moore] -> Majority Element
- **16:00–17:00 Consolidation (anchored):**
  - [ ] D66 mock retro: what stalled — communication / pattern recognition / syntax / complexity?
- **17:00–18:30 System Design:** Alex Xu Vol 2 Ch 3
- **18:30–19:15 Behavioral:** mock-style with timed delivery

#### Day 74 — Sat Jul 18

- **9:00–13:00 DSA Re-solve (1 on the clock):**
  - [ ] Pick from weakness list
- **13:00–14:00** Lunch + walk
- **14:00–16:00 Interview slot OR Pattern coverage rotation (Wk 11):** Saturday default is rotation. If interview scheduled, push rotation to 16:00–18:00.
  - **Pattern coverage rotation — re-solve canonical, hot patterns 2nd hit:**
    - [ ] [Difference Array] -> Corporate Flight Bookings
    - [ ] [Trees] -> Maximum Depth (2nd rotation)
    - [ ] [Graphs] -> Number of Islands (2nd rotation)
- **16:00–17:00 Consolidation (anchored):**
  - [ ] D73 mock retro: what stalled?
- **17:00–18:30 System Design:** Alex Xu Vol 2 Ch 4
- **18:30–19:15 Behavioral:** record top story, listen back, refine

#### Day 81 — Sat Jul 25 (P10 mid)

- **9:00–13:00 DSA Re-solve (1 on the clock):**
  - [ ] Pick from accumulated weakness list
- **13:00–14:00** Lunch + walk
- **14:00–16:00 Interview slot OR Pattern coverage rotation (Wk 12):** Saturday default is rotation. If interview scheduled, push rotation to 16:00–18:00.
  - **Pattern coverage rotation — re-solve canonical, hot patterns 2nd hit:**
    - [ ] [1-D DP] -> House Robber (2nd rotation)
    - [ ] [2-D DP] -> Unique Paths (2nd rotation)
    - [ ] [Arrays & Hashing] -> Two Sum (2nd rotation)
- **16:00–17:00 Consolidation (anchored):**
  - [ ] D80 mock retro
- **17:00–18:30 System Design:** Alex Xu Vol 2 Ch 5
- **18:30–19:15 Behavioral:** "Why are you leaving?" / "Why this company?" — these are top of funnel

#### Day 88 — Sat Aug 1 (P10 final stretch)

- **9:00–13:00 DSA Re-solve (1 on the clock):**
  - [ ] Pick weakest pattern from rotation history
- **13:00–14:00** Lunch + walk
- **14:00–16:00 Interview slot OR Pattern coverage rotation (Wk 13, final):** Saturday default is rotation. If interview scheduled, push rotation to 16:00–18:00.
  - **Pattern coverage rotation — re-solve canonical, weakest patterns:**
    - [ ] [Sliding Window] -> Longest Substring Without Repeating Chars (2nd rotation)
    - [ ] [Backtracking] -> Subsets (2nd rotation)
    - [ ] (open) own choice from accumulated mistakes
- **16:00–17:00 Consolidation (anchored):**
  - [ ] D87 mock retro
- **17:00–18:30 System Design:** Alex Xu Vol 2 Ch 6
- **18:30–19:15 Behavioral:** full-loop simulation — present 5 stories back-to-back

### P8 — Sundays (D54, 61) OFF

Light Fluent Python or DDIA reading allowed.

---

## Phase 9 — Mock-Heavy + System Design Deep Dive (Days 66–78, 11 wd)

**Goal:** ramp mocks to every-other-day. Most days = no new problems, just one re-solve on the clock + heavy SD work.

**Daily shape (Mon–Fri):**

- **9:00–13:00** Pick 1 problem from weakness list, solve on a 30-min clock narrating out loud (interview simulation), then 3 hrs Pythonic refactor + writeup
- **13:00–14:00** Lunch + walk
- **14:00–16:00 Interview / Mock slot**: real screens, paid mocks, scheduled P9 mocks (Tue D67, Thu D69, Tue D74, Thu D76 land here). When empty: SD Alex Xu writeup.
- **16:00–17:00 SD anchor**: DDIA Ch 8-9 reading or SD writeup continuation — runs every day.
- **17:00–18:30** Behavioral: refine + record + listen-back
- **18:30–19:15** review the day's takeaways into Anki

**Mocks in P9:** Tue D67, Thu D69, Tue D74, Thu D76 — 4 in this phase.

**Mock retro template** (after each mock):

- What stalled? (communication / pattern recognition / syntax / complexity reasoning)
- Specific words I fumbled
- Pattern misidentified? (write to `patterns/*/Mistakes`)
- 1-2 Anki cards from the lesson

---

## Phase 10 — Interview Mode (Days 79–90, 10 wd)

**Goal:** simulate the real loop. Daily mocks the last week.

**Daily shape:**

- **9:00–10:30** DSA mock (Pramp / Interviewing.io / friend) — 1 problem timed
- **10:30–12:00** Mock retro + targeted Anki cards
- **12:00–14:00** Lunch + walk
- **14:00–16:00 Interview / Mock slot**: real screens, paid mocks, scheduled P10 mocks (Tue D79, Thu D81, Tue D86, Thu D88 land here). When empty: SD mock (whiteboard-style writeup of a fresh Alex Xu Vol 2 problem on the clock).
- **16:00–17:30** Mock retro (whichever ran in the slot)
- **17:30–19:15** Behavioral run-through (5 stories back-to-back, 60-sec each)

**Mocks in P10:** Tue D79, Thu D81, Tue D86, Thu D88 — at minimum 4 paid mocks. Add daily friend-mocks D85-D89 if possible.

**Last 3 days (D88–90):**

- D88 (Sat): final pattern coverage rotation slot (above)
- D89 (Sun) OFF
- D90 (Mon, sprint end): light review only — re-read top 3 weakest pattern notes, re-read 3 strongest behavioral stories. **NO new problems on the final day** — fatigue accumulates, fresh state for actual interviews matters.

---

## 90-Day Sprint Retrospective — Day 90 (Mon Aug 5)

- Total NC150 problems completed: \_\_\_ / 150
- Net-new problems completed: \_\_\_ / 13
- T2 problems dropped: \_\_\_
- Strongest pattern category: \_\_\_
- Weakest pattern category (target ongoing review): \_\_\_
- Mocks at "would hire" level: \_\_\_ / ~24
- Behavioral stories polished (60-sec ready): \_\_\_ / 10
- DDIA chapters covered: \_\_\_ / 5 (Ch 5–9)
- Alex Xu chapters: Vol 1 \_\_\_ / 16, Vol 2 \_\_\_ / 7
- Pattern notes with non-empty Mistakes section (i.e., real lessons captured): \_\_\_ / 25
- Anki deck retention rate: \_\_\_ %
- Self-assessment of interview readiness (1–10): \_\_\_
