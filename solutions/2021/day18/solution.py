"""
Day 18 - Snailfish
Year: 2021

Reduce snailfish numbers by exploding and splitting, then compute magnitudes.
Uses a flat list of (value, depth) pairs for efficient manipulation.
"""

from itertools import permutations


def parse(line):
    """Convert nested bracket string to list of (value, depth) pairs."""
    tokens = []
    depth = 0
    for ch in line:
        if ch == "[":
            depth += 1
        elif ch == "]":
            depth -= 1
        elif ch.isdigit():
            tokens.append([int(ch), depth])
    return tokens


def explode(tokens):
    """Explode the first pair nested 5 deep. Return True if anything changed."""
    for i in range(len(tokens) - 1):
        if tokens[i][1] >= 5 and tokens[i + 1][1] == tokens[i][1]:
            left_val, depth = tokens[i]
            right_val = tokens[i + 1][0]
            if i > 0:
                tokens[i - 1][0] += left_val
            if i + 2 < len(tokens):
                tokens[i + 2][0] += right_val
            tokens[i:i + 2] = [[0, depth - 1]]
            return True
    return False


def split(tokens):
    """Split the first value >= 10. Return True if anything changed."""
    for i, (val, depth) in enumerate(tokens):
        if val >= 10:
            tokens[i:i + 1] = [[val // 2, depth + 1], [(val + 1) // 2, depth + 1]]
            return True
    return False


def reduce(tokens):
    """Repeatedly explode then split until stable."""
    while True:
        if explode(tokens):
            continue
        if split(tokens):
            continue
        break
    return tokens


def add(a, b):
    """Add two snailfish numbers and reduce."""
    combined = [[v, d + 1] for v, d in a] + [[v, d + 1] for v, d in b]
    return reduce(combined)


def magnitude(tokens):
    """Compute magnitude by repeatedly collapsing deepest pairs."""
    tokens = [t[:] for t in tokens]
    while len(tokens) > 1:
        for i in range(len(tokens) - 1):
            if tokens[i][1] == tokens[i + 1][1]:
                mag = 3 * tokens[i][0] + 2 * tokens[i + 1][0]
                tokens[i:i + 2] = [[mag, tokens[i][1] - 1]]
                break
    return tokens[0][0]


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    numbers = [parse(line) for line in puzzle_input.strip().split("\n")]

    # Part 1: sum all numbers left to right
    result = numbers[0]
    for num in numbers[1:]:
        result = add(result, num)
    part1 = magnitude(result)

    # Part 2: largest magnitude of any two distinct numbers
    part2 = 0
    for i, j in permutations(range(len(numbers)), 2):
        a = [t[:] for t in numbers[i]]
        b = [t[:] for t in numbers[j]]
        part2 = max(part2, magnitude(add(a, b)))

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    """Yield frames showing snailfish arithmetic."""
    lines = puzzle_input.strip().split("\n")
    numbers = [parse(line) for line in lines]

    yield {
        "type": "text",
        "lines": [
            "  Snailfish",
            "",
            f"  Numbers to add: {len(numbers)}",
            f"  First: {lines[0][:60]}{'...' if len(lines[0]) > 60 else ''}",
        ],
        "delay": 600,
    }

    # Show running sum
    result = numbers[0]
    for i, num in enumerate(numbers[1:], 1):
        result = add(result, num)

    part1 = magnitude(result)

    part2 = 0
    for i, j in permutations(range(len(numbers)), 2):
        a = [t[:] for t in numbers[i]]
        b = [t[:] for t in numbers[j]]
        part2 = max(part2, magnitude(add(a, b)))

    yield {
        "type": "text",
        "lines": [
            "  ===================================",
            "  Results",
            "  ===================================",
            "",
            f"  Part 1: {part1} (magnitude of sum)",
            f"  Part 2: {part2} (max pairwise magnitude)",
        ],
        "delay": 500,
    }
