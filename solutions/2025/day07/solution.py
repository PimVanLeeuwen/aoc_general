"""
Day 7 - Downhill Splits
Year: 2025

Traverse a grid downward where '.' moves straight down
and '^' splits into two diagonal paths. Count split points
(part 1) and total distinct routes (part 2).
"""

from functools import lru_cache
from collections import deque


def solve(puzzle_input: str) -> tuple[str, str]:
    grid = [list(line) for line in puzzle_input.split("\n") if line]
    rows = len(grid)
    cols = len(grid[0])

    # The entry point is the center column of the grid
    start_col = cols // 2

    # Part 1: BFS downward, counting split points encountered
    queue = deque([(0, start_col)])
    visited = {(0, start_col)}
    splits = set()

    while queue:
        r, c = queue.popleft()
        if r + 1 >= rows:
            continue

        below = grid[r + 1][c]
        if below == ".":
            if (r + 1, c) not in visited:
                visited.add((r + 1, c))
                queue.append((r + 1, c))
        elif below == "^":
            splits.add((r + 1, c))
            for dc in [-1, 1]:
                nc = c + dc
                if 0 <= nc < cols and (r + 1, nc) not in visited:
                    visited.add((r + 1, nc))
                    queue.append((r + 1, nc))

    part1 = len(splits)

    # Part 2: count all distinct routes from top to bottom
    @lru_cache(maxsize=None)
    def count_routes(r, c):
        if r >= rows or c < 0 or c >= cols:
            return 0
        if r == rows - 1:
            return 1
        if grid[r][c] == "^":
            return count_routes(r + 1, c - 1) + count_routes(r + 1, c + 1)
        else:
            return count_routes(r + 1, c)

    part2 = count_routes(0, start_col)

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    grid = [list(line) for line in puzzle_input.split("\n") if line]
    rows = len(grid)
    cols = len(grid[0])

    start_col = cols // 2

    # Run BFS and record the order cells are visited, plus split locations
    queue = deque([(0, start_col)])
    visited_order = [(0, start_col)]
    visited = {(0, start_col)}
    splits = set()

    while queue:
        r, c = queue.popleft()
        if r + 1 >= rows:
            continue
        below = grid[r + 1][c]
        if below == ".":
            if (r + 1, c) not in visited:
                visited.add((r + 1, c))
                visited_order.append((r + 1, c))
                queue.append((r + 1, c))
        elif below == "^":
            splits.add((r + 1, c))
            if (r + 1, c) not in visited:
                visited_order.append((r + 1, c))
                visited.add((r + 1, c))
            for dc in [-1, 1]:
                nc = c + dc
                if 0 <= nc < cols and (r + 1, nc) not in visited:
                    visited.add((r + 1, nc))
                    visited_order.append((r + 1, nc))
                    queue.append((r + 1, nc))

    # Determine display window centered on the visited cells
    if visited_order:
        min_c = min(c for _, c in visited_order)
        max_c = max(c for _, c in visited_order)
    else:
        min_c, max_c = start_col, start_col

    display_cols = 60
    center_c = (min_c + max_c) // 2
    col_start = max(0, center_c - display_cols // 2)
    col_end = min(cols, col_start + display_cols)
    col_start = max(0, col_end - display_cols)

    display_rows = min(50, rows)

    colors = {
        " ": "#0d1117",  # dark background
        ".": "#21262d",  # dim grid dots
        "S": "#f0c040",  # start marker
        "P": "#00ff41",  # path (green)
        "X": "#ff4444",  # split points (red)
        "H": "#58a6ff",  # wavefront head (blue)
    }

    def build_frame(path_so_far, head_cells=None):
        path_set = set(path_so_far)
        head_set = set(head_cells) if head_cells else set()
        frame = []
        for r in range(display_rows):
            row = []
            for c in range(col_start, col_end):
                if (r, c) in head_set:
                    row.append("H")
                elif (r, c) in splits and (r, c) in path_set:
                    row.append("X")
                elif (r, c) in path_set:
                    row.append("P")
                elif r == 0 and c == start_col:
                    row.append("S")
                elif grid[r][c] in (".", "^"):
                    row.append(".")
                else:
                    row.append(" ")
            frame.append(row)
        return frame

    # Show the raw grid first
    yield {
        "type": "grid",
        "cells": build_frame([]),
        "colors": colors,
        "delay": 600,
    }

    # Animate the BFS traversal in chunks
    num_frames = 12
    chunk_size = max(1, len(visited_order) // num_frames)

    for i in range(0, len(visited_order), chunk_size):
        path_so_far = visited_order[: i + chunk_size]
        head = visited_order[i : i + chunk_size]
        yield {
            "type": "grid",
            "cells": build_frame(path_so_far, head),
            "colors": colors,
            "delay": 250,
        }

    # Final frame with all paths highlighted, no wavefront
    yield {
        "type": "grid",
        "cells": build_frame(visited_order),
        "colors": colors,
        "delay": 600,
    }

    # Results
    part1, part2 = solve(puzzle_input)

    yield {
        "type": "text",
        "lines": [
            "  Downhill Splits",
            "  ─────────────────────────────",
            "",
            f"  Grid size:       {rows} x {cols}",
            f"  Cells reached:   {len(visited_order)}",
            f"  Split points:    {part1}",
            f"  Distinct routes: {part2}",
        ],
        "delay": 500,
    }
