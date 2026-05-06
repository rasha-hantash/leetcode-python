# Math & Geometry

## Trigger

Matrix manipulation (rotate, spiral, set-zeroes), arithmetic identities (powers, repeated digits), grid geometry (squares, points). Pattern: small clever observation + careful indexing.

## Template

### Spiral traversal (4 directions, layer-by-layer)

```python
result = []
top, bot, left, right = 0, len(m)-1, 0, len(m[0])-1
while top <= bot and left <= right:
    for c in range(left, right+1): result.append(m[top][c])
    top += 1
    for r in range(top, bot+1): result.append(m[r][right])
    right -= 1
    if top <= bot:
        for c in range(right, left-1, -1): result.append(m[bot][c])
        bot -= 1
    if left <= right:
        for r in range(bot, top-1, -1): result.append(m[r][left])
        left += 1
return result
```

### Rotate 90° in place (transpose + reverse rows)

```python
n = len(m)
for i in range(n):
    for j in range(i+1, n):
        m[i][j], m[j][i] = m[j][i], m[i][j]
for row in m:
    row.reverse()
```

### Fast power

```python
def pow_iter(x, n):
    if n < 0: x, n = 1/x, -n
    result = 1.0
    while n:
        if n & 1: result *= x
        x *= x
        n >>= 1
    return result
```

## Canonical: [Spiral Matrix](https://leetcode.com/problems/spiral-matrix/)

### Mistakes

- (none yet)

## Variants

### [Rotate Image](https://leetcode.com/problems/rotate-image/)

- (none yet) — transpose + reverse rows

### [Set Matrix Zeroes](https://leetcode.com/problems/set-matrix-zeroes/)

- (none yet) — use first row/col as marker buffers (O(1) space)

### [Happy Number](https://leetcode.com/problems/happy-number/)

- (none yet) — Floyd's cycle detection on digit-square sum

### [Plus One](https://leetcode.com/problems/plus-one/)

- (none yet) — carry propagation

### [Pow(x, n)](https://leetcode.com/problems/powx-n/)

- (none yet) — fast power by halving exponent

### [Multiply Strings](https://leetcode.com/problems/multiply-strings/)

- (none yet) — schoolbook multiplication, position math

### [Detect Squares](https://leetcode.com/problems/detect-squares/)

- (none yet) — counter of points; for each diagonal candidate, multiply counts of the two corners

## Why these belong together

These problems aren't really "an algorithm" — they're careful math/indexing. The wins come from observing structure (rotation = transpose + reverse, spiral = layer peeling, fast power = exponent halving) rather than from a generic technique.

## Edge cases / invariants

- Spiral: guard with `if top <= bot` and `if left <= right` for the third/fourth directions when the matrix is single-row or single-col.
- Set Matrix Zeroes O(1): track the first row/col separately since they're used as markers.
- For pow with negative n, flip to `1/x` and make `n` positive — careful about integer overflow (not an issue in Python but a real one elsewhere).
