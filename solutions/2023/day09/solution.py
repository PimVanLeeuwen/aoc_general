"""
Day 9 - Mirage Maintenance
Year: 2023

Extrapolate the next and previous values in sequences
by repeatedly taking differences until all zeros.
"""


def extrapolate(sequence):
    """Return (next_value, previous_value) by difference reduction."""
    layers = [sequence]
    while not all(v == 0 for v in layers[-1]):
        prev = layers[-1]
        layers.append([prev[i + 1] - prev[i] for i in range(len(prev) - 1)])

    # Extrapolate forward and backward
    next_val = sum(layer[-1] for layer in layers)
    prev_val = 0
    for layer in reversed(layers):
        prev_val = layer[0] - prev_val

    return next_val, prev_val


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    sequences = [
        list(map(int, line.split()))
        for line in puzzle_input.strip().split("\n")
    ]

    part1 = 0
    part2 = 0
    for seq in sequences:
        nxt, prv = extrapolate(seq)
        part1 += nxt
        part2 += prv

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    """Yield frames showing sequence extrapolation."""
    lines = puzzle_input.strip().split("\n")

    yield {
        "type": "text",
        "lines": [
            "  Mirage Maintenance",
            "",
            f"  Sequences: {len(lines)}",
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
            f"  Part 1: {part1} (next values)",
            f"  Part 2: {part2} (previous values)",
        ],
        "delay": 500,
    }
