"""
Day 9 - All in a Single Night
Year: 2015

Find the shortest (and longest) route that visits every location exactly once.
"""

from itertools import permutations
from collections import defaultdict


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    lines = puzzle_input.strip().split("\n")

    dist = defaultdict(dict)
    cities = set()

    for line in lines:
        route, d = line.split(" = ")
        a, b = route.split(" to ")
        dist[a][b] = int(d)
        dist[b][a] = int(d)
        cities.add(a)
        cities.add(b)

    def route_distance(route):
        return sum(dist[route[i]][route[i + 1]] for i in range(len(route) - 1))

    distances = [route_distance(perm) for perm in permutations(cities)]

    part1 = str(min(distances))
    part2 = str(max(distances))

    return part1, part2
