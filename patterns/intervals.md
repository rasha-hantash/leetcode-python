# Intervals

## Trigger

Input is a list of `[start, end]` ranges. Operations: merge, insert, count overlaps, schedule. Almost always: **sort by start (or end), then scan**.

## Template

### Merge overlapping

```python
intervals.sort(key=lambda x: x[0])
merged = [intervals[0]]
for s, e in intervals[1:]:
    if s <= merged[-1][1]:
        merged[-1][1] = max(merged[-1][1], e)
    else:
        merged.append([s, e])
return merged
```

### Min-rooms-required (heap of end times)

```python
import heapq
intervals.sort(key=lambda x: x[0])
heap = []  # end times
for s, e in intervals:
    if heap and heap[0] <= s:
        heapq.heappop(heap)
    heapq.heappush(heap, e)
return len(heap)
```

## Canonical: [Merge Intervals](https://leetcode.com/problems/merge-intervals/)

### Mistakes

- (none yet)

## Variants

### [Insert Interval](https://leetcode.com/problems/insert-interval/)

- (none yet) — three phases: before, overlapping (merge), after

### [Non-overlapping Intervals](https://leetcode.com/problems/non-overlapping-intervals/)

- (none yet) — sort by END; greedy keep earliest-ending non-overlapping

### [Meeting Rooms](https://leetcode.com/problems/meeting-rooms/)

- (none yet) — sort by start; check any consecutive pair overlaps

### [Meeting Rooms II](https://leetcode.com/problems/meeting-rooms-ii/)

- (none yet) — heap of end times; OR sweep-line with +1/-1 (see sweep-line.md)

### [Minimum Interval to Include Each Query](https://leetcode.com/problems/minimum-interval-to-include-each-query/)

- (none yet) — sort intervals + queries; min-heap keyed by interval length

## Why these belong together

Sorted-by-start order makes overlap checks local: only the previous merged-end matters. Sorting by _end_ unlocks classic interval scheduling (greedy keep earliest end). Heap variants fit when you need to track "currently open" intervals.

## Edge cases / invariants

- Closed `[a,b]` vs half-open `[a,b)` matters for the overlap test — `s <= prev_end` vs `s < prev_end`.
- "Min rooms" = max overlap at any point = peak active count.
- For huge-coordinate ranges, use sweep line over events instead of materializing the merged list.
