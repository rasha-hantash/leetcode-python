# 2-D Dynamic Programming

## Trigger

"Two sequences/dimensions with overlapping subproblems" — `dp[i][j]` represents some optimum involving prefix of `i` from one input and prefix of `j` from another (or row `i`, col `j` of a grid).

## Template

```python
m, n = len(a), len(b)
dp = [[0] * (n + 1) for _ in range(m + 1)]
# initialize first row/col base cases
for i in range(m + 1): dp[i][0] = base_i
for j in range(n + 1): dp[0][j] = base_j

for i in range(1, m + 1):
    for j in range(1, n + 1):
        if matches(a[i-1], b[j-1]):
            dp[i][j] = dp[i-1][j-1] + 1  # or some merge
        else:
            dp[i][j] = combine(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])
return dp[m][n]
```

## Canonical: [Unique Paths](https://leetcode.com/problems/unique-paths/)

### Mistakes

- (none yet)

## Variants

### [Longest Common Subsequence](https://leetcode.com/problems/longest-common-subsequence/)

- (none yet)

### [Best Time to Buy and Sell Stock with Cooldown](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-with-cooldown/)

- (none yet) — state machine: hold / sold / rest

### [Coin Change II](https://leetcode.com/problems/coin-change-ii/)

- (none yet) — count combinations; outer loop coins, inner amount

### [Target Sum](https://leetcode.com/problems/target-sum/)

- (none yet) — convert to subset-sum problem

### [Interleaving String](https://leetcode.com/problems/interleaving-string/)

- (none yet) — `dp[i][j]` = can form s3[:i+j] from s1[:i] + s2[:j]

### [Longest Increasing Path in a Matrix](https://leetcode.com/problems/longest-increasing-path-in-a-matrix/)

- (none yet) — DFS with memoization

### [Distinct Subsequences](https://leetcode.com/problems/distinct-subsequences/)

- (none yet)

### [Edit Distance](https://leetcode.com/problems/edit-distance/)

- (none yet) — insert/delete/replace transitions

### [Burst Balloons](https://leetcode.com/problems/burst-balloons/)

- (none yet) — interval DP, choose LAST balloon to burst in range

### [Regular Expression Matching](https://leetcode.com/problems/regular-expression-matching/) `T2`

- (none yet) — handle '.' single match and '\*' zero-or-more

## Why these belong together

The dimensions can be: two strings, two arrays, grid coords, or interval `(l, r)`. The DP table is rectangular and the recurrence hops between adjacent cells. Most 2D DP problems are _one_ of these archetypes: edit distance shape (3-way min), grid path (sum/count from above-or-left), interval DP (split point), or knapsack-rolled-2D.

## Edge cases / invariants

- Off-by-one: `dp[i][j]` represents prefixes of length `i` and `j`, so the actual character access is `a[i-1]` and `b[j-1]`.
- Interval DP iterates by increasing range length, not by index.
- Many 2D DPs are space-optimizable to 1D rolling array — do correctness first.
