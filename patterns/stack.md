# Stack (incl. Monotonic Stack)

## Trigger

"Match nested brackets," "next greater/smaller element," "histogram-like extremum." LIFO order is intrinsic to the problem.

## Template

### Bracket matching

```python
pairs = {')': '(', ']': '[', '}': '{'}
stack = []
for c in s:
    if c in '([{':
        stack.append(c)
    elif not stack or stack[-1] != pairs[c]:
        return False
    else:
        stack.pop()
return not stack
```

### Monotonic stack (next greater)

```python
stack = []  # indices, values strictly decreasing
result = [-1] * len(arr)
for i, x in enumerate(arr):
    while stack and arr[stack[-1]] < x:
        result[stack.pop()] = x
    stack.append(i)
return result
```

## Canonical: [Daily Temperatures](https://leetcode.com/problems/daily-temperatures/) _(monotonic)_ + [Valid Parentheses](https://leetcode.com/problems/valid-parentheses/) _(matching)_

### Mistakes

- (none yet)

## Variants

### [Min Stack](https://leetcode.com/problems/min-stack/)

- (none yet) — auxiliary stack of running minima

### [Evaluate Reverse Polish Notation](https://leetcode.com/problems/evaluate-reverse-polish-notation/)

- (none yet) — push operands, pop two on operator

### [Car Fleet](https://leetcode.com/problems/car-fleet/)

- (none yet) — sort by position desc, stack of arrival times; pop if current ≥ stack top

### [Largest Rectangle in Histogram](https://leetcode.com/problems/largest-rectangle-in-histogram/)

- (none yet) — monotonic stack, compute area when popping a taller bar

### [Generate Parentheses](https://leetcode.com/problems/generate-parentheses/)

- (none yet) — backtracking with implicit stack via recursion depth

## Why these belong together

Either you literally need LIFO order (brackets), or you need to defer "I'll know later" decisions (monotonic stack: "I don't know the next greater yet, hold onto this index"). The monotonic discipline (always strictly inc/dec) is what gives O(n) — each element is pushed and popped at most once.

## Edge cases / invariants

- Pop the stack at the END as well — leftover elements have no answer (assign default).
- For "previous greater," reverse the iteration or flip comparisons.
- Histograms benefit from sentinels (`heights = [0] + heights + [0]`) to flush the stack cleanly.
