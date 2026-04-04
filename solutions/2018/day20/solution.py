"""
Day 20 - A Regular Map
Year: 2018

Parse a regex describing paths through a facility to build a map of rooms
and doors, then BFS to find shortest distances.
"""

from collections import deque


def build_graph(regex: str) -> dict[tuple[int, int], set[tuple[int, int]]]:
    """Parse the regex and return an adjacency graph of room positions."""
    DIRS = {'N': (0, -1), 'S': (0, 1), 'E': (1, 0), 'W': (-1, 0)}
    graph: dict[tuple[int, int], set[tuple[int, int]]] = {}
    # Stack of sets of positions (for branches)
    stack: list[tuple[set, set]] = []  # (starts, ends)
    pos = {(0, 0)}  # current set of positions

    for ch in regex[1:-1]:  # skip ^ and $
        if ch in DIRS:
            dx, dy = DIRS[ch]
            new_pos = set()
            for x, y in pos:
                nx, ny = x + dx, y + dy
                graph.setdefault((x, y), set()).add((nx, ny))
                graph.setdefault((nx, ny), set()).add((x, y))
                new_pos.add((nx, ny))
            pos = new_pos
        elif ch == '(':
            stack.append((pos, set()))
        elif ch == '|':
            starts, ends = stack[-1]
            stack[-1] = (starts, ends | pos)
            pos = starts
        elif ch == ')':
            starts, ends = stack.pop()
            pos = ends | pos

    return graph


def bfs_distances(graph: dict) -> dict[tuple[int, int], int]:
    """BFS from (0,0), return distance to every reachable room."""
    dist = {(0, 0): 0}
    queue = deque([(0, 0)])
    while queue:
        node = queue.popleft()
        d = dist[node]
        for nb in graph.get(node, ()):
            if nb not in dist:
                dist[nb] = d + 1
                queue.append(nb)
    return dist


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    regex = puzzle_input.strip()
    graph = build_graph(regex)
    distances = bfs_distances(graph)

    part1 = max(distances.values())
    part2 = sum(1 for d in distances.values() if d >= 1000)

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    """Yield visualization frames showing the map being explored."""
    regex = puzzle_input.strip()
    graph = build_graph(regex)
    distances = bfs_distances(graph)

    # Build the grid representation
    all_rooms = set(graph.keys())
    if not all_rooms:
        return

    min_x = min(x for x, y in all_rooms)
    max_x = max(x for x, y in all_rooms)
    min_y = min(y for x, y in all_rooms)
    max_y = max(y for x, y in all_rooms)

    # Grid: each room is at (2*(x-min_x)+1, 2*(y-min_y)+1) in grid coords
    gw = 2 * (max_x - min_x) + 3
    gh = 2 * (max_y - min_y) + 3

    def make_grid():
        grid = [['#'] * gw for _ in range(gh)]
        for (rx, ry) in all_rooms:
            gx = 2 * (rx - min_x) + 1
            gy = 2 * (ry - min_y) + 1
            grid[gy][gx] = '.'
            for (nx, ny) in graph.get((rx, ry), ()):
                dx, dy = nx - rx, ny - ry
                grid[gy + dy][gx + dx] = '-' if dy != 0 else '|'
        sx = 2 * (0 - min_x) + 1
        sy = 2 * (0 - min_y) + 1
        grid[sy][sx] = 'X'
        return grid

    grid = make_grid()

    yield {
        "type": "grid",
        "cells": grid,
        "colors": {
            "#": "#333333",
            ".": "#0f0f23",
            "|": "#666666",
            "-": "#666666",
            "X": "#ff0000",
        },
        "delay": 2000,
    }

    # Animate BFS exploration in waves
    max_dist = max(distances.values())
    wave_step = max(1, max_dist // 60)

    for wave in range(0, max_dist + 1, wave_step):
        colored_grid = [row[:] for row in grid]
        for (rx, ry), d in distances.items():
            if d <= wave:
                gx = 2 * (rx - min_x) + 1
                gy = 2 * (ry - min_y) + 1
                if d >= 1000:
                    colored_grid[gy][gx] = 'F'  # far
                else:
                    colored_grid[gy][gx] = 'N'  # near

        sx = 2 * (0 - min_x) + 1
        sy = 2 * (0 - min_y) + 1
        colored_grid[sy][sx] = 'X'

        yield {
            "type": "grid",
            "cells": colored_grid,
            "colors": {
                "#": "#333333",
                ".": "#0f0f23",
                "|": "#666666",
                "-": "#666666",
                "X": "#ff0000",
                "N": "#00ff41",
                "F": "#ff6600",
            },
            "delay": 80,
        }

    # Final summary
    yield {
        "type": "text",
        "lines": [
            f"Map: {len(all_rooms)} rooms explored",
            f"Part 1: Furthest room is {max(distances.values())} doors away",
            f"Part 2: {sum(1 for d in distances.values() if d >= 1000)} rooms ≥ 1000 doors away",
        ],
        "delay": 3000,
    }
