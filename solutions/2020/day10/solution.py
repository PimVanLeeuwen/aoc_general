"""
Day 10 - Adapter Array
Year: 2020

Chain joltage adapters and count the number of distinct valid arrangements
using dynamic programming.
"""


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    adapters = sorted(int(x) for x in puzzle_input.strip().split("\n"))
    adapters = [0] + adapters + [adapters[-1] + 3]

    # Part 1: count 1-jolt and 3-jolt differences
    diffs = [adapters[i] - adapters[i - 1] for i in range(1, len(adapters))]
    part1 = diffs.count(1) * diffs.count(3)

    # Part 2: count distinct valid arrangements via DP
    ways = {0: 1}
    for jolt in adapters[1:]:
        ways[jolt] = sum(ways.get(jolt - d, 0) for d in (1, 2, 3))

    part2 = ways[adapters[-1]]

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    """Yield frames showing the adapter chain analysis."""
    adapters = sorted(int(x) for x in puzzle_input.strip().split("\n"))
    adapters = [0] + adapters + [adapters[-1] + 3]

    diffs = [adapters[i] - adapters[i - 1] for i in range(1, len(adapters))]

    yield {
        "type": "text",
        "lines": [
            "  Adapter Array",
            "",
            f"  Adapters: {len(adapters) - 2} (+ outlet + device)",
            f"  Joltage range: 0 - {adapters[-1]}",
            "",
            f"  1-jolt gaps: {diffs.count(1)}",
            f"  2-jolt gaps: {diffs.count(2)}",
            f"  3-jolt gaps: {diffs.count(3)}",
        ],
        "delay": 600,
    }

    ways = {0: 1}
    for jolt in adapters[1:]:
        ways[jolt] = sum(ways.get(jolt - d, 0) for d in (1, 2, 3))

    yield {
        "type": "text",
        "lines": [
            "  ===================================",
            "  Results",
            "  ===================================",
            "",
            f"  Part 1: {diffs.count(1) * diffs.count(3)}",
            f"  Part 2: {ways[adapters[-1]]:,} arrangements",
        ],
        "delay": 500,
    }
