"""
Day 18 - Many-Worlds Interpretation
Year: 2019

Navigate a vault maze collecting all keys in the fewest steps.
Part 2 splits the maze into four quadrants with four robots.
"""

from collections import deque
from heapq import heappush, heappop


def parse_grid(text):
    """Parse the maze into a 2D list of characters."""
    return [list(line) for line in text.strip().split("\n")]


def bfs_reachable(grid, start):
    """BFS from a position, returning {key_char: (dist, doors_bitmask)} for all reachable keys.

    doors_bitmask tracks which door keys are needed to reach each target.
    """
    sx, sy = start
    queue = deque([(sx, sy, 0, 0)])
    visited = {(sx, sy)}
    results = {}

    while queue:
        x, y, dist, doors = queue.popleft()
        ch = grid[y][x]

        if dist > 0 and "a" <= ch <= "z":
            results[ch] = (dist, doors)

        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if 0 <= ny < len(grid) and 0 <= nx < len(grid[0]) and (nx, ny) not in visited:
                cell = grid[ny][nx]
                if cell == "#":
                    continue
                visited.add((nx, ny))
                new_doors = doors
                if "A" <= cell <= "Z":
                    new_doors = doors | (1 << (ord(cell) - ord("A")))
                queue.append((nx, ny, dist + 1, new_doors))

    return results


def solve_maze(grid, starts):
    """Dijkstra on (robot_positions, keys_held) state space.

    Precomputes BFS distances between all points of interest (starts + keys),
    then searches over key collection orderings.
    """
    # Find all keys and assign bit indices
    keys = {}
    for y, row in enumerate(grid):
        for x, ch in enumerate(row):
            if "a" <= ch <= "z":
                keys[ch] = (x, y)

    all_keys_mask = (1 << len(keys)) - 1
    key_to_bit = {k: i for i, k in enumerate(sorted(keys))}

    # Points of interest: starts labeled '0'..'3', keys labeled by letter
    poi = {}
    for i, s in enumerate(starts):
        poi[str(i)] = s
    for k, pos in keys.items():
        poi[k] = pos

    # BFS from each POI to find reachable keys with distances and door requirements
    graph = {}
    for label, pos in poi.items():
        graph[label] = bfs_reachable(grid, pos)

    # Dijkstra over state (positions_tuple, keys_bitmask)
    start_labels = tuple(str(i) for i in range(len(starts)))
    dist_map = {(start_labels, 0): 0}
    heap = [(0, start_labels, 0)]

    while heap:
        d, positions, keys_held = heappop(heap)

        if keys_held == all_keys_mask:
            return d

        if d > dist_map.get((positions, keys_held), float("inf")):
            continue

        for ri, pos_label in enumerate(positions):
            if pos_label not in graph:
                continue
            for target_key, (step_dist, doors_needed) in graph[pos_label].items():
                # Skip if we already have this key
                target_bit = key_to_bit[target_key]
                if keys_held & (1 << target_bit):
                    continue
                # Skip if we don't have keys for the doors in the way
                if doors_needed & ~keys_held:
                    continue

                new_keys = keys_held | (1 << target_bit)
                new_positions = list(positions)
                new_positions[ri] = target_key
                new_positions = tuple(new_positions)

                new_dist = d + step_dist
                state = (new_positions, new_keys)

                if new_dist < dist_map.get(state, float("inf")):
                    dist_map[state] = new_dist
                    heappush(heap, (new_dist, new_positions, new_keys))

    return -1


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    grid = parse_grid(puzzle_input)

    # Find the single entrance
    starts = []
    for y, row in enumerate(grid):
        for x, ch in enumerate(row):
            if ch == "@":
                starts.append((x, y))

    # Part 1: single robot
    part1 = solve_maze(grid, starts)

    # Part 2: split into four quadrants
    sx, sy = starts[0]
    grid2 = parse_grid(puzzle_input)
    grid2[sy - 1][sx - 1] = "@"
    grid2[sy - 1][sx] = "#"
    grid2[sy - 1][sx + 1] = "@"
    grid2[sy][sx - 1] = "#"
    grid2[sy][sx] = "#"
    grid2[sy][sx + 1] = "#"
    grid2[sy + 1][sx - 1] = "@"
    grid2[sy + 1][sx] = "#"
    grid2[sy + 1][sx + 1] = "@"

    starts2 = [
        (sx - 1, sy - 1), (sx + 1, sy - 1),
        (sx - 1, sy + 1), (sx + 1, sy + 1),
    ]
    part2 = solve_maze(grid2, starts2)

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    """Yield frames showing the vault maze and key collection."""
    grid = parse_grid(puzzle_input)

    # Find keys, doors, and start
    keys = {}
    doors = {}
    start = None
    for y, row in enumerate(grid):
        for x, ch in enumerate(row):
            if ch == "@":
                start = (x, y)
            elif "a" <= ch <= "z":
                keys[ch] = (x, y)
            elif "A" <= ch <= "Z":
                doors[ch] = (x, y)

    # Render the maze
    cells = []
    for y, row in enumerate(grid):
        r = []
        for x, ch in enumerate(row):
            if ch == "#":
                r.append("#")
            elif ch == "@":
                r.append("@")
            elif "a" <= ch <= "z":
                r.append("k")
            elif "A" <= ch <= "Z":
                r.append("D")
            else:
                r.append(".")
        cells.append(r)

    yield {
        "type": "grid",
        "cells": cells,
        "colors": {
            "#": "#444466",
            ".": "#1a1a2e",
            "@": "#00ff41",
            "k": "#ffff00",
            "D": "#ff6644",
        },
        "delay": 800,
    }

    yield {
        "type": "text",
        "lines": [
            "  Many-Worlds Interpretation",
            "",
            f"  Maze: {len(grid[0])}x{len(grid)}",
            f"  Keys: {len(keys)} ({', '.join(sorted(keys))})",
            f"  Doors: {len(doors)}",
            "",
            "  Finding shortest path to collect all keys...",
        ],
        "delay": 600,
    }

    starts = [start]
    part1 = solve_maze(grid, starts)

    # Part 2
    sx, sy = start
    grid2 = parse_grid(puzzle_input)
    grid2[sy - 1][sx - 1] = "@"
    grid2[sy - 1][sx] = "#"
    grid2[sy - 1][sx + 1] = "@"
    grid2[sy][sx - 1] = "#"
    grid2[sy][sx] = "#"
    grid2[sy][sx + 1] = "#"
    grid2[sy + 1][sx - 1] = "@"
    grid2[sy + 1][sx] = "#"
    grid2[sy + 1][sx + 1] = "@"

    starts2 = [
        (sx - 1, sy - 1), (sx + 1, sy - 1),
        (sx - 1, sy + 1), (sx + 1, sy + 1),
    ]

    # Show modified grid
    cells2 = []
    for y, row in enumerate(grid2):
        r = []
        for x, ch in enumerate(row):
            if ch == "#":
                r.append("#")
            elif ch == "@":
                r.append("@")
            elif "a" <= ch <= "z":
                r.append("k")
            elif "A" <= ch <= "Z":
                r.append("D")
            else:
                r.append(".")
        cells2.append(r)

    yield {
        "type": "grid",
        "cells": cells2,
        "colors": {
            "#": "#444466",
            ".": "#1a1a2e",
            "@": "#00ff41",
            "k": "#ffff00",
            "D": "#ff6644",
        },
        "delay": 800,
    }

    part2 = solve_maze(grid2, starts2)

    yield {
        "type": "text",
        "lines": [
            "  ===================================",
            "  Results",
            "  ===================================",
            "",
            f"  Part 1: {part1} steps (single robot)",
            f"  Part 2: {part2} steps (four robots)",
        ],
        "delay": 500,
    }
