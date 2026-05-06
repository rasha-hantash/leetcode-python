# Sweep Line (event-based deltas)

## Trigger

"Max overlapping intervals at any point," "skyline of buildings," "number of concurrent meetings/calls/bookings." Generally: when interval start/end can be modeled as +1/-1 events processed in sorted order with a running counter or running data structure.

## Template

```python
def max_overlap(intervals):
    events = []
    for start, end in intervals:
        events.append((start, +1))
        events.append((end, -1))
    # sort by time; for ties, end (-1) before start (+1) if endpoints don't count as overlap
    # OR start (+1) before end (-1) if endpoints DO count as overlap
    events.sort(key=lambda e: (e[0], -e[1]))  # +1 before -1 for closed intervals

    active = 0
    max_active = 0
    for _, delta in events:
        active += delta
        max_active = max(max_active, active)
    return max_active
```

## Canonical: [My Calendar III](https://leetcode.com/problems/my-calendar-iii/)

### Mistakes

- (none yet)

## Variants

### [The Skyline Problem](https://leetcode.com/problems/the-skyline-problem/)

- (none yet) — events are (x, +height, -height); use a max-heap keyed by height with lazy deletion

## Why these belong together

Each interval contributes a `+1` at its start and a `-1` just past its end. Sort the events by position, scan once with a running counter — overlap count at any x is just the running sum. Distinct from heap-based Meeting Rooms II (NC150) because sweep extends naturally to multi-dimensional problems (skyline) and to range-aggregate queries the heap approach can't express cleanly.

## Edge cases / invariants

- Tie-breaking matters: for closed intervals `[a,b]` (b counts as overlap), process +1 before -1 at same x. For half-open `[a,b)`, process -1 first.
- Sweep is O(n log n) for the sort, O(n) for the scan.
- Online variants need a balanced BST (Python: `sortedcontainers.SortedList`) instead of a sorted events array.
