"""
Day 1 - The Tyranny of the Rocket Equation
Year: 2019

Calculate fuel requirements for spacecraft modules, accounting for the
mass of fuel itself.
"""


def fuel_for_mass(mass):
    """Basic fuel calculation: mass // 3 - 2."""
    return max(0, mass // 3 - 2)


def total_fuel_for_mass(mass):
    """Recursively account for the fuel's own mass."""
    total = 0
    fuel = fuel_for_mass(mass)
    while fuel > 0:
        total += fuel
        fuel = fuel_for_mass(fuel)
    return total


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    masses = [int(x) for x in puzzle_input.strip().splitlines()]

    part1 = sum(fuel_for_mass(m) for m in masses)
    part2 = sum(total_fuel_for_mass(m) for m in masses)

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    """Yield frames showing fuel calculations for each module."""
    masses = [int(x) for x in puzzle_input.strip().splitlines()]

    running_p1 = 0
    running_p2 = 0
    step = max(1, len(masses) // 30)

    yield {
        "type": "text",
        "lines": [
            "  The Tyranny of the Rocket Equation",
            "",
            f"  Modules to process: {len(masses)}",
            f"  Mass range: {min(masses):,} - {max(masses):,}",
        ],
        "delay": 600,
    }

    for i, mass in enumerate(masses):
        simple = fuel_for_mass(mass)
        running_p1 += simple

        # Show the recursive fuel chain for a few interesting modules
        if i < 3 or i == len(masses) - 1:
            chain = []
            fuel = fuel_for_mass(mass)
            while fuel > 0:
                chain.append(fuel)
                fuel = fuel_for_mass(fuel)
            total = sum(chain)
            running_p2 += total

            lines = [
                f"  Module {i+1}/{len(masses)}: mass = {mass:,}",
                "",
                f"  Fuel chain: {' + '.join(str(f) for f in chain[:8])}",
            ]
            if len(chain) > 8:
                lines[-1] += " + ..."
            lines += [
                f"  Simple fuel: {simple:,}",
                f"  Total fuel:  {total:,}  ({len(chain)} steps)",
                "",
                f"  Running Part 1: {running_p1:>10,}",
                f"  Running Part 2: {running_p2:>10,}",
            ]
            yield {"type": "text", "lines": lines, "delay": 400}
        else:
            running_p2 += total_fuel_for_mass(mass)

            if (i + 1) % step == 0:
                pct = (i + 1) * 100 // len(masses)
                bar_w = 30
                fill = (i + 1) * bar_w // len(masses)
                bar = "=" * fill + ">" + " " * (bar_w - fill - 1)

                yield {
                    "type": "text",
                    "lines": [
                        f"  Processing modules...",
                        "",
                        f"  [{bar}] {pct}%",
                        "",
                        f"  Running Part 1: {running_p1:>10,}",
                        f"  Running Part 2: {running_p2:>10,}",
                    ],
                    "delay": 60,
                }

    yield {
        "type": "text",
        "lines": [
            "  ===================================",
            "  Results",
            "  ===================================",
            "",
            f"  Part 1: {running_p1:,}",
            f"  Part 2: {running_p2:,}",
            "",
            f"  Extra fuel from recursion: {running_p2 - running_p1:,}",
            f"  ({(running_p2 - running_p1) * 100 // running_p1}% more)",
        ],
        "delay": 500,
    }