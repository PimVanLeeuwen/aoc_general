from itertools import pairwise


def next_value(sequence):
    """Extrapolate a polynomial sequence by repeated differences (until all zero)."""
    if all(value == 0 for value in sequence):
        return 0
    differences = [b - a for a, b in pairwise(sequence)]
    return sequence[-1] + next_value(differences)


def quadratic_at(y0, y1, y2, n):
    """
    Value at step n of a quadratic known at steps 0, 1, 2 (Newton forward
    differences). Typical use: measure the answer after k, k + period and
    k + 2 * period steps, then jump to the huge target step.
    """
    first_difference = y1 - y0
    second_difference = y2 - 2 * y1 + y0
    return y0 + first_difference * n + second_difference * n * (n - 1) // 2
