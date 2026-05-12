"""
Day 15 - Oxygen System
Year: 2019

Explore a maze with an Intcode-driven repair droid using DFS, then
find shortest path to oxygen system and time to fill with oxygen.
"""

from collections import deque
from intcode import IntcodeComputer

# Movement commands and their reverse
DIRS = {1: (0, -1), 2: (0, 1), 3: (-1, 0), 4: (1, 0)}  # N, S, W, E
REVERSE = {1: 2, 2: 1, 3: 4, 4: 3}


def explore_map(program):
    """DFS-explore the entire map via the Intcode droid. Returns (grid, oxygen_pos)."""
    cpu = IntcodeComputer(program)
    grid = {(0, 0): 1}  # 0=wall, 1=open, 2=oxygen
    oxygen_pos = None
    x, y = 0, 0

    def dfs():
        nonlocal x, y, oxygen_pos
        for cmd, (dx, dy) in DIRS.items():
            nx, ny = x + dx, y + dy
            if (nx, ny) in grid:
                continue

            cpu.add_input(cmd)
            cpu.run_until_block()
            status = cpu.outputs.pop()

            grid[(nx, ny)] = status

            if status == 0:
                continue  # wall, droid didn't move

            if status == 2:
                oxygen_pos = (nx, ny)

            # Droid moved — recurse, then backtrack
            x, y = nx, ny
            dfs()

            cpu.add_input(REVERSE[cmd])
            cpu.run_until_block()
            cpu.outputs.pop()
            x, y = x - dx, y - dy

    dfs()
    return grid, oxygen_pos


def bfs_distance(grid, start, target):
    """BFS shortest path on the explored grid."""
    queue = deque([(start, 0)])
    visited = {start}
    while queue:
        pos, dist = queue.popleft()
        if pos == target:
            return dist
        x, y = pos
        for dx, dy in DIRS.values():
            npos = (x + dx, y + dy)
            if npos not in visited and grid.get(npos, 0) != 0:
                visited.add(npos)
                queue.append((npos, dist + 1))
    return -1


def oxygen_fill_time(grid, oxygen_pos):
    """BFS from oxygen system — time for oxygen to fill all open spaces."""
    queue = deque([(oxygen_pos, 0)])
    visited = {oxygen_pos}
    max_dist = 0
    while queue:
        pos, dist = queue.popleft()
        max_dist = max(max_dist, dist)
        x, y = pos
        for dx, dy in DIRS.values():
            npos = (x + dx, y + dy)
            if npos not in visited and grid.get(npos, 0) != 0:
                visited.add(npos)
                queue.append((npos, dist + 1))
    return max_dist


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    program = [int(x) for x in puzzle_input.strip().split(",")]

    grid, oxygen_pos = explore_map(program)

    part1 = bfs_distance(grid, (0, 0), oxygen_pos)
    part2 = oxygen_fill_time(grid, oxygen_pos)

    return str(part1), str(part2)


def render_grid(grid, oxygen_pos, highlight=None, filled=None):
    """Render the explored grid as cells for visualization."""
    all_pos = grid.keys()
    min_x = min(x for x, y in all_pos)
    max_x = max(x for x, y in all_pos)
    min_y = min(y for x, y in all_pos)
    max_y = max(y for x, y in all_pos)

    cells = []
    for y in range(min_y, max_y + 1):
        row = []
        for x in range(min_x, max_x + 1):
            pos = (x, y)
            if pos == (0, 0):
                row.append("S")
            elif filled and pos in filled:
                row.append("O")
            elif pos == oxygen_pos:
                row.append("T")
            elif highlight and pos in highlight:
                row.append("P")
            elif grid.get(pos, -1) == 0:
                row.append("#")
            elif grid.get(pos, -1) in (1, 2):
                row.append(".")
            else:
                row.append(" ")
        cells.append(row)
    return cells


def visualize(puzzle_input: str):
    """Yield frames showing maze exploration and oxygen fill."""
    program = [int(x) for x in puzzle_input.strip().split(",")]

    grid, oxygen_pos = explore_map(program)
    open_count = sum(1 for v in grid.values() if v != 0)

    yield {
        "type": "text",
        "lines": [
            "  Oxygen System — Repair Droid",
            "",
            f"  Map explored: {len(grid)} cells",
            f"  Open spaces: {open_count}",
            f"  Oxygen system at: {oxygen_pos}",
        ],
        "delay": 600,
    }

    # Show the full map
    cells = render_grid(grid, oxygen_pos)
    yield {
        "type": "grid",
        "cells": cells,
        "colors": {
            " ": "#0f0f23",
            "#": "#444466",
            ".": "#1a1a2e",
            "S": "#00ff41",
            "T": "#ff4444",
        },
        "delay": 600,
    }

    # Show shortest path
    dist = bfs_distance(grid, (0, 0), oxygen_pos)

    # Trace path via BFS parent tracking
    queue = deque([(0, 0)])
    parent = {(0, 0): None}
    while queue:
        pos = queue.popleft()
        if pos == oxygen_pos:
            break
        px, py = pos
        for dx, dy in DIRS.values():
            npos = (px + dx, py + dy)
            if npos not in parent and grid.get(npos, 0) != 0:
                parent[npos] = pos
                queue.append(npos)

    path = set()
    pos = oxygen_pos
    while pos is not None:
        path.add(pos)
        pos = parent.get(pos)

    cells = render_grid(grid, oxygen_pos, highlight=path)
    yield {
        "type": "grid",
        "cells": cells,
        "colors": {
            " ": "#0f0f23",
            "#": "#444466",
            ".": "#1a1a2e",
            "S": "#00ff41",
            "T": "#ff4444",
            "P": "#ffff00",
        },
        "delay": 600,
    }

    # Show oxygen fill
    fill_time = oxygen_fill_time(grid, oxygen_pos)
    filled = {oxygen_pos}
    frontier = deque([(oxygen_pos, 0)])
    step = max(1, fill_time // 15)

    while frontier:
        pos, t = frontier.popleft()
        px, py = pos
        for dx, dy in DIRS.values():
            npos = (px + dx, py + dy)
            if npos not in filled and grid.get(npos, 0) != 0:
                filled.add(npos)
                frontier.append((npos, t + 1))

        if t % step == 0 and t > 0:
            cells = render_grid(grid, oxygen_pos, filled=filled)
            yield {
                "type": "grid",
                "cells": cells,
                "colors": {
                    " ": "#0f0f23",
                    "#": "#444466",
                    ".": "#1a1a2e",
                    "S": "#00ff41",
                    "T": "#ff4444",
                    "O": "#4488ff",
                },
                "delay": 80,
            }

    yield {
        "type": "text",
        "lines": [
            "  ===================================",
            "  Results",
            "  ===================================",
            "",
            f"  Part 1: {dist} steps to oxygen system",
            f"  Part 2: {fill_time} minutes to fill with oxygen",
        ],
        "delay": 500,
    }
