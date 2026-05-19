"""
Day 22 - Monkey Market
Year: 2024

Generate pseudo-random secret numbers and find the best
4-change sequence to maximise banana purchases.
"""

from collections import defaultdict


def next_secret(s):
    s = (s ^ (s << 6)) & 0xFFFFFF
    s = (s ^ (s >> 5)) & 0xFFFFFF
    s = (s ^ (s << 11)) & 0xFFFFFF
    return s


def solve(puzzle_input: str) -> tuple[str, str]:
    initials = list(map(int, puzzle_input.strip().split("\n")))

    part1 = 0
    sequence_totals = defaultdict(int)

    for secret in initials:
        prices = [secret % 10]
        s = secret

        for _ in range(2000):
            s = next_secret(s)
            prices.append(s % 10)

        part1 += s

        # Track first occurrence of each 4-change sequence
        seen = set()
        for i in range(4, len(prices)):
            key = (
                prices[i - 3] - prices[i - 4],
                prices[i - 2] - prices[i - 3],
                prices[i - 1] - prices[i - 2],
                prices[i] - prices[i - 1],
            )
            if key not in seen:
                seen.add(key)
                sequence_totals[key] += prices[i]

    part2 = max(sequence_totals.values())

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    initials = list(map(int, puzzle_input.strip().split("\n")))

    yield {
        "type": "text",
        "lines": [
            "  Monkey Market",
            "",
            f"  Buyers: {len(initials)}",
            f"  Sample seeds: {initials[:5]}",
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
            f"  Part 1: {part1} (sum of 2000th secrets)",
            f"  Part 2: {part2} (max bananas)",
        ],
        "delay": 500,
    }
