# Linked List

## Trigger

Anything operating on a `ListNode` chain — reverse, merge, detect cycle, reorder, partition, or design (LRU). Two recurring sub-tools: **dummy head** for clean insertions, **fast/slow pointers** for finding middles or cycles.

## Template

### Reverse in place

```python
prev, curr = None, head
while curr:
    nxt = curr.next
    curr.next = prev
    prev = curr
    curr = nxt
return prev
```

### Dummy head (insertion / merge)

```python
dummy = ListNode(0)
tail = dummy
while a and b:
    if a.val < b.val: tail.next, a = a, a.next
    else: tail.next, b = b, b.next
    tail = tail.next
tail.next = a or b
return dummy.next
```

### Fast/slow (middle, cycle)

```python
slow = fast = head
while fast and fast.next:
    slow = slow.next
    fast = fast.next.next
# slow is middle (or "upper middle" for even length)
```

## Canonical: [Reverse Linked List](https://leetcode.com/problems/reverse-linked-list/)

### Mistakes

- (none yet)

## Variants

### [Merge Two Sorted Lists](https://leetcode.com/problems/merge-two-sorted-lists/)

- (none yet) — dummy head idiom

### [Linked List Cycle](https://leetcode.com/problems/linked-list-cycle/)

- (none yet) — fast/slow

### [Reorder List](https://leetcode.com/problems/reorder-list/)

- (none yet) — split at middle, reverse second half, weave

### [Remove Nth Node From End](https://leetcode.com/problems/remove-nth-node-from-end-of-list/)

- (none yet) — two-pointer with N-gap

### [Copy List with Random Pointer](https://leetcode.com/problems/copy-list-with-random-pointer/)

- (none yet) — interleave clones, then split

### [Add Two Numbers](https://leetcode.com/problems/add-two-numbers/)

- (none yet) — carry propagation

### [Find the Duplicate Number](https://leetcode.com/problems/find-the-duplicate-number/)

- (none yet) — Floyd's cycle detection on indexes-as-pointers

### [LRU Cache](https://leetcode.com/problems/lru-cache/)

- (none yet) — doubly linked list + hashmap

### [Merge K Sorted Lists](https://leetcode.com/problems/merge-k-sorted-lists/)

- (none yet) — min-heap of head pointers, OR pairwise merge

### [Reverse Nodes in K-Group](https://leetcode.com/problems/reverse-nodes-in-k-group/)

- (none yet) — reverse-helper invoked per group, stitch back

## Why these belong together

Operations on a linked list rarely need the rest of CS — they need careful pointer choreography and a couple of recurring tricks (dummy head, fast/slow). The bugs are almost always pointer-update order or null-checks at the boundary.

## Edge cases / invariants

- Always save `next` before rewriting `curr.next` — otherwise you lose the rest of the list.
- Dummy head spares you "is it the first node?" branching for any problem that inserts/removes.
- Fast/slow termination: `while fast and fast.next` (need both to take the second hop).
