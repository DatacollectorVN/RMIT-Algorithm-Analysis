package main

import "fmt"

type Solution struct{}

func (s *Solution) diagonalSum(squareMatrix [][]int) int {
	sum := 0
	n := len(squareMatrix) - 1
	for i := 0; i <= n; i++ {
		sum += squareMatrix[i][i]
	}
	return sum
}

func main() {
	s := Solution{}
	squareMatrix := [][]int{{5, 2, 3}, {0, 6, 7}, {1, 2, 3}}
	result := s.diagonalSum(squareMatrix)
	fmt.Println(result)

}
