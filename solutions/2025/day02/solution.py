"""
Day 2 - Repeating IDs
Year: 2025

Check numeric ID ranges for repeating-pattern numbers.
Part 1: two equal halves. Part 2: any repeating substring.
"""


def solve(puzzle_input: str) -> tuple[str, str]:
    ranges = puzzle_input.strip().split("\n")[0].split(",")

    part1 = 0
    part2 = 0

    for r in ranges:
        a, b = r.split("-")
        for i in range(int(a), int(b) + 1):
            s = str(i)
            n = len(s)

            # Part 1: two equal halves
            if n % 2 == 0 and s[:n // 2] == s[n // 2:]:
                part1 += i

            # Part 2: any repeating substring pattern
            for j in range(1, n // 2 + 1):
                if n % j == 0 and s == s[:j] * (n // j):
                    part2 += i
                    break

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    ranges = puzzle_input.strip().split("\n")[0].split(",")

    yield {
        "type": "text",
        "lines": [
            "  Repeating IDs",
            "",
            f"  ID ranges: {len(ranges)}",
            f"  Sample: {ranges[0]}, {ranges[1]}..." if len(ranges) > 1 else f"  Range: {ranges[0]}",
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
            f"  Part 1: {part1} (half-repeat sum)",
            f"  Part 2: {part2} (any-repeat sum)",
        ],
        "delay": 500,
    }
