package main

import "fmt"

type Solution struct{}

func (s *Solution) runningSum(nums []int) []int {
	result := make([]int, len(nums))
	// TODO: Write your code here
	cum_sum := 0
	for idx, item := range nums {
		cum_sum += item
		result[idx] = cum_sum
	}
	return result
}

func main() {
	s := Solution{}
	result := s.runningSum([]int{1, 2, 3, 4})
	fmt.Println(result)

}
