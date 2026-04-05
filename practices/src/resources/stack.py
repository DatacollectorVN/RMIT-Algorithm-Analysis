"""
In python Stack is implemented using a list.
"""

# Stack implementation using a list (dynamic, unbounded)
class RMITStack:
    # Constructor to initialize stack
    def __init__(self):
        self.stack = []

    # Push operation
    def push(self, value):
        self.stack.append(value)
        print(f"{value} pushed to stack.")

    # Pop operation
    def pop(self):
        if self.isEmpty():
            print("Stack Underflow! No elements to pop.")
            return -1  # Return -1 to indicate error
        return self.stack.pop()

    # Peek operation
    def peek(self):
        if self.isEmpty():
            print("Stack is empty!")
            return -1
        return self.stack[-1]

    # Check if the stack is empty
    def isEmpty(self):
        return len(self.stack) == 0


# Main method to demonstrate stack operations
if __name__ == "__main__":
    stack = RMITStack()

    stack.push(10)
    stack.push(20)
    stack.push(30)
    print("Top element:", stack.peek())  # Output: 30

    print("Popped:", stack.pop())  # Output: 30
    print("Popped:", stack.pop())  # Output: 20

    print("Is stack empty?", stack.isEmpty())  # Output: False
    stack.pop()  # Popping last element
    print("Is stack empty?", stack.isEmpty())  # Output: True
