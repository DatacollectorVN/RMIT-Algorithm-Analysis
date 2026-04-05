def find_max_value(l: list[int]) -> int:
    max_v: int = l[0]
    v: int
    for v in l:
        if v > max_v:
            max_v = v
    return max_v

def find_second_max_value(l: list[int]) -> int:
    max_v: int = find_max_value(l)
    new_l: list[int] = [v for v in l if v != max_v]
    return find_max_value(new_l)

def main():
    a: list[int] = [7, 6, 9, 3, 2, 5] 
    print(find_max_value(a))
    print(find_second_max_value(a))


if __name__ == "__main__":
    main()