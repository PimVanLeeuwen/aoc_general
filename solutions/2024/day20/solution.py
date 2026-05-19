"""
Day 20 - Race Condition
Year: 2024

Find shortcuts through walls on a racetrack that save at
least 100 picoseconds. Part 1 allows 2-step cheats, part 2 allows 20.
"""

from collections import deque


def find_path(grid):
    """BFS to find the unique path from S to E."""
    rows, cols = len(grid), len(grid[0])
    start = end = None
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "S":
                start = (r, c)
            elif grid[r][c] == "E":
                end = (r, c)

    queue = deque([start])
    visited = {start: 0}
    parent = {start: None}

    while queue:
        r, c = queue.popleft()
        if (r, c) == end:
            break
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) not in visited:
                if grid[nr][nc] != "#":
                    visited[(nr, nc)] = visited[(r, c)] + 1
                    parent[(nr, nc)] = (r, c)
                    queue.append((nr, nc))

    # Reconstruct path
    path = []
    node = end
    while node is not None:
        path.append(node)
        node = parent[node]
    path.reverse()
    return path


def count_cheats(path, max_cheat_dist, min_saving):
    """Count pairs of path positions where a cheat saves enough time."""
    pos_to_idx = {pos: i for i, pos in enumerate(path)}
    count = 0

    for i, (r1, c1) in enumerate(path):
        for j in range(i + min_saving + 1, len(path)):
            r2, c2 = path[j]
            dist = abs(r1 - r2) + abs(c1 - c2)
            if dist <= max_cheat_dist and (j - i - dist) >= min_saving:
                count += 1

    return count


def solve(puzzle_input: str) -> tuple[str, str]:
    grid = puzzle_input.strip().split("\n")
    path = find_path(grid)

    part1 = count_cheats(path, 2, 100)
    part2 = count_cheats(path, 20, 100)

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    grid = puzzle_input.strip().split("\n")
    rows, cols = len(grid), len(grid[0])

    display_rows = min(25, rows)
    display_cols = min(40, cols)
    cells = []
    colors = {"#": "#666666", ".": "#1a1a1a", "S": "#00ff41", "E": "#ff0000"}

    for r in range(display_rows):
        row = []
        for c in range(display_cols):
            row.append(grid[r][c])
        cells.append(row)

    yield {"type": "grid", "cells": cells, "colors": colors, "delay": 800}

    part1, part2 = solve(puzzle_input)

    yield {
        "type": "text",
        "lines": [
            "  ===================================",
            "  Race Condition",
            "  ===================================",
            "",
            f"  Track: {rows} x {cols}",
            f"  Part 1: {part1} (2-step cheats saving 100+)",
            f"  Part 2: {part2} (20-step cheats saving 100+)",
        ],
        "delay": 500,
    }
