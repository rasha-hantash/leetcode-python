# Advanced Graphs (Dijkstra, MST, Topo with Constraints)

## Trigger

"Shortest path with **weighted** edges," "minimum spanning tree," "constrained traversal" (e.g., at most K stops), "Eulerian path / itinerary." Past basic BFS/DFS — now edge weights, custom orderings, or budget constraints matter.

## Template

### Dijkstra (single-source, non-negative weights)

```python
import heapq
dist = [float('inf')] * n
dist[src] = 0
pq = [(0, src)]
while pq:
    d, u = heapq.heappop(pq)
    if d > dist[u]: continue
    for v, w in adj[u]:
        nd = d + w
        if nd < dist[v]:
            dist[v] = nd
            heapq.heappush(pq, (nd, v))
```

### Prim's MST

```python
import heapq
visited = {0}
pq = [(w, 0, v) for v, w in adj[0]]
heapq.heapify(pq)
total = 0
while pq and len(visited) < n:
    w, _, v = heapq.heappop(pq)
    if v in visited: continue
    visited.add(v)
    total += w
    for nb, nw in adj[v]:
        if nb not in visited:
            heapq.heappush(pq, (nw, v, nb))
```

### Bellman-Ford-style with K-edge limit

```python
# K stops = K+1 edges
dist = [float('inf')] * n
dist[src] = 0
for _ in range(K + 1):
    new_dist = dist[:]
    for u, v, w in edges:
        if dist[u] + w < new_dist[v]:
            new_dist[v] = dist[u] + w
    dist = new_dist
```

## Canonical: [Network Delay Time](https://leetcode.com/problems/network-delay-time/)

### Mistakes

- (none yet)

## Variants

### [Reconstruct Itinerary](https://leetcode.com/problems/reconstruct-itinerary/)

- (none yet) — Hierholzer's: DFS, append to result on backtrack, reverse

### [Min Cost to Connect All Points](https://leetcode.com/problems/min-cost-to-connect-all-points/)

- (none yet) — Prim's MST on Manhattan distances

### [Swim in Rising Water](https://leetcode.com/problems/swim-in-rising-water/)

- (none yet) — Dijkstra where "distance" is max cell value seen

### [Alien Dictionary](https://leetcode.com/problems/alien-dictionary/)

- (none yet) — derive edges from adjacent word pairs, topological sort

### [Cheapest Flights Within K Stops](https://leetcode.com/problems/cheapest-flights-within-k-stops/)

- (none yet) — Bellman-Ford with K+1 iterations OR Dijkstra with `(cost, node, stops_used)` state

## Why these belong together

These are weighted/constrained graph problems where vanilla BFS/DFS doesn't cut it. Dijkstra for non-negative weights, Bellman-Ford when constraints exist or weights might be negative, Prim's/Kruskal's for MST, Hierholzer's for Eulerian paths. The right algorithm is signaled by: "weighted? non-negative? bounded path length?"

## Edge cases / invariants

- Dijkstra: skip stale heap entries with `if d > dist[u]: continue`.
- Bellman-Ford with edge-count cap: copy `dist` per iteration, otherwise an edge can be used multiple times in a single pass.
- For "K stops" interpret carefully — K stops = K+1 edges.
