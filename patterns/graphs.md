# Graphs (BFS/DFS, Connected Components, Topo Basics)

## Trigger

"Number of islands," "connected groups," "shortest path in unweighted grid/graph," "ordering with prerequisites." Tells: explicit graph (adj list) or implicit (grid neighbors).

## Template

### DFS on grid

```python
def dfs(r, c):
    if not (0 <= r < rows and 0 <= c < cols) or grid[r][c] != '1':
        return
    grid[r][c] = '#'  # mark visited via mutation
    for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
        dfs(r + dr, c + dc)

count = 0
for r in range(rows):
    for c in range(cols):
        if grid[r][c] == '1':
            dfs(r, c)
            count += 1
```

### BFS on graph (shortest unweighted path)

```python
from collections import deque
q = deque([(start, 0)])
visited = {start}
while q:
    node, d = q.popleft()
    if node == target: return d
    for nb in adj[node]:
        if nb not in visited:
            visited.add(nb)
            q.append((nb, d + 1))
```

### Topological sort (Kahn's, BFS-based)

```python
from collections import deque
indeg = [0] * n
for u, v in edges: indeg[v] += 1
q = deque(i for i in range(n) if indeg[i] == 0)
order = []
while q:
    u = q.popleft()
    order.append(u)
    for v in adj[u]:
        indeg[v] -= 1
        if indeg[v] == 0: q.append(v)
return order if len(order) == n else []  # [] = cycle exists
```

## Canonical: [Number of Islands](https://leetcode.com/problems/number-of-islands/)

### Mistakes

- (none yet)

## Variants

### [Max Area of Island](https://leetcode.com/problems/max-area-of-island/)

- (none yet) — DFS returns area count, take max

### [Clone Graph](https://leetcode.com/problems/clone-graph/)

- (none yet) — BFS with old→new map

### [Walls and Gates](https://leetcode.com/problems/walls-and-gates/)

- (none yet) — multi-source BFS from all gates simultaneously

### [Rotting Oranges](https://leetcode.com/problems/rotting-oranges/)

- (none yet) — multi-source BFS, track minutes elapsed

### [Pacific Atlantic Water Flow](https://leetcode.com/problems/pacific-atlantic-water-flow/)

- (none yet) — DFS from each ocean's borders, intersect

### [Surrounded Regions](https://leetcode.com/problems/surrounded-regions/)

- (none yet) — mark border-connected 'O' as safe, flip the rest

### [Course Schedule](https://leetcode.com/problems/course-schedule/)

- (none yet) — cycle detection via topo

### [Course Schedule II](https://leetcode.com/problems/course-schedule-ii/)

- (none yet) — return topo order

### [Graph Valid Tree](https://leetcode.com/problems/graph-valid-tree/)

- (none yet) — `n-1` edges + connected + no cycle (UF or BFS)

### [Number of Connected Components](https://leetcode.com/problems/number-of-connected-components-in-an-undirected-graph/)

- (none yet) — Union-Find or DFS count

### [Redundant Connection](https://leetcode.com/problems/redundant-connection/)

- (none yet) — UF; the edge that completes a cycle is the answer

### [Word Ladder](https://leetcode.com/problems/word-ladder/)

- (none yet) — BFS over word transformations; precompute pattern → words index for speed

## Why these belong together

Three sub-flavors share infrastructure: traversal (BFS/DFS), connectivity (UF or DFS counting), and topological order (Kahn's). All run on either explicit `adj` lists or implicit grid neighbors. Most graph interview problems are one of these three — the trick is recognizing which.

## Edge cases / invariants

- Visited handling: set OR in-place mutation. Set is cleaner; mutation saves memory but changes input.
- For BFS shortest-path-in-unweighted, distance is "level," not edge weight.
- Topological sort cycle detection: if not all nodes reach `indeg == 0`, there's a cycle.
