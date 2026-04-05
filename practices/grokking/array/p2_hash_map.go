package main

import "fmt"

// Solution struct type
type Solution struct{}

// containsDuplicate checks for duplicates in a slice of integers
func (s *Solution) containsDuplicate(nums []int) bool {
	// ToDo: Write Your Code Here.
	maps := make(map[int]bool)

	for _, num := range nums {
		if _, ok := maps[num]; ok {
			return true
		}
		maps[num] = true
	}
	return false
}

func main() {
	s := Solution{}
	result := s.containsDuplicate([]int{1, 2, 3, 1})
	fmt.Println(result)

}
