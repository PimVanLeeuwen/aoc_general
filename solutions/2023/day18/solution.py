"""
Day 18 - Lavaduct Lagoon
Year: 2023

Calculate the area of a polygon defined by digging instructions,
using the Shoelace formula and Pick's theorem.
"""


DIRS = {"R": (0, 1), "L": (0, -1), "U": (-1, 0), "D": (1, 0)}
HEX_DIRS = {"0": "R", "1": "D", "2": "L", "3": "U"}


def polygon_area(instructions):
    """Compute total area including boundary using Shoelace + Pick's theorem."""
    r, c = 0, 0
    perimeter = 0
    shoelace = 0

    for direction, steps in instructions:
        dr, dc = DIRS[direction]
        nr, nc = r + dr * steps, c + dc * steps
        shoelace += r * nc - nr * c  # cross product term
        perimeter += steps
        r, c = nr, nc

    interior_area = abs(shoelace) // 2
    # Pick's theorem: A = i + b/2 - 1, so i + b = A + b/2 + 1
    return interior_area + perimeter // 2 + 1


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    instructions1 = []
    instructions2 = []

    for line in puzzle_input.strip().split("\n"):
        parts = line.split()
        direction, steps = parts[0], int(parts[1])
        instructions1.append((direction, steps))

        # Part 2: decode from hex color
        hex_code = parts[2][2:-1]  # strip (# and )
        hex_steps = int(hex_code[:5], 16)
        hex_dir = HEX_DIRS[hex_code[5]]
        instructions2.append((hex_dir, hex_steps))

    part1 = polygon_area(instructions1)
    part2 = polygon_area(instructions2)

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    """Yield frames showing lagoon digging."""
    lines = puzzle_input.strip().split("\n")

    yield {
        "type": "text",
        "lines": [
            "  Lavaduct Lagoon",
            "",
            f"  Instructions: {len(lines)}",
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
            f"  Part 1: {part1} (direct instructions)",
            f"  Part 2: {part2} (hex-decoded)",
        ],
        "delay": 500,
    }
