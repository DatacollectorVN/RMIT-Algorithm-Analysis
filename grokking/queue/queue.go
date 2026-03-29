package main

import "fmt"

// Node struct for storing data and the reference to the next node
type Node struct {
	Data interface{}
	Next *Node
}

// Queue struct using linked list
type Queue struct {
	front *Node
	rear  *Node
	size  int
}

// NewQueue creates a new Queue instance
func NewQueue() *Queue {
	return &Queue{nil, nil, 0}
}

// Enqueue adds an element to the rear of the queue
func (q *Queue) Enqueue(data interface{}) {
	newNode := &Node{Data: data}
	if q.rear == nil {
		q.front = newNode
		q.rear = newNode
	} else {
		q.rear.Next = newNode
		q.rear = newNode
	}
	q.size++
}

// Dequeue removes an element from the front of the queue
func (q *Queue) Dequeue() interface{} {
	if q.front == nil {
		return nil
	}
	temp := q.front
	q.front = q.front.Next
	if q.front == nil {
		q.rear = nil
	}
	q.size--
	return temp.Data
}

// Peek gets the front element of the queue
func (q *Queue) Peek() interface{} {
	if q.front == nil {
		return nil
	}
	return q.front.Data
}

// IsEmpty checks if the queue is empty
func (q *Queue) IsEmpty() bool {
	return q.size == 0
}

// Size returns the number of elements in the queue
func (q *Queue) Size() int {
	return q.size
}

// Example usage
func main() {
	queue := NewQueue()

	// Enqueue elements
	queue.Enqueue(1)
	queue.Enqueue(2)
	queue.Enqueue(3)

	// Display front element
	fmt.Println("Front element:", queue.Peek())
	// Dequeue and display the dequeued element
	fmt.Println("Dequeued:", queue.Dequeue())
	// Display front element again
	fmt.Println("Front element:", queue.Peek())
	// Display the size of the queue
	fmt.Println("Queue size:", queue.Size())
}
