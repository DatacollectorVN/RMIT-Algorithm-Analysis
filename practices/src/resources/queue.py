"""
Queue implemented using a list only (FIFO, dynamic, unbounded).
Enqueue: append at rear. Dequeue: pop from front (O(n) due to list shift).
"""


# Queue implementation using a list
class RMITLinearQueue:
    def __init__(self):
        self.queue = []
    
    def enqueue(self, value):
        """Add an element to the rear of the queue"""
        self.queue.append(value)
        print(f"{value} enqueued to queue.")
    
    def dequeue(self):
        """Remove an element from the front of the queue"""
        if self.isEmpty():
            print("Queue Underflow! No elements to dequeue.")
            return -1
        return self.queue.pop(0)
    
    def peek(self):
        """Get the front element of the queue"""
        if self.isEmpty():
            print("Queue is empty!")
            return -1
        return self.queue[0]
    
    def isEmpty(self):
        """Check if the queue is empty"""
        return len(self.queue) == 0


"""
Double-ended queue (deque) using a list only (dynamic, unbounded).
Rear: append / pop — O(1). Front: insert(0) / pop(0) — O(n) due to shifting.
"""
class RMITDeQueue:
    def __init__(self):
        self.deque = []
    
    def addFront(self, value):
        """Add an element at the front of the deque."""
        self.deque.insert(0, value)
        print(f"{value} added to front of deque.")
    
    def addRear(self, value):
        """Add an element at the rear of the deque."""
        self.deque.append(value)
        print(f"{value} added to rear of deque.")
    
    def removeFront(self):
        """Remove an element from the front of the deque."""
        if self.isEmpty():
            print("Deque Underflow! No elements to remove from front.")
            return -1
        return self.deque.pop(0)
    
    def removeRear(self):
        """Remove an element from the rear of the deque."""
        if self.isEmpty():
            print("Deque Underflow! No elements to remove from rear.")
            return -1
        return self.deque.pop()
    
    def peekFront(self):
        """Return the front element without removing it."""
        if self.isEmpty():
            print("Deque is empty!")
            return -1
        return self.deque[0]
    
    def peekRear(self):
        """Return the rear element without removing it."""
        if self.isEmpty():
            print("Deque is empty!")
            return -1
        return self.deque[-1]
    
    def isEmpty(self):
        """Check if the deque is empty."""
        return len(self.deque) == 0


"""
Circular queue: fixed-size array treated as a ring. Enqueue/dequeue are O(1); indices
wrap with % capacity instead of shifting the whole list.
  self.front — index of the next slot to DEQUEUE (the oldest item / head of the queue).
               After dequeue, we move forward: front = (front + 1) % capacity.
  self.rear  — index of the next FREE slot where the NEXT enqueue will WRITE (tail).
               After enqueue, we move forward: rear = (rear + 1) % capacity.
  self.capacity — length of the backing list; needed for wrap-around and overflow checks.
  self.size — how many elements are stored. We use it so we can tell empty vs full:
              when the ring is full, front and rear can coincide with the empty case,
              so size == 0 vs size == capacity disambiguates.
"""
class RMITCirQueue:
    def __init__(self, capacity):
        self.capacity = capacity
        self.queue = [None] * capacity
        # Head: next index to dequeue from.
        self.front = 0
        # Tail: next index to write on enqueue (slot is empty until we place a value).
        self.rear = 0
        self.size = 0
    
    def enqueue(self, value):
        """Add an element at the rear of the queue."""
        if self.isFull():
            print(f"Queue Overflow! Cannot enqueue {value}")
            return
        self.queue[self.rear] = value
        self.rear = (self.rear + 1) % self.capacity
        self.size += 1
        print(f"{value} enqueued to queue.")
    
    def dequeue(self):
        """Remove an element from the front of the queue."""
        if self.isEmpty():
            print("Queue Underflow! No elements to dequeue.")
            return -1
        value = self.queue[self.front]
        self.queue[self.front] = None
        self.front = (self.front + 1) % self.capacity
        self.size -= 1
        return value
    
    def peek(self):
        """Get the front element without removing it."""
        if self.isEmpty():
            print("Queue is empty!")
            return -1
        return self.queue[self.front]
    
    def isEmpty(self):
        """Return True if the queue has no elements."""
        return self.size == 0
    
    def isFull(self):
        """Return True if the queue cannot accept another element."""
        return self.size == self.capacity


if __name__ == "__main__":
    print("--- RMITLinearQueue ---")
    q = RMITLinearQueue()
    q.enqueue(10)
    q.enqueue(20)
    q.enqueue(30)
    print("Front element:", q.peek())
    print("Dequeued:", q.dequeue())
    print("Dequeued:", q.dequeue())
    print("Is queue empty?", q.isEmpty())
    q.dequeue()
    print("Is queue empty?", q.isEmpty())

    print("--- RMITDeQueue ---")
    d = RMITDeQueue()
    d.addRear(10)
    d.addRear(20)
    d.addFront(5)
    print("Front:", d.peekFront(), "Rear:", d.peekRear())
    print("Removed rear:", d.removeRear())
    print("Removed front:", d.removeFront())
    print("Is empty?", d.isEmpty())

    print("--- RMITCirQueue ---")
    cq = RMITCirQueue(3)
    cq.enqueue(1)
    cq.enqueue(2)
    print("Peek:", cq.peek())
    print("Dequeue:", cq.dequeue())
    cq.enqueue(3)
    cq.enqueue(4)
    print("Full?", cq.isFull())
    print("Dequeue:", cq.dequeue(), cq.dequeue(), cq.dequeue())
    print("Empty?", cq.isEmpty())