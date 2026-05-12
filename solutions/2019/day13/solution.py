"""
Day 13 - Care Package
Year: 2019

Play a breakout-style arcade game powered by Intcode. Count blocks,
then beat the game by tracking the ball with the paddle.
"""

from intcode import IntcodeComputer

TILES = {0: " ", 1: "#", 2: "B", 3: "=", 4: "o"}


def parse_screen(outputs):
    """Parse triplets of outputs into a screen dict and score."""
    screen = {}
    score = 0
    for i in range(0, len(outputs), 3):
        x, y, tile = outputs[i], outputs[i + 1], outputs[i + 2]
        if x == -1 and y == 0:
            score = tile
        else:
            screen[(x, y)] = tile
    return screen, score


def play_game(program):
    """Play the game automatically by following the ball with the paddle."""
    cpu = IntcodeComputer(program)
    cpu.memory[0] = 2  # insert quarters

    screen = {}
    score = 0
    ball_x = 0
    paddle_x = 0

    while not cpu.halted:
        cpu.run_until_block()

        # Process outputs in triplets
        while len(cpu.outputs) >= 3:
            x = cpu.outputs.pop(0)
            y = cpu.outputs.pop(0)
            tile = cpu.outputs.pop(0)
            if x == -1 and y == 0:
                score = tile
            else:
                screen[(x, y)] = tile
                if tile == 4:
                    ball_x = x
                elif tile == 3:
                    paddle_x = x

        if cpu.waiting_for_input:
            # Move paddle toward ball
            if paddle_x < ball_x:
                joystick = 1
            elif paddle_x > ball_x:
                joystick = -1
            else:
                joystick = 0
            cpu.add_input(joystick)

    return screen, score


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    program = [int(x) for x in puzzle_input.strip().split(",")]

    # Part 1: count block tiles
    cpu = IntcodeComputer(program)
    cpu.run()
    screen, _ = parse_screen(cpu.outputs)
    part1 = sum(1 for t in screen.values() if t == 2)

    # Part 2: play and get final score
    _, part2 = play_game(program)

    return str(part1), str(part2)


def render_screen(screen):
    """Convert screen dict to grid cells."""
    if not screen:
        return []
    max_x = max(x for x, y in screen)
    max_y = max(y for x, y in screen)
    cells = []
    for y in range(max_y + 1):
        row = []
        for x in range(max_x + 1):
            row.append(TILES.get(screen.get((x, y), 0), " "))
        cells.append(row)
    return cells


def visualize(puzzle_input: str):
    """Yield frames showing the breakout game being played."""
    program = [int(x) for x in puzzle_input.strip().split(",")]

    # Part 1: initial screen
    cpu = IntcodeComputer(program)
    cpu.run()
    screen, _ = parse_screen(cpu.outputs)
    blocks = sum(1 for t in screen.values() if t == 2)

    yield {
        "type": "grid",
        "cells": render_screen(screen),
        "colors": {
            " ": "#0f0f23",
            "#": "#444466",
            "B": "#00ff41",
            "=": "#ffffff",
            "o": "#ff4444",
        },
        "delay": 600,
    }

    yield {
        "type": "text",
        "lines": [
            f"  Part 1: {blocks} block tiles",
            "",
            "  Now playing the game...",
        ],
        "delay": 400,
    }

    # Part 2: play with visualization
    cpu = IntcodeComputer(program)
    cpu.memory[0] = 2

    screen = {}
    score = 0
    ball_x = 0
    paddle_x = 0
    frame_count = 0

    while not cpu.halted:
        cpu.run_until_block()

        while len(cpu.outputs) >= 3:
            x = cpu.outputs.pop(0)
            y = cpu.outputs.pop(0)
            tile = cpu.outputs.pop(0)
            if x == -1 and y == 0:
                score = tile
            else:
                screen[(x, y)] = tile
                if tile == 4:
                    ball_x = x
                elif tile == 3:
                    paddle_x = x

        remaining = sum(1 for t in screen.values() if t == 2)
        frame_count += 1

        if frame_count % 50 == 0 or remaining == 0:
            cells = render_screen(screen)
            # Add score line
            score_line = list(f"  Score: {score:<8}  Blocks: {remaining:<4}")
            yield {
                "type": "grid",
                "cells": cells,
                "colors": {
                    " ": "#0f0f23",
                    "#": "#444466",
                    "B": "#00ff41",
                    "=": "#ffffff",
                    "o": "#ff4444",
                },
                "delay": 40,
            }

        if cpu.waiting_for_input:
            if paddle_x < ball_x:
                joystick = 1
            elif paddle_x > ball_x:
                joystick = -1
            else:
                joystick = 0
            cpu.add_input(joystick)

    yield {
        "type": "text",
        "lines": [
            "  ===================================",
            "  Game Over!",
            "  ===================================",
            "",
            f"  Part 1: {blocks} blocks",
            f"  Part 2: {score} (final score)",
        ],
        "delay": 500,
    }
