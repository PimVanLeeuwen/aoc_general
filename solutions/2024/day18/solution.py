"""
Day 18 - RAM Run
Year: 2024

Navigate a grid with falling corrupted bytes. Find shortest
path after 1024 bytes, then find the byte that blocks all paths.
"""

from collections import deque


SIZE = 70


def bfs(blocked):
    """BFS from (0,0) to (SIZE,SIZE). Returns distance or -1 if unreachable."""
    if (0, 0) in blocked or (SIZE, SIZE) in blocked:
        return -1

    queue = deque([(0, 0, 0)])
    visited = {(0, 0)}

    while queue:
        x, y, dist = queue.popleft()

        if x == SIZE and y == SIZE:
            return dist

        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx <= SIZE and 0 <= ny <= SIZE and (nx, ny) not in visited and (nx, ny) not in blocked:
                visited.add((nx, ny))
                queue.append((nx, ny, dist + 1))

    return -1


def solve(puzzle_input: str) -> tuple[str, str]:
    lines = puzzle_input.strip().split("\n")
    bytes_list = []
    for line in lines:
        x, y = map(int, line.split(","))
        bytes_list.append((x, y))

    # Part 1: shortest path after first 1024 bytes
    blocked = set(bytes_list[:1024])
    part1 = bfs(blocked)

    # Part 2: binary search for the first byte that blocks all paths
    lo, hi = 1024, len(bytes_list) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        blocked = set(bytes_list[:mid + 1])
        if bfs(blocked) == -1:
            hi = mid
        else:
            lo = mid + 1

    part2 = f"{bytes_list[lo][0]},{bytes_list[lo][1]}"

    return str(part1), part2


def visualize(puzzle_input: str):
    lines = puzzle_input.strip().split("\n")
    bytes_list = []
    for line in lines:
        x, y = map(int, line.split(","))
        bytes_list.append((x, y))

    blocked = set(bytes_list[:1024])
    display = min(SIZE + 1, 30)
    cells = []
    colors = {"#": "#ff0000", ".": "#1a1a1a"}

    for y in range(display):
        row = []
        for x in range(display):
            row.append("#" if (x, y) in blocked else ".")
        cells.append(row)

    yield {"type": "grid", "cells": cells, "colors": colors, "delay": 800}

    part1, part2 = solve(puzzle_input)

    yield {
        "type": "text",
        "lines": [
            "  ===================================",
            "  RAM Run",
            "  ===================================",
            "",
            f"  Grid: {SIZE+1} x {SIZE+1}",
            f"  Total bytes: {len(bytes_list)}",
            f"  Part 1: {part1} (steps after 1024 bytes)",
            f"  Part 2: {part2} (blocking byte)",
        ],
        "delay": 500,
    }
