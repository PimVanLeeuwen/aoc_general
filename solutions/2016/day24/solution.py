"""
Day 24 - Air Duct Spelunking
Year: 2016

BFS pairwise distances between numbered locations, then bitmask DP (TSP)
to find the shortest route visiting every location starting from 0.
"""

from collections import deque
from itertools import permutations


def parse(puzzle_input):
    grid = puzzle_input.strip().splitlines()
    locations = {}
    for r, row in enumerate(grid):
        for c, ch in enumerate(row):
            if ch.isdigit():
                locations[int(ch)] = (r, c)
    return grid, locations


def bfs_dist(grid, start):
    """BFS from start; returns dict of (row,col) -> steps."""
    dist = {start: 0}
    queue = deque([start])
    while queue:
        r, c = queue.popleft()
        for dr, dc in ((-1,0),(1,0),(0,-1),(0,1)):
            nb = (r+dr, c+dc)
            if nb not in dist and grid[nb[0]][nb[1]] != '#':
                dist[nb] = dist[(r,c)] + 1
                queue.append(nb)
    return dist


def pairwise(grid, locations):
    """BFS distances between every pair of numbered locations."""
    ids = sorted(locations)
    dist = {}
    for i in ids:
        d = bfs_dist(grid, locations[i])
        for j in ids:
            if i != j:
                dist[(i, j)] = d[locations[j]]
    return dist


def tsp(dist, locations, return_to_start=False):
    """Bitmask DP: shortest path starting at 0 visiting all locations."""
    ids = sorted(locations)
    n = len(ids)
    idx = {v: i for i, v in enumerate(ids)}
    full = (1 << n) - 1

    # dp[mask][node] = min steps to have visited exactly the nodes in mask,
    # ending at node
    INF = float("inf")
    dp = [[INF] * n for _ in range(1 << n)]
    dp[1 << idx[0]][idx[0]] = 0

    for mask in range(1 << n):
        for last in range(n):
            if dp[mask][last] == INF:
                continue
            if not (mask >> last & 1):
                continue
            for nxt in range(n):
                if mask >> nxt & 1:
                    continue
                li, ni = ids[last], ids[nxt]
                new_mask = mask | (1 << nxt)
                cost = dp[mask][last] + dist[(li, ni)]
                if cost < dp[new_mask][nxt]:
                    dp[new_mask][nxt] = cost

    if return_to_start:
        return min(
            dp[full][i] + dist[(ids[i], 0)]
            for i in range(n) if dp[full][i] < INF
        )
    return min(dp[full][i] for i in range(n))


def solve(puzzle_input: str) -> tuple[str, str]:
    grid, locations = parse(puzzle_input)
    d = pairwise(grid, locations)
    part1 = tsp(d, locations, return_to_start=False)
    part2 = tsp(d, locations, return_to_start=True)
    return str(part1), str(part2)


def visualize(puzzle_input: str):
    """Show the grid, animate BFS from each location, then highlight the optimal route."""
    grid, locations = parse(puzzle_input)
    rows, cols = len(grid), len(grid[0])

    def base_cells(highlight=None):
        highlight = highlight or {}
        cells = []
        for r, row in enumerate(grid):
            cells.append([])
            for c, ch in enumerate(row):
                if (r, c) in highlight:
                    cells[-1].append("*")
                else:
                    cells[-1].append(ch)
        return cells

    colors = {
        "#": "#1a1a3e",
        ".": "#0f0f23",
        "*": "#ffff66",
        "0": "#00aaff",
        "1": "#ff5555",
        "2": "#00cc44",
        "3": "#ff9900",
        "4": "#cc44cc",
        "5": "#44cccc",
        "6": "#cccc44",
        "7": "#cc4444",
    }

    # Initial grid
    yield {"type": "grid", "cells": base_cells(), "colors": colors, "delay": 500}

    # BFS from location 0 — show wavefront expanding
    start = locations[0]
    visited = {start: 0}
    queue = deque([start])
    frame_interval = max(1, (rows * cols) // 60)
    step = 0
    while queue:
        r, c = queue.popleft()
        for dr, dc in ((-1,0),(1,0),(0,-1),(0,1)):
            nb = (r+dr, c+dc)
            if nb not in visited and grid[nb[0]][nb[1]] != '#':
                visited[nb] = visited[(r,c)] + 1
                queue.append(nb)
        step += 1
        if step % frame_interval == 0:
            yield {
                "type": "grid",
                "cells": base_cells(highlight=set(visited)),
                "colors": colors,
                "delay": 60,
            }

    # Compute optimal route
    d = pairwise(grid, locations)
    ids = sorted(locations)
    n = len(ids)
    idx = {v: i for i, v in enumerate(ids)}
    full = (1 << n) - 1
    INF = float("inf")
    dp = [[INF]*n for _ in range(1 << n)]
    parent = [[None]*n for _ in range(1 << n)]
    dp[1 << idx[0]][idx[0]] = 0

    for mask in range(1 << n):
        for last in range(n):
            if dp[mask][last] == INF or not (mask >> last & 1):
                continue
            for nxt in range(n):
                if mask >> nxt & 1:
                    continue
                li, ni = ids[last], ids[nxt]
                cost = dp[mask][last] + d[(li, ni)]
                new_mask = mask | (1 << nxt)
                if cost < dp[new_mask][nxt]:
                    dp[new_mask][nxt] = cost
                    parent[new_mask][nxt] = (mask, last)

    # Reconstruct order
    best_last = min(range(n), key=lambda i: dp[full][i])
    order = []
    mask, last = full, best_last
    while parent[mask][last] is not None:
        order.append(ids[last])
        prev_mask, prev_last = parent[mask][last]
        mask, last = prev_mask, prev_last
    order.append(0)
    order.reverse()

    # Animate the route segment by segment
    route_visited: set = set()
    for i in range(len(order) - 1):
        a, b = order[i], order[i+1]
        # BFS path from a to b
        seg_dist = {locations[a]: 0}
        seg_prev = {locations[a]: None}
        q2 = deque([locations[a]])
        while q2:
            pos = q2.popleft()
            if pos == locations[b]:
                break
            for dr, dc in ((-1,0),(1,0),(0,-1),(0,1)):
                nb = (pos[0]+dr, pos[1]+dc)
                if nb not in seg_dist and grid[nb[0]][nb[1]] != '#':
                    seg_dist[nb] = seg_dist[pos] + 1
                    seg_prev[nb] = pos
                    q2.append(nb)
        # Trace back path
        path = []
        cur = locations[b]
        while cur is not None:
            path.append(cur)
            cur = seg_prev.get(cur)
        path.reverse()
        for pos in path:
            route_visited.add(pos)
            yield {
                "type": "grid",
                "cells": base_cells(highlight=route_visited),
                "colors": colors,
                "delay": 40,
            }

    yield {
        "type": "text",
        "lines": [
            f"  Optimal visit order: {' → '.join(str(x) for x in order)}",
            f"  Total steps (part 1): {tsp(d, locations, False)}",
            f"  Return to 0 (part 2): {tsp(d, locations, True)}",
        ],
        "delay": 1000,
    }
