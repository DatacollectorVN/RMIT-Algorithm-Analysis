class DLNode:
    def __init__(self, val):
        self.val = val     
        self.prev = None   
        self.next = None   


# Linked List class with traversal methods
class RMITDoubleLinkedList:
    def __init__(self):
        self.head = None  # Head pointer of the doubly linked list

    # Forward traversal: Visit each node from head to tail.
    def traverseForward(self):
        current = self.head  # Start at the head
        while current:
            print(current.val, "⇄", end=" ")  # Print current node's value
            current = current.next            # Move to the next node
        print("NULL")  # End marker

    # Reverse traversal: Visit each node from tail to head.
    def traverseBackward(self):
        if self.head is None:
            print("List is empty!")
            return
        current = self.head
        # Traverse to the tail
        while current.next:
            current = current.next
        # Traverse backwards using the 'prev' pointer
        while current:
            print(current.val, "⇄", end=" ")
            current = current.prev
        print("NULL")
    
    # Method to insert a node at a specific position.
    def insertAtPosition(self, val, position):
        new_node = DLNode(val)  # Create a new node with the given value.

        # If inserting at the beginning:
        if position == 0:
            new_node.next = self.head          # Link new node to current head.
            if self.head is not None:
                self.head.prev = new_node      # Update current head's prev pointer.
            self.head = new_node               # Update head to new node.
            return

        # Find the node at (position - 1).
        prev = self.head
        for _ in range(position - 1):
            if prev is None:
                print("Invalid Position!")
                return
            prev = prev.next

        # Check if the position is invalid.
        if prev is None:
            print("Invalid Position!")
            return

        # Insert the new node between prev and prev.next.
        new_node.next = prev.next            # New node points to the node that was after prev.
        if prev.next is not None:            # If not inserting at the end,
            prev.next.prev = new_node        # update that node's prev pointer to the new node.
        prev.next = new_node                 # Link prev to the new node.
        new_node.prev = prev                 # New node's prev pointer points back to prev.

    # Method to delete a node at a specific position.
    def deleteAtPosition(self, position):
        # If list is empty.
        if self.head is None:
            print("List is empty!")
            return

        # If deleting the first node.
        if position == 0:
            self.head = self.head.next  # Update head to next node.
            if self.head is not None:
                self.head.prev = None   # Set new head's prev pointer to None.
            return

        # Traverse to find the node at (position - 1).
        prev = self.head
        for _ in range(position - 1):
            if prev is None:
                print("Invalid Position!")
                return
            prev = prev.next

        # Check for invalid position.
        if prev is None or prev.next is None:
            print("Invalid Position!")
            return

        # Delete the target node.
        target = prev.next           # Node to be deleted.
        prev.next = target.next      # Link previous node to target's next.
        if target.next is not None:  # If target is not the last node.
            target.next.prev = prev  # Update next node's prev pointer.

# Main function to create and traverse the doubly linked list
if __name__ == "__main__":
    list = RMITDoubleLinkedList()

    # Creating initial doubly linked list: 10 ⇄ 20 ⇄ 30 ⇄ NULL
    list.head = DLNode(10)
    list.head.next = DLNode(20)
    list.head.next.prev = list.head
    list.head.next.next = DLNode(30)
    list.head.next.next.prev = list.head.next

    print("Original Doubly Linked List (Forward):")
    list.traverseForward()

    # Insert at different positions.
    list.insertAtPosition(5, 0)    # Insert 5 at position 0 (beginning).
    list.insertAtPosition(25, 2)   # Insert 25 at position 2 (middle).
    list.insertAtPosition(40, 5)   # Insert 40 at position 5 (end).

    print("\nDoubly Linked List after Insertions (Forward):")
    list.traverseForward()

    # Delete at different positions.
    list.deleteAtPosition(0)  # Delete node at position 0 (beginning)
    list.deleteAtPosition(2)  # Delete node at position 2 (middle)
    list.deleteAtPosition(2)  # Delete node at position 2 (end)

    print("\nDoubly Linked List after Deletions (Forward):")
    list.traverseForward()
