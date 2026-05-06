# Arrays & Hashing

## Trigger

"Find pair/group with constant lookup," "frequency count," "deduplicate," "check existence in O(1)." First pattern to reach for any time you see "given an array, return..."

## Template

```python
# Frequency map
from collections import Counter
freq = Counter(arr)

# Lookup-as-you-go (one-pass)
seen = {}
for i, x in enumerate(arr):
    if target - x in seen:
        return [seen[target - x], i]
    seen[x] = i

# Group-by-key
groups = {}
for x in arr:
    key = make_key(x)
    groups.setdefault(key, []).append(x)
```

## Canonical: [Two Sum](https://leetcode.com/problems/two-sum/)

### Mistakes

- (none yet)

## Variants

### [Contains Duplicate](https://leetcode.com/problems/contains-duplicate/)

- (none yet)

### [Valid Anagram](https://leetcode.com/problems/valid-anagram/)

- (none yet)

### [Group Anagrams](https://leetcode.com/problems/group-anagrams/)

- (none yet) — key by sorted-string OR by 26-tuple of letter counts (faster)

### [Top K Frequent Elements](https://leetcode.com/problems/top-k-frequent-elements/)

- (none yet) — bucket sort by frequency for O(n)

### [Encode and Decode Strings](https://leetcode.com/problems/encode-and-decode-strings/)

- (none yet) — length-prefix delimiter (e.g., `"5#hello"`)

### [Product of Array Except Self](https://leetcode.com/problems/product-of-array-except-self/)

- (none yet) — prefix product L→R, then post-multiply R→L

### [Valid Sudoku](https://leetcode.com/problems/valid-sudoku/)

- (none yet) — three sets per cell: row, col, 3×3 box

### [Longest Consecutive Sequence](https://leetcode.com/problems/longest-consecutive-sequence/)

- (none yet) — only start counting from `x` if `x-1` not in set (O(n) total)

## Why these belong together

The unifying idea: hash maps/sets give O(1) lookup. Most "given an array, find..." problems collapse to "build a hashmap of [something] then check it." Different problems vary the _key_ (raw value, sorted-anagram, frequency, prefix-product) but the lookup-and-respond shape is constant.

## Edge cases / invariants

- `Counter(arr)` is the fastest path to frequency.
- For "longest run starting from x," skip elements that aren't a run-start.
- `setdefault` and `defaultdict` are equivalent for grouping; pick one and stick with it.
