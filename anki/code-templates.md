# Code Templates — Anki Source

Each entry is one Anki card. Front = trigger phrase. Back = code skeleton (the part between the dashes).

Import to Anki by copy-pasting each `Front: / Back:` block, or use the [AnkiConnect](https://ankiweb.net/shared/info/2055492159) plugin and a short script if you'd rather automate.

These are **muscle-memory drills** — you should be able to type each from memory in <90 seconds. The trigger on the front is the _signal_; the back is the canonical Python form.

---

## 1. Binary search (lo <= hi)

**Front:** "sorted array, find target or insertion point"

**Back:**

```python
lo, hi = 0, len(arr) - 1
while lo <= hi:
    mid = (lo + hi) // 2
    if arr[mid] == target: return mid
    elif arr[mid] < target: lo = mid + 1
    else: hi = mid - 1
return lo  # insertion point
```

---

## 2. Binary search on answer space

**Front:** "monotonic predicate over integer range — find smallest x where condition(x) is True"

**Back:**

```python
lo, hi = min_possible, max_possible
while lo < hi:
    mid = (lo + hi) // 2
    if condition(mid):
        hi = mid
    else:
        lo = mid + 1
return lo
```

---

## 3. Sliding window (variable size)

**Front:** "longest/shortest substring or subarray with [property]"

**Back:**

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

---

## 4. Two pointers (sorted, converging)

**Front:** "sorted array, find pair/triple with sum/property"

**Back:**

```python
left, right = 0, len(arr) - 1
while left < right:
    s = arr[left] + arr[right]
    if s == target: return [left, right]
    elif s < target: left += 1
    else: right -= 1
```

---

## 5. Fast/slow pointers (cycle detection)

**Front:** "linked list — detect cycle / find middle"

**Back:**

```python
slow = fast = head
while fast and fast.next:
    slow = slow.next
    fast = fast.next.next
    if slow is fast: return True  # cycle
return False
# at end: slow = middle (for odd) or upper-middle (for even)
```

---

## 6. Reverse linked list (iterative)

**Front:** "reverse a linked list in place"

**Back:**

```python
prev, curr = None, head
while curr:
    nxt = curr.next
    curr.next = prev
    prev = curr
    curr = nxt
return prev
```

---

## 7. BFS (level order)

**Front:** "shortest path in unweighted graph / level-order traversal"

**Back:**

```python
from collections import deque
q = deque([start])
visited = {start}
level = 0
while q:
    for _ in range(len(q)):
        node = q.popleft()
        if node == target: return level
        for nb in neighbors(node):
            if nb not in visited:
                visited.add(nb)
                q.append(nb)
    level += 1
return -1
```

---

## 8. DFS with backtracking

**Front:** "all permutations / combinations / valid configurations"

**Back:**

```python
def backtrack(path, choices):
    if is_complete(path):
        result.append(path[:])
        return
    for c in choices:
        if not valid(c, path): continue
        path.append(c)
        backtrack(path, next_choices(choices, c))
        path.pop()  # undo
```

---

## 9. Topological sort (Kahn's BFS)

**Front:** "course prerequisites / dependency ordering"

**Back:**

```python
from collections import deque
indeg = [0] * n
for u, v in edges: indeg[v] += 1  # edge u→v
q = deque(i for i in range(n) if indeg[i] == 0)
order = []
while q:
    u = q.popleft()
    order.append(u)
    for v in adj[u]:
        indeg[v] -= 1
        if indeg[v] == 0: q.append(v)
return order if len(order) == n else []  # [] = cycle
```

---

## 10. Dijkstra (single-source shortest path, non-negative)

**Front:** "shortest path with positive edge weights"

**Back:**

```python
import heapq
dist = [float('inf')] * n
dist[src] = 0
pq = [(0, src)]
while pq:
    d, u = heapq.heappop(pq)
    if d > dist[u]: continue
    for v, w in adj[u]:
        if dist[u] + w < dist[v]:
            dist[v] = dist[u] + w
            heapq.heappush(pq, (dist[v], v))
```

---

## 11. Union-Find (path compression + union by rank)

**Front:** "connectivity / cycle detection in undirected graph"

**Back:**

```python
parent = list(range(n))
rank = [0] * n

def find(x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]  # path compression
        x = parent[x]
    return x

def union(a, b):
    ra, rb = find(a), find(b)
    if ra == rb: return False
    if rank[ra] < rank[rb]: ra, rb = rb, ra
    parent[rb] = ra
    if rank[ra] == rank[rb]: rank[ra] += 1
    return True
```

---

## 12. Monotonic stack

**Front:** "next greater / next smaller element"

**Back:**

```python
stack = []  # holds indices
result = [-1] * len(arr)
for i, x in enumerate(arr):
    while stack and arr[stack[-1]] < x:
        result[stack.pop()] = x  # next greater for popped
    stack.append(i)
return result
```

---

## 13. Heap — top K

**Front:** "K largest / smallest elements"

**Back:**

```python
import heapq
heap = []  # min-heap; for top-K largest
for x in arr:
    heapq.heappush(heap, x)
    if len(heap) > k: heapq.heappop(heap)
return heap  # contains K largest
```

---

## 14. Heap — running median (two heaps)

**Front:** "find median from data stream"

**Back:**

```python
import heapq
small, large = [], []  # small: max-heap (negate), large: min-heap

def add(num):
    heapq.heappush(small, -num)
    heapq.heappush(large, -heapq.heappop(small))
    if len(large) > len(small):
        heapq.heappush(small, -heapq.heappop(large))

def median():
    if len(small) > len(large): return -small[0]
    return (-small[0] + large[0]) / 2
```

---

## 15. Trie (string)

**Front:** "prefix matching / many strings sharing prefixes"

**Back:**

```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.end = False

class Trie:
    def __init__(self):
        self.root = TrieNode()
    def insert(self, w):
        node = self.root
        for c in w:
            if c not in node.children: node.children[c] = TrieNode()
            node = node.children[c]
        node.end = True
    def search(self, w):
        node = self.root
        for c in w:
            if c not in node.children: return False
            node = node.children[c]
        return node.end
```

---

## 16. Tree DFS — return tuple of metrics

**Front:** "tree problem needing two values from each subtree (e.g., diameter, balanced)"

**Back:**

```python
def dfs(node):
    if not node: return 0, 0  # height, metric
    lh, lm = dfs(node.left)
    rh, rm = dfs(node.right)
    h = 1 + max(lh, rh)
    m = max(lm, rm, lh + rh)  # combine
    return h, m
return dfs(root)[1]
```

---

## 17. Iterative inorder (BST)

**Front:** "BST traversal in sorted order without recursion"

**Back:**

```python
stack = []
node = root
while stack or node:
    while node:
        stack.append(node)
        node = node.left
    node = stack.pop()
    visit(node)
    node = node.right
```

---

## 18. 1D DP — Kadane (max subarray)

**Front:** "max sum contiguous subarray"

**Back:**

```python
best = current = arr[0]
for x in arr[1:]:
    current = max(x, current + x)
    best = max(best, current)
return best
```

---

## 19. 1D DP — house robber pattern

**Front:** "max value choosing non-adjacent elements"

**Back:**

```python
prev2 = prev1 = 0
for x in arr:
    take = prev2 + x
    skip = prev1
    prev2, prev1 = prev1, max(take, skip)
return prev1
```

---

## 20. 2D DP — edit distance / LCS shape

**Front:** "two sequences, find min edits / longest common"

**Back:**

```python
m, n = len(a), len(b)
dp = [[0] * (n + 1) for _ in range(m + 1)]
for i in range(m + 1): dp[i][0] = i  # base for edit distance
for j in range(n + 1): dp[0][j] = j
for i in range(1, m + 1):
    for j in range(1, n + 1):
        if a[i-1] == b[j-1]:
            dp[i][j] = dp[i-1][j-1]
        else:
            dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])
return dp[m][n]
```

---

## 21. Quickselect (partition-based selection)

**Front:** "Kth largest in O(n) average WITHOUT a heap"

**Back:**

```python
import random
def quickselect(arr, k):  # k = 1-indexed Kth largest
    def partition(lo, hi):
        pivot = arr[random.randint(lo, hi)]
        i = lo
        for j in range(lo, hi + 1):
            if arr[j] > pivot:  # > for largest, < for smallest
                arr[i], arr[j] = arr[j], arr[i]
                i += 1
        return i - 1  # last index of "greater" partition

    lo, hi = 0, len(arr) - 1
    target = k - 1
    while True:
        p = partition(lo, hi)
        if p == target: return arr[p]
        elif p < target: lo = p + 1
        else: hi = p - 1
```

_Note: NC150's Kth Largest Element in Array can be solved this way for the "without heap" follow-up._

---

## 22. Reservoir sampling (single pick)

**Front:** "pick uniform random from stream of unknown size"

**Back:**

```python
import random
chosen = None
for i, item in enumerate(stream):
    if random.randint(0, i) == 0:
        chosen = item
return chosen
```

---

## 23. Boyer-Moore voting

**Front:** "majority element > n/2, O(1) space"

**Back:**

```python
candidate = None
count = 0
for x in nums:
    if count == 0: candidate = x; count = 1
    elif x == candidate: count += 1
    else: count -= 1
return candidate
```

---

## 24. Difference array (range updates)

**Front:** "many +k updates on ranges, then read final state"

**Back:**

```python
diff = [0] * (n + 1)
for L, R, k in updates:
    diff[L] += k
    diff[R + 1] -= k
out = [0] * n
out[0] = diff[0]
for i in range(1, n):
    out[i] = out[i-1] + diff[i]
return out
```

---

## 25. Bitmask DP transition

**Front:** "≤20 elements, visit each once, find optimal"

**Back:**

```python
n = len(items)
FULL = (1 << n) - 1
dp = [[float('inf')] * n for _ in range(1 << n)]
for i in range(n): dp[1 << i][i] = 0
for mask in range(1 << n):
    for i in range(n):
        if not (mask & (1 << i)) or dp[mask][i] == float('inf'): continue
        for j in range(n):
            if mask & (1 << j): continue
            new_mask = mask | (1 << j)
            cost = dp[mask][i] + edge(i, j)
            if cost < dp[new_mask][j]: dp[new_mask][j] = cost
return min(dp[FULL])
```

---

## 26. Bit-trie (max XOR walk)

**Front:** "max XOR pair in array"

**Back:**

```python
# Insert all numbers as bit-paths MSB→LSB into trie {0,1 → child}.
# For each num, walk the trie preferring the OPPOSITE bit at each level.
# That walk yields the partner that maximizes the XOR with num.
# Full code in patterns/bit-trie.md.
```

---

## 27. Sweep line (event deltas)

**Front:** "max overlapping intervals at any point"

**Back:**

```python
events = []
for s, e in intervals:
    events.append((s, +1))
    events.append((e, -1))
events.sort(key=lambda x: (x[0], -x[1]))  # +1 before -1 at same x
active = best = 0
for _, d in events:
    active += d
    best = max(best, active)
return best
```

---

## 28. Segment tree (sum, point update) — see pattern note

**Front:** "range sum with point updates in O(log n)"

**Back:** *Full class is too long for muscle-memory level — see patterns/segment-tree.md. Memorize the *shape*: build (recursive split), update (recurse to leaf, recompute on the way up), query (cover/disjoint/partial trichotomy).*

---

## 29. Bit manipulation tricks

**Front:** "common bit operations cheat sheet"

**Back:**

```python
x & (x - 1)         # clear lowest set bit
x & -x              # isolate lowest set bit
x | (1 << i)        # set bit i
x & ~(1 << i)       # clear bit i
x ^ (1 << i)        # toggle bit i
(x >> i) & 1        # read bit i
bin(x).count('1')   # popcount (Python: int.bit_count() in 3.10+)
```

---

## 30. Rabin-Karp rolling hash (awareness only)

**Front:** "substring search in O(n+m) average — when Python's `in` won't cut it"

**Back:**

```python
# Hash window of length m, slide one char at a time:
#   new_hash = (old_hash - s[i]*BASE^(m-1)) * BASE + s[i+m]   (mod P)
# Compare hash first, then verify chars on collision.
# Use BASE=31 or 257, P=large prime (e.g., 10**9 + 7).
# Bare-bones; for KMP failure-function form, see CLRS Ch 32 or Sedgewick.
```

_Awareness only — Python's `s.find(t)` and `t in s` are usually accepted in interviews. Reach for KMP/Rabin-Karp if asked specifically about substring matching internals._
