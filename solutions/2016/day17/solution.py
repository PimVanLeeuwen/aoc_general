"""
Day 17 - Two Steps Forward
Year: 2016

BFS through a 4x4 vault where open doors are determined by the MD5 hash of
the passcode plus the path taken so far.
"""

import hashlib
from collections import deque

# Directions: (name, dx, dy, hash_index)
DIRS = [("U", 0, -1, 0), ("D", 0, 1, 1), ("L", -1, 0, 2), ("R", 1, 0, 3)]


def open_doors(passcode, path):
    digest = hashlib.md5((passcode + path).encode()).hexdigest()
    return [d for d in DIRS if digest[d[3]] in "bcdef"]


def bfs(passcode):
    """Yield every path that reaches (3,3). First yielded is shortest."""
    queue = deque([(0, 0, "")])  # x, y, path
    while queue:
        x, y, path = queue.popleft()
        for name, dx, dy, _ in open_doors(passcode, path):
            nx, ny = x + dx, y + dy
            if not (0 <= nx < 4 and 0 <= ny < 4):
                continue
            new_path = path + name
            if nx == 3 and ny == 3:
                yield new_path
            else:
                queue.append((nx, ny, new_path))


def solve(puzzle_input: str) -> tuple[str, str]:
    passcode = puzzle_input.strip()
    paths = list(bfs(passcode))
    part1 = paths[0]
    part2 = len(paths[-1])
    return part1, str(part2)


def visualize(puzzle_input: str):
    """Animate BFS exploration of the vault, then replay the shortest path."""
    passcode = puzzle_input.strip()

    ROOM = "."
    WALL = "#"
    START = "S"
    END = "V"
    CURRENT = "@"
    VISITED = "+"

    def render(pos, visited_rooms, highlight_path=None):
        # 9x9 display grid (4 rooms + walls between)
        grid = []
        for row in range(9):
            grid.append([])
            for col in range(9):
                # corners / fixed walls
                if row % 2 == 0 and col % 2 == 0:
                    grid[row].append(WALL)
                elif row % 2 == 0:  # horizontal wall row
                    grid[row].append(WALL)
                elif col % 2 == 0:  # vertical wall col
                    grid[row].append(WALL)
                else:
                    rx, ry = col // 2, row // 2
                    if (rx, ry) == pos:
                        grid[row].append(CURRENT)
                    elif highlight_path and (rx, ry) in highlight_path:
                        grid[row].append(VISITED)
                    elif (rx, ry) == (0, 0):
                        grid[row].append(START)
                    elif (rx, ry) == (3, 3):
                        grid[row].append(END)
                    elif (rx, ry) in visited_rooms:
                        grid[row].append(VISITED)
                    else:
                        grid[row].append(ROOM)
        return grid

    colors = {
        WALL: "#1a1a3e",
        ROOM: "#0f0f23",
        START: "#00aaff",
        END: "#ff5555",
        CURRENT: "#ffff66",
        VISITED: "#003322",
    }

    # BFS with frame snapshots
    queue = deque([(0, 0, "")])
    visited_rooms = {(0, 0)}
    shortest = None
    longest_len = 0
    paths_found = 0
    frame_interval = 30
    step = 0

    while queue:
        x, y, path = queue.popleft()

        for name, dx, dy, _ in open_doors(passcode, path):
            nx, ny = x + dx, y + dy
            if not (0 <= nx < 4 and 0 <= ny < 4):
                continue
            new_path = path + name
            if nx == 3 and ny == 3:
                paths_found += 1
                if shortest is None:
                    shortest = new_path
                if len(new_path) > longest_len:
                    longest_len = len(new_path)
            else:
                visited_rooms.add((nx, ny))
                queue.append((nx, ny, new_path))

        step += 1
        if step % frame_interval == 0:
            yield {
                "type": "grid",
                "cells": render((x, y), visited_rooms),
                "colors": colors,
                "delay": 60,
            }

    # Replay shortest path step by step
    if shortest:
        path_rooms = set()
        x, y = 0, 0
        for move in shortest:
            dx, dy = {"U": (0,-1), "D": (0,1), "L": (-1,0), "R": (1,0)}[move]
            x, y = x + dx, y + dy
            path_rooms.add((x, y))
            yield {
                "type": "grid",
                "cells": render((x, y), visited_rooms, highlight_path=path_rooms),
                "colors": {**colors, VISITED: "#005533", CURRENT: "#ffff66"},
                "delay": 200,
            }

        yield {
            "type": "text",
            "lines": [
                f"  Shortest path: {shortest}",
                f"  Length: {len(shortest)}",
                "",
                f"  Longest path length: {longest_len}",
                f"  Total paths found: {paths_found}",
            ],
            "delay": 1000,
        }
