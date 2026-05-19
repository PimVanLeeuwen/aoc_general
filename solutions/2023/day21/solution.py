"""
Day 21 - Step Counter
Year: 2023

Count reachable garden plots after a given number of steps,
with quadratic extrapolation for the infinite grid in part 2.
"""

from collections import deque


def reachable_after(grid, start, steps):
    """BFS to count positions reachable in exactly `steps` steps."""
    rows, cols = len(grid), len(grid[0])
    current = {start}
    for _ in range(steps):
        next_set = set()
        for r, c in current:
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != "#":
                    next_set.add((nr, nc))
        current = next_set
    return len(current)


def reachable_infinite(grid, start, steps):
    """BFS on infinite tiling grid, counting positions at exact step parity."""
    rows, cols = len(grid), len(grid[0])
    visited = {}
    queue = deque([(start[0], start[1], 0)])
    visited[(start[0], start[1])] = 0

    while queue:
        r, c, dist = queue.popleft()
        if dist >= steps:
            continue
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if (nr, nc) not in visited and grid[nr % rows][nc % cols] != "#":
                visited[(nr, nc)] = dist + 1
                queue.append((nr, nc, dist + 1))

    parity = steps % 2
    return sum(1 for d in visited.values() if d % 2 == parity)


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    grid = puzzle_input.strip().split("\n")
    rows, cols = len(grid), len(grid[0])

    # Find start
    start = None
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "S":
                start = (r, c)
                break
        if start:
            break

    # Part 1: 64 steps (or 6 for small sample)
    p1_steps = 64 if rows > 20 else 6
    part1 = reachable_after(grid, start, p1_steps)

    # Part 2: 26501365 steps on infinite grid
    # The real input is 131x131 with S at center (65,65).
    # 26501365 = 65 + 202300 * 131
    # The reachable count is quadratic in the number of full grid widths.
    # Sample three points and fit a quadratic.
    target = 26501365
    if rows == 131 and cols == 131:
        half = rows // 2  # 65
        # Evaluate at n=0,1,2 grid-widths from center
        f0 = reachable_infinite(grid, start, half)
        f1 = reachable_infinite(grid, start, half + rows)
        f2 = reachable_infinite(grid, start, half + 2 * rows)

        # Quadratic interpolation: f(n) = a*n^2 + b*n + c
        c = f0
        a = (f2 - 2 * f1 + f0) // 2
        b = f1 - f0 - a
        n = (target - half) // rows  # 202300
        part2 = a * n * n + b * n + c
    else:
        part2 = 0

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    """Yield frames showing garden exploration."""
    grid = puzzle_input.strip().split("\n")
    rows, cols = len(grid), len(grid[0])

    start = None
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "S":
                start = (r, c)
                break
        if start:
            break

    # Show initial grid
    colors = {"#": "#666666", ".": "#0f0f23", "S": "#ffff00", "R": "#00ff41"}
    yield {
        "type": "grid",
        "cells": [list(row) for row in grid],
        "colors": colors,
        "delay": 300,
    }

    # Show reachable after a few steps
    steps = 6 if rows <= 20 else 10
    current = {start}
    for _ in range(steps):
        nxt = set()
        for r, c in current:
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != "#":
                    nxt.add((nr, nc))
        current = nxt

    cells = [list(row) for row in grid]
    for r, c in current:
        cells[r][c] = "R"

    yield {"type": "grid", "cells": cells, "colors": colors, "delay": 300}

    part1, part2 = solve(puzzle_input)
    yield {
        "type": "text",
        "lines": [
            "  ===================================",
            "  Results",
            "  ===================================",
            "",
            f"  Part 1: {part1} (finite grid)",
            f"  Part 2: {part2} (infinite grid)",
        ],
        "delay": 500,
    }
