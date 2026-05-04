"""
Day 20 - Infinite Elves and Infinite Houses
Year: 2015

Find the first house to receive at least N presents from infinite elves.
"""


def find_house(target, presents_per_elf=10, max_visits=None):
    """Sieve approach: for each elf, add presents to its multiples."""
    limit = target // presents_per_elf + 1
    houses = [0] * (limit + 1)

    for elf in range(1, limit + 1):
        if max_visits is None:
            stop = limit
        else:
            stop = min(elf * max_visits, limit)
        for house in range(elf, stop + 1, elf):
            houses[house] += elf * presents_per_elf

    for house in range(1, limit + 1):
        if houses[house] >= target:
            return house
    return -1


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    target = int(puzzle_input.strip())

    part1 = find_house(target, presents_per_elf=10)
    part2 = find_house(target, presents_per_elf=11, max_visits=50)

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    """Yield frames showing the sieve filling houses with presents."""
    target = int(puzzle_input.strip())

    # Part 1 sieve with progress snapshots
    limit = target // 10 + 1
    houses = [0] * (limit + 1)

    sample_step = max(1, limit // 40)
    answer1 = None

    for elf in range(1, limit + 1):
        for house in range(elf, limit + 1, elf):
            houses[house] += elf * 10

        if answer1 is None and houses[elf] >= target:
            answer1 = elf

        if elf % sample_step == 0 or elf == answer1:
            best_so_far = max(houses[1:elf + 1]) if elf > 0 else 0
            bar_w = 40
            fill = min(round(best_so_far / target * bar_w), bar_w)
            bar = "█" * fill + "░" * (bar_w - fill)

            lines = [
                f"  Part 1: Sieving elves (10 presents each)",
                f"  Target: {target:>12,}",
                "",
                f"  Elf {elf:>8,} / {limit:,}",
                f"  Best house so far: {best_so_far:>12,} presents",
                f"  [{bar}]",
            ]

            if answer1 and elf >= answer1:
                lines.append("")
                lines.append(f"  ★ Part 1: House {answer1}")
                yield {"type": "text", "lines": lines, "delay": 400}
                break
            else:
                yield {"type": "text", "lines": lines, "delay": 80}

    # Part 2 sieve
    houses2 = [0] * (limit + 1)
    answer2 = None

    for elf in range(1, limit + 1):
        stop = min(elf * 50, limit)
        for house in range(elf, stop + 1, elf):
            houses2[house] += elf * 11

        if answer2 is None and houses2[elf] >= target:
            answer2 = elf

        if elf % sample_step == 0 or elf == answer2:
            best_so_far = max(houses2[1:elf + 1]) if elf > 0 else 0
            bar_w = 40
            fill = min(round(best_so_far / target * bar_w), bar_w)
            bar = "█" * fill + "░" * (bar_w - fill)

            lines = [
                f"  Part 2: Sieving elves (11 presents, max 50 houses)",
                f"  Target: {target:>12,}",
                "",
                f"  Elf {elf:>8,} / {limit:,}",
                f"  Best house so far: {best_so_far:>12,} presents",
                f"  [{bar}]",
            ]

            if answer2 and elf >= answer2:
                lines.append("")
                lines.append(f"  ★ Part 2: House {answer2}")
                yield {"type": "text", "lines": lines, "delay": 400}
                break
            else:
                yield {"type": "text", "lines": lines, "delay": 80}
