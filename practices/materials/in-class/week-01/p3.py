def compare_list(l1: list[int], l2: list[int]) -> bool:
    return sorted(l1) == sorted(l2)

# Naive approach: iterate over every cell in the list.
def sort_list(l: list[int]) -> list[int]:
    i: int
    j: int
    for i in range(len(l)):
        for j in range(i+1, len(l)):
            if l[i] > l[j]:
                l[i], l[j] = l[j], l[i] # swap list items
    return l

# Naive approach: iterate over every cell in the list.
def compare_list_raw(l1: list[int], l2: list[int]) -> bool:
    l1: list[int] = sort_list(l1)
    l2: list[int] = sort_list(l2)
    return l1 == l2


if __name__ == "__main__":
    l1: list[int] = [1, 2, 3, 4]
    l2: list[int] = [4, 3, 2, 1]
    print(compare_list_raw(l1, l2))

    l1 = [1, 2, 3, 4]
    l2 = [1, 2, 3, 4]
    print(compare_list_raw(l1, l2))

    l1 = [1, 2, 3]
    l2 =[1, 2, 4]
    print(compare_list_raw(l1, l2))