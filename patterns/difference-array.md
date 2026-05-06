# Difference Array / Range Updates

## Trigger

"Apply many `+k` updates to ranges `[L, R]`, then query the final state." Tells: batch range updates, single final read, or range increments described in the problem statement.

## Template

```python
def apply_range_updates(n, updates):
    diff = [0] * (n + 1)
    for L, R, k in updates:
        diff[L] += k
        diff[R + 1] -= k
    # prefix-sum to recover final array
    out = [0] * n
    out[0] = diff[0]
    for i in range(1, n):
        out[i] = out[i - 1] + diff[i]
    return out
```

## Canonical: [Corporate Flight Bookings](https://leetcode.com/problems/corporate-flight-bookings/)

### Mistakes

- (none yet)

## Variants

### [Car Pooling](https://leetcode.com/problems/car-pooling/)

- (none yet) — same trick: passengers pickup at L (+capacity), dropoff at R (-capacity)

### [Range Addition](https://leetcode.com/problems/range-addition/)

- (none yet) — the bare canonical (free LeetCode lock).

## Why these belong together

The inverse of prefix sum. Prefix sum: O(n) preprocessing → O(1) range query. Difference array: O(1) range update → O(n) finalization. Each `+k` on `[L, R]` becomes `diff[L] += k; diff[R+1] -= k`. After all updates, prefix-summing `diff` recovers the final array. Distinct from NC150's prefix-sum problems (Product of Array Except Self) which never do range _updates_.

## Edge cases / invariants

- Allocate `diff` with size `n+1` (or guard `R+1 < n`) so the closing -k doesn't fall off.
- Works for adds; for range _multiplies_ you need a segment tree with lazy propagation (out of scope here).
- If you also need to support point queries DURING the updates (not just at the end), use a Fenwick tree variant — see segment-tree.md.
