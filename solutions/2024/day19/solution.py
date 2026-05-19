"""
Day 19 - Linen Layout
Year: 2024

Count how many towel designs can be composed from available
patterns, and the total number of ways to compose them.
"""


def count_ways(design, patterns):
    """DP to count how many ways the design can be built from patterns."""
    n = len(design)
    dp = [0] * (n + 1)
    dp[0] = 1  # empty prefix: one way

    for i in range(1, n + 1):
        for p in patterns:
            plen = len(p)
            if i >= plen and design[i - plen:i] == p:
                dp[i] += dp[i - plen]

    return dp[n]


def solve(puzzle_input: str) -> tuple[str, str]:
    parts = puzzle_input.strip().split("\n\n")
    patterns = [p.strip() for p in parts[0].split(",")]
    designs = parts[1].split("\n")

    part1 = 0
    part2 = 0

    for design in designs:
        ways = count_ways(design, patterns)
        if ways > 0:
            part1 += 1
        part2 += ways

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    parts = puzzle_input.strip().split("\n\n")
    patterns = [p.strip() for p in parts[0].split(",")]
    designs = parts[1].split("\n")

    yield {
        "type": "text",
        "lines": [
            "  Linen Layout",
            "",
            f"  Available patterns: {len(patterns)}",
            f"  Designs to check: {len(designs)}",
            "",
            "  Sample patterns: " + ", ".join(patterns[:8]) + "...",
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
            f"  Part 1: {part1} (possible designs)",
            f"  Part 2: {part2} (total arrangements)",
        ],
        "delay": 500,
    }
