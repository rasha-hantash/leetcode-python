# Reservoir Sampling

## Trigger

"Pick a uniformly random element from a stream of unknown size" or "pick K uniformly random." Tells: stream input, can only iterate once, can't store everything in memory.

## Template

### Single sample

```python
import random

def pick(stream_iter):
    chosen = None
    count = 0
    for item in stream_iter:
        count += 1
        # replace `chosen` with prob 1/count
        if random.randint(1, count) == 1:
            chosen = item
    return chosen
```

### K samples (Algorithm R)

```python
def pick_k(stream_iter, k):
    reservoir = []
    for i, item in enumerate(stream_iter):
        if i < k:
            reservoir.append(item)
        else:
            j = random.randint(0, i)
            if j < k:
                reservoir[j] = item
    return reservoir
```

## Canonical: [Linked List Random Node](https://leetcode.com/problems/linked-list-random-node/)

### Mistakes

- (none yet)

## Variants

### [Random Pick with Weight](https://leetcode.com/problems/random-pick-with-weight/)

- (none yet) — different technique (prefix sum + binary search), but lives in the same "random selection" mental bucket

### [Random Pick Index](https://leetcode.com/problems/random-pick-index/)

- (none yet) — single-pass uniform pick among indices matching target

## Why these belong together

The proof: at element `i`, you keep it with probability `1/i`. By induction, every element seen so far has probability `1/n` after n elements. This argument is the whole pattern — once you see "stream of unknown size" or "you can only iterate once," reach for it.

## Edge cases / invariants

- `random.randint(1, count) == 1` is one common idiom; `random.randrange(count) == 0` is equivalent.
- For weighted variants, reservoir sampling generalizes (Algorithm A-Res) but the prefix-sum approach is usually simpler when the weights are static.
