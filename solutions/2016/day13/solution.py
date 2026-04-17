"""
Day 13 - A Maze of Twisty Little Cubicles
Year: 2016

BFS through a procedurally generated maze to find shortest path and reachable area.
"""

from collections import deque


def is_wall(x, y, fav):
    if x < 0 or y < 0:
        return True
    n = x*x + 3*x + 2*x*y + y + y*y + fav
    return bin(n).count("1") % 2 == 1


def bfs(fav, target=None, max_steps=None):
    """BFS from (1,1). If target given, return steps to reach it.
    If max_steps given, return the set of reachable positions."""
    queue = deque([(1, 1, 0)])
    visited = {(1, 1)}

    while queue:
        x, y, steps = queue.popleft()

        if target and (x, y) == target:
            return steps
        if max_steps is not None and steps == max_steps:
            continue

        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if (nx, ny) not in visited and not is_wall(nx, ny, fav):
                visited.add((nx, ny))
                queue.append((nx, ny, steps + 1))

    return visited if max_steps is not None else -1


def solve(puzzle_input: str) -> tuple[str, str]:
    fav = int(puzzle_input.strip())

    part1 = bfs(fav, target=(31, 39))
    reachable = bfs(fav, max_steps=50)
    part2 = len(reachable)

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    """Animate BFS expanding through the maze, then highlight the solution path."""
    fav = int(puzzle_input.strip())
    target = (31, 39)
    width, height = 45, 45

    # Build static maze grid
    def render(visited, path=None, frontier=None):
        path_set = set(path) if path else set()
        frontier_set = set(frontier) if frontier else set()
        cells = []
        for y in range(height):
            row = []
            for x in range(width):
                if (x, y) == (1, 1):
                    row.append("S")
                elif (x, y) == target:
                    row.append("E")
                elif (x, y) in path_set:
                    row.append("*")
                elif (x, y) in frontier_set:
                    row.append("o")
                elif (x, y) in visited:
                    row.append(".")
                elif is_wall(x, y, fav):
                    row.append("#")
                else:
                    row.append(" ")
            cells.append(row)
        return cells

    colors = {
        "#": "#1a1a3e",
        " ": "#0f0f23",
        ".": "#003300",
        "o": "#00aa44",
        "*": "#ffff66",
        "S": "#00aaff",
        "E": "#ff5555",
    }

    # BFS with frame snapshots
    queue = deque([(1, 1, 0, [(1, 1)])])
    visited = {(1, 1): [(1, 1)]}  # pos -> path
    found_path = None
    frame_interval = 8
    step = 0

    while queue:
        x, y, steps, path = queue.popleft()

        if (x, y) == target:
            found_path = path
            break

        frontier = []
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if (nx, ny) not in visited and not is_wall(nx, ny, fav):
                visited[(nx, ny)] = path + [(nx, ny)]
                queue.append((nx, ny, steps + 1, path + [(nx, ny)]))
                frontier.append((nx, ny))

        step += 1
        if step % frame_interval == 0:
            yield {
                "type": "grid",
                "cells": render(visited, frontier=frontier),
                "colors": colors,
                "delay": 60,
            }

    # Final frame: show solution path
    if found_path:
        for _ in range(8):
            yield {
                "type": "grid",
                "cells": render(visited, path=found_path),
                "colors": colors,
                "delay": 120,
            }
