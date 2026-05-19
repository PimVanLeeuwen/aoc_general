"""
Day 2 - Red-Nosed Reports
Year: 2024

Check reactor reports for safety: levels must be strictly
monotonic with differences between 1 and 3.
"""


def is_safe(levels):
    diffs = [levels[i + 1] - levels[i] for i in range(len(levels) - 1)]
    all_increasing = all(d > 0 for d in diffs)
    all_decreasing = all(d < 0 for d in diffs)
    bounded = all(1 <= abs(d) <= 3 for d in diffs)
    return (all_increasing or all_decreasing) and bounded


def solve(puzzle_input: str) -> tuple[str, str]:
    lines = puzzle_input.strip().split("\n")

    part1 = 0
    part2 = 0

    for line in lines:
        levels = list(map(int, line.split()))

        if is_safe(levels):
            part1 += 1
            part2 += 1
        else:
            # Try removing each single level (Problem Dampener)
            for i in range(len(levels)):
                dampened = levels[:i] + levels[i + 1:]
                if is_safe(dampened):
                    part2 += 1
                    break

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    lines = puzzle_input.strip().split("\n")

    text_lines = ["  Red-Nosed Reports", "", "  Sample reports:"]
    for line in lines[:6]:
        levels = list(map(int, line.split()))
        safe = is_safe(levels)
        tag = "SAFE" if safe else "UNSAFE"
        text_lines.append(f"  {str(levels):40s} {tag}")

    yield {"type": "text", "lines": text_lines, "delay": 600}

    part1, part2 = solve(puzzle_input)

    yield {
        "type": "text",
        "lines": [
            "  ===================================",
            "  Results",
            "  ===================================",
            "",
            f"  Part 1: {part1} (safe reports)",
            f"  Part 2: {part2} (with dampener)",
        ],
        "delay": 500,
    }
