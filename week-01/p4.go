package main

import "fmt"

// sumRange returns the sum of the sub-matrix defined by topLeft and bottomRight
// (0-based, inclusive on both ends).
//
// Naive approach: visits every cell in the queried region.
// Time complexity: O(n * m) per query.
func sumRange(m [][]int, topLeft, bottomRight [2]int) int {
	total := 0
	for i := topLeft[0]; i <= bottomRight[0]; i++ {
		for j := topLeft[1]; j <= bottomRight[1]; j++ {
			total += m[i][j]
		}
	}
	return total
}

func main() {
	matrix := [][]int{
		{1, 2, 3, 4, 5},
		{8, 6, 9, 1, 3},
		{8, 3, 1, 4, 3},
		{4, 8, 2, 9, 6},
	}

	fmt.Printf("%d\n", sumRange(matrix, [2]int{1, 2}, [2]int{2, 3}))
}
