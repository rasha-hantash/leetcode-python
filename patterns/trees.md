# Trees (Binary / BST)

## Trigger

`TreeNode` input, recursion smell, "validate / traverse / find LCA / measure depth." DFS for most metrics, BFS for level-order.

## Template

### DFS returning multiple metrics from each subtree

```python
def dfs(node):
    if not node: return 0, 0  # height, metric (e.g., diameter contribution)
    lh, lm = dfs(node.left)
    rh, rm = dfs(node.right)
    h = 1 + max(lh, rh)
    m = max(lm, rm, lh + rh)  # combine across the subtree boundary
    return h, m
return dfs(root)[1]
```

### BFS level order

```python
from collections import deque
q = deque([root])
levels = []
while q:
    level = []
    for _ in range(len(q)):
        node = q.popleft()
        level.append(node.val)
        if node.left: q.append(node.left)
        if node.right: q.append(node.right)
    levels.append(level)
return levels
```

### BST property — inorder gives sorted

```python
def validate(node, lo=float('-inf'), hi=float('inf')):
    if not node: return True
    if not lo < node.val < hi: return False
    return validate(node.left, lo, node.val) and validate(node.right, node.val, hi)
```

## Canonical: [Maximum Depth of Binary Tree](https://leetcode.com/problems/maximum-depth-of-binary-tree/)

### Mistakes

- (none yet)

## Variants

### [Invert Binary Tree](https://leetcode.com/problems/invert-binary-tree/)

- (none yet) — swap children, recurse

### [Diameter of Binary Tree](https://leetcode.com/problems/diameter-of-binary-tree/)

- (none yet) — return height, update global diameter at each node

### [Balanced Binary Tree](https://leetcode.com/problems/balanced-binary-tree/)

- (none yet) — return height OR -1 sentinel for unbalanced

### [Same Tree](https://leetcode.com/problems/same-tree/)

- (none yet)

### [Subtree of Another Tree](https://leetcode.com/problems/subtree-of-another-tree/)

- (none yet)

### [Lowest Common Ancestor of BST](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-search-tree/)

- (none yet) — split-point where p, q diverge

### [Binary Tree Level Order Traversal](https://leetcode.com/problems/binary-tree-level-order-traversal/)

- (none yet)

### [Binary Tree Right Side View](https://leetcode.com/problems/binary-tree-right-side-view/)

- (none yet) — last node of each BFS level

### [Count Good Nodes in Binary Tree](https://leetcode.com/problems/count-good-nodes-in-binary-tree/)

- (none yet) — DFS passing max-so-far down

### [Validate Binary Search Tree](https://leetcode.com/problems/validate-binary-search-tree/)

- (none yet)

### [Kth Smallest Element in a BST](https://leetcode.com/problems/kth-smallest-element-in-a-bst/)

- (none yet) — iterative inorder, count to k

### [Construct Binary Tree from Preorder and Inorder](https://leetcode.com/problems/construct-binary-tree-from-preorder-and-inorder-traversal/)

- (none yet) — root from preorder, partition inorder, recurse

### [Binary Tree Maximum Path Sum](https://leetcode.com/problems/binary-tree-maximum-path-sum/)

- (none yet) — return max-gain-from-this-node, update global max

### [Serialize and Deserialize Binary Tree](https://leetcode.com/problems/serialize-and-deserialize-binary-tree/)

- (none yet) — preorder with null markers

## Why these belong together

Recursive tree problems share a structure: combine answers from left + right, sometimes return multiple values. BSTs add the inorder = sorted invariant. BFS unlocks level-aware problems. The decision is almost always: DFS or BFS? DFS for most metrics (single-path), BFS for level-related ones.

## Edge cases / invariants

- Always handle `if not node: return ...` first.
- For "max path through a node," return one-sided gain to the parent but update a global with both-sided.
- BST validation: bounds `(lo, hi)` not just `node.left.val < node.val` (the violation can be deeper).
