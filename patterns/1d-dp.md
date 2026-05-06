# 1-D Dynamic Programming

## Trigger

"Decision per element with overlap" — at each index, you choose among options whose answers depend on smaller subproblems with overlapping recursion. Tells: "max/min/count," single sequence input, can be reduced to `dp[i]` depending on `dp[i-1]`, `dp[i-2]`, etc.

## Template

```python
# Bottom-up form
dp = [0] * (n + 1)
dp[0] = base_case_0
dp[1] = base_case_1
for i in range(2, n + 1):
    dp[i] = transition(dp[i-1], dp[i-2], arr[i-1])
return dp[n]

# Space-optimized when only last 1-2 states needed
prev2, prev1 = 0, 0
for x in arr:
    curr = transition(prev1, prev2, x)
    prev2, prev1 = prev1, curr
return prev1
```

## Canonical: [House Robber](https://leetcode.com/problems/house-robber/)

### Mistakes

- (none yet)

## Variants

### [Climbing Stairs](https://leetcode.com/problems/climbing-stairs/)

- (none yet) — Fibonacci

### [Min Cost Climbing Stairs](https://leetcode.com/problems/min-cost-climbing-stairs/)

- (none yet)

### [House Robber II](https://leetcode.com/problems/house-robber-ii/)

- (none yet) — circular: take max of robbing [0..n-2] OR [1..n-1]

### [Longest Palindromic Substring](https://leetcode.com/problems/longest-palindromic-substring/)

- (none yet) — expand around each center (O(n²)); 2D DP also works

### [Palindromic Substrings](https://leetcode.com/problems/palindromic-substrings/)

- (none yet) — same expand-around-center, count each

### [Decode Ways](https://leetcode.com/problems/decode-ways/)

- (none yet) — `dp[i]` from `dp[i-1]` (single digit valid) + `dp[i-2]` (two-digit valid)

### [Coin Change](https://leetcode.com/problems/coin-change/)

- (none yet) — `dp[amount] = min(dp[amount - coin] + 1 for coin in coins)`

### [Maximum Product Subarray](https://leetcode.com/problems/maximum-product-subarray/)

- (none yet) — track BOTH max and min so far (negative \* negative)

### [Word Break](https://leetcode.com/problems/word-break/)

- (none yet) — `dp[i]` true if `dp[j]` true and `s[j:i]` in dict

### [Longest Increasing Subsequence](https://leetcode.com/problems/longest-increasing-subsequence/)

- (none yet) — `dp[i] = 1 + max(dp[j] for j < i if arr[j] < arr[i])`; binary-search trick gives O(n log n)

### [Partition Equal Subset Sum](https://leetcode.com/problems/partition-equal-subset-sum/)

- (none yet) — subset-sum DP: `dp[s]` reachable

## Why these belong together

The core question — "what's the optimal answer ending at index i?" — admits the same skeleton: a recurrence on `dp[i]` from a few earlier states. Most NC150 1D DP problems collapse to "dp[i] = max/min/sum of dp[i-k] + something." Recognizing this shape is 80% of solving the problem.

## Edge cases / invariants

- Always state the DP definition explicitly: "dp[i] = X for prefix ending at i" — vagueness here is the source of most bugs.
- Initialize base cases carefully (`dp[0]`, sometimes `dp[-1]` via padding).
- Space-optimize after correctness: most "rolling" DPs only need the last 1-2 states.
