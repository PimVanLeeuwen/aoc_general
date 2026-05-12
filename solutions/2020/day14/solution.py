"""
Day 14 - Docking Data
Year: 2020

Apply bitmasks to values (Part 1) or to memory addresses with floating
bits that expand into multiple writes (Part 2).
"""

import re
from itertools import product


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    lines = puzzle_input.strip().split("\n")

    # Part 1: mask overwrites value bits (X = unchanged)
    mem1 = {}
    mask = ""
    for line in lines:
        if line.startswith("mask"):
            mask = line.split(" = ")[1]
        else:
            addr, val = map(int, re.findall(r"\d+", line))
            # Apply mask: 1 forces 1, 0 forces 0, X keeps original
            or_mask = int(mask.replace("X", "0"), 2)
            and_mask = int(mask.replace("X", "1"), 2)
            mem1[addr] = (val | or_mask) & and_mask

    part1 = sum(mem1.values())

    # Part 2: mask applied to address (1 = force 1, X = floating)
    mem2 = {}
    for line in lines:
        if line.startswith("mask"):
            mask = line.split(" = ")[1]
        else:
            addr, val = map(int, re.findall(r"\d+", line))
            # Apply mask to address
            addr |= int(mask.replace("X", "0"), 2)
            # Find floating bit positions
            floating = [i for i, ch in enumerate(mask) if ch == "X"]
            # Generate all combinations of floating bits
            for bits in product("01", repeat=len(floating)):
                a = addr
                for pos, bit in zip(floating, bits):
                    bit_pos = 35 - pos
                    if bit == "1":
                        a |= (1 << bit_pos)
                    else:
                        a &= ~(1 << bit_pos)
                mem2[a] = val

    part2 = sum(mem2.values())

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    """Yield frames showing bitmask operations."""
    lines = puzzle_input.strip().split("\n")
    mask_count = sum(1 for l in lines if l.startswith("mask"))
    write_count = len(lines) - mask_count

    yield {
        "type": "text",
        "lines": [
            "  Docking Data — Bitmask Operations",
            "",
            f"  Instructions: {len(lines)}",
            f"  Mask updates: {mask_count}",
            f"  Memory writes: {write_count}",
        ],
        "delay": 600,
    }

    part1, part2 = solve("\n".join(lines))

    yield {
        "type": "text",
        "lines": [
            "  ===================================",
            "  Results",
            "  ===================================",
            "",
            f"  Part 1: {part1} (value masking)",
            f"  Part 2: {part2} (address masking with floating bits)",
        ],
        "delay": 500,
    }
