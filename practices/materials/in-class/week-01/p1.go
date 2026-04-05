package main

import "fmt"

func findMaxValue(l []int) int {
	maxV := l[0]
	for _, v := range l {
		if v > maxV {
			maxV = v
		}
	}
	return maxV
}

func findSecondMaxValue(l []int) int {
	maxV := findMaxValue(l)
	newL := []int{}
	for _, v := range l {
		if v != maxV {
			newL = append(newL, v)
		}
	}
	return findMaxValue(newL)
}

func main() {
	a := []int{7, 6, 9, 3, 2, 5}
	fmt.Println(findMaxValue(a))
	fmt.Println(findSecondMaxValue(a))
}
