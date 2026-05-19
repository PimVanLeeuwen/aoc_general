"""
Day 11 - Plutonian Pebbles
Year: 2024

Simulate stones that split and transform on each blink.
Track counts per stone value rather than individual stones.
"""

from collections import Counter


def blink(stones):
    """Apply one blink transformation to stone counts."""
    result = Counter()
    for stone, count in stones.items():
        if stone == 0:
            result[1] += count
        elif len(str(stone)) % 2 == 0:
            s = str(stone)
            mid = len(s) // 2
            result[int(s[:mid])] += count
            result[int(s[mid:])] += count
        else:
            result[stone * 2024] += count
    return result


def solve(puzzle_input: str) -> tuple[str, str]:
    numbers = list(map(int, puzzle_input.strip().split()))
    stones = Counter(numbers)

    for _ in range(25):
        stones = blink(stones)
    part1 = sum(stones.values())

    for _ in range(50):
        stones = blink(stones)
    part2 = sum(stones.values())

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    numbers = list(map(int, puzzle_input.strip().split()))
    stones = Counter(numbers)

    yield {
        "type": "text",
        "lines": [
            "  Plutonian Pebbles",
            "",
            f"  Initial stones: {len(numbers)}",
            f"  Unique values: {len(stones)}",
        ],
        "delay": 600,
    }

    # Show growth over a few blinks
    growth = []
    s = Counter(numbers)
    for i in range(10):
        s = blink(s)
        growth.append(f"  Blink {i+1:2d}: {sum(s.values()):>10d} stones ({len(s)} unique)")

    yield {
        "type": "text",
        "lines": ["  Growth over first 10 blinks:", ""] + growth,
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
            f"  Part 1: {part1} (25 blinks)",
            f"  Part 2: {part2} (75 blinks)",
        ],
        "delay": 500,
    }
