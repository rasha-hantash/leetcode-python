# Greedy

## Trigger

"Local optimal → global optimal." Each step has a clear best move, no backtracking needed. Tells: sort first, then scan; track running optimum; "Kadane-like" running aggregate.

## Template

### Kadane (max subarray)

```python
best = current = arr[0]
for x in arr[1:]:
    current = max(x, current + x)  # restart vs extend
    best = max(best, current)
return best
```

### Sort + scan

```python
arr.sort(key=...)
result = initial
for x in arr:
    if condition(x, result):
        result = update(x, result)
return result
```

## Canonical: [Maximum Subarray (Kadane's)](https://leetcode.com/problems/maximum-subarray/)

### Mistakes

- (none yet)

## Variants

### [Jump Game](https://leetcode.com/problems/jump-game/)

- (none yet) — track furthest reachable; if `i > furthest`, return False

### [Jump Game II](https://leetcode.com/problems/jump-game-ii/)

- (none yet) — BFS-like: track current jump's end and next jump's furthest

### [Gas Station](https://leetcode.com/problems/gas-station/)

- (none yet) — if total tank ≥ 0 a solution exists; start = first index where running sum stays ≥ 0

### [Hand of Straights](https://leetcode.com/problems/hand-of-straights/)

- (none yet) — min-heap (or sorted Counter), greedily form group from smallest available

### [Merge Triplets to Form Target Triplet](https://leetcode.com/problems/merge-triplets-to-form-target-triplet/)

- (none yet) — only consider triplets where every component ≤ target's; check each component is achievable

### [Partition Labels](https://leetcode.com/problems/partition-labels/)

- (none yet) — for each char, last index; partition ends when scan reaches max-last

### [Valid Parenthesis String](https://leetcode.com/problems/valid-parenthesis-string/)

- (none yet) — track range `[lo, hi]` of possible open counts; '\*' widens, ')' narrows

## Why these belong together

The shape: at each step you commit irrevocably to a local choice without lookahead — and the correctness rests on a small _greedy lemma_ unique to each problem. Pattern recognition is more about "is there a clean greedy argument here?" than about template matching.

## Edge cases / invariants

- The reasoning is the hard part — _why_ the greedy works. Always ask: "what swap argument shows my choice is optimal?"
- Sort decisions: by start? by end? by ratio? It's the design choice that makes or breaks the problem.
- Kadane's restart-vs-extend is the cleanest greedy in the canon — practice it.
