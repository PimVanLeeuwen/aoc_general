"""
Day 11 - Dumbo Octopus
Year: 2021

Simulate flashing octopuses on a 10x10 grid, counting total flashes
after 100 steps and finding the first synchronized flash.
"""

from collections import deque


def step(grid):
    """Run one step: increment, flash cascades, reset. Returns flash count."""
    rows, cols = len(grid), len(grid[0])
    flashed = set()
    queue = deque()

    # Increment all
    for r in range(rows):
        for c in range(cols):
            grid[r][c] += 1
            if grid[r][c] > 9:
                queue.append((r, c))
                flashed.add((r, c))

    # Cascade flashes
    while queue:
        r, c = queue.popleft()
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) not in flashed:
                    grid[nr][nc] += 1
                    if grid[nr][nc] > 9:
                        flashed.add((nr, nc))
                        queue.append((nr, nc))

    # Reset flashed octopuses
    for r, c in flashed:
        grid[r][c] = 0

    return len(flashed)


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    grid = [[int(c) for c in line] for line in puzzle_input.strip().split("\n")]
    total = len(grid) * len(grid[0])

    part1 = 0
    part2 = 0
    s = 0

    while part2 == 0:
        s += 1
        flashes = step(grid)
        if s <= 100:
            part1 += flashes
        if flashes == total:
            part2 = s

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    """Yield frames showing octopus flashing."""
    grid = [[int(c) for c in line] for line in puzzle_input.strip().split("\n")]
    total = len(grid) * len(grid[0])

    # Show initial state
    cells = [[str(grid[r][c]) for c in range(len(grid[0]))] for r in range(len(grid))]
    colors = {str(i): f"#{30 + i * 25:02x}{30 + i * 25:02x}{50 + i * 20:02x}" for i in range(10)}
    colors["F"] = "#ffffff"

    yield {
        "type": "grid",
        "cells": cells,
        "colors": colors,
        "delay": 400,
    }

    # Show select steps
    part1 = 0
    for s in range(1, 300):
        flashes = step(grid)
        if s <= 100:
            part1 += flashes

        if s <= 10 or s % 10 == 0 or flashes == total:
            cells = []
            for r in range(len(grid)):
                row = []
                for c in range(len(grid[0])):
                    row.append("F" if grid[r][c] == 0 else str(grid[r][c]))
                cells.append(row)

            yield {
                "type": "grid",
                "cells": cells,
                "colors": colors,
                "delay": 200 if s <= 10 else 100,
            }

        if flashes == total:
            yield {
                "type": "text",
                "lines": [
                    "  ===================================",
                    "  Results",
                    "  ===================================",
                    "",
                    f"  Part 1: {part1} (flashes in 100 steps)",
                    f"  Part 2: {s} (first sync flash)",
                ],
                "delay": 500,
            }
            break
