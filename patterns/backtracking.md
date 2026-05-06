# Backtracking

## Trigger

"Generate ALL [permutations / combinations / subsets / valid configurations]." If the answer is "the count" or "any one valid," DP is often better. If the answer is "list every one," backtracking is the play.

## Template

```python
def backtrack(path, choices):
    if is_complete(path):
        result.append(path[:])  # COPY — path is mutated in place
        return
    for c in choices:
        if not valid(c, path): continue
        path.append(c)        # choose
        backtrack(path, next_choices(choices, c))  # explore
        path.pop()            # un-choose
```

## Canonical: [Subsets](https://leetcode.com/problems/subsets/)

### Mistakes

- (none yet)

## Variants

### [Combination Sum](https://leetcode.com/problems/combination-sum/)

- (none yet) — pass `start` to allow reuse, recurse with same start

### [Combination Sum II](https://leetcode.com/problems/combination-sum-ii/)

- (none yet) — sort, skip duplicates with `if i > start and arr[i] == arr[i-1]`

### [Permutations](https://leetcode.com/problems/permutations/)

- (none yet) — track `used` boolean array

### [Subsets II](https://leetcode.com/problems/subsets-ii/)

- (none yet) — sort, skip duplicates the same way as Combination Sum II

### [Generate Parentheses](https://leetcode.com/problems/generate-parentheses/)

- (none yet) — track open/close counts; only add ')' if closes < opens

### [Word Search](https://leetcode.com/problems/word-search/)

- (none yet) — DFS the grid; mark visited via in-place mutation, restore on backtrack

### [Palindrome Partitioning](https://leetcode.com/problems/palindrome-partitioning/)

- (none yet) — at each cut, try every prefix that's a palindrome

### [Letter Combinations of a Phone Number](https://leetcode.com/problems/letter-combinations-of-a-phone-number/)

- (none yet) — recurse digit by digit

### [N-Queens](https://leetcode.com/problems/n-queens/)

- (none yet) — track three sets: cols, diag (r-c), anti-diag (r+c)

## Why these belong together

The choose / explore / un-choose dance. The base case identifies a complete solution; the loop tries each candidate; the un-choose restores state so the next iteration has a clean slate. Pruning (skipping invalid choices early) is what keeps it tractable.

## Edge cases / invariants

- ALWAYS append `path[:]` not `path` — the latter stores a reference that changes as you continue mutating.
- Sort the input first when you need to skip duplicates.
- For grid DFS, "mark visited" can be in-place mutation (set to '#') restored on backtrack — avoids a separate visited set.
