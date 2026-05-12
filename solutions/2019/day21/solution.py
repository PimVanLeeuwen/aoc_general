"""
Day 21 - Springdroid Adventure
Year: 2019

Program a springdroid with boolean logic to jump over holes in the hull.
The droid jumps 4 tiles and must avoid falling into gaps.
"""

from intcode import IntcodeComputer


def run_springscript(program, script):
    """Run a springscript program on the Intcode computer, return damage value or None."""
    cpu = IntcodeComputer(program)
    # Feed the script as ASCII input
    for ch in script:
        cpu.inputs.append(ord(ch))
    cpu.run()

    # If the last output is outside ASCII range, it's the damage value
    if cpu.outputs and cpu.outputs[-1] > 127:
        return cpu.outputs[-1]
    return None


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    program = [int(x) for x in puzzle_input.strip().split(",")]

    # Part 1: WALK mode (sensors A-D)
    # Jump if any of the next 3 tiles is a hole AND landing tile D is ground
    # J = (!A || !B || !C) && D
    walk_script = "\n".join([
        "NOT A J",   # J = !A
        "NOT B T",   # T = !B
        "OR T J",    # J = !A || !B
        "NOT C T",   # T = !C
        "OR T J",    # J = !A || !B || !C
        "AND D J",   # J = (!A || !B || !C) && D
        "WALK",
    ]) + "\n"

    part1 = run_springscript(program, walk_script)

    # Part 2: RUN mode (sensors A-I)
    # Same base logic, but also ensure we can proceed after landing:
    # after jumping to D, we need either E (walk) or H (jump again) to be ground
    # J = (!A || !B || !C) && D && (E || H)
    run_script = "\n".join([
        "NOT A J",   # J = !A
        "NOT B T",   # T = !B
        "OR T J",    # J = !A || !B
        "NOT C T",   # T = !C
        "OR T J",    # J = !A || !B || !C
        "AND D J",   # J = (!A || !B || !C) && D
        "NOT E T",   # T = !E
        "NOT T T",   # T = E
        "OR H T",    # T = E || H
        "AND T J",   # J = ... && (E || H)
        "RUN",
    ]) + "\n"

    part2 = run_springscript(program, run_script)

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    """Yield frames showing the springdroid programming."""
    program = [int(x) for x in puzzle_input.strip().split(",")]

    yield {
        "type": "text",
        "lines": [
            "  Springdroid Adventure",
            "",
            "  The springdroid jumps exactly 4 tiles forward.",
            "  Sensors detect ground at distances A(1) through D(4).",
            "  Program boolean logic to decide when to jump.",
        ],
        "delay": 800,
    }

    # Part 1
    walk_script = "\n".join([
        "NOT A J", "NOT B T", "OR T J",
        "NOT C T", "OR T J", "AND D J", "WALK",
    ]) + "\n"

    yield {
        "type": "text",
        "lines": [
            "  Part 1 — WALK mode (sensors A-D)",
            "",
            "  Logic: jump if hole in next 3 AND D is ground",
            "  J = (!A || !B || !C) && D",
            "",
            "  Springscript (6 instructions):",
            "    NOT A J",
            "    NOT B T",
            "    OR  T J",
            "    NOT C T",
            "    OR  T J",
            "    AND D J",
        ],
        "delay": 600,
    }

    part1 = run_springscript(program, walk_script)

    # Part 2
    run_script = "\n".join([
        "NOT A J", "NOT B T", "OR T J",
        "NOT C T", "OR T J", "AND D J",
        "NOT E T", "NOT T T", "OR H T", "AND T J", "RUN",
    ]) + "\n"

    yield {
        "type": "text",
        "lines": [
            "  Part 2 — RUN mode (sensors A-I)",
            "",
            "  Extra check: after landing on D, ensure",
            "  we can walk (E) or jump again (H).",
            "  J = (!A || !B || !C) && D && (E || H)",
            "",
            "  Springscript (10 instructions):",
            "    NOT A J    NOT E T",
            "    NOT B T    NOT T T",
            "    OR  T J    OR  H T",
            "    NOT C T    AND T J",
            "    OR  T J",
            "    AND D J",
        ],
        "delay": 600,
    }

    part2 = run_springscript(program, run_script)

    yield {
        "type": "text",
        "lines": [
            "  ===================================",
            "  Results",
            "  ===================================",
            "",
            f"  Part 1: {part1} (hull damage, WALK)",
            f"  Part 2: {part2} (hull damage, RUN)",
        ],
        "delay": 500,
    }
