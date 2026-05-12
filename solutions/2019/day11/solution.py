"""
Day 11 - Space Police
Year: 2019

Run a hull-painting robot driven by an Intcode brain. It reads panel
colors, outputs paint + turn instructions, and moves forward.
"""

from intcode import IntcodeComputer

# Directions: up, right, down, left
DX = [0, 1, 0, -1]
DY = [-1, 0, 1, 0]


def run_robot(program, start_color=0):
    """Run the painting robot. Returns the painted panels dict {(x,y): color}."""
    cpu = IntcodeComputer(program)
    panels = {}
    x, y = 0, 0
    direction = 0  # 0=up, 1=right, 2=down, 3=left

    if start_color:
        panels[(0, 0)] = start_color

    while not cpu.halted:
        # Provide current panel color as input
        cpu.add_input(panels.get((x, y), 0))
        cpu.run_until_block()

        if cpu.halted:
            break

        # Read two outputs: paint color, then turn direction
        if len(cpu.outputs) >= 2:
            color = cpu.outputs[-2]
            turn = cpu.outputs[-1]

            panels[(x, y)] = color

            if turn == 0:
                direction = (direction - 1) % 4
            else:
                direction = (direction + 1) % 4

            x += DX[direction]
            y += DY[direction]

    return panels


def render_panels(panels):
    """Render painted panels to a list of strings."""
    white = {pos for pos, color in panels.items() if color == 1}
    if not white:
        return ["(empty)"]

    min_x = min(x for x, y in white)
    max_x = max(x for x, y in white)
    min_y = min(y for x, y in white)
    max_y = max(y for x, y in white)

    lines = []
    for y in range(min_y, max_y + 1):
        line = ""
        for x in range(min_x, max_x + 1):
            line += "#" if (x, y) in white else " "
        lines.append(line)
    return lines


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    program = [int(x) for x in puzzle_input.strip().split(",")]

    panels1 = run_robot(program, start_color=0)
    part1 = len(panels1)

    panels2 = run_robot(program, start_color=1)
    part2 = "\n".join(render_panels(panels2))

    return str(part1), part2


def visualize(puzzle_input: str):
    """Yield frames showing the robot painting the hull."""
    program = [int(x) for x in puzzle_input.strip().split(",")]

    # Run Part 2 (the interesting one — paints a message)
    cpu = IntcodeComputer(program)
    panels = {(0, 0): 1}
    x, y = 0, 0
    direction = 0
    steps = 0

    # Collect snapshots
    snapshots = []
    while not cpu.halted:
        cpu.add_input(panels.get((x, y), 0))
        cpu.run_until_block()

        if cpu.halted:
            break

        if len(cpu.outputs) >= 2:
            color = cpu.outputs[-2]
            turn = cpu.outputs[-1]

            panels[(x, y)] = color

            if turn == 0:
                direction = (direction - 1) % 4
            else:
                direction = (direction + 1) % 4

            x += DX[direction]
            y += DY[direction]
            steps += 1

    yield {
        "type": "text",
        "lines": [
            "  Space Police — Hull Painting Robot",
            "",
            f"  Total steps: {steps}",
            f"  Panels painted: {len(panels)}",
        ],
        "delay": 600,
    }

    # Render Part 1
    panels1 = run_robot(program, start_color=0)
    yield {
        "type": "text",
        "lines": [
            f"  Part 1: {len(panels1)} panels painted (starting on black)",
        ],
        "delay": 400,
    }

    # Render Part 2 as grid
    white = {pos for pos, c in panels.items() if c == 1}
    if white:
        min_x = min(x for x, y in white)
        max_x = max(x for x, y in white)
        min_y = min(y for x, y in white)
        max_y = max(y for x, y in white)

        cells = []
        for row in range(min_y, max_y + 1):
            r = []
            for col in range(min_x, max_x + 1):
                r.append("#" if (col, row) in white else ".")
            cells.append(r)

        yield {
            "type": "grid",
            "cells": cells,
            "colors": {
                ".": "#0f0f23",
                "#": "#00ff41",
            },
            "delay": 800,
        }

    yield {
        "type": "text",
        "lines": [
            "  Part 2: Registration identifier",
            "",
        ] + ["  " + line for line in render_panels(panels)],
        "delay": 500,
    }
