package main

import "fmt"

type Solution struct{}

func (s *Solution) largestAltitude(gain []int) int {
	maxAltitude := 0
	currentAltitude := 0
	for i := 0; i < len(gain); i++ {
		currentAltitude += gain[i]
		if currentAltitude > maxAltitude {
			maxAltitude = currentAltitude
		}
	}
	return maxAltitude
}

func main() {
	s := Solution{}
	gain := []int{-838, -981, 750, 232, -960}
	fmt.Println(s.largestAltitude(gain))
}
