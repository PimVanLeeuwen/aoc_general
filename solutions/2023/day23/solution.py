"""
Day 23 - A Long Walk
Year: 2023

Find the longest path through a hiking trail maze,
with and without slope constraints.
"""

from collections import deque


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    grid = puzzle_input.strip().split("\n")
    rows, cols = len(grid), len(grid[0])

    start = (0, grid[0].index("."))
    end = (rows - 1, grid[rows - 1].index("."))

    slope_dirs = {">": (0, 1), "<": (0, -1), "v": (1, 0), "^": (-1, 0)}

    def neighbors(r, c, respect_slopes):
        """Yield valid neighbor positions from (r, c)."""
        ch = grid[r][c]
        if respect_slopes and ch in slope_dirs:
            dr, dc = slope_dirs[ch]
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != "#":
                yield nr, nc
            return

        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != "#":
                yield nr, nc

    def longest_path(respect_slopes):
        """Find longest path from start to end using condensed graph + DFS."""
        # Find junction nodes (nodes with 3+ non-wall neighbors)
        junctions = {start, end}
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == "#":
                    continue
                count = sum(1 for _ in neighbors(r, c, False))
                if count >= 3:
                    junctions.add((r, c))

        # Build condensed graph using BFS from each junction
        adj = {j: [] for j in junctions}

        for jr, jc in junctions:
            # BFS but stop at other junctions
            queue = deque()
            visited = {(jr, jc)}
            for nr, nc in neighbors(jr, jc, respect_slopes):
                queue.append((nr, nc, 1))
                visited.add((nr, nc))

            while queue:
                r, c, dist = queue.popleft()
                if (r, c) in junctions:
                    adj[(jr, jc)].append(((r, c), dist))
                    continue
                for nr, nc in neighbors(r, c, respect_slopes):
                    if (nr, nc) not in visited:
                        visited.add((nr, nc))
                        queue.append((nr, nc, dist + 1))

        # DFS for longest path in condensed graph
        best = 0
        junction_list = list(junctions)
        junction_idx = {j: i for i, j in enumerate(junction_list)}
        adj_indexed = [[] for _ in range(len(junction_list))]
        for j in junctions:
            for neighbor, dist in adj[j]:
                adj_indexed[junction_idx[j]].append((junction_idx[neighbor], dist))

        start_idx = junction_idx[start]
        end_idx = junction_idx[end]

        def dfs(node, dist, visited_bits):
            nonlocal best
            if node == end_idx:
                best = max(best, dist)
                return
            for neighbor, edge_dist in adj_indexed[node]:
                bit = 1 << neighbor
                if not (visited_bits & bit):
                    dfs(neighbor, dist + edge_dist, visited_bits | bit)

        dfs(start_idx, 0, 1 << start_idx)
        return best

    part1 = longest_path(respect_slopes=True)
    part2 = longest_path(respect_slopes=False)

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    """Yield frames showing the hiking trail."""
    grid = puzzle_input.strip().split("\n")

    colors = {"#": "#666666", ".": "#0f0f23", ">": "#00ff41", "<": "#00ff41", "v": "#00ff41", "^": "#00ff41"}
    yield {
        "type": "grid",
        "cells": [list(row) for row in grid],
        "colors": colors,
        "delay": 400,
    }

    part1, part2 = solve(puzzle_input)

    yield {
        "type": "text",
        "lines": [
            "  ===================================",
            "  Results",
            "  ===================================",
            "",
            f"  Part 1: {part1} (with slopes)",
            f"  Part 2: {part2} (ignoring slopes)",
        ],
        "delay": 500,
    }
