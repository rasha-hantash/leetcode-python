# Binary Search

## Trigger

"Sorted array, find target/insertion." OR "monotonic predicate over an answer space" (you're searching not for an index but for a _value_ that satisfies a yes/no condition that flips exactly once).

## Template

### Classic search

```python
lo, hi = 0, len(arr) - 1
while lo <= hi:
    mid = (lo + hi) // 2
    if arr[mid] == target: return mid
    elif arr[mid] < target: lo = mid + 1
    else: hi = mid - 1
return -1  # or `lo` for insertion point
```

### Search on answer space (smallest x where condition is True)

```python
lo, hi = min_possible, max_possible
while lo < hi:
    mid = (lo + hi) // 2
    if condition(mid):
        hi = mid          # mid is feasible, try smaller
    else:
        lo = mid + 1
return lo
```

## Canonical: [Binary Search](https://leetcode.com/problems/binary-search/) _(classic)_ + [Koko Eating Bananas](https://leetcode.com/problems/koko-eating-bananas/) _(answer space)_

### Mistakes

- (none yet)

## Variants

### [Search a 2D Matrix](https://leetcode.com/problems/search-a-2d-matrix/)

- (none yet) — flatten by `idx → (idx // cols, idx % cols)`

### [Find Minimum in Rotated Sorted Array](https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/)

- (none yet) — compare `arr[mid]` to `arr[hi]` to decide which half is sorted

### [Search in Rotated Sorted Array](https://leetcode.com/problems/search-in-rotated-sorted-array/)

- (none yet) — identify sorted half, then test if target lies in it

### [Time Based Key-Value Store](https://leetcode.com/problems/time-based-key-value-store/)

- (none yet) — bisect on timestamps per key

### [Median of Two Sorted Arrays](https://leetcode.com/problems/median-of-two-sorted-arrays/)

- (none yet) — binary search on partition split of shorter array

## Why these belong together

Two flavors of the same idea: O(log n) by halving each step. Classic = halve an array. Answer-space = halve a numeric range. The trickiest part is the loop invariant — `lo <= hi` with `lo = mid+1, hi = mid-1` for classic; `lo < hi` with `hi = mid` for answer-space (because `mid` itself might be the answer).

## Edge cases / invariants

- Use `(lo + hi) // 2`. Python ints don't overflow, but the discipline matters in other languages.
- Off-by-one: `lo <= hi` vs `lo < hi` is determined by whether `mid` can BE the answer or only points past it.
- `bisect.bisect_left` / `bisect.bisect_right` cover most "insertion point" needs without writing the loop.
