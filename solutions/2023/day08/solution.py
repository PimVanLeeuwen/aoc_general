"""
Day 8 - Haunted Wasteland
Year: 2023

Navigate a network of nodes following L/R instructions,
using LCM for simultaneous ghost paths.
"""

import math
import re


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    lines = puzzle_input.strip().split("\n")
    instructions = lines[0]

    network = {}
    for line in lines[2:]:
        parts = re.findall(r"[A-Z0-9]+", line)
        network[parts[0]] = (parts[1], parts[2])

    def steps_to_end(start, end_condition):
        """Count steps from start until end_condition(node) is True."""
        node = start
        step = 0
        while not end_condition(node):
            direction = 0 if instructions[step % len(instructions)] == "L" else 1
            node = network[node][direction]
            step += 1
        return step

    # Part 1: AAA to ZZZ
    if "AAA" in network:
        part1 = steps_to_end("AAA", lambda n: n == "ZZZ")
    else:
        part1 = 0

    # Part 2: all **A nodes simultaneously reach **Z
    starts = [n for n in network if n.endswith("A")]
    if starts:
        cycles = [steps_to_end(s, lambda n: n.endswith("Z")) for s in starts]
        part2 = math.lcm(*cycles)
    else:
        part2 = 0

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    """Yield frames showing network navigation."""
    lines = puzzle_input.strip().split("\n")
    instructions = lines[0]
    node_count = len(lines) - 2

    yield {
        "type": "text",
        "lines": [
            "  Haunted Wasteland",
            "",
            f"  Instructions: {len(instructions)} steps",
            f"  Nodes: {node_count}",
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
            f"  Part 1: {part1} (AAA → ZZZ)",
            f"  Part 2: {part2} (ghost LCM)",
        ],
        "delay": 500,
    }
