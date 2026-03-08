import numpy as np

def sum_matrix(matrix: list[list[int]]) -> int:
    return sum(sum(row) for row in matrix)

def sum_matrix_raw(matrix: list[list[int]]) -> int:
    total: int = 0
    row: list[int]
    item: int
    for row in matrix:
        for item in row:
            total += item
    return total

def sum_range(matrix: list[list[int]], top_left: tuple[int, int], bottom_right: tuple[int, int]) -> int:
    """
    Naive approach: iterate over every cell in the sub-matrix.
    Time complexity: O(n*m) per query, where n and m are the dimensions of the queried region.
    """
    total: int = 0
    i: int
    j: int
    for i in range(top_left[0], bottom_right[0] + 1):
        for j in range(top_left[1], bottom_right[1] + 1):
            total += matrix[i][j]
    return total

def sum_range_v2(matrix: list[list[int]], top_left: tuple[int, int], bottom_right: tuple[int, int]) -> int:
    """
    NumPy slice approach: syntactically cleaner but still O(n*m) under the hood.
    """
    matrix: np.ndarray = np.array(matrix)
    return int(np.sum(matrix[top_left[0]:bottom_right[0] + 1, top_left[1]:bottom_right[1] + 1]))

if __name__ == "__main__":
    matrix: list[list[int]] = [[1, 2, 3, 4, 5], [8, 6, 9, 1, 3], [8, 3, 1, 4, 3], [4, 8, 2, 9, 6]]

    result: int = sum_range(matrix, (1, 2), (2, 3))
    print(f"sum_range (1,2)->(2,3) = {result}")

    result_v2 = sum_range_v2(matrix, (1, 2), (2, 3))
    print(f"sum_range_v2 (1,2)->(2,3) = {result_v2}")
