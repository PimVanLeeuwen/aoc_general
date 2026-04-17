"""
Day 22 - Grid Computing
Year: 2016

Count viable node pairs, then find the minimum steps to move target data
from the top-right corner to node (0,0) via a sliding-puzzle analysis.
"""

import re
from collections import deque


def parse(puzzle_input):
    nodes = {}
    for line in puzzle_input.strip().splitlines():
        m = re.match(
            r"/dev/grid/node-x(\d+)-y(\d+)\s+(\d+)T\s+(\d+)T\s+(\d+)T", line
        )
        if not m:
            continue
        x, y, size, used, avail = map(int, m.groups())
        nodes[(x, y)] = (size, used, avail)
    return nodes


def viable_pairs(nodes):
    count = 0
    node_list = list(nodes.items())
    for i, (pos_a, (_, used_a, _)) in enumerate(node_list):
        if used_a == 0:
            continue
        for j, (pos_b, (_, _, avail_b)) in enumerate(node_list):
            if i != j and used_a <= avail_b:
                count += 1
    return count


def steps_to_move_goal(nodes):
    """
    The grid has three types of nodes:
      - Empty node (used=0): the "hole" we move around
      - Wall nodes (used > any avail): immovable, act as obstacles
      - Normal nodes: can exchange data freely

    Strategy:
      1. BFS the empty node to the position just left of the goal data at (max_x, 0)
      2. Then each left-step of the goal takes 5 moves (empty goes around it)
         except for the first step which is free once empty is adjacent
    """
    max_x = max(x for x, _ in nodes)

    # Determine movable nodes: not a wall (used <= max avail in the grid)
    max_avail = max(avail for _, _, avail in nodes.values())
    walls = {pos for pos, (_, used, _) in nodes.items() if used > max_avail}

    empty = next(pos for pos, (_, used, _) in nodes.items() if used == 0)
    goal = (max_x, 0)
    target_empty = (max_x - 1, 0)  # where empty needs to be to start moving goal

    # BFS: move empty to target_empty, avoiding walls
    dist = {empty: 0}
    queue = deque([empty])
    while queue:
        cx, cy = queue.popleft()
        if (cx, cy) == target_empty:
            break
        for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)):
            nb = (cx+dx, cy+dy)
            if nb in nodes and nb not in walls and nb not in dist:
                dist[nb] = dist[(cx, cy)] + 1
                queue.append(nb)

    steps_to_reach = dist[target_empty]

    # Each leftward move of goal: 1 step to move goal + 4 steps for empty to
    # loop around (down, left×2, up) = 5 per move, for (max_x - 1) moves,
    # plus the final 1-step move into (0,0)
    return steps_to_reach + 1 + (max_x - 1) * 5


def solve(puzzle_input: str) -> tuple[str, str]:
    nodes = parse(puzzle_input)
    part1 = viable_pairs(nodes)
    part2 = steps_to_move_goal(nodes)
    return str(part1), str(part2)


def visualize(puzzle_input: str):
    """Render the grid, marking wall/empty/goal/normal nodes."""
    nodes = parse(puzzle_input)
    max_x = max(x for x, _ in nodes)
    max_y = max(y for _, y in nodes)
    max_avail = max(avail for _, _, avail in nodes.values())

    walls = {pos for pos, (_, used, _) in nodes.items() if used > max_avail}
    empty = next(pos for pos, (_, used, _) in nodes.items() if used == 0)
    goal = (max_x, 0)

    # Build display grid
    # Symbols: # wall, _ empty, G goal, . normal, S start/target (0,0)
    def make_grid(highlight=None):
        cells = []
        for y in range(max_y + 1):
            row = []
            for x in range(max_x + 1):
                pos = (x, y)
                if highlight and pos in highlight:
                    row.append("*")
                elif pos in walls:
                    row.append("#")
                elif pos == empty:
                    row.append("_")
                elif pos == goal:
                    row.append("G")
                elif pos == (0, 0):
                    row.append("S")
                else:
                    row.append(".")
            cells.append(row)
        return cells

    colors = {
        "#": "#1a1a3e",   # wall — very dark
        "_": "#00aaff",   # empty — blue
        "G": "#ff5555",   # goal — red
        "S": "#00cc44",   # start — green
        ".": "#2a4a2a",   # normal — dark green
        "*": "#ffff66",   # BFS path — gold
    }

    # Initial grid
    yield {
        "type": "grid",
        "cells": make_grid(),
        "colors": colors,
        "delay": 600,
    }

    # BFS path of empty toward goal
    target_empty = (max_x - 1, 0)
    dist = {empty: 0}
    prev = {empty: None}
    queue = deque([empty])
    while queue:
        cx, cy = queue.popleft()
        if (cx, cy) == target_empty:
            break
        for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)):
            nb = (cx+dx, cy+dy)
            if nb in nodes and nb not in walls and nb not in dist:
                dist[nb] = dist[(cx, cy)] + 1
                prev[nb] = (cx, cy)
                queue.append(nb)

    # Reconstruct and animate path
    path = []
    cur = target_empty
    while cur is not None:
        path.append(cur)
        cur = prev.get(cur)
    path.reverse()

    for step, pos in enumerate(path):
        yield {
            "type": "grid",
            "cells": make_grid(highlight=set(path[:step+1])),
            "colors": colors,
            "delay": 60,
        }

    # Final summary
    steps = dist[target_empty] + 1 + (max_x - 1) * 5
    yield {
        "type": "text",
        "lines": [
            f"  Grid: {max_x+1} × {max_y+1} nodes",
            f"  Walls:  {len(walls)}",
            f"  Empty at: {empty}",
            f"  Goal at:  {goal}",
            "",
            f"  Steps to move empty beside goal: {dist[target_empty]}",
            f"  Steps to slide goal to (0,0):    1 + {max_x-1} × 5 = {1+(max_x-1)*5}",
            f"  Total: {steps}",
        ],
        "delay": 1000,
    }
