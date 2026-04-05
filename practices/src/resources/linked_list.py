# Class to define a Node
class Node:
    def __init__(self, val):
        self.val = val  # Data stored in the node
        self.next = None  # Pointer to the next node
    
    def __str__(self):
        next_val = self.next.val if self.next else None
        return f"Node(val={self.val}, next→{next_val})"


class RMITSinglyLList:
    """Singly linked list with head pointer; supports build, insert, delete, traverse."""

    def __init__(self, values: list):
        self.head: Node | None = None
        if not values:
            return
        
        it = iter(values)
        self.head = Node(next(it))
        curr: Node = self.head
        for v in it:
            curr.next = Node(v)
            # type hinting the current node to the next node
            curr = curr.next

    def traverse(self):
        curr: Node | None = self.head
        while curr:
            print(curr.val, end=" → ")
            curr = curr.next
        print("NULL")
    
    def get_node(self, position: int) -> Node:
        curr: Node | None = self.head
        for _ in range(position):
            if not curr:
                raise ValueError(f"Position {position} is out of bounds")
            curr = curr.next
        return curr

    def _insert_at_beginning(self, new_node: Node):
        # link the new node to the current head
        new_node.next = self.head 
        # update the head to the new node
        self.head = new_node
    
    def insert(self, val: any, position: int):
        new_node = Node(val)
        if position == 0:
            self._insert_at_beginning(new_node)
            return
        
        # Find the previous node before the insertion point
        prev_node = self.get_node(position - 1)
        if not prev_node:
            raise ValueError(f"Previous node at position {position - 1} is out of bounds")
        
        # link the new node to the next node of the previous node
        new_node.next = prev_node.next
        # link the previous node to the new node
        prev_node.next = new_node
    
    def delete(self, position: int):
        if position == 0:
            self.head = self.head.next
            return
        
        # Find the previous node before the deletion point
        prev_node = self.get_node(position - 1)
        if not prev_node:
            raise ValueError(f"Previous node at position {position - 1} is out of bounds")
        
        # link the previous node to the next node of the target node
        prev_node.next = prev_node.next.next


class DLNode:
    def __init__(self, val):
        self.val = val
        self.next = None
        self.prev = None
    
    def __str__(self):
        next_val = self.next.val if self.next else None
        prev_val = self.prev.val if self.prev else None
        return f"DLNode(val={self.val}, prev→{prev_val}, next→{next_val})"


class RMITDoublyLList:
    """Doubly linked list with head and tail pointers; supports build, insert, delete, traverse."""
    def __init__(self, values: list):
        self.head: DLNode | None = None
        if not values:
            return
        
        it = iter(values)
        self.head = DLNode(next(it))
        curr: DLNode = self.head
        for v in it:
            curr.next = DLNode(v)
            curr.next.prev = curr
            curr = curr.next
    
    def traverse(self, is_forward: bool = True):
        curr: DLNode | None = self.head
        if not curr:
            print("List is empty!")
            return
            
        if is_forward:
            while curr and curr.next:
                print(curr.val, end=" ⇄ ")
                curr = curr.next
            print(curr.val, end=" ⇄ NULL\n")
        else:
            # reach the tail node
            while curr.next:
                curr = curr.next

            # traverse backwards using the prev pointer
            while curr and curr.prev:
                print(curr.val, end=" ⇄ ")
                curr = curr.prev
            print(curr.val, end=" ⇄ NULL\n")
    
    def get_node(self, position: int) -> DLNode:
        curr: DLNode | None = self.head
        for _ in range(position):
            if not curr:
                raise ValueError(f"Position {position} is out of bounds")
            curr = curr.next
        return curr
    
    def _insert_at_beginning(self, new_node: DLNode):
        new_node.next = self.head
        self.head.prev = new_node
        self.head = new_node

    def insert(self, val: any, position: int):
        if not self.head:
            raise ValueError("Node is empty!")
        
        new_node = DLNode(val)
        if position == 0:
            self._insert_at_beginning(new_node)
            return
        
        prev_node = self.get_node(position - 1)
        new_node.next = prev_node.next 
        if prev_node.next is not None: # If not inserting at the end,
            prev_node.next.prev = new_node # update that node's prev pointer to the new node.
        prev_node.next = new_node # Link prev to the new node.
        new_node.prev = prev_node # New node's prev pointer points back to prev.

    def delete(self, position: int):
        if not self.head:
            raise ValueError("Node is empty!")
        
        # If deleting the first node
        if position == 0:
            self.head = self.head.next
            if self.head:
                self.head.prev = None
            return
        
        # Find the previous node before the deletion point
        prev_node = self.get_node(position - 1)
        if not prev_node:
            raise ValueError(f"Previous node at position {position - 1} is out of bounds")
        
        # Delete the target node.
        target_node = prev_node.next           # Node to be deleted.
        prev_node.next = target_node.next      # Link previous node to target's next.
        if target_node.next is not None:  # If target is not the last node.
            target_node.next.prev = prev_node  # Update next node's prev pointer.


class RMTCircularLinkedList():
    def __init__(self, values: list):
        self.head: Node | None = None
        self.tail: Node | None = None
        if not values:
            return

        it = iter(values)
        self.head = Node(next(it))
        curr: Node = self.head
        for v in it:
            curr.next = Node(v)
            curr = curr.next
        self.tail = curr
        self.tail.next = self.head

    def traverse(self):
        if not self.head:
            print("(empty)")
            return
        curr: Node = self.head
        while True:
            print(curr.val, end=" → ")
            curr = curr.next
            if curr == self.head:
                break
        print("(head)")

    def get_node(self, position: int) -> Node:
        if not self.head:
            raise ValueError("List is empty")
        curr: Node = self.head
        for _ in range(position):
            curr = curr.next
            if curr == self.head:
                raise ValueError(f"Position {position} is out of bounds")
        return curr

    def _insert_at_beginning(self, new_node: Node):
        new_node.next = self.head
        self.tail.next = new_node
        self.head = new_node

    def insert(self, val: any, position: int):
        new_node = Node(val)
        if not self.head:
            new_node.next = new_node
            self.head = new_node
            self.tail = new_node
            return

        if position == 0:
            self._insert_at_beginning(new_node)
            return

        prev_node = self.get_node(position - 1)
        new_node.next = prev_node.next
        prev_node.next = new_node
        if prev_node == self.tail:
            self.tail = new_node

    def delete(self, position: int):
        if not self.head:
            raise ValueError("List is empty")

        # Single node
        if self.head == self.tail:
            self.head = None
            self.tail = None
            return

        if position == 0:
            self.head = self.head.next
            self.tail.next = self.head
            return

        prev_node = self.get_node(position - 1)
        if prev_node.next == self.head:
            raise ValueError(f"Position {position} is out of bounds")

        target_node = prev_node.next
        prev_node.next = target_node.next
        if target_node == self.tail:
            self.tail = prev_node

    def get_head(self) -> Node:
        if not self.head:
            raise ValueError("List is empty")
        return self.head
    
    def get_tail(self) -> Node:
        if not self.tail:
            raise ValueError("List is empty")
        return self.tail


if __name__ == "__main__":
    print("=== RMITSinglyLList Tests ===")
    llist = RMITSinglyLList([1, 2, 3, 4, 5])
    llist.traverse()
    print(llist.get_node(2))
    llist.insert(10, 2)
    llist.traverse()
    llist.delete(0)
    llist.traverse()
    llist.delete(2)
    llist.traverse()

    print("=== RMITDoublyLList Tests ===")
    dlist = RMITDoublyLList([1, 2, 3, 4, 5])
    dlist.traverse()
    print(dlist.get_node(2))
    dlist.insert(10, 2)
    dlist.traverse()
    dlist.delete(0)
    dlist.traverse()
    dlist.delete(2)
    dlist.traverse()

    print("=== RMTCircularLinkedList Tests ===")
    clist = RMTCircularLinkedList([1, 2, 3, 4, 5])
    clist.traverse()
    print(clist.get_node(2))
    clist.insert(10, 2)
    clist.traverse()
    clist.delete(0)
    clist.traverse()
    clist.delete(2)
    clist.traverse()