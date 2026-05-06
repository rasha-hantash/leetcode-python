# Bitmask DP

## Trigger

"≤ 20 elements, visit each at most once, find optimal arrangement / minimum cost / count." The small-N constraint is the tell — once `n ≤ 20`, `2^n ≤ 1M` states becomes feasible. Other phrasing: "TSP-like," "every node visited," "subset cover."

## Template

```python
def bitmask_dp(graph_or_items):
    n = len(graph_or_items)
    FULL = (1 << n) - 1

    # dp[mask][i] = best cost to reach state `mask` ending at element i
    INF = float('inf')
    dp = [[INF] * n for _ in range(1 << n)]

    # base case: starting at each element with only itself visited
    for i in range(n):
        dp[1 << i][i] = 0  # or starting cost

    for mask in range(1 << n):
        for i in range(n):
            if not (mask & (1 << i)): continue
            if dp[mask][i] == INF: continue
            # transition: try adding each unvisited j
            for j in range(n):
                if mask & (1 << j): continue
                new_mask = mask | (1 << j)
                cost = dp[mask][i] + edge_cost(i, j)
                if cost < dp[new_mask][j]:
                    dp[new_mask][j] = cost

    return min(dp[FULL][i] for i in range(n))
```

## Canonical: [Shortest Path Visiting All Nodes](https://leetcode.com/problems/shortest-path-visiting-all-nodes/)

### Mistakes

- (none yet)

## Variants

### [Partition to K Equal Sum Subsets](https://leetcode.com/problems/partition-to-k-equal-sum-subsets/)

- (none yet) — `dp[mask] = current sum mod target` after using elements in mask

## Why these belong together

State = subset of elements already used. Transition = pick one element NOT in the mask. The exponential state space (`2^n`) is what makes it feasible only for small N. Distinct from sum-as-state DP (Partition Equal Subset Sum, in 1D DP), which only tracks an aggregate, not which items.

## Edge cases / invariants

- Use `mask | (1 << j)` to add bit, `mask & (1 << j)` to test, `mask & ~(1 << j)` to remove.
- Iterate masks low-to-high for forward DP; the dependency `mask → mask | (1<<j)` only adds bits.
- For "visit all nodes" the answer is `dp[FULL][*]`.
