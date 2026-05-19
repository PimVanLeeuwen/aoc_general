"""
Day 12 - Garden Groups
Year: 2024

Calculate fencing costs for garden regions: area * perimeter
for part 1, area * number of sides for part 2.
"""

from collections import deque


def find_region(grid, start_r, start_c, visited):
    """BFS to find all cells in a connected region."""
    rows, cols = len(grid), len(grid[0])
    plant = grid[start_r][start_c]
    region = set()
    queue = deque([(start_r, start_c)])
    region.add((start_r, start_c))

    while queue:
        r, c = queue.popleft()
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) not in region:
                if grid[nr][nc] == plant:
                    region.add((nr, nc))
                    queue.append((nr, nc))

    visited.update(region)
    return region


def perimeter(region):
    """Count edges between region cells and non-region cells."""
    count = 0
    for r, c in region:
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            if (r + dr, c + dc) not in region:
                count += 1
    return count


def count_corners(region):
    """Count corners of the region polygon (equals number of sides)."""
    corners = 0
    for r, c in region:
        # Outer corners: two adjacent sides are outside
        if (r - 1, c) not in region and (r, c - 1) not in region:
            corners += 1
        if (r - 1, c) not in region and (r, c + 1) not in region:
            corners += 1
        if (r + 1, c) not in region and (r, c - 1) not in region:
            corners += 1
        if (r + 1, c) not in region and (r, c + 1) not in region:
            corners += 1
        # Inner corners: two adjacent sides are inside but diagonal is outside
        if (r - 1, c) in region and (r, c - 1) in region and (r - 1, c - 1) not in region:
            corners += 1
        if (r - 1, c) in region and (r, c + 1) in region and (r - 1, c + 1) not in region:
            corners += 1
        if (r + 1, c) in region and (r, c - 1) in region and (r + 1, c - 1) not in region:
            corners += 1
        if (r + 1, c) in region and (r, c + 1) in region and (r + 1, c + 1) not in region:
            corners += 1
    return corners


def solve(puzzle_input: str) -> tuple[str, str]:
    grid = puzzle_input.strip().split("\n")
    rows, cols = len(grid), len(grid[0])
    visited = set()

    part1 = 0
    part2 = 0

    for r in range(rows):
        for c in range(cols):
            if (r, c) not in visited:
                region = find_region(grid, r, c, visited)
                area = len(region)
                part1 += area * perimeter(region)
                part2 += area * count_corners(region)

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    grid = puzzle_input.strip().split("\n")
    rows, cols = len(grid), len(grid[0])

    display_rows = min(20, rows)
    display_cols = min(40, cols)
    cells = []
    colors = {}
    palette = ["#ff0000", "#00ff41", "#00aaff", "#ffaa00", "#ff00ff",
               "#00ffaa", "#ffff00", "#aa00ff", "#ff6600", "#0066ff"]
    for i, ch in enumerate(sorted(set(grid[r][c] for r in range(rows) for c in range(cols)))):
        colors[ch] = palette[i % len(palette)]

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
            "  Garden Groups",
            "  ===================================",
            "",
            f"  Grid: {rows} x {cols}",
            f"  Part 1: {part1} (area * perimeter)",
            f"  Part 2: {part2} (area * sides)",
        ],
        "delay": 500,
    }
