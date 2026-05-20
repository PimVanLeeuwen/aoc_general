"""
Day 3 - Digit Picker
Year: 2025

From a string of digits, form the largest 2-digit number (part 1)
or largest 12-digit number (part 2) by picking digits in order.
"""


def solve(puzzle_input: str) -> tuple[str, str]:
    lines = puzzle_input.strip().split("\n")

    part1 = 0
    part2 = 0

    for line in lines:
        digits = list(line.strip())
        n = len(digits)

        # Part 1: largest 2-digit number from any two positions i < j
        part1 += max(
            int(digits[i] + digits[j])
            for i in range(n)
            for j in range(i + 1, n)
        )

        # Part 2: largest 12-digit number by greedy selection
        # Pick 12 digits left-to-right, always choosing the largest
        # available digit that still leaves enough remaining digits
        result = []
        start = 0
        for remaining in range(12, 0, -1):
            end = n - remaining + 1
            best = max(range(start, end), key=lambda i: digits[i])
            result.append(digits[best])
            start = best + 1

        part2 += int("".join(result))

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    lines = puzzle_input.strip().split("\n")

    yield {
        "type": "text",
        "lines": [
            "  Digit Picker",
            "",
            f"  Lines: {len(lines)}",
            f"  Digit lengths: {len(lines[0])} chars each",
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
            f"  Part 1: {part1} (max 2-digit numbers)",
            f"  Part 2: {part2} (max 12-digit numbers)",
        ],
        "delay": 500,
    }
