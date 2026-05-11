# Python Gotchas — Anki Source

Each entry is one Anki card. Front = the trap (often as a code snippet or a "what does this do?" question). Back = the gotcha + the fix.

These are **language-level** failure modes — distinct from algorithm cards. The bug isn't the algorithm; it's Python.

Source for additions: append-only `docs/python-gotchas.md`. As you hit a real one mid-problem, log it there, then promote here as a card if it's likely to recur.

---

## 1. 2D grid initialization

**Front:** "What's wrong with `grid = [[0] * n] * m`?"

**Back:** All m rows are the **same list reference**. `grid[0][0] = 1` mutates row 0, but row 0 = row 1 = ... = row m-1, so all rows show the change.

Fix: `grid = [[0] * n for _ in range(m)]`.

---

## 2. Default mutable argument

**Front:** "What's wrong with `def f(x=[])`?"

**Back:** The default list is evaluated **once at function definition**. Every call without `x=` shares it; mutations persist across calls.

Fix: `def f(x=None): x = [] if x is None else x`.

---

## 3. Late-binding closures in loops

**Front:** "`fns = [lambda: i for i in range(3)]` — what does each call return?"

**Back:** All return `2` (the final value of `i`). Lambdas close over the _variable_, not the value at definition time.

Fix: `fns = [lambda i=i: i for i in range(3)]` (binds at definition via default arg).

---

## 4. Integer division vs true division

**Front:** "In Python 3, what is `5 / 2`?"

**Back:** `2.5` (float). For integer division use `5 // 2 == 2`. Common bug: `mid = (lo + hi) / 2` returns a float and breaks indexing.

Use `//` for indices and integer math.

---

## 5. divmod argument order

**Front:** "What does `divmod(7, 3)` return?"

**Back:** `(2, 1)` — quotient first, remainder second. Easy to flip when destructuring.

---

## 6. Mutating a list while iterating

**Front:** "`for x in lst: if cond(x): lst.remove(x)` — what's wrong?"

**Back:** Skips elements (the iterator advances even though you removed one). Can also raise odd errors.

Fix: iterate a copy (`for x in lst[:]:`) or build a new list (`lst = [x for x in lst if not cond(x)]`).

---

## 7. `is` vs `==`

**Front:** "When is `a is b` different from `a == b`?"

**Back:** `is` checks identity (same object); `==` checks equality. `[1,2] == [1,2]` is True; `[1,2] is [1,2]` is False. Small ints (`-5..256`) are cached so `a is b` may be True coincidentally — don't rely on it.

Use `is` only for `None`, `True`, `False`.

---

## 8. range excludes the stop value

**Front:** "What does `range(1, 5)` produce?"

**Back:** `1, 2, 3, 4` — stop is exclusive. To loop over `arr` indices: `range(len(arr))`. To include `n`: `range(n + 1)`.

---

## 9. Slice never raises IndexError

**Front:** "`arr = [1,2,3]; arr[10:20]` — what does this return?"

**Back:** `[]` — out-of-bounds slices silently return empty (or partial) result. `arr[10]` would raise IndexError.

This makes "subtle off-by-one in slicing" a hidden bug — won't crash, just gives wrong answer.

---

## 10. `sorted()` vs `list.sort()`

**Front:** "Difference between `sorted(lst)` and `lst.sort()`?"

**Back:** `sorted(lst)` returns a **new list** and leaves `lst` unchanged. `lst.sort()` sorts **in place** and returns `None`. Common bug: `result = lst.sort()` → `result` is None.

---

## 11. `str` is immutable

**Front:** "`s = 'abc'; s[0] = 'x'` — what happens?"

**Back:** TypeError. Strings are immutable. Build a list of chars (`list(s)`), mutate, then `''.join(...)` back.

---

## 12. String concat in a loop

**Front:** "Why is `s += word` in a loop O(n²)?"

**Back:** Strings are immutable, so each `+=` creates a new string copying all prior content. n iterations × n-length string = O(n²).

Fix: `parts = []; parts.append(word); ''.join(parts)` is O(n total).

---

## 13. `min` / `max` on empty iterable

**Front:** "`min([])` — what happens?"

**Back:** `ValueError: min() arg is an empty sequence`.

Fix: provide `default`: `min([], default=0)`. Or guard with `if lst:`.

---

## 14. `bool` is a subclass of `int`

**Front:** "`True == 1` and `isinstance(True, int)` — what do these evaluate to?"

**Back:** Both `True`. Booleans are ints under the hood. `True + True == 2`. Caution: a "count of trues" via `sum([True, False, True])` works (returns 2), which is occasionally what you want.

---

## 15. Recursion limit

**Front:** "Default Python recursion depth?"

**Back:** ~1000. DFS on a 10⁴-node linear tree blows the stack.

Fix: `import sys; sys.setrecursionlimit(10**6)` for LeetCode. Or convert to iterative DFS with an explicit stack.
