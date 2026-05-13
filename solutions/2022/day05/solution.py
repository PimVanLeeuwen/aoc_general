"""
Day 5 - Supply Stacks
Year: 2022

Simulate a crane moving crates between stacks, one at a time
for part 1 and in bulk for part 2.
"""

import re
from copy import deepcopy


def parse(text):
    """Parse initial stacks and move instructions."""
    crate_section, move_section = text.split("\n\n")

    crate_lines = crate_section.split("\n")
    num_stacks = len(crate_lines[-1].split())
    stacks = [[] for _ in range(num_stacks)]

    # Parse crates from bottom to top (skip the number line)
    for line in reversed(crate_lines[:-1]):
        for i in range(num_stacks):
            pos = 1 + i * 4
            if pos < len(line) and line[pos] != " ":
                stacks[i].append(line[pos])

    moves = []
    for line in move_section.strip().split("\n"):
        nums = list(map(int, re.findall(r"\d+", line)))
        moves.append((nums[0], nums[1] - 1, nums[2] - 1))

    return stacks, moves


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    stacks, moves = parse(puzzle_input)
    stacks2 = deepcopy(stacks)

    # Part 1: move one at a time (reverses order)
    for count, src, dst in moves:
        for _ in range(count):
            stacks[dst].append(stacks[src].pop())

    # Part 2: move all at once (preserves order)
    for count, src, dst in moves:
        stacks2[dst].extend(stacks2[src][-count:])
        del stacks2[src][-count:]

    part1 = "".join(s[-1] for s in stacks if s)
    part2 = "".join(s[-1] for s in stacks2 if s)

    return part1, part2


def visualize(puzzle_input: str):
    """Yield frames showing crate movement."""
    stacks, moves = parse(puzzle_input)

    max_h = max(len(s) for s in stacks)
    lines = ["  Initial stacks:", ""]
    for row in range(max_h - 1, -1, -1):
        line = "  "
        for s in stacks:
            if row < len(s):
                line += f"[{s[row]}] "
            else:
                line += "    "
        lines.append(line)
    lines.append("  " + "  ".join(f" {i + 1} " for i in range(len(stacks))))

    yield {"type": "text", "lines": lines, "delay": 600}

    part1, part2 = solve(puzzle_input)

    yield {
        "type": "text",
        "lines": [
            "  ===================================",
            "  Results",
            "  ===================================",
            "",
            f"  Part 1: {part1} (one at a time)",
            f"  Part 2: {part2} (bulk move)",
        ],
        "delay": 500,
    }
