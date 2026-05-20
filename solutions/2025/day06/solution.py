"""
Day 6 - Column Calculator
Year: 2025

Parse columnar arithmetic problems where numbers are stacked
vertically with an operator. Part 1: single-column digits.
Part 2: multi-column numbers read right-to-left.
"""

from math import prod


def solve(puzzle_input: str) -> tuple[str, str]:
    lines_raw = input_data_to_lines(puzzle_input)
    part1 = 0
    part2 = 0

    # Part 1: parse as space-separated columns, each column is one problem
    parsed = [list(r for r in line.split(" ") if r) for line in lines_raw]
    for i in range(len(parsed[0])):
        nums = [int(parsed[r][i]) for r in range(4)]
        op = parsed[4][i]
        if op == "*":
            part1 += prod(nums)
        else:
            part1 += sum(nums)

    # Part 2: handle multi-digit columnar numbers
    # Pad all lines to the same length
    stripped = [line.rstrip("\n") for line in puzzle_input.splitlines() if line.strip()]
    max_len = max(len(line) for line in stripped)
    grid = [line.ljust(max_len) for line in stripped]

    col = 0
    prob_idx = 0
    while col < len(grid[0]):
        # Skip empty columns
        if all(grid[r][col] == " " for r in range(5)):
            col += 1
            continue

        # Collect columns for this problem
        problem_cols = []
        while col < len(grid[0]) and not all(grid[r][col] == " " for r in range(4)):
            problem_cols.append(col)
            col += 1

        # Read numbers from columns right-to-left
        numbers = []
        for c in reversed(problem_cols):
            num_str = "".join(grid[r][c] for r in range(4)).strip()
            if num_str:
                numbers.append(int(num_str))

        # Get operator from part 1 parsing
        op = parsed[4][prob_idx]
        if op == "+":
            part2 += sum(numbers)
        else:
            part2 += prod(numbers)

        prob_idx += 1

    return str(part1), str(part2)


def input_data_to_lines(text):
    return text.strip().split("\n")


def visualize(puzzle_input: str):
    lines = puzzle_input.strip().split("\n")

    yield {
        "type": "text",
        "lines": [
            "  Column Calculator",
            "",
            f"  Input lines: {len(lines)}",
            "  Sample:",
        ] + [f"    {line[:60]}" for line in lines[:5]],
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
            f"  Part 1: {part1} (single-column)",
            f"  Part 2: {part2} (multi-column)",
        ],
        "delay": 500,
    }
