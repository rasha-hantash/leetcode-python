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
