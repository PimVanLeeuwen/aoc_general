"""
Day 2 - Password Philosophy
Year: 2020

Validate passwords against two different policy interpretations.
"""

import re


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    part1 = part2 = 0

    for line in puzzle_input.strip().split("\n"):
        lo, hi, char, password = re.match(r"(\d+)-(\d+) (.): (.+)", line).groups()
        lo, hi = int(lo), int(hi)

        # Part 1: character count must be in range
        if lo <= password.count(char) <= hi:
            part1 += 1

        # Part 2: exactly one of the two positions must match
        if (password[lo - 1] == char) ^ (password[hi - 1] == char):
            part2 += 1

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    """Yield frames showing password validation."""
    lines = puzzle_input.strip().split("\n")

    yield {
        "type": "text",
        "lines": [
            "  Password Philosophy",
            "",
            f"  Passwords to check: {len(lines)}",
            f"  Example: {lines[0]}",
        ],
        "delay": 600,
    }

    part1 = part2 = 0
    for line in lines:
        lo, hi, char, password = re.match(r"(\d+)-(\d+) (.): (.+)", line).groups()
        lo, hi = int(lo), int(hi)
        if lo <= password.count(char) <= hi:
            part1 += 1
        if (password[lo - 1] == char) ^ (password[hi - 1] == char):
            part2 += 1

    yield {
        "type": "text",
        "lines": [
            "  ===================================",
            "  Results",
            "  ===================================",
            "",
            f"  Part 1: {part1} valid (count policy)",
            f"  Part 2: {part2} valid (position policy)",
        ],
        "delay": 500,
    }
