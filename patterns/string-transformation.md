# String Transformation

## Trigger

"Parse the string char-by-char and produce a new one." Tokens, encodings, compressions, base conversions, character mappings with lookahead. If the answer is a transformed version of the input — not a search or count over it — this is the pattern.

## Template

### Char-by-char with index pointer

```python
i, n = 0, len(s)
out = []
while i < n:
    if s[i].isdigit():
        j = i
        while j < n and s[j].isdigit():
            j += 1
        # s[i:j] is the number; advance i = j
        ...
    else:
        out.append(s[i])
        i += 1
return "".join(out)
```

### Stack for nested structure

```python
stack = []
for ch in s:
    if ch == "]":
        chunk = []
        while stack and stack[-1] != "[":
            chunk.append(stack.pop())
        stack.pop()  # drop the "["
        k = ""
        while stack and stack[-1].isdigit():
            k = stack.pop() + k
        stack.append("".join(reversed(chunk)) * int(k))
    else:
        stack.append(ch)
return "".join(stack)
```

### Digit-by-digit with carry (right → left)

```python
i, j, carry = len(a) - 1, len(b) - 1, 0
out = []
while i >= 0 or j >= 0 or carry:
    x = int(a[i]) if i >= 0 else 0
    y = int(b[j]) if j >= 0 else 0
    s = x + y + carry
    out.append(str(s % 10))
    carry = s // 10
    i -= 1; j -= 1
return "".join(reversed(out))
```

## Canonical: [Decode String](https://leetcode.com/problems/decode-string/)

### Mistakes

- (none yet)

## Variants

### [Roman to Integer](https://leetcode.com/problems/roman-to-integer/)

- (none yet) — map char→value; subtract when `val[i] < val[i+1]` (e.g. `IV`, `IX`)

### [Longest Common Prefix](https://leetcode.com/problems/longest-common-prefix/)

- (none yet) — compare char `i` across all strings; stop on mismatch or short string

### [Valid Word Abbreviation](https://leetcode.com/problems/valid-word-abbreviation/)

- (none yet) — two pointers; on a digit in `abbr`, parse the full number and jump `word` by that count. Reject leading zeros.

### [Add Binary](https://leetcode.com/problems/add-binary/)

- (none yet) — digit-by-digit from the right with carry; same shape as add-two-numbers on LL

### [String Compression](https://leetcode.com/problems/string-compression/)

- (none yet) — in-place two pointers: `write` for output index, `read` walks runs

### [Basic Calculator II](https://leetcode.com/problems/basic-calculator-ii/)

- (none yet) — stack holds running terms; on `+/-` push signed number, on `*//` pop and combine

### [String to Integer (atoi)](https://leetcode.com/problems/string-to-integer-atoi/)

- (none yet) — state machine: skip ws → optional sign → digits → stop on non-digit; clamp to int32

### snake_case → camelCase

- (none yet) — walk chars; on `_`, drop it and uppercase the next char

## Why these belong together

The unifying property: input is a string, output is a string, and you traverse the input once. Most are O(n) time and O(n) space. The hard bit is usually a small state machine or a stack for nesting — once you spot which, the code falls out.

## Edge cases / invariants

- Empty string → return empty (don't assume `s[0]` exists).
- Numeric prefixes: parse the full number, don't peel one digit at a time.
- Right-to-left passes (Add Binary, atoi) need an explicit reverse at the end.
- For in-place compression: the read pointer must stay ahead of the write pointer — true because runs of length 1 produce 1 output char, longer runs produce fewer chars than they consume.
