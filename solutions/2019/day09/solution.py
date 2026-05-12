"""
Day 9 - Sensor Boost
Year: 2019

Complete the Intcode computer with relative mode and extensible memory,
then run the BOOST diagnostic and sensor boost programs.
"""

from intcode import IntcodeComputer


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    program = [int(x) for x in puzzle_input.strip().split(",")]

    cpu1 = IntcodeComputer(program, inputs=[1])
    cpu1.run()
    part1 = cpu1.outputs[-1]

    cpu2 = IntcodeComputer(program, inputs=[2])
    cpu2.run()
    part2 = cpu2.outputs[-1]

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    """Yield frames showing BOOST test and sensor boost execution."""
    program = [int(x) for x in puzzle_input.strip().split(",")]

    yield {
        "type": "text",
        "lines": [
            "  BOOST — Basic Operation Of System Test",
            "",
            f"  Program size: {len(program)} instructions",
            "",
            "  New Intcode features:",
            "    - Relative parameter mode (mode 2)",
            "    - Opcode 9: adjust relative base",
            "    - Extensible memory (auto-grows)",
            "    - Large number support",
        ],
        "delay": 800,
    }

    # Part 1: test mode
    cpu1 = IntcodeComputer(program, inputs=[1])
    cpu1.run()

    diagnostics = cpu1.outputs[:-1] if len(cpu1.outputs) > 1 else []
    keycode = cpu1.outputs[-1]

    lines = [
        "  Mode 1: Diagnostic test",
        "",
    ]
    if diagnostics:
        failed = [d for d in diagnostics if d != 0]
        lines.append(f"  Diagnostic outputs: {len(diagnostics)}")
        if failed:
            lines.append(f"  FAILED opcodes: {failed}")
        else:
            lines.append(f"  All checks passed")
        lines.append("")
    lines.append(f"  BOOST keycode: {keycode}")
    lines.append(f"  Memory used: {len(cpu1.memory):,} cells")

    yield {"type": "text", "lines": lines, "delay": 600}

    # Part 2: sensor boost
    cpu2 = IntcodeComputer(program, inputs=[2])
    cpu2.run()
    coords = cpu2.outputs[-1]

    yield {
        "type": "text",
        "lines": [
            "  Mode 2: Sensor boost",
            "",
            f"  Distress signal coordinates: {coords}",
            f"  Memory used: {len(cpu2.memory):,} cells",
        ],
        "delay": 600,
    }

    yield {
        "type": "text",
        "lines": [
            "  ===================================",
            "  Results",
            "  ===================================",
            "",
            f"  Part 1 (BOOST keycode): {keycode}",
            f"  Part 2 (coordinates):   {coords}",
            "",
            "  Intcode computer: COMPLETE",
        ],
        "delay": 500,
    }
