"""
Day 22 - Mode Maze
Year: 2018

Compute cave terrain from erosion levels, then Dijkstra with equipment swaps.
"""

import heapq


def build_erosion(depth, tx, ty, margin=0):
    """Build erosion level grid. Extends margin beyond target for part 2."""
    w, h = tx + margin + 1, ty + margin + 1
    erosion = [[0] * w for _ in range(h)]
    for y in range(h):
        for x in range(w):
            if (x == 0 and y == 0) or (x == tx and y == ty):
                geo = 0
            elif y == 0:
                geo = x * 16807
            elif x == 0:
                geo = y * 48271
            else:
                geo = erosion[y][x - 1] * erosion[y - 1][x]
            erosion[y][x] = (geo + depth) % 20183
    return erosion


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    lines = puzzle_input.strip().splitlines()
    depth = int(lines[0].split()[1])
    tx, ty = map(int, lines[1].split()[1].split(','))

    # Part 1: risk level
    erosion = build_erosion(depth, tx, ty, margin=50)
    part1 = sum(erosion[y][x] % 3 for y in range(ty + 1) for x in range(tx + 1))

    # Part 2: Dijkstra on (x, y, equipment)
    # Equipment: 0=neither, 1=torch, 2=climbing gear
    # Rocky(0): torch(1) or climbing(2)
    # Wet(1): neither(0) or climbing(2)
    # Narrow(2): neither(0) or torch(1)
    # Valid equipment for terrain type t: the two where equipment != t
    h = len(erosion)
    w = len(erosion[0])

    dist = {}
    pq = [(0, 0, 0, 1)]  # (time, x, y, equip=torch)

    while pq:
        time, x, y, equip = heapq.heappop(pq)
        if (x, y, equip) in dist:
            continue
        dist[(x, y, equip)] = time

        if x == tx and y == ty and equip == 1:
            part2 = time
            break

        terrain = erosion[y][x] % 3

        # Switch equipment (7 min) — the other valid one
        other = 3 - terrain - equip  # the third valid equipment for this terrain
        if (x, y, other) not in dist:
            heapq.heappush(pq, (time + 7, x, y, other))

        # Move to neighbors (1 min)
        for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < w and 0 <= ny < h:
                nt = erosion[ny][nx] % 3
                if equip != nt and (nx, ny, equip) not in dist:
                    heapq.heappush(pq, (time + 1, nx, ny, equip))

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    """Visualize the cave terrain."""
    lines = puzzle_input.strip().splitlines()
    depth = int(lines[0].split()[1])
    tx, ty = map(int, lines[1].split()[1].split(','))

    erosion = build_erosion(depth, tx, ty, margin=5)
    symbols = {0: '.', 1: '=', 2: '|'}

    grid = []
    for y in range(min(ty + 6, len(erosion))):
        row = []
        for x in range(min(tx + 6, len(erosion[0]))):
            if x == 0 and y == 0:
                row.append('M')
            elif x == tx and y == ty:
                row.append('T')
            else:
                row.append(symbols[erosion[y][x] % 3])
        grid.append(row)

    yield {
        "type": "grid",
        "cells": grid,
        "colors": {
            ".": "#888888",
            "=": "#4444ff",
            "|": "#884400",
            "M": "#ff0000",
            "T": "#00ff41",
        },
        "delay": 3000,
    }

    # Run Dijkstra and show path
    h = len(erosion)
    w = len(erosion[0])
    dist = {}
    prev = {}
    pq = [(0, 0, 0, 1)]

    while pq:
        time, x, y, equip = heapq.heappop(pq)
        if (x, y, equip) in dist:
            continue
        dist[(x, y, equip)] = time

        if x == tx and y == ty and equip == 1:
            break

        terrain = erosion[y][x] % 3
        other = 3 - terrain - equip
        if (x, y, other) not in dist:
            heapq.heappush(pq, (time + 7, x, y, other))
            if (x, y, other) not in prev:
                prev[(x, y, other)] = (x, y, equip)

        for ddx, ddy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            nx, ny = x + ddx, y + ddy
            if 0 <= nx < w and 0 <= ny < h:
                nt = erosion[ny][nx] % 3
                if equip != nt and (nx, ny, equip) not in dist:
                    heapq.heappush(pq, (time + 1, nx, ny, equip))
                    if (nx, ny, equip) not in prev:
                        prev[(nx, ny, equip)] = (x, y, equip)

    # Trace path
    path = set()
    state = (tx, ty, 1)
    while state in prev:
        path.add((state[0], state[1]))
        state = prev[state]
    path.add((0, 0))

    path_grid = []
    for y in range(min(ty + 6, len(erosion))):
        row = []
        for x in range(min(tx + 6, len(erosion[0]))):
            if x == 0 and y == 0:
                row.append('M')
            elif x == tx and y == ty:
                row.append('T')
            elif (x, y) in path:
                row.append('*')
            else:
                row.append(symbols[erosion[y][x] % 3])
        path_grid.append(row)

    yield {
        "type": "grid",
        "cells": path_grid,
        "colors": {
            ".": "#888888",
            "=": "#4444ff",
            "|": "#884400",
            "M": "#ff0000",
            "T": "#00ff41",
            "*": "#ffff00",
        },
        "delay": 3000,
    }

    yield {
        "type": "text",
        "lines": [
            f"Cave: depth={depth}, target=({tx},{ty})",
            f"Part 1 (risk level): {sum(erosion[y][x] % 3 for y in range(ty+1) for x in range(tx+1))}",
            f"Part 2 (fastest path): {dist.get((tx, ty, 1), '?')} minutes",
        ],
        "delay": 4000,
    }