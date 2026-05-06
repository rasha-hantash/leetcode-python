# Sliding Window

## Trigger

"Longest/shortest subarray or substring with [some property]" — contiguous, single sequence, looking for an extremum. Variable-size window expands right, contracts left when an invariant breaks.

## Template

### Variable-size window

```python
left = 0
state = {}
result = 0
for right in range(len(arr)):
    state[arr[right]] = state.get(arr[right], 0) + 1
    while invariant_broken(state):
        state[arr[left]] -= 1
        if state[arr[left]] == 0: del state[arr[left]]
        left += 1
    result = max(result, right - left + 1)
return result
```

### Fixed-size window

```python
window_sum = sum(arr[:k])
best = window_sum
for right in range(k, len(arr)):
    window_sum += arr[right] - arr[right - k]
    best = max(best, window_sum)
return best
```

## Canonical: [Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/)

### Mistakes

- (none yet)

## Variants

### [Best Time to Buy and Sell Stock](https://leetcode.com/problems/best-time-to-buy-and-sell-stock/)

- (none yet) — track min-so-far, update best profit

### [Longest Repeating Character Replacement](https://leetcode.com/problems/longest-repeating-character-replacement/)

- (none yet) — invariant: `(window_size - max_count_in_window) <= k`

### [Permutation in String](https://leetcode.com/problems/permutation-in-string/)

- (none yet) — fixed-size window, compare counter against target

### [Minimum Window Substring](https://leetcode.com/problems/minimum-window-substring/)

- (none yet) — `formed` counter for "have all required chars at required count"

### [Sliding Window Maximum](https://leetcode.com/problems/sliding-window-maximum/)

- (none yet) — monotonic decreasing deque, evict out-of-window indices

## Why these belong together

The invariant is the only thing that changes between problems. The skeleton — expand right, contract left while broken, update result — is identical. Pattern recognition is just "what state should I track?" and "what condition makes it broken?"

## Edge cases / invariants

- Window length is `right - left + 1` (inclusive both sides).
- Contract using `while`, not `if` — the window may need to shrink multiple steps.
- For fixed-size windows, no inner loop — just slide one step at a time.
