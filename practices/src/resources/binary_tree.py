"""
Binary Search Tree (BST): for each node, left subtree values are smaller, right subtree larger.
"""


class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


class RMITBST:
    def __init__(self, values=None):
        self.root = None
        if values:
            for v in values:
                self.insert(v)

    def insert(self, val):
        """Insert a value; duplicates are ignored with a message."""
        self.root = self._insert(self.root, val)

    def _insert(self, node, val):
        if node is None:
            return TreeNode(val)
        if val < node.val:
            node.left = self._insert(node.left, val)
        elif val > node.val:
            node.right = self._insert(node.right, val)
        else:
            print(f"{val} already in tree; skipped.")
        return node

    def search(self, val):
        """Return True if val is in the tree."""
        return self._search(self.root, val)

    def _search(self, node, val):
        if node is None:
            return False
        if val == node.val:
            return True
        if val < node.val:
            return self._search(node.left, val)
        return self._search(node.right, val)

    def delete(self, val):
        """Remove val if present; otherwise print not found."""
        self.root = self._delete(self.root, val)

    def _delete(self, node, val):
        if node is None:
            print(f"{val} not found.")
            return None
        if val < node.val:
            node.left = self._delete(node.left, val)
        elif val > node.val:
            node.right = self._delete(node.right, val)
        else:
            # Node to remove
            if node.left is None:
                return node.right
            if node.right is None:
                return node.left
            # Two children: replace value with inorder successor (min of right subtree)
            succ = self._min_node(node.right)
            node.val = succ.val
            node.right = self._delete(node.right, succ.val)
        return node

    def _min_node(self, node):
        while node.left is not None:
            node = node.left
        return node

    def inorder(self):
        """Left → root → right (prints sorted order for a valid BST)."""
        self._inorder(self.root)
        print()

    def _inorder(self, node):
        if node is None:
            return
        self._inorder(node.left)
        print(node.val, end=" ")
        self._inorder(node.right)

    def preorder(self):
        """Root → left → right."""
        self._preorder(self.root)
        print()

    def _preorder(self, node):
        if node is None:
            return
        print(node.val, end=" ")
        self._preorder(node.left)
        self._preorder(node.right)

    def postorder(self):
        """Left → right → root."""
        self._postorder(self.root)
        print()

    def _postorder(self, node):
        if node is None:
            return
        self._postorder(node.left)
        self._postorder(node.right)
        print(node.val, end=" ")


if __name__ == "__main__":
    t = RMITBST([50, 30, 70, 20, 40, 60, 80])
    print("Inorder:  ", end="")
    t.inorder()
    print("Search 40:", t.search(40))
    t.delete(30)
    print("After delete 30, inorder:", end="")
    t.inorder()