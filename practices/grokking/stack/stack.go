// Stack implementation using an array
package main

import "fmt"

type RMITStack struct {
	stack    []int
	top      int
	capacity int
}

// Constructor to initialize stack
func NewRMITStack(capacity int) *RMITStack {
	return &RMITStack{
		stack:    make([]int, capacity),
		top:      -1, // Stack is initially empty
		capacity: capacity,
	}
}

// Push operation
func (s *RMITStack) push(value int) {
	if s.top == s.capacity-1 {
		fmt.Println("Stack Overflow! Cannot push", value)
		return
	}
	s.top++
	s.stack[s.top] = value
	fmt.Println(value, "pushed to stack.")
}

// Pop operation
func (s *RMITStack) pop() int {
	if s.isEmpty() {
		fmt.Println("Stack Underflow! No elements to pop.")
		return -1 // Return -1 to indicate error
	}
	value := s.stack[s.top]
	s.top--
	return value
}

// Peek operation
func (s *RMITStack) peek() int {
	if s.isEmpty() {
		fmt.Println("Stack is empty!")
		return -1
	}
	return s.stack[s.top]
}

// Check if the stack is empty
func (s *RMITStack) isEmpty() bool {
	return s.top == -1
}

type ListNode struct {
	Val  int
	Next *ListNode
}

type RMITStackLinkedList struct {
	top *ListNode // Top of the stack
}

// Constructor
func NewRMITStackLinkedList() *RMITStackLinkedList {
	return &RMITStackLinkedList{top: nil}
}

// Push operation
func (s *RMITStackLinkedList) push(value int) {
	newNode := &ListNode{Val: value, Next: s.top}
	s.top = newNode
	fmt.Println(value, "pushed to stack.")
}

// Pop operation
func (s *RMITStackLinkedList) pop() int {
	if s.isEmpty() {
		fmt.Println("Stack Underflow! No elements to pop.")
		return -1
	}
	poppedValue := s.top.Val
	s.top = s.top.Next
	return poppedValue
}

// Peek operation
func (s *RMITStackLinkedList) peek() int {
	if s.isEmpty() {
		fmt.Println("Stack is empty!")
		return -1
	}
	return s.top.Val
}

// Check if the stack is empty
func (s *RMITStackLinkedList) isEmpty() bool {
	return s.top == nil
}

// Main method to demonstrate stack operations
func main() {
	stack := NewRMITStack(5)

	stack.push(10)
	stack.push(20)
	stack.push(30)
	fmt.Println("Top element:", stack.peek()) // Output: 30

	fmt.Println("Popped:", stack.pop()) // Output: 30
	fmt.Println("Popped:", stack.pop()) // Output: 20

	fmt.Println("Is stack empty?", stack.isEmpty()) // Output: false
	stack.pop()                                     // Popping last element
	fmt.Println("Is stack empty?", stack.isEmpty()) // Output: true

	stackLinkedList := NewRMITStackLinkedList()

	stackLinkedList.push(10)
	stackLinkedList.push(20)
	stackLinkedList.push(30)
	fmt.Println("Top element:", stackLinkedList.peek())

	fmt.Println("Popped:", stackLinkedList.pop())
	fmt.Println("Popped:", stack.pop())

	fmt.Println("Is stack empty?", stack.isEmpty())
	stack.pop()
	fmt.Println("Is stack empty?", stack.isEmpty())
}
