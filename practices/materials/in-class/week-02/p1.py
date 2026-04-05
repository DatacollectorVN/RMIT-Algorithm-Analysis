def example_t_n_v2(n: int) -> int:
    total = 0
    for i in range(n):
        for _ in range(999):
            total += 1
    k = int(n ** 0.5)
    for _ in range(k):
        total += 1
    return total

print(example_t_n_v2(1000))