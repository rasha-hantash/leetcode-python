# NC450 Coverage Gap Analysis

**Question:** Within the 182 problems in `curriculum.md`, can you handle any problem in NeetCode's broader 450-problem dataset? Where are the **atomic technique gaps** that wouldn't transfer from existing problems?

**Method:** Cross-referenced curriculum.md against `neetcode-gh/leetcode/.problemSiteData.json` (450 problems). Of those 450, your curriculum covers 156 in NeetCode's namespace (the other 26 of your 182 are company questions outside the NeetCode dataset). Walked the 294 uncovered problems by pattern and identified atomic techniques NOT derivable from your covered set. Filter: **a gap only counts if the technique is genuinely distinct, not a variation or composition of techniques you already drill.**

Excluded from analysis: 30 JavaScript-pattern problems (Promise/closure problems for JS interview prep — not relevant to your Python track).

---

## Genuine gaps (sorted by leverage)

### 1. Game-theory / minimax DP

**Why it's a gap:** All your DP coverage is single-agent optimization (House Robber, Coin Change, LCS, Climbing Stairs, etc.). Adversarial DP requires a distinct mental model — both players play optimally and you reason about the _difference_ between scores, not maximization in isolation. The recurrence shape is `dp[i][j] = max(score - dp[next state])`. Not derivable from optimization-DP alone.

**Closes problems:** Stone Game (M), Stone Game II (M), Stone Game III (H). Also unlocks Predict the Winner (M) and similar combinatorial-game classics outside NC450.

**Leverage:** ~3 NC450 problems + ~5 commonly-asked LC mediums.

**Recall load:** 3 problems × 5 SM-2 touches = 15 future morning-recall events (~50 min total spread over the rest of the sprint).

---

### 2. Prefix sum + hashmap (subarray problems)

**Why it's a gap:** Your Two Sum / 3Sum coverage handles "find pair/triplet summing to X." Subarray problems (`sum equals K`, `sum divisible by K`, `pivot index`, `2D range sum`) require the cumulative-sum + hashmap-of-prefixes trick, which has a different "aha" — it's not a pair-search, it's a difference-search. NC150 doesn't include a single canonical "subarray sum equals K" problem.

**Closes problems:** Subarray Sum Equals K (M), Continuous Subarray Sum (M), Range Sum Query 2D Immutable (M), Find Pivot Index (E). Also a workhorse for many off-list LC problems — `subarray sum divisible by K`, `binary subarrays with sum`, etc.

**Leverage:** ~5 NC450 problems + ~10 commonly-asked LC variations.

**Recall load:** 4 problems × 5 touches = 20 events (~60 min).

**Editorial note:** The 2D variant (Range Sum Query 2D Immutable) extends the technique non-trivially — closes a separate sub-pattern.

---

### 3. Cyclic sort / index-as-hash (in-place with O(1) space)

**Why it's a gap:** A specific trick — when problem says "array of size n contains values in `[1, n]`," you can use indices as a hash for O(1) extra space. The recurrence is "swap value to its target index until array fixed." Not derivable from the hashmap-based approaches you've drilled (which use O(n) space). NC150 doesn't include this trick.

**Closes problems:** First Missing Positive (H), Find All Numbers Disappeared In an Array (E), Find the Duplicate Number (M, NC150 — covered) ← covered but solved differently. Adding First Missing Positive cements the cyclic-sort approach.

**Leverage:** ~2 NC450 problems but **First Missing Positive is a popular interview problem at FAANG-tier shops** (esp. when O(1) space is required).

**Recall load:** 2 problems × 5 touches = 10 events (~30 min).

---

### 4. Tree serialization for subtree fingerprinting

**Why it's a gap:** Encoding a subtree as a canonical string (or tuple) so you can hash & compare subtrees in a hashmap. The encoding scheme (post-order with `null` markers, e.g. `"3,4,1,#,#,2,#,#,#"`) is non-obvious until you've seen it. Distinct from Serialize/Deserialize Binary Tree (NC150 — covered) which is about communication, not comparison-by-content.

**Closes problems:** Find Duplicate Subtrees (M). Also relevant in tree-isomorphism interview questions.

**Leverage:** 1 direct NC450 problem, but the technique transfers to any "find structurally equal subtrees" question.

**Recall load:** 1 problem × 5 touches = 5 events (~15 min).

---

### 5. LFU cache (multi-level DLL with frequency buckets)

**Why it's a gap:** LRU Cache (NC150 — covered) is hash + single doubly-linked list. LFU requires hash + dictionary-of-DLLs (one DLL per frequency level) + minFreq tracker. The data-structure design is non-trivial and not derivable from LRU alone — it's a step up in complexity.

**Closes problems:** LFU Cache (H).

**Leverage:** 1 direct NC450 problem, but LFU is a known interview-question for staff-tier system design / OOP screens.

**Recall load:** 1 problem × 5 touches = 5 events (~15 min). High per-touch cost (LFU is notoriously fiddly).

---

### 6. Iterative DFS with explicit stack (tree traversals without recursion)

**Why it's a gap:** Borderline — composable from "DFS recursion + stack data structure" but has its own muscle memory, and interviewers often explicitly ask "do it without recursion." Your curriculum is fully recursive on trees. Listed lower because it IS deducible, just less fluent if untrained.

**Closes problems:** Binary Tree Inorder Traversal (E), Binary Tree Preorder Traversal (E), Binary Tree Postorder Traversal (E), Binary Search Tree Iterator (M). The BST Iterator is the meaningful one — uses the same "lazy-stack" pattern that recurs in iterator-design questions.

**Leverage:** 4 NC450 problems + occasional "no recursion" interview ask.

**Recall load:** 1–2 problems if you only add BST Iterator (5–10 events). Skipping the easy three is fine if you understand the pattern.

---

## Niche / low-priority (mention for completeness, NOT recommended unless you have time)

### 7. Tarjan's bridges / articulation points

**Why it's listed:** Genuinely distinct algorithm (DFS lowlink). NOT derivable.

**Closes problems:** Find Critical and Pseudo Critical Edges in MST (H).

**Why low-priority:** Almost never asked at Big Tech mid / startup senior level. Niche.

**Skip unless:** you're targeting a competitive-programming-flavored interview (some quant or trading shops).

---

## Summary table

| Gap                  | Problems to add                           | NC450 leverage | Recall cost | Priority   |
| -------------------- | ----------------------------------------- | -------------- | ----------- | ---------- |
| Minimax DP           | Stone Game (M), Stone Game II (M)         | 3 + 5 off-list | ~30–50 min  | **High**   |
| Prefix sum + hashmap | Subarray Sum Equals K (M), 2D Range Sum   | 5 + 10         | ~60 min     | **High**   |
| Cyclic sort          | First Missing Positive (H)                | 2 + interview  | ~15 min     | **High**   |
| Tree serialization   | Find Duplicate Subtrees (M)               | 1 + transfer   | ~15 min     | **Medium** |
| LFU Cache            | LFU Cache (H)                             | 1 + interview  | ~15 min     | **Medium** |
| Iterative tree DFS   | Binary Search Tree Iterator (M)           | 1–4            | ~15–30 min  | **Low**    |
| Tarjan's             | Find Critical / Pseudo-Critical Edges (H) | 1              | ~15 min     | **Skip**   |

**Total recommended additions (High + Medium):** ~7 problems · ~135 min/total recall load over the rest of the sprint (about 9 events/week amortized post-D1).

## Recommended placement

Phase 7 fallback queue (D59–D78) — the existing slot for "Recall fully drained, what next." Add to `curriculum.md`'s Phase 7 — NC150+ Extras section as `(nc-150+)` problems. Don't reach earlier — don't disturb the current acquisition cadence.

## What is NOT a gap (covered explicitly to forestall second-guessing)

Searched and verified — these patterns/techniques are present in your covered set, no gap:

- Union-Find (Number of Connected Components, Graph Valid Tree)
- Topological sort (Course Schedule, Course Schedule II, Alien Dictionary)
- Dijkstra (Network Delay Time, Swim in Rising Water)
- MST (Min Cost to Connect All Points)
- Bellman-Ford (Cheapest Flights Within K Stops)
- Bitmask DP (NC-150+ heavy pattern: Shortest Path Visiting All Nodes)
- Sweep line (NC-150+: Skyline)
- Segment tree (NC-150+: My Calendar III)
- Fenwick tree / BIT (NC-150+: Count of Smaller Numbers After Self)
- Trie (Implement Trie, Word Search II, Design Add and Search Words)
- Two-heap median (Find Median from Data Stream)
- Quickselect (Kth Largest Element in an Array)
- Backtracking with pruning (N-Queens, Word Search, Sudoku Solver)
- Floyd's tortoise & hare (Linked List Cycle, Find the Duplicate Number)

## Caveat

This is a title + pattern + my prior-knowledge analysis, not editorial-deep. If a flagged gap turns out to be solvable via a technique you already have, drop it. If you discover an additional gap during Phase 7 fallback drills, add to this file as a "found in practice" appendix.

---

# Full extras inventory — per-problem justification

The leverage analysis above identifies the **highest-priority** technique gaps. This appendix walks **every extra** in the curriculum (currently 31 problems explicitly tagged `(nc-150+)` or `(lc-only)`, plus a few untagged additions in the Phase 6 "NC150+ Extras" section), grouped by pattern, with a one-paragraph justification for each.

The standard for inclusion: **the problem teaches a technique that NC150 doesn't already cover, OR it's a canonical version of a pattern that NC150 covers obliquely.** Problems that are pure variations of existing NC150 problems aren't included — those would just inflate the curriculum without adding distinct learning.

Each justification answers: (a) what technique does this problem drill, (b) why doesn't NC150 already cover it, (c) does this show up in real interviews.

## Arrays — index-as-hash and in-place tricks

**Find Pivot Index (E)** — Builds the prefix-sum intuition before the harder subarray-sum-equals-K problem. NC150's array section is hashmap-heavy (Two Sum, Group Anagrams, Contains Duplicate); prefix sums are absent. This is the cheap warm-up.

**Find All Numbers Disappeared in an Array (E)** — Easy entry to the cyclic-sort / index-as-hash family. The trick: when values are guaranteed to be in `[1, n]`, you can use indices as a hash for O(1) extra space. NC150 doesn't include any cyclic-sort problem. This problem trains the muscle before First Missing Positive (Hard).

**First Missing Positive (H)** — The canonical cyclic-sort problem. O(1) extra space is the interview constraint that makes the hashmap solution unacceptable. **Asked at FAANG-tier shops.** See gap analysis section 3.

## Prefix sum + hashmap (subarray problems)

**Subarray Sum Equals K (M)** — The canonical "subarray sum equals K" problem. NC150's hashmap-pair coverage (Two Sum, Group Anagrams) doesn't generalize to "find a contiguous range." The technique is prefix-sum + running-difference-hashmap. See gap analysis section 2.

**Continuous Subarray Sum (M)** — Same prefix-sum + hashmap trick, but the key is `prefix_sum % k` instead of `prefix_sum`. Trains the generalization: "what value of the running sum makes the constraint hold?" Common interview ask.

**Range Sum Query 2D Immutable (M)** — Extends prefix sums to 2D. The 2D inclusion-exclusion formula (`P[r2][c2] - P[r1-1][c2] - P[r2][c1-1] + P[r1-1][c1-1]`) is non-obvious and shows up in image-processing and matrix-query interview questions.

## Sliding window — runs of equal characters

**Count Binary Substrings (E)** — Trains a sub-genre of sliding window: counting _groups of consecutive equal characters_ and pairing adjacent groups. NC150's sliding-window problems (Longest Substring Without Repeating, Permutation in String, Minimum Window Substring) are all "expand/shrink based on a set or count." This one expands the mental model to runs.

## Trees — subtree comparison and iterative traversal

**Find Duplicate Subtrees (M)** — Canonical subtree-as-hashable-fingerprint problem. The serialization scheme (post-order with `null` markers) is the technique; once you have it, you can compare subtrees by content in a hashmap. NC150's Serialize/Deserialize Binary Tree is about transmission, not comparison-by-content. See gap analysis section 4.

**Binary Search Tree Iterator (M)** — The "lazy stack" iterator pattern. Same skeleton recurs in many iterator-design interview questions (Peeking Iterator, Zigzag Iterator). NC150 trees are fully recursive; this is the iterative companion. See gap analysis section 6.

## Game-theory DP (minimax / adversarial)

**Stone Game (M)** — Easy entry to minimax DP. Trains the recurrence `dp[i][j] = max(score - dp[next state])` — both players play optimally and you reason about the _difference_ between scores, not absolute maximization. NC150's DP coverage is entirely single-agent. See gap analysis section 1.

**Stone Game II (M)** — Adds a state dimension (how many piles a player can take depends on the opponent's last move). Trains memoization with multi-dimensional state, still in the adversarial framework.

**Stone Game III (H)** — Hard variant; the search space is larger and the optimization opportunities (returning the difference instead of absolute scores) become necessary. Closes the family.

## String parsing & transformation

NC150 includes very few string-parsing problems — most of its string section is sliding-window (Longest Substring Without Repeating) or palindromes (Longest Palindromic Substring). The "messy parser" sub-genre — atoi, decoding, calculators, abbreviations — is a frequent interview category that's almost completely absent. Most use a stack or small state machine, technique-distinct from sliding window.

**Longest Common Prefix (E)** — Canonical "scan all strings character by character" problem. Trivial but trains the "compare columns across strings" mental move.

**Valid Word Abbreviation (E)** — Two-pointer parsing where one pointer counts digits as a skip distance. Tests whether you handle the `"a1b"` → length-3 substring math without off-by-one errors. Easy but commonly bombed.

**Roman to Integer (E)** — Adjacent-pair comparison: subtract instead of add when a smaller numeral precedes a larger one. Trains lookahead in a linear scan.

**Add Binary (E)** — Manual carry-propagation. Often paired with "add two numbers as linked lists" (NC150 — covered) but binary forces you to handle the `1+1=10` carry without library help. Bit-manipulation interview warm-up.

**snake_case → camelCase (E)** _(company question)_ — Real screening question. State machine: track whether the next char should be uppercased. Trains the "single-pass transform with one-bit state" muscle.

**String Compression (M)** — Run-length encoding in place. The challenge is the in-place rewrite without allocating a second array (interviewers will demand it). Trains the two-pointer write-index pattern over strings.

**Decode String (M)** — Stack-based parser for nested patterns like `3[a2[bc]]`. The technique generalizes to _any_ nested-structure parsing problem. NC150 has no canonical "parse nested syntax" problem.

**Basic Calculator II (M)** — Stack-based expression evaluator with operator precedence. The cleaner solution uses a single pass + lazy-multiply pattern. Common interview question, often as a system-design-adjacent ask.

**String to Integer atoi (M)** — The "edge cases" problem. Whitespace, signs, overflow, invalid chars. Tests whether you can enumerate cases without panicking; that _meta-skill_ is what's being graded.

## Difference array (range increments)

**Car Pooling (M)** — Canonical difference-array problem. Instead of incrementing a range `[i, j]` in O(j-i), you mark `+x` at `i` and `-x` at `j+1`, then take prefix sums at the end. O(n) total for any number of range updates. NC150 doesn't include this technique — it shows up constantly in scheduling, booking, and traffic-flow interview questions.

**Corporate Flight Bookings (M)** — Same technique, different framing (bookings instead of pickups/dropoffs). Cements the pattern under a different problem statement so you recognize it cold.

## Boyer-Moore majority voting

**Majority Element (E)** — The O(1)-space majority algorithm: maintain a candidate and count, increment when matching, decrement when not. Simple but the _invariant_ (why does this work?) is what the interviewer wants you to articulate. NC150 doesn't include it.

**Majority Element II (M)** — Same idea, two candidates instead of one. Proves you internalized the invariant rather than memorizing the single-candidate version.

## Bit-trie

**Maximum XOR (M)** — Trie applied to bit representations of numbers. NC150's trie coverage (Implement Trie, Word Search II, Design Add and Search Words) is character-based; this generalizes the structure to any sequence over a small alphabet. Used for "find pair maximizing XOR," "find prefix queries," and several harder graph problems.

## Reservoir sampling

NC150 includes Random Pick with Weight (selection from a weighted distribution), but not the streaming case where you don't know n in advance.

**Linked List Random Node (M)** — Canonical reservoir sampling: as you walk a list of unknown length, replace your sample with probability 1/i at step i. The proof-by-induction (why is this uniform?) is the meat of the interview ask.

**Wordler Random Get/Remove/Has (M)** _(company question)_ — Real screening question. Combines a hashmap (for O(1) has/remove) with an array (for O(1) random pick) and a "swap with last" trick on remove. Trains data-structure composition.

## Segment tree

**Range Sum Query - Mutable (M)** — Explicit segment-tree practice. The immutable version is solvable with prefix sums, but once updates are allowed, prefix sums break (each update is O(n)) and you need a tree. NC150 has no segment-tree problem at the medium level. This is the workhorse problem to lock in the structure.

## Bitmask DP

**Partition to K Equal Sum Subsets (M)** — DP over subsets, where state is "which elements have been used." Trains the bitmask-as-state encoding. NC150 has no bitmask-DP problem.

**Shortest Path Visiting All Nodes (H)** — Bitmask DP applied to graphs (TSP-flavored). State is `(current node, visited set)`. The Hard difficulty comes from combining the bitmask state encoding with BFS, not from algorithmic novelty.

## LFU cache

**LFU Cache (H)** — The data-structure-design Hard. LRU (NC150 — covered) is hash + single DLL; LFU adds frequency tracking via a dictionary of DLLs + minFreq counter. Asked at staff-tier OOP screens. See gap analysis section 5.

## Binary Indexed Tree (Fenwick) / inversion counting

**Count of Smaller Numbers After Self (H)** — Counts inversions in O(n log n). Two valid approaches: BIT (insert values into the tree as you scan right-to-left, query the prefix sum below current value) or merge sort with merge-step counting. Either way, NC150 has neither. Common at competitive-prep-flavored interviews.

## Sweep line / event-based

NC150 has Meeting Rooms II (closest to sweep line) but the multi-event pattern — start/end events with sorting — deserves dedicated practice.

**My Calendar III (H)** — Maintain max concurrent bookings as events arrive. The clean solution uses a sorted map of delta events. Generalizes to any "max concurrent X" question (calls, traffic, allocations).

**Skyline (H)** — Classic sweep-line problem with a heap. Each building contributes a "start" and "end" event; you sweep left-to-right and track the current max height. The discipline of separating events from state is the lesson.

---

## What's deliberately NOT here

A few patterns considered but rejected as duplicates of existing NC150 coverage:

- **Quickselect variations** — Kth Largest is on NC150; additional quickselect problems would just reinforce the same partition technique.
- **More backtracking** — N-Queens, Word Search, Sudoku Solver are already on NC150 and cover the pruning patterns.
- **More monotonic stack** — Daily Temperatures, Largest Rectangle, Trapping Rain Water are on NC150; the technique is well-trained.
- **Most "II" or "III" variants** — Coin Change II, Word Search II, Combination Sum II are on NC150 themselves and already drill the variation muscle.

## Methodology

The 150 vs 450 cross-reference was done by parsing `neetcode-gh/leetcode/.problemSiteData.json` for the canonical 450-problem dataset and diffing against the curriculum. Pattern attribution and technique-distinctness judgments are my own. Where Claude Code helped: navigating the 450-problem dataset, cross-referencing pattern tags, surfacing candidate gaps. Final inclusion decisions, justifications, and curriculum placement are mine — each problem above earned its slot on the merits described.
