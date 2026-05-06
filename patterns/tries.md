# Tries

## Trigger

"Many strings sharing prefixes," "fast prefix lookup," "wildcard / regex-lite search," "search on a board for many words." Tells: explicit "prefix" wording, or repeated lookups against a fixed dictionary.

## Template

```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.end = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for c in word:
            node = node.children.setdefault(c, TrieNode())
        node.end = True

    def search(self, word):
        node = self._walk(word)
        return node is not None and node.end

    def starts_with(self, prefix):
        return self._walk(prefix) is not None

    def _walk(self, s):
        node = self.root
        for c in s:
            if c not in node.children: return None
            node = node.children[c]
        return node
```

## Canonical: [Implement Trie (Prefix Tree)](https://leetcode.com/problems/implement-trie-prefix-tree/)

### Mistakes

- (none yet)

## Variants

### [Design Add and Search Words Data Structure](https://leetcode.com/problems/design-add-and-search-words-data-structure/)

- (none yet) — `.` wildcard branches into all children via DFS

### [Word Search II](https://leetcode.com/problems/word-search-ii/)

- (none yet) — build trie from word list, then DFS the board pruning by trie children

## Why these belong together

A trie is the optimal data structure when the operations involve prefixes. Every variant adds a small twist (wildcards, board search, stream search) on the same node-with-children-dict skeleton.

## Edge cases / invariants

- Use a dict for `children` (sparse) for general inputs; use a 26-array for lowercase-only when speed matters.
- Mark `end = True` only at the FINAL node of `insert`, not at intermediates.
- For Word Search II, prune the trie as you find words to avoid re-traversing dead branches.
