"""
Advanced solution using a 2-D Prefix Sum (Summed Area Table).

------------------
Naive approach (p4.py  sum_range):
  - Each range query loops over every cell in the sub-matrix.
  - Time per query: O(n * m) --> O(n^2) <-- bad when many queries are made

Prefix-sum approach (this file):
  - One-time  O(R * C)  build step to pre-compute prefix_sum[][].
  - Every range query after that is answered in O(1) with 4 table
    look-ups and 3 arithmetic operations.
  - Time per query: O(1) <-- constant, regardless of region size

This matters when the same matrix is queried many times (Q queries):
  Naive        : O(Q * n * m)
  Prefix-sum   : O(R*C)  +  O(Q)   ≈ O(R*C + Q)
"""


def build_prefix_sum(matrix: list[list[int]]) -> list[list[int]]:
    """
    Build a (rows+1) x (cols+1) prefix-sum table using 1-based indexing
    so that edge cases (row 0 / col 0) never require bounds checks.

    prefix_sum[i][j] = sum of all cells matrix[r][c]
                       where 0 <= r < i  and  0 <= c < j

    Recurrence:
        prefix_sum[i][j] = prefix_sum[i-1][j]
                         + prefix_sum[i][j-1]
                         - prefix_sum[i-1][j-1]   # subtracted twice above
                         + matrix[i-1][j-1]

    Build time : O(R * C)
    Space      : O(R * C)
    """
    rows = len(matrix)
    cols = len(matrix[0])
    # Extra row and column of zeros act as a sentinel border
    ps = [[0] * (cols + 1) for _ in range(rows + 1)]

    for i in range(1, rows + 1):
        for j in range(1, cols + 1):
            ps[i][j] = (
                ps[i - 1][j]
                + ps[i][j - 1]
                - ps[i - 1][j - 1]
                + matrix[i - 1][j - 1]
            )
    return ps


def efficient_sum_range(
    prefix_sum: list[list[int]],
    top_left: tuple[int, int],
    bottom_right: tuple[int, int],
) -> int:
    """
    Return the sum of the sub-matrix defined by top_left and bottom_right
    (0-based, inclusive on both ends) using the pre-built prefix-sum table.

    Formula (inclusion-exclusion on the Summed Area Table):

        sum = ps[r2+1][c2+1]
            - ps[r1  ][c2+1]   # strip above the region
            - ps[r2+1][c1  ]   # strip left of the region
            + ps[r1  ][c1  ]   # re-add the top-left corner (subtracted twice)

    Query time: O(1)  <-- only 4 table lookups + 3 additions
    """
    r1, c1 = top_left
    r2, c2 = bottom_right
    return (
        prefix_sum[r2 + 1][c2 + 1]
        - prefix_sum[r1][c2 + 1]
        - prefix_sum[r2 + 1][c1]
        + prefix_sum[r1][c1]
    )


if __name__ == "__main__":
    matrix = [[1, 2, 3, 4, 5], [8, 6, 9, 1, 3], [8, 3, 1, 4, 3], [4, 8, 2, 9, 6]]

    ps = build_prefix_sum(matrix)

    result = efficient_sum_range(ps, (1, 2), (2, 3))
    print(f"efficient_sum_range (1,2)->(2,3) = {result}")

    # Multiple queries all run in O(1) after the single O(R*C) build
    queries = [
        ((0, 0), (3, 4)),   # entire matrix
        ((0, 0), (0, 4)),   # first row
        ((0, 0), (3, 0)),   # first column
        ((1, 1), (2, 2)),   # inner 2x2 block
    ]
    for tl, br in queries:
        print(f"  sum {tl} -> {br} = {efficient_sum_range(ps, tl, br)}")
