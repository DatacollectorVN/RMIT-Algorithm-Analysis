# Class to define a Node
class Node:
    def __init__(self, val):
        self.val = val  
        self.next = None  


class RMITLinkedList:
    def __init__(self):
        self.head = None  # Head pointer to the linked list

    # Method to insert at a specific position
    def insertAtPosition(self, val, position):
        new_node = Node(val)

        # If inserting at the beginning
        if position == 0:
            new_node.next = self.head
            self.head = new_node
            return

        # Find the previous node before insertion point
        prev = self.head
        for _ in range(position - 1):
            if prev is None:
                print("Invalid Position!")
                return
            prev = prev.next

        # If position is invalid
        if prev is None:
            print("Invalid Position!")
            return

        # Insert the new node
        new_node.next = prev.next
        prev.next = new_node

    # Method to delete a node at a specific position
    def deleteAtPosition(self, position):
        # If the list is empty
        if self.head is None:
            print("List is empty!")
            return

        # If deleting the first node
        if position == 0:
            self.head = self.head.next
            return

        # Find the previous node before the target position
        prev = self.head
        for i in range(position - 1):
            if prev is None or prev.next is None:
                print("Invalid Position!")
                return
            prev = prev.next

        # If position is invalid
        if prev is None or prev.next is None:
            print("Invalid Position!")
            return

        # Remove the node
        prev.next = prev.next.next

    # Traversal method to print all elements
    def traverse(self):
        current = self.head  # Start from the head node
        while current:
            print(current.val, end=" → ")  # Print current node value
            current = current.next  # Move to the next node
        print("NULL")  # Indicate end of the list

    # Method to artificially create a loop for testing purposes
    def createLoop(self, position):
        if self.head is None:
            return
        
        loop_node = None
        tail = self.head
        count = 0
        
        while tail.next:
            if count == position:
                loop_node = tail
            tail = tail.next
            count += 1
            
        # Connect the last node to the loop_node to create a cycle
        if loop_node:
            tail.next = loop_node
            print(f"Loop created connecting tail to node at position {position}.")

    def removeLoop(self, verbose=False):
        slow = self.head
        fast = self.head

        # Step 1: Detect Loop using Floyd's Algorithm
        loop_exists = False
        while fast and fast.next:
            if verbose: print("Slow:", slow.val, "Fast:", fast.val)
            slow = slow.next
            fast = fast.next.next
            if verbose: print("(After) Slow:", slow.val, "Fast:", fast.val)
            if slow == fast:
                if verbose: print("Loop detected!")
                loop_exists = True
                break

        # Step 2 & 3: Find the start of the loop and break it
        if loop_exists:
            slow = self.head
            
            # Edge Case: If the loop starts exactly at the head node
            if slow == fast:
                if verbose: print("Loop starts at the head node!")
                while fast.next != slow:
                    if verbose: print("Fast:", fast.val, "Slow:", slow.val)
                    fast = fast.next
                    if verbose: print("(After) Fast:", fast.val, "Slow:", slow.val)
                fast.next = None
            else:
                # Move both one step at a time to find the start of the loop
                while slow.next != fast.next:
                    if verbose: print("Slow:", slow.val, "Fast:", fast.val)
                    slow = slow.next
                    if verbose: print("(After) Slow:", slow.val, "Fast:", fast.val)
                    fast = fast.next
                
                # fast.next is the start of the loop, so fast is the last node
                fast.next = None
            if verbose: print("Loop successfully removed!")
        else:
            if verbose: print("No loop detected.")

# Main function to create and modify the linked list
if __name__ == "__main__":
    llist = RMITLinkedList()

    # Creating a linked list: 10 → 20 → 30 → 40 → 50
    llist.head = Node(10)
    llist.head.next = Node(20)
    llist.head.next.next = Node(30)
    llist.head.next.next.next = Node(40)
    llist.head.next.next.next.next = Node(50)

    print("Original Linked List:")
    llist.traverse()

    # Create a loop connecting the tail (50) to position 1 (20)
    llist.createLoop(1)

    # print("Linked List after creating the loop:")
    # llist.traverse()

    # # Note: If you run llist.traverse() right now, it will print forever!
    
    # Remove the loop
    llist.removeLoop()

    # print("\nLinked List after removing the loop:")
    # llist.traverse()