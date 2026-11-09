from itertools import accumulate


def prefix_sums(values):
    """sums[j] - sums[i] == sum(values[i:j]) in O(1) per query."""
    return [0, *accumulate(values)]


def first_distinct_window(text, size):
    """Index just after the first window of `size` all-different characters."""
    for end in range(size, len(text) + 1):
        if len(set(text[end - size:end])) == size:
            return end
    return None


def summed_area(grid):
    """2D prefix sums: total[r][c] = sum of grid[0..r-1][0..c-1]."""
    rows, cols = len(grid), len(grid[0])
    total = [[0] * (cols + 1) for _ in range(rows + 1)]
    for r in range(rows):
        for c in range(cols):
            total[r + 1][c + 1] = grid[r][c] + total[r][c + 1] + total[r + 1][c] - total[r][c]
    return total


def area_sum(total, top, left, bottom, right):
    """Sum of the inclusive rectangle in O(1), using summed_area()."""
    return total[bottom + 1][right + 1] - total[top][right + 1] - total[bottom + 1][left] + total[top][left]
