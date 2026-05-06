# Pattern Recognition — Anki Source

Each entry is one Anki card. Front = problem-statement trigger phrase. Back = pattern name + 1-line "why this pattern."

These train **the smell** — the sub-second classification you do when reading a fresh problem. The code itself is in `templates.md`; this deck is purely about reaching for the right tool.

---

## 1. Pair sum in sorted array

**Front:** "sorted array, find pair summing to K, O(1) extra space"

**Back:** Two pointers (converging from ends). Sorted order lets you decide which side to move based on current sum vs target.

---

## 2. Pair sum in unsorted array

**Front:** "unsorted array, find pair summing to K, fast lookup"

**Back:** Hash map (seen-set). For each x, look for K - x in the set. Trade space for time.

---

## 3. Longest substring with property

**Front:** "longest substring/subarray with [at most K distinct / no repeats / valid property]"

**Back:** Sliding window (variable size). Expand right, shrink left while violated.

---

## 4. Min-length subarray meeting threshold

**Front:** "shortest subarray with sum ≥ S"

**Back:** Sliding window (shrinking). Or prefix sum + monotonic deque if values can be negative.

---

## 5. Sorted-rotated array search

**Front:** "search in rotated sorted array"

**Back:** Modified binary search. Determine which half is sorted, then check if target fits there.

---

## 6. "Find smallest X where condition holds"

**Front:** "monotonic predicate over an integer range"

**Back:** Binary search on answer space. The answer space (not the array) is what's binary-searched.

---

## 7. Tree-depth/path metric

**Front:** "max depth, diameter, sum-along-path in a tree"

**Back:** DFS returning a tuple of metrics (e.g., (depth, best_so_far)). Post-order recursion.

---

## 8. Shortest path on unweighted graph

**Front:** "fewest steps from A to B in a grid or unweighted graph"

**Back:** BFS. Level-by-level expansion gives shortest path automatically.

---

## 9. Shortest path on weighted graph (non-negative)

**Front:** "shortest path with positive edge weights"

**Back:** Dijkstra (heap-based). For arbitrary weights, Bellman-Ford.

---

## 10. Course-schedule / dependency ordering

**Front:** "ordering with prerequisites, detect cycle"

**Back:** Topological sort (Kahn's BFS via in-degree). Cycle = not all nodes processed.

---

## 11. Connectivity / grouping queries

**Front:** "are these two in the same component? merge groups dynamically"

**Back:** Union-Find (DSU) with path compression + union by rank.

---

## 12. Top-K elements

**Front:** "K largest / K smallest / K most frequent"

**Back:** Min-heap of size K (for K largest). Or quickselect for O(n) average — but heap is interview-default.

---

## 13. Running median

**Front:** "median of a stream of numbers"

**Back:** Two heaps — max-heap for lower half, min-heap for upper half. Balance after each insert.

---

## 14. Word/prefix lookup

**Front:** "many words, query if any starts with prefix / spelling-checker"

**Back:** Trie. Insert all words; walk the trie char-by-char.

---

## 15. "Next greater element" / span problems

**Front:** "for each element, find next/prev greater (or smaller)"

**Back:** Monotonic stack. Pop while stack top is ≤ current; current's answer is what's now on top.

---

## 16. All combinations / subsets / permutations

**Front:** "enumerate all subsets, all combinations, all permutations"

**Back:** Backtracking (DFS with choose / explore / un-choose). State = current path.

---

## 17. Optimal value with overlapping subproblems

**Front:** "min cost / max value, choices repeat across subproblems"

**Back:** DP. Identify state, transition, base case. Top-down memo first; convert to bottom-up if needed.

---

## 18. "Find the duplicate / find the missing"

**Front:** "exactly one number missing or duplicated, O(1) extra space"

**Back:** XOR all elements (and 0..n if missing), or Floyd's cycle detection on indices for duplicate.

---

## 19. Majority element (> n/2 occurrences)

**Front:** "element that appears more than n/2 times, O(1) space"

**Back:** Boyer-Moore voting. Maintain candidate + count.

---

## 20. Random pick with weights or from a stream

**Front:** "uniform random pick from a stream of unknown length"

**Back:** Reservoir sampling. Replace current pick with probability 1/i at index i.

---

## 21. Range sum / range update over array

**Front:** "many range updates, then point queries (or vice versa)"

**Back:** Difference array (range update + prefix sum), Fenwick tree (point update + range query), or segment tree (both).

---

## 22. "Visit all nodes / states with bitmask"

**Front:** "n ≤ 20, visit all subsets / smallest set covering all"

**Back:** Bitmask DP. State = (current_node, visited_mask).

---

## 23. Max XOR query

**Front:** "max XOR of two numbers in array"

**Back:** Bit-trie. Insert binary representations; for each query, walk preferring the opposite bit.

---

## 24. Overlapping intervals / scheduling

**Front:** "merge overlapping intervals, max concurrent meetings, scheduling"

**Back:** Sort by start (or end). Sweep line for "max concurrent." Heap for "min rooms."

---

## 25. Many points / events on a number line

**Front:** "max overlap at any point, skyline, calendar with K bookings"

**Back:** Sweep line — events as +1/-1 deltas, sort by coordinate, scan and track running sum.

---

## 26. Greedy with sort + scan

**Front:** "irrevocable local choice each step, no backtracking"

**Back:** Greedy. Usually sort by some key, then scan with a running aggregate. Justify with swap argument.

---

## 27. "Cycle in linked list / array of indices"

**Front:** "detect cycle, find cycle start"

**Back:** Floyd's tortoise-and-hare. Phase 1 detects cycle, phase 2 (reset one to head) finds entry.

---

## 28. Reverse a linked list

**Front:** "reverse linked list (full or sublist)"

**Back:** Iterative with prev/curr/next, or recursive returning new head. Practice both.

---

## 29. K-th element in unsorted array

**Front:** "k-th largest / smallest in unsorted"

**Back:** Quickselect (O(n) avg). Or min-heap of size K (O(n log K)). Heap is safer in interviews.

---

## 30. "Single element appearing once, others twice"

**Front:** "every element appears twice except one"

**Back:** XOR all elements. Pairs cancel; result = the lone element.
