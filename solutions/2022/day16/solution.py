"""
Day 16 - Proboscidea Volcanium
Year: 2022

Find the maximum pressure release by opening valves in a tunnel network,
alone in 30 minutes or with an elephant helper in 26 minutes.
"""

import re
from itertools import combinations


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    # Parse valves
    valves = {}
    for line in puzzle_input.strip().split("\n"):
        match = re.match(
            r"Valve (\w+) has flow rate=(\d+); tunnels? leads? to valves? (.+)",
            line,
        )
        name = match.group(1)
        rate = int(match.group(2))
        tunnels = match.group(3).split(", ")
        valves[name] = (rate, tunnels)

    # Map valve names to indices
    names = list(valves.keys())
    idx = {n: i for i, n in enumerate(names)}

    # Floyd-Warshall for shortest distances
    n = len(names)
    dist = [[float("inf")] * n for _ in range(n)]
    for i in range(n):
        dist[i][i] = 0
        for t in valves[names[i]][1]:
            dist[i][idx[t]] = 1

    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]

    # Only care about valves with nonzero flow
    useful = [i for i in range(n) if valves[names[i]][0] > 0]
    rates = [valves[names[i]][0] for i in range(n)]
    start = idx["AA"]

    def search(time_limit):
        """DFS returning dict mapping frozenset of opened valves to max flow."""
        best = {}

        def dfs(pos, time_left, flow, opened):
            key = frozenset(opened)
            best[key] = max(best.get(key, 0), flow)

            for j in useful:
                if j in opened:
                    continue
                t = dist[pos][j] + 1
                if t >= time_left:
                    continue
                opened.add(j)
                dfs(j, time_left - t, flow + (time_left - t) * rates[j], opened)
                opened.remove(j)

        dfs(start, time_limit, 0, set())
        return best

    # Part 1: solo, 30 minutes
    results_30 = search(30)
    part1 = max(results_30.values())

    # Part 2: with elephant, 26 minutes each, disjoint valve sets
    results_26 = search(26)
    part2 = 0
    items = list(results_26.items())
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            if items[i][0].isdisjoint(items[j][0]):
                part2 = max(part2, items[i][1] + items[j][1])

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    """Yield frames showing valve network."""
    lines = puzzle_input.strip().split("\n")
    valve_count = len(lines)
    nonzero = sum(1 for l in lines if not l.endswith("rate=0;"))

    yield {
        "type": "text",
        "lines": [
            "  Proboscidea Volcanium",
            "",
            f"  Total valves: {valve_count}",
            f"  Nonzero flow valves: {nonzero}",
        ],
        "delay": 600,
    }

    part1, part2 = solve(puzzle_input)

    yield {
        "type": "text",
        "lines": [
            "  ===================================",
            "  Results",
            "  ===================================",
            "",
            f"  Part 1: {part1} (solo, 30 min)",
            f"  Part 2: {part2} (with elephant, 26 min)",
        ],
        "delay": 500,
    }
