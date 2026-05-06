# Bit Manipulation

## Trigger

"XOR cancellation," "count set bits," "encode multiple flags compactly," "no extra memory." If the problem screams O(1) space or fancy tricks, look at bits.

## Template

### Common operations

```python
x & (x - 1)          # clear lowest set bit
x & -x               # isolate lowest set bit
x | (1 << i)         # set bit i
x & ~(1 << i)        # clear bit i
x ^ (1 << i)         # toggle bit i
(x >> i) & 1         # read bit i
bin(x).count('1')    # popcount (or x.bit_count() in 3.10+)
```

### Single number (XOR)

```python
result = 0
for x in nums:
    result ^= x
return result  # XOR of all = lone number, since pairs cancel
```

### Add without `+`

```python
def add(a, b):
    MASK = 0xFFFFFFFF
    while b:
        carry = ((a & b) << 1) & MASK
        a = (a ^ b) & MASK
        b = carry
    # Python: handle the sign manually
    return a if a < 0x80000000 else ~(a ^ MASK)
```

## Canonical: [Single Number](https://leetcode.com/problems/single-number/)

### Mistakes

- (none yet)

## Variants

### [Number of 1 Bits](https://leetcode.com/problems/number-of-1-bits/)

- (none yet) — `x &= x-1` until 0, count iterations

### [Counting Bits](https://leetcode.com/problems/counting-bits/)

- (none yet) — `dp[i] = dp[i >> 1] + (i & 1)`

### [Reverse Bits](https://leetcode.com/problems/reverse-bits/)

- (none yet) — shift result left, OR in lowest bit of input, shift input right

### [Missing Number](https://leetcode.com/problems/missing-number/)

- (none yet) — XOR all 0..n + all elements; result = missing

### [Sum of Two Integers](https://leetcode.com/problems/sum-of-two-integers/)

- (none yet) — XOR for sum-without-carry, AND<<1 for carry, repeat

### [Reverse Integer](https://leetcode.com/problems/reverse-integer/) `T2`

- (none yet) — pop digits via `% 10`, push via `* 10`, watch overflow bounds

## Why these belong together

The unifying property: bits are a representation choice. XOR is both "addition mod 2" and "find the odd one out." A bitset can encode a small subset in a single integer (basis of bitmask DP). Most bit-manip problems are short — under 20 lines — but rely on knowing the right identity.

## Edge cases / invariants

- For "appears twice except one" → XOR all (Single Number).
- For "appears thrice except one" → bitwise count mod 3 per position.
- Python integers are arbitrary precision — bit tricks that depend on overflow (Sum of Two Integers) need explicit 32-bit masking.
