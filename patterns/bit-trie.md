# Bit-Trie (XOR maximization)

## Trigger

"Find pair (x, y) in array maximizing `x XOR y`." Or any problem where you process numbers bit-by-bit MSB→LSB and want the _opposite_ bit at each step to be greedy-optimal.

## Template

```python
class BitTrie:
    def __init__(self, max_bits=31):
        self.root = {}
        self.max_bits = max_bits

    def insert(self, num):
        node = self.root
        for i in range(self.max_bits, -1, -1):
            b = (num >> i) & 1
            if b not in node:
                node[b] = {}
            node = node[b]

    def max_xor_with(self, num):
        node = self.root
        result = 0
        for i in range(self.max_bits, -1, -1):
            b = (num >> i) & 1
            opposite = 1 - b
            if opposite in node:
                result |= (1 << i)
                node = node[opposite]
            else:
                node = node[b]
        return result

def find_max_xor(nums):
    trie = BitTrie()
    for n in nums: trie.insert(n)
    return max(trie.max_xor_with(n) for n in nums)
```

## Canonical: [Maximum XOR of Two Numbers in an Array](https://leetcode.com/problems/maximum-xor-of-two-numbers-in-an-array/)

### Mistakes

- (none yet)

## Variants

### [Maximum XOR With an Element From Array](https://leetcode.com/problems/maximum-xor-with-an-element-from-array/)

- (none yet) — offline queries sorted by limit, insert into trie as you go

## Why these belong together

The trick: at each bit position MSB→LSB, you greedily prefer the _opposite_ bit because that contributes `2^i` to the XOR — and since higher bits dominate, locking in a high bit early is always correct. Regular tries don't have this greedy-walk property; bit manipulation alone doesn't have the trie's per-bit decision tree.

## Edge cases / invariants

- 32 bits for typical signed-int LeetCode constraints (`max_bits=31` covers `0..2^31-1`).
- Walk from MSB down — reversing the order breaks the greedy.
- O(32n) time, O(32n) space.
