"""
Day 12 - Present Packing
Year: 2025

Check if presents can fit into delivery regions based on
capacity constraints.
"""


def solve(puzzle_input: str) -> tuple[str, str]:
    # Parse regions from the last section of input
    sections = puzzle_input.split("\n\n")
    region_lines = sections[-1].strip().split("\n")

    part1 = 0

    for line in region_lines:
        left, right = line.split(":")
        w, h = map(int, left.split("x"))
        counts = list(map(int, right.strip().split()))
        total_presents = sum(counts)

        # Each 3x3 area can hold one present
        capacity = (w // 3) * (h // 3)

        if total_presents <= capacity:
            part1 += 1

    return str(part1), "Merry Christmas!"


def visualize(puzzle_input: str):
    sections = puzzle_input.split("\n\n")
    region_lines = sections[-1].strip().split("\n")

    yield {
        "type": "text",
        "lines": [
            "  Present Packing",
            "",
            f"  Regions: {len(region_lines)}",
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
            f"  Part 1: {part1} (fitting regions)",
            f"  Part 2: {part2}",
        ],
        "delay": 500,
    }
