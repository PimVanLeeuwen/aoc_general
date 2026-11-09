from fractions import Fraction


def solve_linear(matrix, rhs):
    """
    Exact Gaussian elimination with Fractions (no float rounding).
    solve_linear([[94, 22], [34, 67]], [8400, 5400]) -> [80, 40]
    Check .denominator == 1 when only whole-number answers count.
    """
    n = len(matrix)
    rows = [[Fraction(v) for v in row] + [Fraction(b)] for row, b in zip(matrix, rhs)]
    for col in range(n):
        pivot = next(r for r in range(col, n) if rows[r][col] != 0)
        rows[col], rows[pivot] = rows[pivot], rows[col]
        for r in range(n):
            if r != col and rows[r][col] != 0:
                factor = rows[r][col] / rows[col][col]
                rows[r] = [a - factor * b for a, b in zip(rows[r], rows[col])]
    return [rows[i][n] / rows[i][i] for i in range(n)]
