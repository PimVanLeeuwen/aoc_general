"""
Day 5 - Range Checker
Year: 2025

Check which numbers fall within given ranges (part 1),
then merge overlapping ranges and count total coverage (part 2).
"""


def solve(puzzle_input: str) -> tuple[str, str]:
    lines = puzzle_input.strip().split("\n")

    ranges = [tuple(map(int, line.split("-"))) for line in lines if "-" in line]
    numbers = [int(line) for line in lines if line.strip().isdigit()]

    # Part 1: count numbers that fall within any range
    part1 = 0
    for n in numbers:
        if any(start <= n <= end for start, end in ranges):
            part1 += 1

    # Part 2: merge overlapping ranges, sum their total coverage
    ranges.sort()
    merged = [list(ranges[0])]
    for start, end in ranges[1:]:
        if start <= merged[-1][1] + 1:
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])

    part2 = sum(end - start + 1 for start, end in merged)

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    lines = puzzle_input.strip().split("\n")
    ranges = [line for line in lines if "-" in line]
    numbers = [line for line in lines if line.strip().isdigit()]

    yield {
        "type": "text",
        "lines": [
            "  Range Checker",
            "",
            f"  Ranges: {len(ranges)}",
            f"  Numbers to check: {len(numbers)}",
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
            f"  Part 1: {part1} (numbers in range)",
            f"  Part 2: {part2} (total coverage)",
        ],
        "delay": 500,
    }
