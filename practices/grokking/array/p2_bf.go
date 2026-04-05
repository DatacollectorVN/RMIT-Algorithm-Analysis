package main

import "fmt"

// Solution struct type
type Solution struct{}

// containsDuplicate checks for duplicates in a slice of integers
func (s *Solution) containsDuplicate(nums []int) bool {
	// ToDo: Write Your Code Here.
	for i := 0; i < len(nums); i++ {
		for j := i + 1; j < len(nums); j++ {
			if nums[i] == nums[j] {
				return true
			}
		}
	}
	return false
}

func main() {
	s := Solution{}
	result := s.containsDuplicate([]int{1, 2, 3, 1})
	fmt.Println(result)

}
