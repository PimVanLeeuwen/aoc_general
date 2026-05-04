"""
Day 19 - Medicine for Rudolph
Year: 2015

Calibrate a molecule machine: count distinct single-step products,
then find the minimum steps to synthesize the target molecule from 'e'.
"""

import re
from random import shuffle


def parse(puzzle_input):
    parts = puzzle_input.strip().split("\n\n")
    rules = []
    for line in parts[0].split("\n"):
        src, dst = line.split(" => ")
        rules.append((src, dst))
    molecule = parts[1].strip()
    return rules, molecule


def one_step_products(rules, molecule):
    """All distinct molecules reachable in one replacement."""
    results = set()
    for src, dst in rules:
        start = 0
        while True:
            idx = molecule.find(src, start)
            if idx == -1:
                break
            new = molecule[:idx] + dst + molecule[idx + len(src):]
            results.add(new)
            start = idx + 1
    return results


def find_steps_to_e(rules, molecule):
    """Reduce molecule back to 'e' using greedy reverse replacements.
    Shuffle rule order and retry if stuck — works reliably for AoC inputs."""
    reverse_rules = [(dst, src) for src, dst in rules]

    for _ in range(100):
        mol = molecule
        steps = 0
        shuffle(reverse_rules)
        while mol != "e":
            replaced = False
            for dst, src in reverse_rules:
                while dst in mol:
                    mol = mol.replace(dst, src, 1)
                    steps += 1
                    replaced = True
            if not replaced:
                break
        if mol == "e":
            return steps
    return -1


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    rules, molecule = parse(puzzle_input)

    part1 = len(one_step_products(rules, molecule))
    part2 = find_steps_to_e(rules, molecule)

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    """Yield frames showing the molecule reduction process."""
    rules, molecule = parse(puzzle_input)
    reverse_rules = [(dst, src) for src, dst in rules]

    # Part 1 frame
    products = one_step_products(rules, molecule)
    yield {
        "type": "text",
        "lines": [
            "  Part 1: Single-step calibration",
            "",
            f"  Starting molecule length: {len(molecule)}",
            f"  Replacement rules: {len(rules)}",
            f"  Distinct products: {len(products)}",
        ],
        "delay": 400,
    }

    # Part 2: show reduction
    from random import shuffle as shuf
    shuf(reverse_rules)

    mol = molecule
    steps = 0
    max_len = len(mol)
    frames_data = []

    while mol != "e":
        replaced = False
        for dst, src in reverse_rules:
            while dst in mol:
                mol = mol.replace(dst, src, 1)
                steps += 1
                replaced = True
                if steps <= 30 or steps % 10 == 0 or len(mol) < 50:
                    frames_data.append((steps, len(mol), mol))
        if not replaced:
            break

    if mol == "e":
        frames_data.append((steps, 1, "e"))

    # Emit sampled frames
    step_size = max(1, len(frames_data) // 60)
    shown = frames_data[::step_size]
    if frames_data[-1] not in shown:
        shown.append(frames_data[-1])

    for s, length, current in shown:
        bar_w = 50
        fill = round((1 - length / max_len) * bar_w)
        bar = "█" * fill + "░" * (bar_w - fill)

        display = current if len(current) <= 70 else current[:67] + "..."

        lines = [
            f"  Part 2: Reducing molecule to 'e'",
            "",
            f"  Step {s:>4d}  |  Length: {length:>4d} / {max_len}",
            f"  [{bar}]",
            "",
            f"  {display}",
        ]

        is_last = current == "e"
        if is_last:
            lines.append("")
            lines.append(f"  ★ Part 1: {len(products)} distinct molecules")
            lines.append(f"  ★ Part 2: {s} steps to reach 'e'")

        yield {"type": "text", "lines": lines, "delay": 500 if is_last else 80}
