from collections import Counter
from functools import cache


def count_ways(design, towels):
    """Number of ways to build design from towel patterns: overlapping subproblems -> @cache."""

    @cache
    def ways(position):
        if position == len(design):
            return 1
        return sum(ways(position + len(towel)) for towel in towels if design.startswith(towel, position))

    return ways(0)


def evolve_counts(items, step, n):
    """
    When only how many of each value matters (lanternfish, pebbles), track a
    Counter instead of a list: step(value) returns the values it turns into.
    """
    counts = Counter(items)
    for _ in range(n):
        next_counts = Counter()
        for value, count in counts.items():
            for new_value in step(value):
                next_counts[new_value] += count
        counts = next_counts
    return sum(counts.values())
