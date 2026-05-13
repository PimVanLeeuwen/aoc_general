"""
Day 12 - Hill Climbing Algorithm
Year: 2022

BFS shortest path on a heightmap from start to end,
with elevation constraints.
"""

from collections import deque


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    grid = puzzle_input.strip().split("\n")
    rows, cols = len(grid), len(grid[0])

    # Find S and E, build height map
    height = {}
    start = end = None
    for r in range(rows):
        for c in range(cols):
            ch = grid[r][c]
            if ch == "S":
                start = (r, c)
                height[(r, c)] = 0
            elif ch == "E":
                end = (r, c)
                height[(r, c)] = 25
            else:
                height[(r, c)] = ord(ch) - ord("a")

    # BFS backwards from E — can step to neighbor if neighbor's height >= current - 1
    dist = {end: 0}
    queue = deque([end])

    while queue:
        r, c = queue.popleft()
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if (nr, nc) in height and (nr, nc) not in dist:
                if height[(nr, nc)] >= height[(r, c)] - 1:
                    dist[(nr, nc)] = dist[(r, c)] + 1
                    queue.append((nr, nc))

    part1 = dist.get(start, -1)

    # Part 2: shortest path from any 'a' elevation
    part2 = min(
        dist.get((r, c), float("inf"))
        for r in range(rows)
        for c in range(cols)
        if height[(r, c)] == 0
    )

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    """Yield frames showing the heightmap."""
    grid = puzzle_input.strip().split("\n")

    colors = {}
    for ch in "abcdefghijklmnopqrstuvwxyz":
        intensity = int(30 + (ord(ch) - ord("a")) * 8)
        colors[ch] = f"#00{intensity:02x}00"
    colors["S"] = "#ff0000"
    colors["E"] = "#ffff00"

    cells = [list(row) for row in grid]
    yield {"type": "grid", "cells": cells, "colors": colors, "delay": 600}

    part1, part2 = solve(puzzle_input)

    yield {
        "type": "text",
        "lines": [
            "  ===================================",
            "  Results",
            "  ===================================",
            "",
            f"  Part 1: {part1} (from S)",
            f"  Part 2: {part2} (from any 'a')",
        ],
        "delay": 500,
    }
