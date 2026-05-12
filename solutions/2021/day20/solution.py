"""
Day 20 - Trench Map
Year: 2021

Enhance an image using a 9-pixel lookup algorithm.
Handle the infinite background flipping on each step.
"""


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    sections = puzzle_input.strip().split("\n\n")
    algorithm = sections[0].replace("\n", "")
    image_lines = sections[1].split("\n")

    # Store lit pixels as a set of (row, col)
    lit = set()
    for r, line in enumerate(image_lines):
        for c, ch in enumerate(line):
            if ch == "#":
                lit.add((r, c))

    # The infinite background alternates if algorithm[0] == '#' and algorithm[511] == '.'
    bg_flips = algorithm[0] == "#"

    # Track the known region explicitly (everything outside is background)
    prev_min_r, prev_max_r = 0, len(image_lines) - 1
    prev_min_c, prev_max_c = 0, len(image_lines[0]) - 1

    part1 = None

    for step in range(50):
        bg_lit = bg_flips and step % 2 == 1

        # Expand iteration range by 1 beyond previous known region
        iter_min_r = prev_min_r - 1
        iter_max_r = prev_max_r + 1
        iter_min_c = prev_min_c - 1
        iter_max_c = prev_max_c + 1

        new_lit = set()
        for r in range(iter_min_r, iter_max_r + 1):
            for c in range(iter_min_c, iter_max_c + 1):
                index = 0
                for dr in (-1, 0, 1):
                    for dc in (-1, 0, 1):
                        index <<= 1
                        nr, nc = r + dr, c + dc
                        if prev_min_r <= nr <= prev_max_r and prev_min_c <= nc <= prev_max_c:
                            if (nr, nc) in lit:
                                index |= 1
                        elif bg_lit:
                            index |= 1
                if algorithm[index] == "#":
                    new_lit.add((r, c))

        lit = new_lit
        prev_min_r, prev_max_r = iter_min_r, iter_max_r
        prev_min_c, prev_max_c = iter_min_c, iter_max_c

        if step == 1:
            part1 = len(lit)

    return str(part1), str(len(lit))


def visualize(puzzle_input: str):
    """Yield frames showing image enhancement."""
    sections = puzzle_input.strip().split("\n\n")
    image_lines = sections[1].split("\n")

    yield {
        "type": "text",
        "lines": [
            "  Trench Map",
            "",
            f"  Algorithm: {len(sections[0].replace(chr(10), ''))} entries",
            f"  Image: {len(image_lines)}x{len(image_lines[0])}",
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
            f"  Part 1: {part1} (after 2 enhancements)",
            f"  Part 2: {part2} (after 50 enhancements)",
        ],
        "delay": 500,
    }
