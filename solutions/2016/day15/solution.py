"""
Day 15 - Timing is Everything
Year: 2016

Find the earliest button-press time so a falling capsule passes through every
spinning disc's slot simultaneously.
"""

import re


def parse(puzzle_input):
    discs = []
    for line in puzzle_input.strip().splitlines():
        nums = list(map(int, re.findall(r"\d+", line)))
        # nums: [disc_number, positions, 0, start_pos]
        discs.append((nums[1], nums[3]))  # (positions, start)
    return discs


def first_pass(discs):
    """Return the earliest t where (start + t + depth) % positions == 0 for all discs."""
    t = 0
    step = 1
    for depth, (positions, start) in enumerate(discs, start=1):
        while (start + t + depth) % positions != 0:
            t += step
        step *= positions  # lcm shortcut: all sizes are coprime in AoC inputs
    return t


def solve(puzzle_input: str) -> tuple[str, str]:
    discs = parse(puzzle_input)

    part1 = first_pass(discs)
    part2 = first_pass(discs + [(11, 0)])

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    """Animate the discs spinning and the capsule falling at the solution time."""
    discs = parse(puzzle_input)
    t_solution = first_pass(discs)

    num_discs = len(discs)
    # Show the discs ticking from t=0 up to the solution, then the winning drop
    frames_before = min(t_solution, 60)
    show_times = list(range(frames_before)) + [t_solution]

    for t in show_times:
        lines = [f"  Button pressed at t = {t}", ""]
        all_pass = True
        for i, (positions, start) in enumerate(discs, start=1):
            pos = (start + t + i) % positions
            slot_char = "O" if pos == 0 else str(pos)
            indicator = " <-- PASS" if pos == 0 else ""
            if pos != 0:
                all_pass = False
            # Draw a simple disc: [...pos...]
            disc_str = ""
            for p in range(positions):
                if p == pos:
                    disc_str += "[*]"
                elif p == 0:
                    disc_str += "[ ]"
                else:
                    disc_str += "---"
            lines.append(f"  Disc {i} (size {positions:>2}): {disc_str}  pos={pos}{indicator}")

        lines.append("")
        if t == t_solution:
            lines.append("  >> CAPSULE FALLS THROUGH! <<")
        else:
            lines.append("  (capsule would be blocked)")

        yield {
            "type": "text",
            "lines": lines,
            "delay": 120 if t != t_solution else 1000,
        }
