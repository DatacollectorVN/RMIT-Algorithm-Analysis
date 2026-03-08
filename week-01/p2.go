package main

import "fmt"

func findMissValue(l []int, n int) []int {
	expectedL := make([]int, n+1)
	missVs := []int{}
	for i := range expectedL {
		is_exist := false
		for j := range l {
			if l[j] == i {
				is_exist = true
				break
			}
		}
		if !is_exist {
			missVs = append(missVs, i)
		}
	}
	return missVs
}

func main() {
	l := []int{1, 2, 3, 4, 5, 6, 7, 8, 10}
	n := 10
	miss := findMissValue(l, n)
	fmt.Println(miss) // [0 9] — one or many missing values
}
