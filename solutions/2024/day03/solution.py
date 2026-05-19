"""
Day 3 - Mull It Over
Year: 2024

Parse corrupted memory for mul(X,Y) instructions,
with do()/don't() conditional toggles in part 2.
"""

import re


def solve(puzzle_input: str) -> tuple[str, str]:
    text = puzzle_input.strip()

    # Match mul(X,Y), do(), and don't() instructions
    pattern = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)|do\(\)|don't\(\)")

    part1 = 0
    part2 = 0
    enabled = True

    for match in pattern.finditer(text):
        token = match.group()
        if token == "do()":
            enabled = True
        elif token == "don't()":
            enabled = False
        else:
            a, b = int(match.group(1)), int(match.group(2))
            part1 += a * b
            if enabled:
                part2 += a * b

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    text = puzzle_input.strip()

    pattern = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)|do\(\)|don't\(\)")
    matches = list(pattern.finditer(text))

    mul_count = sum(1 for m in matches if m.group().startswith("mul"))
    do_count = sum(1 for m in matches if m.group() == "do()")
    dont_count = sum(1 for m in matches if m.group() == "don't()")

    yield {
        "type": "text",
        "lines": [
            "  Mull It Over",
            "",
            f"  Input length: {len(text)} chars",
            f"  mul() instructions: {mul_count}",
            f"  do() toggles: {do_count}",
            f"  don't() toggles: {dont_count}",
        ],
        "delay": 600,
    }

    part1, part2 = solve(text)

    yield {
        "type": "text",
        "lines": [
            "  ===================================",
            "  Results",
            "  ===================================",
            "",
            f"  Part 1: {part1} (all multiplications)",
            f"  Part 2: {part2} (conditional only)",
        ],
        "delay": 500,
    }
