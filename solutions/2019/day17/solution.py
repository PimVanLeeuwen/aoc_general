"""
Day 17 - Set and Forget
Year: 2019

Map scaffolding from an Intcode ASCII camera, find intersections,
then compress a path for the vacuum robot to traverse all scaffolding.
"""

from intcode import IntcodeComputer

DIRS = [(0, -1), (1, 0), (0, 1), (-1, 0)]  # up, right, down, left
DIR_CHARS = {'^': 0, '>': 1, 'v': 2, '<': 3}


def get_map(program):
    """Run the ASCII program and return the scaffold grid as a list of strings."""
    cpu = IntcodeComputer(program)
    cpu.run()
    text = "".join(chr(c) for c in cpu.outputs)
    return [line for line in text.split("\n") if line]


def find_intersections(grid):
    """Find scaffold intersections and return their positions."""
    h = len(grid)
    w = len(grid[0]) if grid else 0
    intersections = []
    for y in range(1, h - 1):
        for x in range(1, w - 1):
            if grid[y][x] == '#' and all(
                grid[y + dy][x + dx] in '#^v<>' for dx, dy in DIRS
            ):
                intersections.append((x, y))
    return intersections


def trace_path(grid):
    """Walk the scaffold and return the path as a list of turn/move commands."""
    h = len(grid)
    w = len(grid[0])

    # Find robot position and direction
    rx, ry, rd = 0, 0, 0
    for y in range(h):
        for x in range(w):
            if grid[y][x] in DIR_CHARS:
                rx, ry, rd = x, y, DIR_CHARS[grid[y][x]]

    scaffold = set()
    for y in range(h):
        for x in range(w):
            if grid[y][x] in '#^v<>':
                scaffold.add((x, y))

    path = []
    while True:
        # Try turning left or right
        left_dir = (rd - 1) % 4
        right_dir = (rd + 1) % 4
        ldx, ldy = DIRS[left_dir]
        rdx, rdy = DIRS[right_dir]

        if (rx + ldx, ry + ldy) in scaffold:
            rd = left_dir
            turn = "L"
        elif (rx + rdx, ry + rdy) in scaffold:
            rd = right_dir
            turn = "R"
        else:
            break

        # Walk forward as far as possible
        dx, dy = DIRS[rd]
        steps = 0
        while (rx + dx, ry + dy) in scaffold:
            rx += dx
            ry += dy
            steps += 1

        path.append(turn)
        path.append(str(steps))

    return path


def compress_path(path):
    """Find main routine + 3 functions (A,B,C) that cover the full path.

    Each function is max 20 chars when comma-separated.
    """
    path_str = ",".join(path)

    def try_compress(a_len, b_len, c_len):
        """Try specific function lengths (in number of path elements, must be even)."""
        a = ",".join(path[:a_len])
        if len(a) > 20:
            return None

        rest = path_str
        main_parts = []

        # Greedily match A from the front, then find B
        while rest.startswith(a):
            main_parts.append("A")
            rest = rest[len(a):]
            if rest.startswith(","):
                rest = rest[1:]

        if not rest:
            return None  # need B and C too

        b = ",".join(rest.split(",")[:b_len])
        if len(b) > 20:
            return None

        # Now greedily match A and B, then find C from remainder
        rest = path_str
        main_parts = []
        while rest:
            if rest.startswith(a):
                main_parts.append("A")
                rest = rest[len(a):]
            elif rest.startswith(b):
                main_parts.append("B")
                rest = rest[len(b):]
            else:
                break
            if rest.startswith(","):
                rest = rest[1:]

        if not rest:
            return None

        c = ",".join(rest.split(",")[:c_len])
        if len(c) > 20:
            return None

        # Verify full coverage
        rest = path_str
        main_parts = []
        while rest:
            if rest.startswith(a):
                main_parts.append("A")
                rest = rest[len(a):]
            elif rest.startswith(b):
                main_parts.append("B")
                rest = rest[len(b):]
            elif rest.startswith(c):
                main_parts.append("C")
                rest = rest[len(c):]
            else:
                return None
            if rest.startswith(","):
                rest = rest[1:]

        main = ",".join(main_parts)
        if len(main) > 20:
            return None

        return main, a, b, c

    # Try all reasonable function lengths (must be even: turn,steps pairs)
    for a_len in range(2, 12, 2):
        for b_len in range(2, 12, 2):
            for c_len in range(2, 12, 2):
                result = try_compress(a_len, b_len, c_len)
                if result:
                    return result

    return None


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    program = [int(x) for x in puzzle_input.strip().split(",")]

    grid = get_map(program)
    intersections = find_intersections(grid)
    part1 = sum(x * y for x, y in intersections)

    # Part 2: traverse all scaffolding
    path = trace_path(grid)
    main, a, b, c = compress_path(path)

    cpu = IntcodeComputer(program)
    cpu.memory[0] = 2

    # Send movement program as ASCII
    input_lines = [main, a, b, c, "n"]  # "n" = no continuous video feed
    input_str = "\n".join(input_lines) + "\n"
    for ch in input_str:
        cpu.inputs.append(ord(ch))

    cpu.run()
    part2 = cpu.outputs[-1]

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    """Yield frames showing the scaffold map and path compression."""
    program = [int(x) for x in puzzle_input.strip().split(",")]

    grid = get_map(program)
    intersections = find_intersections(grid)

    # Show scaffold with intersections highlighted
    cells = []
    int_set = set(intersections)
    for y, row in enumerate(grid):
        r = []
        for x, ch in enumerate(row):
            if (x, y) in int_set:
                r.append("O")
            elif ch in '^v<>':
                r.append("R")
            elif ch == '#':
                r.append("#")
            else:
                r.append(".")
        cells.append(r)

    yield {
        "type": "grid",
        "cells": cells,
        "colors": {
            ".": "#0f0f23",
            "#": "#666688",
            "O": "#ffff00",
            "R": "#00ff41",
        },
        "delay": 800,
    }

    part1 = sum(x * y for x, y in intersections)

    yield {
        "type": "text",
        "lines": [
            "  Set and Forget — Scaffold Map",
            "",
            f"  Grid: {len(grid[0])}x{len(grid)} pixels",
            f"  Intersections: {len(intersections)}",
            f"  Alignment sum: {part1}",
        ],
        "delay": 600,
    }

    # Path compression
    path = trace_path(grid)
    result = compress_path(path)

    if result:
        main, a, b, c = result
        yield {
            "type": "text",
            "lines": [
                "  Path compression:",
                "",
                f"  Full path: {len(path)//2} moves",
                f"  Main: {main}",
                f"  A: {a}",
                f"  B: {b}",
                f"  C: {c}",
            ],
            "delay": 600,
        }

    # Run Part 2
    cpu = IntcodeComputer(program)
    cpu.memory[0] = 2
    input_lines = [main, a, b, c, "n"]
    for ch in "\n".join(input_lines) + "\n":
        cpu.inputs.append(ord(ch))
    cpu.run()
    part2 = cpu.outputs[-1]

    yield {
        "type": "text",
        "lines": [
            "  ===================================",
            "  Results",
            "  ===================================",
            "",
            f"  Part 1: {part1} (alignment parameter sum)",
            f"  Part 2: {part2} (dust collected)",
        ],
        "delay": 500,
    }
