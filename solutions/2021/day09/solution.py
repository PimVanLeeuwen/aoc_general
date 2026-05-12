"""
Day 09 - Smoke Basin
Year: 2021

Find low points in a heightmap and flood-fill basins to find
the three largest.
"""

from collections import deque


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    grid = [[int(c) for c in line] for line in puzzle_input.strip().split("\n")]
    rows, cols = len(grid), len(grid[0])
    neighbors = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # Part 1: find low points (lower than all adjacent)
    low_points = []
    risk_sum = 0
    for r in range(rows):
        for c in range(cols):
            h = grid[r][c]
            if all(
                grid[r + dr][c + dc] > h
                for dr, dc in neighbors
                if 0 <= r + dr < rows and 0 <= c + dc < cols
            ):
                low_points.append((r, c))
                risk_sum += h + 1

    # Part 2: BFS flood-fill basins from each low point
    visited = set()
    basin_sizes = []

    for lr, lc in low_points:
        if (lr, lc) in visited:
            continue
        queue = deque([(lr, lc)])
        visited.add((lr, lc))
        size = 0
        while queue:
            r, c = queue.popleft()
            size += 1
            for dr, dc in neighbors:
                nr, nc = r + dr, c + dc
                if (0 <= nr < rows and 0 <= nc < cols
                        and (nr, nc) not in visited
                        and grid[nr][nc] != 9):
                    visited.add((nr, nc))
                    queue.append((nr, nc))
        basin_sizes.append(size)

    basin_sizes.sort(reverse=True)
    part2 = basin_sizes[0] * basin_sizes[1] * basin_sizes[2]

    return str(risk_sum), str(part2)


def visualize(puzzle_input: str):
    """Yield frames showing the heightmap and basins."""
    grid = [[int(c) for c in line] for line in puzzle_input.strip().split("\n")]
    rows, cols = len(grid), len(grid[0])

    # Show heightmap as a grid
    shade = " .:-=+*#%@"
    cells = []
    for r in range(rows):
        row = []
        for c in range(cols):
            row.append(str(grid[r][c]))
        cells.append(row)

    colors = {}
    for i in range(10):
        intensity = int(35 + i * 22)
        colors[str(i)] = f"#{intensity:02x}{intensity:02x}{intensity + 20:02x}"

    yield {
        "type": "grid",
        "cells": cells,
        "colors": colors,
        "delay": 800,
    }

    # Compute results
    neighbors = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    low_points = []
    risk_sum = 0
    for r in range(rows):
        for c in range(cols):
            h = grid[r][c]
            if all(
                grid[r + dr][c + dc] > h
                for dr, dc in neighbors
                if 0 <= r + dr < rows and 0 <= c + dc < cols
            ):
                low_points.append((r, c))
                risk_sum += h + 1

    visited = set()
    basin_sizes = []
    for lr, lc in low_points:
        if (lr, lc) in visited:
            continue
        queue = deque([(lr, lc)])
        visited.add((lr, lc))
        size = 0
        while queue:
            r, c = queue.popleft()
            size += 1
            for dr, dc in neighbors:
                nr, nc = r + dr, c + dc
                if (0 <= nr < rows and 0 <= nc < cols
                        and (nr, nc) not in visited
                        and grid[nr][nc] != 9):
                    visited.add((nr, nc))
                    queue.append((nr, nc))
        basin_sizes.append(size)

    basin_sizes.sort(reverse=True)
    part2 = basin_sizes[0] * basin_sizes[1] * basin_sizes[2]

    yield {
        "type": "text",
        "lines": [
            "  ===================================",
            "  Results",
            "  ===================================",
            "",
            f"  Low points: {len(low_points)}",
            f"  Part 1: {risk_sum} (risk level sum)",
            "",
            f"  Basins found: {len(basin_sizes)}",
            f"  Top 3 sizes: {basin_sizes[0]}, {basin_sizes[1]}, {basin_sizes[2]}",
            f"  Part 2: {part2}",
        ],
        "delay": 500,
    }
