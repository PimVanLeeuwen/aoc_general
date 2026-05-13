"""
Day 24 - Blizzard Basin
Year: 2022

Navigate through a valley with moving blizzards using BFS,
making three trips (there, back, there again).
"""

from collections import deque
from math import gcd


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    lines = puzzle_input.strip().split("\n")
    height = len(lines)
    width = len(lines[0])
    inner_h = height - 2
    inner_w = width - 2

    blizzards = []
    walls = set()
    for y, line in enumerate(lines):
        for x, ch in enumerate(line):
            if ch == "#":
                walls.add((x, y))
            elif ch in "^v<>":
                blizzards.append((x, y, ch))

    start = (lines[0].index("."), 0)
    goal = (lines[-1].index("."), height - 1)

    period = inner_w * inner_h // gcd(inner_w, inner_h)

    # Precompute blizzard positions for each time step
    blizzard_maps = [set() for _ in range(period)]
    for minute in range(period):
        for bx, by, d in blizzards:
            if d == ">":
                nx = 1 + (bx - 1 + minute) % inner_w
                blizzard_maps[minute].add((nx, by))
            elif d == "<":
                nx = 1 + (bx - 1 - minute) % inner_w
                blizzard_maps[minute].add((nx, by))
            elif d == "v":
                ny = 1 + (by - 1 + minute) % inner_h
                blizzard_maps[minute].add((bx, ny))
            elif d == "^":
                ny = 1 + (by - 1 - minute) % inner_h
                blizzard_maps[minute].add((bx, ny))

    def bfs(start_pos, goal_pos, start_time):
        queue = deque([(start_pos[0], start_pos[1], start_time)])
        visited = {(start_pos[0], start_pos[1], start_time % period)}

        while queue:
            x, y, t = queue.popleft()
            nt = t + 1
            bliz = blizzard_maps[nt % period]

            for dx, dy in [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)]:
                nx, ny = x + dx, y + dy

                if (nx, ny) == goal_pos:
                    return nt

                if nx < 0 or ny < 0 or nx >= width or ny >= height:
                    continue
                if (nx, ny) in walls or (nx, ny) in bliz:
                    continue
                if (nx, ny) != start_pos and (ny == 0 or ny == height - 1):
                    continue

                state = (nx, ny, nt % period)
                if state not in visited:
                    visited.add(state)
                    queue.append((nx, ny, nt))

        return -1

    t1 = bfs(start, goal, 0)
    t2 = bfs(goal, start, t1)
    t3 = bfs(start, goal, t2)

    return str(t1), str(t3)


def visualize(puzzle_input: str):
    """Yield frames showing blizzard basin."""
    lines = puzzle_input.strip().split("\n")

    yield {
        "type": "text",
        "lines": [
            "  Blizzard Basin",
            "",
            f"  Valley: {len(lines[0])}×{len(lines)}",
        ],
        "delay": 600,
    }

    part1, part2 = solve(puzzle_input)

    yield {
        "type": "text",
        "lines": [
            "  ===================================",
            "  Results",
            "  ===================================",
            "",
            f"  Part 1: {part1} (there)",
            f"  Part 2: {part2} (there, back, there)",
        ],
        "delay": 500,
    }
