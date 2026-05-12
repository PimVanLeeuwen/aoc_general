"""
Day 07 - The Treachery of Whales
Year: 2021

Align crab submarines to a single position minimizing fuel cost,
with constant and triangular fuel models.
"""


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    positions = [int(x) for x in puzzle_input.strip().split(",")]
    positions.sort()

    # Part 1: minimize sum of |x - target|
    # The optimal point is the median
    median = positions[len(positions) // 2]
    part1 = sum(abs(p - median) for p in positions)

    # Part 2: minimize sum of n*(n+1)/2 where n = |x - target|
    # The optimal point is near the mean (check both floor and ceil)
    mean = sum(positions) / len(positions)
    best = float("inf")
    for target in (int(mean), int(mean) + 1):
        cost = sum(abs(p - target) * (abs(p - target) + 1) // 2 for p in positions)
        best = min(best, cost)
    part2 = best

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    """Yield frames showing crab alignment analysis."""
    positions = [int(x) for x in puzzle_input.strip().split(",")]
    positions.sort()

    yield {
        "type": "text",
        "lines": [
            "  The Treachery of Whales",
            "",
            f"  Crabs: {len(positions)}",
            f"  Position range: {positions[0]} - {positions[-1]}",
            f"  Median: {positions[len(positions) // 2]}",
            f"  Mean: {sum(positions) / len(positions):.1f}",
        ],
        "delay": 600,
    }

    median = positions[len(positions) // 2]
    part1 = sum(abs(p - median) for p in positions)

    mean = sum(positions) / len(positions)
    best = float("inf")
    best_target = 0
    for target in (int(mean), int(mean) + 1):
        cost = sum(abs(p - target) * (abs(p - target) + 1) // 2 for p in positions)
        if cost < best:
            best = cost
            best_target = target

    yield {
        "type": "text",
        "lines": [
            "  ===================================",
            "  Results",
            "  ===================================",
            "",
            f"  Part 1: {part1}",
            f"    Target: {median} (median)",
            f"    Fuel model: constant",
            "",
            f"  Part 2: {best}",
            f"    Target: {best_target} (near mean)",
            f"    Fuel model: triangular (n*(n+1)/2)",
        ],
        "delay": 500,
    }
