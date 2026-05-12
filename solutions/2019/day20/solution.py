"""
Day 20 - Donut Maze
Year: 2019

Navigate a donut-shaped maze with labeled portals. Part 2 adds
recursive depth — outer portals go up, inner portals go down.
"""

from collections import deque


def parse_maze(text):
    """Parse the maze, returning walkable tiles, portals, start, and end.

    Returns:
        passages: set of (x, y) open tiles
        portals: dict mapping (x, y) -> (x2, y2) for portal connections
        start: (x, y) of AA
        end: (x, y) of ZZ
        is_outer: dict mapping portal (x, y) -> True if on outer edge
    """
    lines = text.split("\n")
    # Pad lines to uniform width
    width = max(len(line) for line in lines)
    lines = [line.ljust(width) for line in lines]
    height = len(lines)

    passages = set()
    for y in range(height):
        for x in range(width):
            if lines[y][x] == ".":
                passages.add((x, y))

    # Find all two-letter labels adjacent to a passage
    labels = {}  # label_str -> list of (passage_x, passage_y, is_outer)

    # Find the bounds of the actual maze (the # border)
    maze_top = maze_left = float("inf")
    maze_bottom = maze_right = 0
    for y in range(height):
        for x in range(width):
            if lines[y][x] == "#":
                maze_top = min(maze_top, y)
                maze_bottom = max(maze_bottom, y)
                maze_left = min(maze_left, x)
                maze_right = max(maze_right, x)

    def is_outer_pos(x, y):
        """Check if a portal position is on the outer edge of the maze."""
        return x <= maze_left + 1 or x >= maze_right - 1 or y <= maze_top + 1 or y >= maze_bottom - 1

    for y in range(height):
        for x in range(width):
            ch = lines[y][x]
            if not ch.isupper():
                continue

            # Horizontal label: two letters side by side
            if x + 1 < width and lines[y][x + 1].isupper():
                label = ch + lines[y][x + 1]
                # The passage is either to the left of first or right of second
                if x - 1 >= 0 and (x - 1, y) in passages:
                    pos = (x - 1, y)
                elif x + 2 < width and (x + 2, y) in passages:
                    pos = (x + 2, y)
                else:
                    continue
                outer = is_outer_pos(x, y)
                labels.setdefault(label, []).append((pos[0], pos[1], outer))

            # Vertical label: two letters stacked
            if y + 1 < height and lines[y + 1][x].isupper():
                label = ch + lines[y + 1][x]
                if y - 1 >= 0 and (x, y - 1) in passages:
                    pos = (x, y - 1)
                elif y + 2 < height and (x, y + 2) in passages:
                    pos = (x, y + 2)
                else:
                    continue
                outer = is_outer_pos(x, y)
                labels.setdefault(label, []).append((pos[0], pos[1], outer))

    start = end = None
    portals = {}
    is_outer = {}

    for label, positions in labels.items():
        if label == "AA":
            start = (positions[0][0], positions[0][1])
        elif label == "ZZ":
            end = (positions[0][0], positions[0][1])
        else:
            # Connect the two portal endpoints
            x1, y1, o1 = positions[0]
            x2, y2, o2 = positions[1]
            portals[(x1, y1)] = (x2, y2)
            portals[(x2, y2)] = (x1, y1)
            is_outer[(x1, y1)] = o1
            is_outer[(x2, y2)] = o2

    return passages, portals, start, end, is_outer


def bfs_flat(passages, portals, start, end):
    """BFS through the maze with portals (no recursion levels)."""
    queue = deque([(start, 0)])
    visited = {start}

    while queue:
        (x, y), dist = queue.popleft()
        if (x, y) == end:
            return dist

        neighbors = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
        # Add portal jump if available
        if (x, y) in portals:
            neighbors.append(portals[(x, y)])

        for nx, ny in neighbors:
            if (nx, ny) in passages and (nx, ny) not in visited:
                visited.add((nx, ny))
                queue.append(((nx, ny), dist + 1))

    return -1


def bfs_recursive(passages, portals, start, end, is_outer):
    """BFS with recursive levels. Outer portals go up (level-1), inner go down (level+1).

    AA and ZZ only work at level 0. Outer portals are walls at level 0.
    """
    queue = deque([(start[0], start[1], 0, 0)])  # x, y, level, dist
    visited = {(start[0], start[1], 0)}

    while queue:
        x, y, level, dist = queue.popleft()

        if (x, y) == end and level == 0:
            return dist

        # Normal movement
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nx, ny = x + dx, y + dy
            if (nx, ny) in passages and (nx, ny, level) not in visited:
                visited.add((nx, ny, level))
                queue.append((nx, ny, level, dist + 1))

        # Portal jump
        if (x, y) in portals:
            outer = is_outer[(x, y)]
            if outer:
                # Outer portal goes up one level (only if not at level 0)
                if level > 0:
                    new_level = level - 1
                    tx, ty = portals[(x, y)]
                    if (tx, ty, new_level) not in visited:
                        visited.add((tx, ty, new_level))
                        queue.append((tx, ty, new_level, dist + 1))
            else:
                # Inner portal goes down one level
                new_level = level + 1
                if new_level <= 30:  # reasonable depth limit
                    tx, ty = portals[(x, y)]
                    if (tx, ty, new_level) not in visited:
                        visited.add((tx, ty, new_level))
                        queue.append((tx, ty, new_level, dist + 1))

    return -1


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    passages, portals, start, end, is_outer = parse_maze(puzzle_input)

    part1 = bfs_flat(passages, portals, start, end)
    part2 = bfs_recursive(passages, portals, start, end, is_outer)

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    """Yield frames showing the donut maze and portal connections."""
    passages, portals, start, end, is_outer = parse_maze(puzzle_input)
    lines = puzzle_input.split("\n")
    width = max(len(line) for line in lines)
    lines = [line.ljust(width) for line in lines]

    # Render the maze
    portal_tiles = set(portals.keys())
    cells = []
    for y, line in enumerate(lines):
        row = []
        for x, ch in enumerate(line):
            if (x, y) == start:
                row.append("S")
            elif (x, y) == end:
                row.append("E")
            elif (x, y) in portal_tiles:
                row.append("P")
            elif ch == "#":
                row.append("#")
            elif ch == ".":
                row.append(".")
            elif ch.isupper():
                row.append("L")
            else:
                row.append(" ")
        cells.append(row)

    yield {
        "type": "grid",
        "cells": cells,
        "colors": {
            " ": "#0f0f23",
            "#": "#444466",
            ".": "#1a1a2e",
            "S": "#00ff41",
            "E": "#ff4444",
            "P": "#ffff00",
            "L": "#666688",
        },
        "delay": 800,
    }

    num_portals = len(portals) // 2
    yield {
        "type": "text",
        "lines": [
            "  Donut Maze",
            "",
            f"  Size: {width}x{len(lines)}",
            f"  Open tiles: {len(passages)}",
            f"  Portal pairs: {num_portals}",
            f"  Start (AA): {start}",
            f"  End (ZZ): {end}",
        ],
        "delay": 600,
    }

    part1 = bfs_flat(passages, portals, start, end)
    part2 = bfs_recursive(passages, portals, start, end, is_outer)

    yield {
        "type": "text",
        "lines": [
            "  ===================================",
            "  Results",
            "  ===================================",
            "",
            f"  Part 1: {part1} steps (flat portals)",
            f"  Part 2: {part2} steps (recursive levels)",
        ],
        "delay": 500,
    }
