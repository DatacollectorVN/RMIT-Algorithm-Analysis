package main

import (
	"fmt"
	"math"
)

type Solution struct{}

func (s *Solution) findDifferenceArray(nums []int) []int {
	result := make([]int, len(nums))
	rightSum := 0
	leftSum := 0
	for i := 0; i < len(nums); i++ {
		rightSum += nums[i]
	}

	for i := 0; i < len(nums); i++ {
		rightSum -= nums[i]
		result[i] = int(math.Abs(float64(rightSum - leftSum)))
		leftSum += nums[i]
	}

	return result

}

func main() {
	solution := &Solution{}

	example1 := []int{2, 5, 1, 6, 1}
	example2 := []int{3, 3, 3}
	example3 := []int{1, 2, 3, 4, 5}

	fmt.Println(solution.findDifferenceArray(example1)) // Output: [13 6 0 7 14]
	fmt.Println(solution.findDifferenceArray(example2)) // Output: [6 0 6]
	fmt.Println(solution.findDifferenceArray(example3)) // Output: [14 11 6 1 10]
}
