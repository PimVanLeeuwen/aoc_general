"""
Day 7 - Bridge Repair
Year: 2024

Determine which equations can be made true by inserting
+, *, and || (concatenation) operators between numbers.
"""


def can_make(target, numbers, use_concat=False):
    """Recursively check if operators can produce the target value."""
    if len(numbers) == 1:
        return numbers[0] == target

    first, second, *rest = numbers

    # Try addition
    if can_make(target, [first + second] + rest, use_concat):
        return True

    # Try multiplication
    if can_make(target, [first * second] + rest, use_concat):
        return True

    # Try concatenation (part 2)
    if use_concat:
        concatenated = int(str(first) + str(second))
        if can_make(target, [concatenated] + rest, use_concat):
            return True

    return False


def solve(puzzle_input: str) -> tuple[str, str]:
    lines = puzzle_input.strip().split("\n")

    part1 = 0
    part2 = 0

    for line in lines:
        target_str, nums_str = line.split(": ")
        target = int(target_str)
        numbers = list(map(int, nums_str.split()))

        if can_make(target, numbers):
            part1 += target
        if can_make(target, numbers, use_concat=True):
            part2 += target

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    lines = puzzle_input.strip().split("\n")

    yield {
        "type": "text",
        "lines": [
            "  Bridge Repair",
            "",
            f"  Equations to check: {len(lines)}",
            "",
            "  Sample equations:",
        ] + [f"    {line}" for line in lines[:5]],
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
            f"  Part 1: {part1} (+ and * only)",
            f"  Part 2: {part2} (with concatenation)",
        ],
        "delay": 500,
    }
