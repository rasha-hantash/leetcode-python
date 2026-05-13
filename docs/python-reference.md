## The different Python data types and when to use them

### 1. dictionary vs defaultdict() and when to use them

**What they are:** `dict` is Python's built-in hash map. `defaultdict` (from `collections`) is a `dict` subclass that auto-creates missing keys via a factory callable.
**DSA Use Case:** Two-sum-style lookups, memoization, frequency counters, adjacency lists for graphs, grouping / bucketing.
**Time Complexity:** $O(1)$ average for read / write / lookup. _Requires for defaultdict: `from collections import defaultdict`._

#### Core methods — access & write

| Method                     | What it does                                     | Returns            | Inserts?               |
| -------------------------- | ------------------------------------------------ | ------------------ | ---------------------- |
| `d[k]`                     | Read or raise `KeyError`                         | value              | no (raises if missing) |
| `d[k] = v`                 | Write                                            | —                  | yes                    |
| `d.get(k)`                 | Read or `None`                                   | value or `None`    | no                     |
| `d.get(k, default)`        | Read or `default`                                | value or `default` | no                     |
| `d.setdefault(k, default)` | Read; if missing, insert `default` and return it | value              | yes if missing         |
| `d.pop(k)`                 | Remove and return; `KeyError` if missing         | value              | removes                |
| `d.pop(k, default)`        | Remove and return; or `default`                  | value or `default` | removes                |
| `d.popitem()`              | Remove last inserted (Python 3.7+)               | `(k, v)`           | removes                |
| `del d[k]`                 | Delete; `KeyError` if missing                    | —                  | removes                |
| `d.clear()`                | Empty the dict                                   | —                  | —                      |
| `d.update(other)`          | Merge `other` into `d` (overwrites)              | —                  | yes                    |

**`del` vs `pop` — rule of thumb:** If you care about the value → `pop`. Otherwise → `del`. If you want missing-key tolerance → `pop(k, default)` is the only option.

#### Membership & inspection

| Method    | What it does                                            |
| --------- | ------------------------------------------------------- |
| `k in d`  | O(1) membership check — doesn't insert, safe everywhere |
| `len(d)`  | Number of keys                                          |
| `bool(d)` | `False` if empty                                        |

#### Iteration (these return _views_, not lists)

| Method       | Yields                         |
| ------------ | ------------------------------ |
| `d.keys()`   | keys                           |
| `d.values()` | values                         |
| `d.items()`  | `(k, v)` pairs — the workhorse |
| `iter(d)`    | same as `d.keys()`             |

```python
for k, v in d.items(): ...      # most common loop
for k in d: ...                 # iterates keys
```

Views are **live** — they reflect later changes. Don't mutate `d` while iterating; convert with `list(d.items())` if you must.

#### Construction patterns

```python
{}                                # empty
{"a": 1, "b": 2}                  # literal
dict(a=1, b=2)                    # kwargs
dict([("a", 1), ("b", 2)])        # from pairs
dict.fromkeys(["a", "b"], 0)      # {"a": 0, "b": 0} — fast init
{x: i for i, x in enumerate(arr)} # dict comprehension (value→index)
{**d1, **d2}                      # merge (3.5+)
d1 | d2                           # merge (3.9+)
```

#### Sorting (returns a list; dicts are insertion-ordered)

```python
sorted(d.items())                          # by key
sorted(d.items(), key=lambda kv: kv[1])    # by value
sorted(d.items(), key=lambda kv: -kv[1])   # by value desc
max(d, key=d.get)                          # key with max value
min(d, key=d.get)                          # key with min value
```

#### Insertion order (Python 3.7+ guarantee)

Dicts preserve insertion order. `next(iter(d))` gives the first inserted key. Useful for **LRU cache** problems and "first non-repeating char" patterns.

#### `defaultdict` — same as dict, plus one thing

```python
from collections import defaultdict
```

Inherits **every dict method above** unchanged. The only addition:

- `d.default_factory` — the callable you passed in (or `None`). On missing-key access via `d[k]`, defaultdict calls `default_factory()` and inserts the result.

`.get()`, `in`, and `.pop()` do **NOT** trigger the factory — only bracket access does.

```python
dd = defaultdict(int)
dd["a"]              # 0, and inserts "a": 0
dd.get("b")          # None — no insertion, factory NOT called
"b" in dd            # False, no insertion

# Common factories
defaultdict(int)              # missing key → 0
defaultdict(list)             # missing key → []
defaultdict(set)              # missing key → set()
defaultdict(dict)             # missing key → {}
defaultdict(lambda: 10)       # missing key → 10 (any constant)
defaultdict(lambda: [0, 0])   # missing key → fresh [0, 0]
```

You can temporarily disable it: `dd.default_factory = None` makes it behave like a plain dict.

#### `Counter` — the third one to know

```python
from collections import Counter
c = Counter("aabbc")            # Counter({'a': 2, 'b': 2, 'c': 1})
c = Counter([1, 1, 2, 3, 3, 3])

c.most_common(2)                # [(3, 3), (1, 2)]
c.most_common()                 # all, sorted desc
c["z"]                          # 0 (doesn't insert! different from defaultdict)
c.update("abc")                 # adds to counts (additive, NOT dict.update)
c.subtract("ab")                # subtractive
c.total()                       # sum of counts (3.10+)
list(c.elements())              # ['a','a','b','b','c'] — expand back

# Arithmetic
Counter("aab") + Counter("ab")  # {'a':3, 'b':2}
Counter("aab") - Counter("ab")  # {'a':1}  (drops <= 0)
Counter("aab") & Counter("ab")  # {'a':1, 'b':1}  intersection (min)
Counter("aab") | Counter("ab")  # {'a':2, 'b':1}  union (max)

# Equality compares counts
Counter(s) == Counter(t)        # anagram check in one line
```

#### "Does this insert?" cheat sheet

| Operation            | plain `dict`           | `defaultdict`          | `Counter`                  |
| -------------------- | ---------------------- | ---------------------- | -------------------------- |
| `d[k]` (missing)     | KeyError               | inserts `factory()`    | returns `0`, **no insert** |
| `d.get(k)` (missing) | `None`, no insert      | `None`, no insert      | n/a                        |
| `k in d`             | `False`, no insert     | `False`, no insert     | `False`, no insert         |
| `d.setdefault(k, x)` | inserts `x` if missing | inserts `x` if missing | inserts                    |

`Counter` is the safe one for **pure counting / lookup** — missing keys read as `0` without polluting the dict.

#### When to use `dict` vs `defaultdict`

**Prefer plain `dict` when:**

- The value is a scalar you set explicitly (two-sum-style `value → index` maps)
- Memoization / DP tables (you want `KeyError` or `in` to mean "not computed")
- Checking membership for absence (defaultdict's bracket-access silently inserts)
- Pure frequency counting → use `Counter` instead
- Small fixed-shape lookup tables (Roman numerals, direction vectors)
- Returning the map from a function (callers don't expect autovivification)

**Prefer `defaultdict` when:**

- Building adjacency lists: `graph[u].append(v)`
- Grouping / bucketing: `groups[key].append(item)`
- Counting interleaved with other logic (where `Counter` doesn't quite fit)
- Nested maps: `defaultdict(lambda: defaultdict(int))`

**When NOT to use `defaultdict` (bug risk):**

If your default value is indistinguishable from a valid computed answer, you can't tell "not computed yet" from "computed, answer happens to equal default":

```python
# Count distinct subsequences / paths / ways — answers include 0
memo = defaultdict(int)
def dp(i, j):
    if memo[(i, j)]:        # ← reads as "not computed" if answer is 0
        return memo[(i, j)]
    # ...recompute every time the real answer is 0 — quietly wrong / infinite loop risk
```

Use plain `dict` + `if (i, j) in memo` to avoid this.

#### The 90% leetcode toolkit

1. `d[k] = v` and `d[k]` — read/write
2. `d.get(k, default)` — safe read
3. `k in d` — membership
4. `d.items()` — iteration
5. `defaultdict(list).append(...)` — grouping
6. `Counter(seq)` and `.most_common(k)` — frequency

---

### 2. `set()` — "The Bouncer"

**What it is:** An unordered collection of unique elements. **DSA Use Case:** Checking for duplicates, keeping track of `visited` nodes in BFS/DFS, finding intersections. **Time Complexity:** $O(1)$ for Lookups, Inserts, and Deletes. _O_(n) for Searches.

**Core Methods:**

```python
s = set()
s.add(5)         # Adds 5. O(1)
s.add(5)         # Does nothing (no duplicates allowed)
s.remove(5)      # Removes 5. Throws KeyError if 5 isn't there.
s.discard(10)    # Removes 10 safely (NO error if 10 isn't there).

# The superpower of sets: Fast lookups
if 5 in s:       # O(1) time! (Unlike lists which are O(N))
    pass
```

---

### 3. `defaultdict()` — "The Helpful Assistant"

**What it is:** A dictionary that automatically creates a default value if you try to access a key that doesn't exist yet. **DSA Use Case:** Graph Adjacency Lists, Frequency Counters (Hash Maps). _Requires: `from collections import defaultdict`_

**Core Methods (same as dict, but no KeyErrors):**

```python
# 1. Frequency Counter (defaults to 0)
counts = defaultdict(int)
counts["apple"] += 1   # No error! Normally this throws KeyError in standard dict

# 2. Graph Adjacency List (defaults to empty list [])
graph = defaultdict(list)
graph["node_A"].append("node_B") # No need to check if "node_A" exists first!
```

---

### 4. `[]` (List) — "The Lineup"

**What it is:** An ordered, mutable dynamic array. **DSA Use Case:** Storing ordered data, Stacks (LIFO), sorting, iterating. **Time Complexity:** $O(1)$ append/pop from the _end_. $O(N)$ to insert/remove from the _middle or start_.

**Core Methods:**

```python
arr = []
arr.append(5)      # Adds to end. O(1)
arr.pop()          # Removes and returns last element. O(1) -> Great for STACKS!

arr.insert(0, 10)  # Inserts at index 0. O(N) -> BAD! (Use deque if you need this)
arr.remove(5)      # Finds and removes the first 5. O(N)

# Lookups
if 5 in arr:       # O(N) time! Slower than sets/dicts.
    pass
```
