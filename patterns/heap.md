# Heap / Priority Queue

## Trigger

"Top K," "K-th largest," "running median," "schedule by priority," "merge K sorted streams." The signal is "I need quick access to the extremum, repeatedly, while elements are coming and going."

## Template

### Top-K largest (size-bounded min-heap)

```python
import heapq
heap = []
for x in arr:
    heapq.heappush(heap, x)
    if len(heap) > k:
        heapq.heappop(heap)
return heap  # contains K largest, smallest at heap[0]
```

### Custom comparator via tuples

```python
# Python heapq is a min-heap. For max-heap, negate.
# For multi-key, use tuples; ties broken by next field.
heapq.heappush(heap, (-priority, idx, item))
```

### Two heaps for running median

```python
small, large = [], []  # small: max-heap (negated), large: min-heap

def add(num):
    heapq.heappush(small, -num)
    heapq.heappush(large, -heapq.heappop(small))
    if len(large) > len(small):
        heapq.heappush(small, -heapq.heappop(large))

def median():
    if len(small) > len(large): return -small[0]
    return (-small[0] + large[0]) / 2
```

## Canonical: [Kth Largest Element in a Stream](https://leetcode.com/problems/kth-largest-element-in-a-stream/)

### Mistakes

- (none yet)

## Variants

### [Last Stone Weight](https://leetcode.com/problems/last-stone-weight/)

- (none yet) — repeatedly pop two largest

### [K Closest Points to Origin](https://leetcode.com/problems/k-closest-points-to-origin/)

- (none yet) — size-K max-heap by negated distance

### [Kth Largest Element in an Array](https://leetcode.com/problems/kth-largest-element-in-an-array/)

- (none yet) — heap, OR quickselect (see templates.md)

### [Task Scheduler](https://leetcode.com/problems/task-scheduler/)

- (none yet) — max-heap of counts + cooldown queue

### [Design Twitter](https://leetcode.com/problems/design-twitter/)

- (none yet) — merge K user feeds via heap

### [Find Median from Data Stream](https://leetcode.com/problems/find-median-from-data-stream/)

- (none yet) — two-heap split

## Why these belong together

A heap costs O(log n) per push/pop and gives O(1) peek at the extremum. That tradeoff is the right call whenever you need the "next best" item repeatedly. K-bounded heaps stay at O(n log k) — the classic Top-K play.

## Edge cases / invariants

- Python `heapq` is a **min-heap only**. For max behavior, negate or wrap.
- For tie-breaking, push a tuple — Python compares lexicographically.
- For non-comparable payloads (unhashable dicts, etc.), inject a unique counter as the tie-breaker before the payload.
