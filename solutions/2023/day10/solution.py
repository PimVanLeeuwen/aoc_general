"""
Day 10 - Pipe Maze
Year: 2023

Find the farthest point in a pipe loop from the start,
then count tiles enclosed by the loop.
"""

from collections import deque

# Which directions each pipe connects to: (dy, dx) pairs
CONNECTIONS = {
    "|": [(-1, 0), (1, 0)],
    "-": [(0, -1), (0, 1)],
    "L": [(-1, 0), (0, 1)],
    "J": [(-1, 0), (0, -1)],
    "7": [(1, 0), (0, -1)],
    "F": [(1, 0), (0, 1)],
}


def find_loop(grid, start):
    """BFS from start to find the main loop. Return set of loop positions and distances."""
    rows, cols = len(grid), len(grid[0])
    dist = {start: 0}
    queue = deque([start])

    while queue:
        r, c = queue.popleft()
        ch = grid[r][c]
        dirs = CONNECTIONS.get(ch, [])
        if ch == "S":
            # S connects in any direction that has a matching pipe
            dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) not in dist:
                neighbor = grid[nr][nc]
                # Check that neighbor connects back
                if neighbor in CONNECTIONS and (-dr, -dc) in CONNECTIONS[neighbor]:
                    dist[(nr, nc)] = dist[(r, c)] + 1
                    queue.append((nr, nc))

    return dist


def count_enclosed(grid, loop_positions):
    """Count tiles enclosed by the loop using the ray casting method.

    Scan each row left to right. Track crossings of the loop boundary.
    A '|' always toggles inside/outside. 'L...7' and 'F...J' also toggle,
    while 'L...J' and 'F...7' do not.
    """
    rows, cols = len(grid), len(grid[0])
    enclosed = 0

    for r in range(rows):
        inside = False
        last_corner = None
        for c in range(cols):
            if (r, c) in loop_positions:
                ch = grid[r][c]
                if ch == "|":
                    inside = not inside
                elif ch in "LF":
                    last_corner = ch
                elif ch == "J":
                    if last_corner == "L":
                        pass  # U-turn, no crossing
                    else:
                        inside = not inside
                    last_corner = None
                elif ch == "7":
                    if last_corner == "F":
                        pass  # U-turn, no crossing
                    else:
                        inside = not inside
                    last_corner = None
            else:
                if inside:
                    enclosed += 1

    return enclosed


def infer_start_pipe(grid, start):
    """Determine what pipe character S actually represents."""
    r, c = start
    rows, cols = len(grid), len(grid[0])
    connects = set()
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols:
            neighbor = grid[nr][nc]
            if neighbor in CONNECTIONS and (-dr, -dc) in CONNECTIONS[neighbor]:
                connects.add((dr, dc))

    for pipe, dirs in CONNECTIONS.items():
        if set(dirs) == connects:
            return pipe
    return "S"


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    grid = puzzle_input.strip().split("\n")

    # Find start
    start = None
    for r, row in enumerate(grid):
        for c, ch in enumerate(row):
            if ch == "S":
                start = (r, c)
                break
        if start:
            break

    dist = find_loop(grid, start)
    part1 = max(dist.values())

    # Replace S with its actual pipe for ray casting
    actual = infer_start_pipe(grid, start)
    grid = [list(row) for row in grid]
    grid[start[0]][start[1]] = actual

    part2 = count_enclosed(grid, set(dist.keys()))

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    """Yield frames showing the pipe maze."""
    grid = puzzle_input.strip().split("\n")
    rows, cols = len(grid), len(grid[0])

    # Find loop
    start = None
    for r, row in enumerate(grid):
        for c, ch in enumerate(row):
            if ch == "S":
                start = (r, c)
                break
        if start:
            break

    dist = find_loop(grid, start)
    loop_set = set(dist.keys())

    # Replace S for enclosed counting
    actual = infer_start_pipe(grid, start)
    grid_list = [list(row) for row in grid]
    grid_list[start[0]][start[1]] = actual

    # Build colored grid
    colors = {
        "P": "#00ff41",  # pipe (loop)
        "I": "#ff6600",  # inside
        ".": "#0f0f23",  # outside/ground
        "S": "#ffff00",  # start
    }

    # First frame: show the loop
    cells = []
    for r in range(rows):
        row = []
        for c in range(cols):
            if (r, c) == start:
                row.append("S")
            elif (r, c) in loop_set:
                row.append("P")
            else:
                row.append(".")
        cells.append(row)

    yield {"type": "grid", "cells": cells, "colors": colors, "delay": 400}

    # Second frame: show enclosed tiles
    # Ray cast to find inside tiles
    for r in range(rows):
        inside = False
        last_corner = None
        for c in range(cols):
            if (r, c) in loop_set:
                ch = grid_list[r][c]
                if ch == "|":
                    inside = not inside
                elif ch in "LF":
                    last_corner = ch
                elif ch == "J":
                    if last_corner != "L":
                        inside = not inside
                    last_corner = None
                elif ch == "7":
                    if last_corner != "F":
                        inside = not inside
                    last_corner = None
            else:
                if inside:
                    cells[r][c] = "I"

    yield {"type": "grid", "cells": cells, "colors": colors, "delay": 400}

    part1, part2 = solve(puzzle_input)

    yield {
        "type": "text",
        "lines": [
            "  ===================================",
            "  Results",
            "  ===================================",
            "",
            f"  Part 1: {part1} (farthest point)",
            f"  Part 2: {part2} (enclosed tiles)",
        ],
        "delay": 500,
    }
