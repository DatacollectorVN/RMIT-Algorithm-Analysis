package main

import (
	"fmt"
	"math"
)

func example_tn_n(n int) int {
	total := 0
	for i := 0; i < n; i++ {
		for j := 0; j < 999; j++ {
			total++
		}
	}
	k := int(math.Sqrt(float64(n)))
	for j := 0; j < k; j++ {
		total++
	}
	return total
}

func main() {
	fmt.Println(example_tn_n(1000))
}
