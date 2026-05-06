# Two Pointers

## Trigger

"Sorted array, find pair/triple with sum/property." Or "compare elements from both ends, converge inward." Tells: input is sorted (or you can sort), you need pairs not subarrays.

## Template

```python
# Converging two pointers (sorted array, find pair)
arr.sort()
left, right = 0, len(arr) - 1
while left < right:
    s = arr[left] + arr[right]
    if s == target: return [arr[left], arr[right]]
    elif s < target: left += 1
    else: right -= 1

# Same-direction (slow/fast for in-place dedup)
slow = 0
for fast in range(len(arr)):
    if arr[fast] != arr[slow]:
        slow += 1
        arr[slow] = arr[fast]
return slow + 1
```

## Canonical: [3Sum](https://leetcode.com/problems/3sum/)

### Mistakes

- (none yet)

## Variants

### [Valid Palindrome](https://leetcode.com/problems/valid-palindrome/)

- (none yet) — converge inward, skip non-alphanumeric

### [Two Sum II - Input Array Is Sorted](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/)

- (none yet)

### [Container With Most Water](https://leetcode.com/problems/container-with-most-water/)

- (none yet) — always move the shorter side inward

### [Trapping Rain Water](https://leetcode.com/problems/trapping-rain-water/)

- (none yet) — converge with running max-left and max-right

## Why these belong together

The common engine: process from both ends or with two cursors moving at different rates, exploit _sorted-ness_ or _symmetry_ to discard half the search space per step. O(n) instead of O(n²).

## Edge cases / invariants

- For triplets, fix the outer index, then two-pointer the rest. Skip duplicates with `while left < right and arr[left] == arr[left+1]: left += 1`.
- "Always move the shorter side" (Container) is the canonical greedy proof.
- Same-direction two-pointer = sliding window when the window expands. They're cousins.
