# Stack implementation using an array
class RMITStack:
    # Constructor to initialize stack
    def __init__(self, capacity):
        self.capacity = capacity
        self.stack = [0] * capacity
        self.top = -1  # Stack is initially empty

    # Push operation
    def push(self, value):
        if self.top == self.capacity - 1:
            print(f"Stack Overflow! Cannot push {value}")
            return
        self.top += 1
        self.stack[self.top] = value
        print(f"{value} pushed to stack.")

    # Pop operation
    def pop(self):
        if self.isEmpty():
            print("Stack Underflow! No elements to pop.")
            return -1  # Return -1 to indicate error
        value = self.stack[self.top]
        self.top -= 1
        return value

    # Peek operation
    def peek(self):
        if self.isEmpty():
            print("Stack is empty!")
            return -1
        return self.stack[self.top]

    # Check if the stack is empty
    def isEmpty(self):
        return self.top == -1


class Node:
    def __init__(self, x):
        self.val = x
        self.next = None


class RMITStackLinkedList:
    def __init__(self):
        self.top = None  # Top of the stack

    # Push operation
    def push(self, value):
        newNode = Node(value)
        newNode.next = self.top
        self.top = newNode
        print(f"{value} pushed to stack.")

    # Pop operation
    def pop(self):
        if self.isEmpty():
            print("Stack Underflow! No elements to pop.")
            return -1
        poppedValue = self.top.val
        self.top = self.top.next
        return poppedValue

    # Peek operation
    def peek(self):
        if self.isEmpty():
            print("Stack is empty!")
            return -1
        return self.top.val

    # Check if the stack is empty
    def isEmpty(self):
        return self.top is None


# Main method to demonstrate stack operations
if __name__ == "__main__":
    stack = RMITStack(5)

    stack.push(10)
    stack.push(20)
    stack.push(30)
    print("Top element:", stack.peek())  # Output: 30

    print("Popped:", stack.pop())  # Output: 30
    print("Popped:", stack.pop())  # Output: 20

    print("Is stack empty?", stack.isEmpty())  # Output: False
    stack.pop()  # Popping last element
    print("Is stack empty?", stack.isEmpty())  # Output: True

    stack = RMITStackLinkedList()

    stack.push(10)
    stack.push(20)
    stack.push(30)
    print("Top element:", stack.peek())  # Output: 30

    print("Popped:", stack.pop())  # Output: 30
    print("Popped:", stack.pop())  # Output: 20

    print("Is stack empty?", stack.isEmpty())  # Output: False
    stack.pop()  # Popping last element
    print("Is stack empty?", stack.isEmpty())  # Output: True


