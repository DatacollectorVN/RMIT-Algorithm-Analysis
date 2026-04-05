class Node:
    def __init__(self, val):
        self.val = val
        self.next = None
    
    def __str__(self):
        next_val = self.next.val if self.next else None
        return f"Node(val={self.val}, next→{next_val})"


class DLNode:
    def __init__(self, val):
        self.val = val
        self.next = None
        self.prev = None
    
    def __str__(self):
        next_val = self.next.val if self.next else None
        prev_val = self.prev.val if self.prev else None
        return f"DLNode(val={self.val}, prev→{prev_val}, next→{next_val})"