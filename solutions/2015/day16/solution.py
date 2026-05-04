"""
Day 16 - Aunt Sue
Year: 2015

Identify which Aunt Sue matches the MFCSAM readings.
"""

import re

READINGS = {
    "children": 3, "cats": 7, "samoyeds": 2, "pomeranians": 3,
    "akitas": 0, "vizslas": 0, "goldfish": 5, "trees": 3,
    "cars": 2, "perfumes": 1,
}


def parse(puzzle_input):
    sues = {}
    for line in puzzle_input.strip().split("\n"):
        m = re.match(r"Sue (\d+): (.+)", line)
        num = int(m.group(1))
        props = {}
        for pair in m.group(2).split(", "):
            key, val = pair.split(": ")
            props[key] = int(val)
        sues[num] = props
    return sues


def matches_exact(props):
    return all(READINGS[k] == v for k, v in props.items())


def matches_ranges(props):
    for k, v in props.items():
        if k in ("cats", "trees"):
            if v <= READINGS[k]:
                return False
        elif k in ("pomeranians", "goldfish"):
            if v >= READINGS[k]:
                return False
        elif READINGS[k] != v:
            return False
    return True


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    sues = parse(puzzle_input)

    part1 = next(num for num, props in sues.items() if matches_exact(props))
    part2 = next(num for num, props in sues.items() if matches_ranges(props))

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    """Yield frames showing the process of elimination."""
    sues = parse(puzzle_input)
    all_nums = sorted(sues.keys())

    # Part 1: eliminate Sues one property at a time
    prop_names = list(READINGS.keys())
    remaining_p1 = set(all_nums)
    remaining_p2 = set(all_nums)

    for prop in prop_names:
        expected = READINGS[prop]

        eliminated_p1 = set()
        for num in remaining_p1:
            if prop in sues[num] and sues[num][prop] != expected:
                eliminated_p1.add(num)
        remaining_p1 -= eliminated_p1

        eliminated_p2 = set()
        for num in remaining_p2:
            if prop not in sues[num]:
                continue
            val = sues[num][prop]
            if prop in ("cats", "trees"):
                if val <= expected:
                    eliminated_p2.add(num)
            elif prop in ("pomeranians", "goldfish"):
                if val >= expected:
                    eliminated_p2.add(num)
            elif val != expected:
                eliminated_p2.add(num)
        remaining_p2 -= eliminated_p2

        lines = [
            f"  MFCSAM Analysis — Filtering by: {prop}",
            f"  Expected: {prop} = {expected}",
            "",
            f"  Part 1 (exact match):",
            f"    Eliminated: {len(eliminated_p1):>3d}   Remaining: {len(remaining_p1):>3d} / {len(all_nums)}",
            f"  Part 2 (range match):",
            f"    Eliminated: {len(eliminated_p2):>3d}   Remaining: {len(remaining_p2):>3d} / {len(all_nums)}",
            "",
        ]

        bar_w = 50
        fill1 = round(len(remaining_p1) / len(all_nums) * bar_w)
        fill2 = round(len(remaining_p2) / len(all_nums) * bar_w)
        lines.append(f"  P1: [{'█' * fill1}{'░' * (bar_w - fill1)}]")
        lines.append(f"  P2: [{'█' * fill2}{'░' * (bar_w - fill2)}]")

        if len(remaining_p1) <= 5:
            lines.append(f"\n  P1 candidates: {', '.join(f'Sue {n}' for n in sorted(remaining_p1))}")
        if len(remaining_p2) <= 5:
            lines.append(f"  P2 candidates: {', '.join(f'Sue {n}' for n in sorted(remaining_p2))}")

        yield {"type": "text", "lines": lines, "delay": 300}

    # Final frame
    p1 = next(iter(remaining_p1))
    p2 = next(iter(remaining_p2))
    lines = [
        "  MFCSAM Analysis Complete!",
        "",
        f"  ★ Part 1: Sue {p1}",
    ]
    for k, v in sues[p1].items():
        lines.append(f"      {k}: {v} (expected {READINGS[k]})")

    lines.append(f"\n  ★ Part 2: Sue {p2}")
    for k, v in sues[p2].items():
        exp = READINGS[k]
        if k in ("cats", "trees"):
            lines.append(f"      {k}: {v} (> {exp})")
        elif k in ("pomeranians", "goldfish"):
            lines.append(f"      {k}: {v} (< {exp})")
        else:
            lines.append(f"      {k}: {v} (= {exp})")

    yield {"type": "text", "lines": lines, "delay": 500}