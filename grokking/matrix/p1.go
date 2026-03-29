package main

import "fmt"

type Solution struct{}

func (s *Solution) maximumWealth(accounts [][]int) int {
	maxWealth := 0
	for i := 0; i < len(accounts); i++ {
		customer := accounts[i]
		wealth := 0
		for j := 0; j < len(customer); j++ {
			wealth += customer[j]
		}
		if wealth > maxWealth {
			maxWealth = wealth
		}
	}
	return maxWealth
}

func main() {
	s := Solution{}
	account := [][]int{{5, 2, 3}, {0, 6, 7}}
	result := s.maximumWealth(account)
	fmt.Println(result)

}
