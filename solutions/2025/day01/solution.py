"""
Day 1 - Dial-a-Code
Year: 2025

Simulate a circular dial (0-99) that turns left or right.
Count how many times it passes through zero.
"""


def solve(puzzle_input: str) -> tuple[str, str]:
    lines = puzzle_input.strip().split("\n")

    # Part 1: just track final crossings through 0 via modular arithmetic
    dial = 50
    part1 = 0
    for line in lines:
        direction, distance = line[0], int(line[1:])
        if direction == "L":
            dial = (dial - distance) % 100
        else:
            dial = (dial + distance) % 100
        if dial == 0:
            part1 += 1

    # Part 2: simulate step by step, count every zero crossing
    dial = 50
    part2 = 0
    for line in lines:
        direction, distance = line[0], int(line[1:])
        for _ in range(distance):
            if direction == "L":
                dial -= 1
                if dial < 0:
                    dial = 99
                if dial == 0:
                    part2 += 1
            else:
                dial += 1
                if dial == 100:
                    dial = 0
                    part2 += 1

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    lines = puzzle_input.strip().split("\n")

    yield {
        "type": "text",
        "lines": [
            "  Dial-a-Code",
            "",
            f"  Instructions: {len(lines)}",
            f"  Sample: {lines[0]}, {lines[1]}, {lines[2]}...",
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
            f"  Part 1: {part1} (final zero hits)",
            f"  Part 2: {part2} (all zero crossings)",
        ],
        "delay": 500,
    }
