from typing import List, Union

def main():
    miss_l: list[int] = [1, 2, 3, 4, 5, 6, 7, 8, 10]
    print(find_miss_value(miss_l, 10))
    print(find_miss_value_v2(miss_l, 10))

def find_miss_value(l: List[int], n: int) -> Union[List[int], int]:
    expected_l: List[int] = [i for i in range(0, n+1)]
    mis_vs: List[int] = [v for v in expected_l if v not in l]
    return len(mis_vs) > 1 and mis_vs or mis_vs[0]


def get_full_sum(n: int) -> int:
    return n * (n + 1) // 2

def find_miss_value_v2(l: List[int], n: int) -> Union[List[int], int]:
    return get_full_sum(n) - sum(l)


if __name__ == "__main__":
    main()