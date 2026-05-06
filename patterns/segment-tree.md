# Segment Tree / Fenwick Tree (BIT)

## Trigger

"Range query (sum / min / max) on an array with **point updates**." If the array is mutable and you need O(log n) for both update AND range query, this is it. Tells: "given queries of two types: update index i, query sum/min/max on [l, r]."

## Template

### Fenwick Tree (BIT) — simpler, sum-style queries only

```python
class BIT:
    def __init__(self, n):
        self.n = n
        self.tree = [0] * (n + 1)  # 1-indexed

    def update(self, i, delta):  # add delta to index i (0-indexed input)
        i += 1
        while i <= self.n:
            self.tree[i] += delta
            i += i & -i

    def query(self, i):  # prefix sum [0..i]
        i += 1
        s = 0
        while i > 0:
            s += self.tree[i]
            i -= i & -i
        return s

    def range_query(self, l, r):  # inclusive
        return self.query(r) - (self.query(l - 1) if l > 0 else 0)
```

### Segment Tree — more flexible (min/max/custom merge)

```python
class SegTree:
    def __init__(self, arr):
        self.n = len(arr)
        self.tree = [0] * (4 * self.n)
        if arr:
            self._build(arr, 1, 0, self.n - 1)

    def _build(self, arr, node, l, r):
        if l == r:
            self.tree[node] = arr[l]
            return
        mid = (l + r) // 2
        self._build(arr, 2*node, l, mid)
        self._build(arr, 2*node+1, mid+1, r)
        self.tree[node] = self.tree[2*node] + self.tree[2*node+1]

    def update(self, idx, val, node=1, l=0, r=None):
        if r is None: r = self.n - 1
        if l == r:
            self.tree[node] = val
            return
        mid = (l + r) // 2
        if idx <= mid: self.update(idx, val, 2*node, l, mid)
        else: self.update(idx, val, 2*node+1, mid+1, r)
        self.tree[node] = self.tree[2*node] + self.tree[2*node+1]

    def query(self, ql, qr, node=1, l=0, r=None):
        if r is None: r = self.n - 1
        if qr < l or ql > r: return 0
        if ql <= l and r <= qr: return self.tree[node]
        mid = (l + r) // 2
        return self.query(ql, qr, 2*node, l, mid) + self.query(ql, qr, 2*node+1, mid+1, r)
```

## Canonical: [Range Sum Query - Mutable](https://leetcode.com/problems/range-sum-query-mutable/)

### Mistakes

- (none yet)

## Variants

### [Count of Smaller Numbers After Self](https://leetcode.com/problems/count-of-smaller-numbers-after-self/)

- (none yet) — process right-to-left, BIT indexed by sorted-rank

## Why these belong together

Both problems need O(log n) updates + O(log n) range queries. Prefix sums alone give O(1) query but O(n) update; sorted structures give the reverse. Segment tree / BIT splits the difference. BIT is cheaper to write when the operation is sum/XOR (anything invertible). Segment tree is needed for min/max or custom merges.

## Edge cases / invariants

- BIT is 1-indexed internally; remember the `+ 1` shift.
- Segment tree array size = `4 * n` to be safe.
- For range _update + point query_ (less common), use a difference-array view in the BIT.
