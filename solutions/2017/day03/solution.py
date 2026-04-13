"""
Day 03 - Spiral Memory
Year: 2017

Part 1: Compute the Manhattan distance from a number's position in a spiral grid
to the center (square 1).

Part 2: Build a spiral where each cell contains the sum of adjacent cells.
Return the first value larger than the puzzle input.
"""


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    n = int(puzzle_input.strip())

    if n == 1:
        part1 = "0"
    else:
        layer = 0
        while (2 * layer + 1) ** 2 < n:
            layer += 1

        max_val = (2 * layer + 1) ** 2
        side = 2 * layer

        midpoints = [max_val - layer - side * i for i in range(4)]
        offset = min(abs(n - m) for m in midpoints)

        part1 = str(layer + offset)

        # Spiral directions: right, up, left, down
        dirs = [(1, 0), (0, 1), (-1, 0), (0, -1)]

        # Neighbor offsets (8 directions)
        neighbors = [
            (-1, -1), (0, -1), (1, -1),
            (-1, 0), (1, 0),
            (-1, 1), (0, 1), (1, 1)
        ]

        grid = {(0, 0): 1}
        x = y = 0
        step_size = 1
        dir_index = 0

        def sum_neighbors(inner_x, inner_y):
            return sum(grid.get((inner_x + inner_dx, inner_y + inner_dy), 0) for inner_dx, inner_dy in neighbors)

        value = 1
        while value <= n:
            for _ in range(2):  # two legs per step size
                dx, dy = dirs[dir_index]
                for _ in range(step_size):
                    x += dx
                    y += dy
                    value = sum_neighbors(x, y)
                    grid[(x, y)] = value
                    if value > n:
                        part2 = str(value)
                        return part1, part2
                dir_index = (dir_index + 1) % 4
            step_size += 1

        # Should never reach here
        part2 = ""

    return part1, part2


def visualize(puzzle_input: str):
    """Yield visualization frames showing the Part 2 spiral being built."""
    target = int(puzzle_input.strip())

    # Spiral directions: right, up, left, down
    dirs = [(1, 0), (0, 1), (-1, 0), (0, -1)]

    # Neighbor offsets (8 directions)
    neighbors = [
        (-1, -1), (0, -1), (1, -1),
        (-1,  0),          (1,  0),
        (-1,  1), (0,  1), (1,  1)
    ]

    grid = {(0, 0): 1}
    x = y = 0
    step_size = 1
    dir_index = 0
    value = 1

    def sum_neighbors(cx, cy):
        return sum(grid.get((cx + dx, cy + dy), 0) for dx, dy in neighbors)

    # Convert sparse dict → dense 2D grid
    def make_canvas():
        xs = [p[0] for p in grid]
        ys = [p[1] for p in grid]
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)

        width = max_x - min_x + 1
        height = max_y - min_y + 1

        canvas = [["." for _ in range(width)] for _ in range(height)]

        for (gx, gy), val in grid.items():
            cx = gx - min_x
            cy = max_y - gy
            canvas[cy][cx] = "*" if val > target else "#"

        return canvas

    # Initial frame
    yield {
        "type": "grid",
        "cells": [["#"]],
        "colors": {"#": "#00ff41"},
        "text": ["Starting spiral...", "Center = 1"],
        "delay": 300,
    }

    # Build the spiral
    while value <= target:
        for _ in range(2):  # two legs per step size
            dx, dy = dirs[dir_index]
            for _ in range(step_size):
                x += dx
                y += dy
                value = sum_neighbors(x, y)
                grid[(x, y)] = value

                # Unified frame: grid + text
                yield {
                    "type": "grid",
                    "cells": make_canvas(),
                    "colors": {
                        "#": "#00ff41",   # normal filled cell
                        "*": "#ff0040",   # the first value > target
                        ".": "#0f0f23"    # empty
                    },
                    "text": [
                        f"Position: ({x}, {y})",
                        f"Value written: {value}",
                        f"Target: {target}"
                    ],
                    "delay": 40,
                }

                if value > target:
                    return

            dir_index = (dir_index + 1) % 4
        step_size += 1


