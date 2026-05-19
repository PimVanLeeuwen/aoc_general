"""
Day 16 - Reindeer Maze
Year: 2024

Navigate a maze where turning costs 1000 and moving costs 1.
Find the shortest path and all tiles on any shortest path.
"""

import heapq


DIRS = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # E, S, W, N


def solve(puzzle_input: str) -> tuple[str, str]:
    grid = puzzle_input.strip().split("\n")
    rows, cols = len(grid), len(grid[0])

    # Find start and end
    start = end = None
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "S":
                start = (r, c)
            elif grid[r][c] == "E":
                end = (r, c)

    # Dijkstra: state = (cost, row, col, direction_index)
    # Start facing East (direction 0)
    dist = {}
    pq = [(0, start[0], start[1], 0)]
    # Track predecessors for all optimal paths
    predecessors = {}
    best_cost = float("inf")

    while pq:
        cost, r, c, d = heapq.heappop(pq)

        if cost > best_cost:
            break

        if (r, c) == end:
            best_cost = cost
            continue

        if (r, c, d) in dist and dist[(r, c, d)] < cost:
            continue
        dist[(r, c, d)] = cost

        # Move forward
        dr, dc = DIRS[d]
        nr, nc = r + dr, c + dc
        if grid[nr][nc] != "#":
            new_cost = cost + 1
            state = (nr, nc, d)
            if state not in dist or dist[state] >= new_cost:
                if state not in dist or dist[state] > new_cost:
                    predecessors[state] = set()
                    dist[state] = new_cost
                predecessors.setdefault(state, set()).add((r, c, d))
                heapq.heappush(pq, (new_cost, nr, nc, d))

        # Turn left and right
        for nd in [(d + 1) % 4, (d - 1) % 4]:
            new_cost = cost + 1000
            state = (r, c, nd)
            if state not in dist or dist[state] >= new_cost:
                if state not in dist or dist[state] > new_cost:
                    predecessors[state] = set()
                    dist[state] = new_cost
                predecessors.setdefault(state, set()).add((r, c, d))
                heapq.heappush(pq, (new_cost, r, c, nd))

    part1 = best_cost

    # Backtrack from end to find all tiles on optimal paths
    tiles = set()
    visited_states = set()
    stack = []
    for d in range(4):
        if (end[0], end[1], d) in dist and dist[(end[0], end[1], d)] == best_cost:
            stack.append((end[0], end[1], d))

    while stack:
        state = stack.pop()
        if state in visited_states:
            continue
        visited_states.add(state)
        tiles.add((state[0], state[1]))
        for pred in predecessors.get(state, []):
            stack.append(pred)

    # Add start tile
    tiles.add(start)
    part2 = len(tiles)

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
            "  Reindeer Maze",
            "  ===================================",
            "",
            f"  Maze: {rows} x {cols}",
            f"  Part 1: {part1} (lowest score)",
            f"  Part 2: {part2} (tiles on best paths)",
        ],
        "delay": 500,
    }
