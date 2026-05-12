"""
Day 15 - Chiton
Year: 2021

Find the lowest-risk path through a cave using Dijkstra's algorithm,
first on the original grid, then on a 5x tiled expansion.
"""

import heapq


def dijkstra(grid, rows, cols):
    """Find shortest path from top-left to bottom-right using Dijkstra."""
    dist = [[float("inf")] * cols for _ in range(rows)]
    dist[0][0] = 0
    heap = [(0, 0, 0)]  # (cost, row, col)

    while heap:
        cost, r, c = heapq.heappop(heap)
        if r == rows - 1 and c == cols - 1:
            return cost
        if cost > dist[r][c]:
            continue
        for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                new_cost = cost + grid[nr][nc]
                if new_cost < dist[nr][nc]:
                    dist[nr][nc] = new_cost
                    heapq.heappush(heap, (new_cost, nr, nc))

    return dist[rows - 1][cols - 1]


def expand_grid(grid):
    """Expand grid 5x in both dimensions with wrapping risk values."""
    rows, cols = len(grid), len(grid[0])
    big = [[0] * (cols * 5) for _ in range(rows * 5)]
    for tr in range(5):
        for tc in range(5):
            for r in range(rows):
                for c in range(cols):
                    val = (grid[r][c] + tr + tc - 1) % 9 + 1
                    big[tr * rows + r][tc * cols + c] = val
    return big


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    grid = [[int(c) for c in line] for line in puzzle_input.strip().split("\n")]
    rows, cols = len(grid), len(grid[0])

    part1 = dijkstra(grid, rows, cols)

    big = expand_grid(grid)
    part2 = dijkstra(big, rows * 5, cols * 5)

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    """Yield frames showing pathfinding."""
    grid = [[int(c) for c in line] for line in puzzle_input.strip().split("\n")]
    rows, cols = len(grid), len(grid[0])

    # Show the risk grid
    cells = [[str(grid[r][c]) for c in range(cols)] for r in range(rows)]
    colors = {str(i): f"#{20 + i * 26:02x}{20 + i * 20:02x}{40 + i * 15:02x}" for i in range(10)}

    yield {
        "type": "grid",
        "cells": cells,
        "colors": colors,
        "delay": 600,
    }

    part1 = dijkstra(grid, rows, cols)

    big = expand_grid(grid)
    part2 = dijkstra(big, rows * 5, cols * 5)

    yield {
        "type": "text",
        "lines": [
            "  Chiton",
            "",
            f"  Grid: {rows}x{cols}",
            f"  Expanded: {rows * 5}x{cols * 5}",
            "",
            "  ===================================",
            "  Results",
            "  ===================================",
            "",
            f"  Part 1: {part1} (original grid)",
            f"  Part 2: {part2} (5x expanded grid)",
        ],
        "delay": 500,
    }
