"""
Day 05 - A Maze of Twisty Trampolines, All Alike
Year: 2017

The puzzle describes a list of integers representing jump offsets.
A pointer starts at position 0, and each step reads the offset at the current position,
jumps that many positions forward or backward, and then modifies
the offset according to the rules of the part.
"""


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    maze = [int(x) for x in puzzle_input.strip().split("\n")]
    maze2 = maze.copy()

    # Part 1
    part1 = 0
    i = 0

    while 0 <= i < len(maze):
        jump = maze[i]
        maze[i] += 1
        i += jump
        part1 += 1


    # Part 2
    part2 = 0
    i = 0

    while 0 <= i < len(maze2):
        jump = maze2[i]
        maze2[i] += 1 if maze2[i] < 3 else -1
        i += jump
        part2 += 1

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    """Yield visualization frames for the trampoline maze (Part 1)."""
    maze = [int(x) for x in puzzle_input.strip().split()]
    i = 0
    steps = 0

    # Helper: convert maze → grid of characters
    def make_canvas(pointer_index=None):
        cells = []
        for idx, val in enumerate(maze):
            if idx == pointer_index:
                # Highlight the current instruction
                cells.append(list(f"[{val}]"))
            else:
                cells.append(list(f" {val} "))
        return cells

    # Initial frame
    yield {
        "type": "grid",
        "cells": make_canvas(pointer_index=0),
        "colors": {
            "[": "#ff0040",  # pointer highlight
            "]": "#ff0040",
            " ": "#0f0f23",
            "-": "#00ff41",
            "0": "#00ff41",
            "1": "#00ff41",
            "2": "#00ff41",
            "3": "#00ff41",
            "4": "#00ff41",
            "5": "#00ff41",
            "6": "#00ff41",
            "7": "#00ff41",
            "8": "#00ff41",
            "9": "#00ff41"
        },
        "text": [
            "Starting Part 1 simulation",
            f"Pointer at index 0",
            f"Value: {maze[0]}",
            f"Steps: {steps}"
        ],
        "delay": 200,
    }

    # Run the simulation
    while 0 <= i < len(maze):
        jump = maze[i]
        maze[i] += 1
        next_i = i + jump
        steps += 1

        # Frame after applying the rule
        yield {
            "type": "grid",
            "cells": make_canvas(pointer_index=i),
            "colors": {
                "[": "#ff0040",
                "]": "#ff0040",
                " ": "#0f0f23",
                "-": "#00ff41",
                "0": "#00ff41",
                "1": "#00ff41",
                "2": "#00ff41",
                "3": "#00ff41",
                "4": "#00ff41",
                "5": "#00ff41",
                "6": "#00ff41",
                "7": "#00ff41",
                "8": "#00ff41",
                "9": "#00ff41"
            },
            "text": [
                "Part 1 rule: offset += 1",
                f"Pointer at index {i}",
                f"Jump value: {jump}",
                f"Next index: {next_i}",
                f"Steps: {steps}"
            ],
            "delay": 60,
        }

        i = next_i

    # Final frame
    yield {
        "type": "text",
        "lines": [
            "Exited the maze!",
            f"Total steps (Part 1): {steps}"
        ],
        "delay": 400,
    }

