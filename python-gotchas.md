# Python Gotchas

Append-only log of language-level stumbles that don't belong under any single algorithmic pattern. Things you'll hit that aren't algorithm bugs — they're Python-being-Python bugs.

## Format

```
## YYYY-MM-DD — short title
- The trap: <what you did that didn't work>
- The fix: <one-line correction>
- Why: <why Python behaves this way>
```

## Categories worth watching

- Mutable default arguments (`def f(x=[])` — same list across calls)
- `is` vs `==` (interning of small ints / strings, but never rely on it)
- Late binding in closures inside loops (`lambdas in [lambda: i for i in range(3)]` all return 2)
- Integer division semantics (`-7 // 2 == -4`, not `-3`)
- `divmod(a, b)` returns `(quotient, remainder)` — NOT the other way
- `dict.setdefault` vs `defaultdict`
- `list.sort()` returns `None`; `sorted(list)` returns the list
- `heapq` is min-heap only — negate values for max-heap
- `string * n` for repetition vs `n * string` (both work, but `[obj] * n` shares references!)
- `[[0]*n]*m` creates m references to the SAME row — use `[[0]*n for _ in range(m)]`
- `range()` is a generator-like object; `list(range())` to materialize
- `set()` is empty; `{}` is empty dict
- Slicing never raises IndexError; indexing does
- Iterating + mutating a dict/list raises RuntimeError or silently misbehaves
- `bool` is subclass of `int` — `True + True == 2`, watch for it in counters
- Recursion limit ~1000 by default — `sys.setrecursionlimit(10**6)` for deep DFS
- `==` on floats — never. Use `math.isclose`.
- `int(x)` truncates toward zero; `math.floor` rounds toward -inf
- f-string format specifiers (`{x:.3f}`, `{x:05d}`, `{x:,}`) — review when needed

---

## Entries

<!-- New entries go here, newest at top -->

## (none yet)
