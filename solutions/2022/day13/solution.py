"""
Day 13 - Distress Signal
Year: 2022

Compare nested list packets and sort them to find decoder key.
"""

import json
from functools import cmp_to_key


def compare(left, right):
    """Compare two packet values. Return -1, 0, or 1."""
    if isinstance(left, int) and isinstance(right, int):
        return (left > right) - (left < right)

    if isinstance(left, int):
        left = [left]
    if isinstance(right, int):
        right = [right]

    for a, b in zip(left, right):
        result = compare(a, b)
        if result != 0:
            return result

    return (len(left) > len(right)) - (len(left) < len(right))


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    pairs = puzzle_input.strip().split("\n\n")

    # Part 1: sum indices of correctly ordered pairs
    part1 = 0
    all_packets = []
    for i, pair in enumerate(pairs):
        left, right = pair.split("\n")
        left, right = json.loads(left), json.loads(right)
        all_packets.extend([left, right])
        if compare(left, right) == -1:
            part1 += i + 1

    # Part 2: sort all packets with divider packets
    div1, div2 = [[2]], [[6]]
    all_packets.extend([div1, div2])
    all_packets.sort(key=cmp_to_key(compare))

    idx1 = all_packets.index(div1) + 1
    idx2 = all_packets.index(div2) + 1
    part2 = idx1 * idx2

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    """Yield frames showing packet comparison."""
    pairs = puzzle_input.strip().split("\n\n")

    yield {
        "type": "text",
        "lines": [
            "  Distress Signal",
            "",
            f"  Packet pairs: {len(pairs)}",
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
            f"  Part 1: {part1} (correct order index sum)",
            f"  Part 2: {part2} (decoder key)",
        ],
        "delay": 500,
    }
