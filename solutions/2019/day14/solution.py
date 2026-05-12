"""
Day 14 - Space Stoichiometry
Year: 2019

Compute ore needed to produce fuel via a chain of chemical reactions,
then binary search for max fuel from 1 trillion ore.
"""

from math import ceil
from collections import defaultdict


def parse_reactions(text):
    """Parse reactions into {output_chem: (output_qty, [(qty, chem), ...])}."""
    reactions = {}
    for line in text.strip().splitlines():
        left, right = line.split(" => ")
        inputs = []
        for part in left.split(", "):
            qty, chem = part.split()
            inputs.append((int(qty), chem))
        qty, chem = right.split()
        reactions[chem] = (int(qty), inputs)
    return reactions


def ore_for_fuel(reactions, fuel_amount):
    """Calculate the minimum ORE needed to produce fuel_amount FUEL."""
    need = defaultdict(int)
    surplus = defaultdict(int)
    need["FUEL"] = fuel_amount

    while True:
        # Find a chemical we still need that isn't ORE
        chem = None
        for c, qty in need.items():
            if c != "ORE" and qty > 0:
                chem = c
                break
        if chem is None:
            break

        required = need[chem]
        del need[chem]

        # Use surplus first
        from_surplus = min(surplus[chem], required)
        surplus[chem] -= from_surplus
        required -= from_surplus

        if required <= 0:
            continue

        out_qty, inputs = reactions[chem]
        batches = ceil(required / out_qty)

        # Add leftover to surplus
        surplus[chem] += batches * out_qty - required

        # Add input requirements
        for in_qty, in_chem in inputs:
            need[in_chem] += batches * in_qty

    return need.get("ORE", 0)


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    reactions = parse_reactions(puzzle_input)

    ore_per_fuel = ore_for_fuel(reactions, 1)
    part1 = ore_per_fuel

    # Binary search for max fuel from 1 trillion ore
    trillion = 1_000_000_000_000
    lo = trillion // ore_per_fuel
    hi = lo * 2
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if ore_for_fuel(reactions, mid) <= trillion:
            lo = mid
        else:
            hi = mid - 1
    part2 = lo

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    """Yield frames showing the reaction chain and binary search."""
    reactions = parse_reactions(puzzle_input)

    yield {
        "type": "text",
        "lines": [
            "  Space Stoichiometry",
            "",
            f"  Reactions: {len(reactions)}",
            f"  Chemicals: {len(reactions) + 1} (including ORE)",
        ],
        "delay": 600,
    }

    ore_per_fuel = ore_for_fuel(reactions, 1)

    yield {
        "type": "text",
        "lines": [
            "  Part 1: ORE for 1 FUEL",
            "",
            f"  Minimum ORE: {ore_per_fuel:,}",
        ],
        "delay": 400,
    }

    # Binary search visualization
    trillion = 1_000_000_000_000
    lo = trillion // ore_per_fuel
    hi = lo * 2
    steps = 0

    while lo < hi:
        mid = (lo + hi + 1) // 2
        ore = ore_for_fuel(reactions, mid)
        fits = ore <= trillion

        steps += 1
        if steps <= 20:
            yield {
                "type": "text",
                "lines": [
                    "  Part 2: Binary search for max FUEL",
                    "",
                    f"  Step {steps}:",
                    f"  Range: [{lo:,} .. {hi:,}]",
                    f"  Try: {mid:,} FUEL -> {ore:,} ORE",
                    f"  {'<= 1T, search higher' if fits else '> 1T, search lower'}",
                ],
                "delay": 100,
            }

        if fits:
            lo = mid
        else:
            hi = mid - 1

    yield {
        "type": "text",
        "lines": [
            "  ===================================",
            "  Results",
            "  ===================================",
            "",
            f"  Part 1: {ore_per_fuel:,} ORE for 1 FUEL",
            f"  Part 2: {lo:,} FUEL from 1 trillion ORE",
            f"  Binary search: {steps} steps",
        ],
        "delay": 500,
    }
