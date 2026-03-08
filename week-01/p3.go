package main

import (
	"fmt"
	"reflect"
)

func compareList(l1 []int, l2 []int) bool {
	return reflect.DeepEqual(sortList(l1), sortList(l2))
}

func sortList(l []int) []int {
	for i := 0; i < len(l); i++ {
		for j := i + 1; j < len(l); j++ {
			if l[i] > l[j] {
				l[i], l[j] = l[j], l[i]
			}
		}
	}
	return l
}

func main() {
	l1 := []int{1, 2, 3, 4}
	l2 := []int{4, 3, 2, 1}
	fmt.Println(compareList(l1, l2))

	l1 = []int{1, 2, 3, 4}
	l2 = []int{1, 2, 3, 4}
	fmt.Println(compareList(l1, l2))

	l1 = []int{1, 2, 3}
	l2 = []int{1, 2, 4}
	fmt.Println(compareList(l1, l2))
}
