def sum_pair(l: list[int]):
    sum_pair: list = []
    n = len(l)
    for i in range(n):
        a = l[i]
        for j in range(i+1, n):
            b = l[j]
            sum = a + b
            delta_with_zero = abs(sum - 0)
            sum_pair.append(
                (a, b, sum, delta_with_zero)
            )
    min_close: int = sum_pair[0][-1]
    idx = 0
    for k in range(len(sum_pair)):
       delta: int = sum_pair[k][-1]
       if min_close > delta:
            min_close = delta
            idx = k
    print(min_close, sum_pair[idx])

sum_pair([2, 3, 9, 6])
sum_pair([-100, 50, -52, 99] )