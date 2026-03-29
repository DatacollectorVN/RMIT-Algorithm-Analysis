def get_unique_list(l: list[int]) -> int:
    # O(n^2)
    # Without sorting
    unique_l: list[int] = []
    for i in range(len(l)):
        for j in range(i+1, len(l)):
            if l[i] == l[j]:
                break
        else:
            unique_l.append(l[i])
    return unique_l


## MERGE SORT
def sort_list_merge(l: list[int]) -> list[int]:
    # O(n log n)
    if len(l) <= 1:
        return l.copy()
    mid = len(l) // 2
    left = sort_list_merge(l[:mid])
    right = sort_list_merge(l[mid:])
    out = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            out.append(left[i])
            i += 1
        else:
            out.append(right[j])
            j += 1
    out.extend(left[i:])
    out.extend(right[j:])
    return out

## BUBBLE SORT
def sort_list_bubble(l: list[int]) -> list[int]:
    # O(n^2)
    a = l.copy()
    n = len(a)
    for i in range(n): # O(n)
        for j in range(n - 1 - i): # O(n)
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
    return a

def get_unique_list_v2(l: list[int]) -> int:
    # O(n log n) 
    # With sorting
    l = sort_list_merge(l) # O(n log n)

    unique_l: list[int] = []

    for i in range(len(l)): # O(n)
        prev_v: int | None = l[i-1] if i > 0 else None
        current_v: int = l[i]
        if not prev_v:
            unique_l.append(current_v)
        elif prev_v != current_v:
            unique_l.append(current_v)
    return unique_l


def get_unique_list_dict(l: list[int]) -> list[int]:
    # O(n)
    seen: dict[int, bool] = {}
    for x in l: # O(n)
        seen[x] = True
    return [k for k in seen.keys()] # O(n)


def main():
    l: list[int] = [6, 8, 10, 11, 6, 10]
    print(get_unique_list(l))
    print(get_unique_list_v2(l))
    print(get_unique_list_dict(l))

if __name__ == "__main__":
    main()