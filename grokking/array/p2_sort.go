package main

import (
	"fmt"
	"sort"
)

// Solution struct type
type Solution struct{}

// containsDuplicate checks for duplicates in a slice of integers
func (s *Solution) containsDuplicate(nums []int) bool {
	// ToDo: Write Your Code Here.
	sort.Ints(nums)
	for i := 0; i < len(nums)-1; i++ {
		if nums[i] == nums[i+1] {
			return true
		}
	}
	return false
}

func main() {
	s := Solution{}
	result := s.containsDuplicate([]int{1, 2, 3, 1})
	fmt.Println(result)

}
