# Boyer-Moore Voting

## Trigger

"Find the majority element (appears > n/2 times)." O(n) time, **O(1) space** is the constraint that signals this — heap or hashmap solutions work but are O(n) space.

## Template

### Majority Element (> n/2)

```python
def majority(nums):
    candidate = None
    count = 0
    for x in nums:
        if count == 0:
            candidate = x
            count = 1
        elif x == candidate:
            count += 1
        else:
            count -= 1
    return candidate  # only valid if a >n/2 majority is guaranteed to exist
```

### Majority Element II (> n/3, at most 2 such elements)

```python
def majority_n3(nums):
    c1 = c2 = None
    n1 = n2 = 0
    for x in nums:
        if x == c1: n1 += 1
        elif x == c2: n2 += 1
        elif n1 == 0: c1, n1 = x, 1
        elif n2 == 0: c2, n2 = x, 1
        else: n1 -= 1; n2 -= 1
    # verify: a candidate is only valid if its actual count is > n/3
    return [c for c in (c1, c2) if c is not None and nums.count(c) > len(nums) // 3]
```

## Canonical: [Majority Element](https://leetcode.com/problems/majority-element/)

### Mistakes

- (none yet)

## Variants

### [Majority Element II](https://leetcode.com/problems/majority-element-ii/)

- (none yet) — generalizes to "more than n/k" with k-1 candidates

## Why these belong together

The cancellation argument: pair up each majority element with a non-majority element; if true majority > n/2, some majority elements remain unpaired and become the surviving candidate. Generalizes: > n/k means up to k-1 candidates. Distinct from frequency counting (Top K Frequent in NC150 uses heap/bucket sort, O(n) space) — Boyer-Moore is the _cancellation_ trick.

## Edge cases / invariants

- The basic version only finds the candidate; if a majority is **not guaranteed** to exist, you must verify with a second pass.
- For n/3 variant, max candidates = 2; for n/k generally, max = k-1.
- Counts are not "real" frequencies during the pass; they're surviving-pair counters.
