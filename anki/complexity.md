# Complexity Reference — Anki Source

Each entry is one Anki card. Front = operation. Back = time/space complexity + the **why** in one line.

These are the facts you'll cite **out loud** during interviews. Memorizing the table flat is fine; understanding the why means you can derive the unfamiliar ones.

---

## 1. dict / set lookup, insert, delete

**Front:** "Time complexity of `d[k]`, `d[k] = v`, `del d[k]`, `k in d`?"

**Back:** **O(1) average, O(n) worst.** Backed by a hash table. Worst case is when all keys hash to the same bucket (rare in practice; CPython uses open addressing + randomized hashing).

---

## 2. list indexing

**Front:** "Time complexity of `lst[i]` and `lst[i] = x`?"

**Back:** **O(1).** Lists are contiguous arrays of pointers; index access is direct.

---

## 3. list append, pop (end)

**Front:** "Time complexity of `lst.append(x)` and `lst.pop()`?"

**Back:** **O(1) amortized.** Append occasionally reallocates (doubling), but the average over n appends is O(1). Pop from end is always O(1).

---

## 4. list insert / pop at index 0 (or middle)

**Front:** "Time complexity of `lst.insert(0, x)` and `lst.pop(0)`?"

**Back:** **O(n).** All elements after the index must shift. For O(1) front operations, use `collections.deque` instead.

---

## 5. deque appendleft / popleft

**Front:** "Time complexity of `deque.appendleft(x)` and `deque.popleft()`?"

**Back:** **O(1).** Deques are doubly-linked-list-of-blocks; both ends are O(1). Use deque for BFS queues.

---

## 6. heapq push / pop

**Front:** "Time complexity of `heapq.heappush(heap, x)` and `heapq.heappop(heap)`?"

**Back:** **O(log n).** Both walk up/down a binary heap. `heap[0]` (peek) is O(1).

---

## 7. heapify

**Front:** "Time complexity of `heapq.heapify(lst)`?"

**Back:** **O(n).** Counterintuitive — building a heap from n elements is linear, not n log n, due to the structure of the sift-down work distribution.

---

## 8. bisect_left / bisect_right

**Front:** "Time complexity of `bisect.bisect_left(sorted_lst, x)`?"

**Back:** **O(log n).** Standard binary search on a sorted sequence.

But: **`sorted_lst.insert(idx, x)` after bisect is O(n)** because of the shift. Use `SortedList` from `sortedcontainers` (O(log n) insert) for fully-sorted dynamic sequences.

---

## 9. sort / sorted

**Front:** "Time complexity of `lst.sort()` and `sorted(lst)`?"

**Back:** **O(n log n)** average and worst. Python uses Timsort (a merge-sort variant). Stable. `lst.sort()` is in-place, `sorted(lst)` allocates a new list.

---

## 10. string slicing and concatenation

**Front:** "Time complexity of `s[a:b]` and `s + t`?"

**Back:** Slice: **O(b - a)** — copies the substring. Concat `s + t`: **O(len(s) + len(t))** — new string allocated.

In a loop, concat is O(n²) total. Use `''.join(parts)` for O(n) total.

---

## 11. set operations

**Front:** "Time complexity of `set.union(other)`, `set.intersection(other)`, `set & other`?"

**Back:** **O(len(self) + len(other))** for union, **O(min(len(self), len(other)))** for intersection. Both backed by hash table iteration.

---

## 12. Counter / collections.defaultdict

**Front:** "Time complexity of `Counter(lst)` and `defaultdict.__getitem__`?"

**Back:** `Counter(lst)`: **O(n)** — single pass. `defaultdict[k]`: **O(1) avg** — same as dict, but auto-creates the value if missing.

---

## 13. min / max / sum on iterable

**Front:** "Time complexity of `min(lst)`, `max(lst)`, `sum(lst)`?"

**Back:** **O(n).** Single pass. (No magic — they don't know about sortedness.)

---

## 14. `in` operator

**Front:** "`x in lst` vs `x in set` vs `x in dict`?"

**Back:** `lst`: **O(n)** linear scan. `set`: **O(1) avg** hash lookup. `dict` (key check): **O(1) avg**. Common pitfall: writing `x in some_list` inside a loop = O(n²) total.

---

## 15. Tree / graph traversal (DFS, BFS)

**Front:** "Time and space complexity of DFS or BFS over a graph?"

**Back:** **Time O(V + E)** — visit each node once, traverse each edge once. **Space O(V)** for the visited set + recursion/queue depth.
