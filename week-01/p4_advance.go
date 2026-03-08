package main

import "fmt"

// Advanced solution using a 2-D Prefix Sum (Summed Area Table).
//
// ------------------
// Naive approach (sumRange in p4.go):
//   - Each range query loops over every cell in the sub-matrix.
//   - Time per query: O(n * m) --> O(n^2) <-- bad when many queries are made
//
// Prefix-sum approach (this file):
//   - One-time O(R * C) build step to pre-compute a prefix-sum table.
//   - Every range query after that is answered in O(1) with 4 table
//     look-ups and 3 arithmetic operations.
//   - Time per query: O(1) --> O(1) <-- constant, regardless of region size
//
// Total cost for Q queries:
//   Naive       : O(Q * n * m)
//   Prefix-sum  : O(R*C) + O(Q)   ≈ O(R*C + Q)

// buildPrefixSum builds a (rows+1) x (cols+1) prefix-sum table using
// 1-based indexing so edge cases (row 0 / col 0) need no bounds checks.
//
// ps[i][j] = sum of all cells matrix[r][c] where 0 <= r < i and 0 <= c < j
//
// Recurrence:
//
//	ps[i][j] = ps[i-1][j] + ps[i][j-1] - ps[i-1][j-1] + matrix[i-1][j-1]
//
// Build time : O(R * C)
// Space      : O(R * C)
func buildPrefixSum(matrix [][]int) [][]int {
	rows := len(matrix)
	cols := len(matrix[0])

	// Allocate (rows+1) x (cols+1) — the extra row/col of zeros is the sentinel border.
	ps := make([][]int, rows+1)
	for i := range ps {
		ps[i] = make([]int, cols+1)
	}

	for i := 1; i <= rows; i++ {
		for j := 1; j <= cols; j++ {
			ps[i][j] = ps[i-1][j] +
				ps[i][j-1] -
				ps[i-1][j-1] +
				matrix[i-1][j-1]
		}
	}
	return ps
}

// efficientSumRange returns the sum of the sub-matrix defined by topLeft
// and bottomRight (0-based, inclusive on both ends) using the pre-built
// prefix-sum table.
func efficientSumRange(ps [][]int, topLeft, bottomRight [2]int) int {
	r1, c1 := topLeft[0], topLeft[1]
	r2, c2 := bottomRight[0], bottomRight[1]
	return ps[r2+1][c2+1] -
		ps[r1][c2+1] -
		ps[r2+1][c1] +
		ps[r1][c1]
}

func main() {
	matrix := [][]int{
		{1, 2, 3, 4, 5},
		{8, 6, 9, 1, 3},
		{8, 3, 1, 4, 3},
		{4, 8, 2, 9, 6},
	}
	ps := buildPrefixSum(matrix)
	fmt.Println(efficientSumRange(ps, [2]int{1, 2}, [2]int{2, 3}))
}
