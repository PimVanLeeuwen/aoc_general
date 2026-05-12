"""
Day 5 - Sunny with a Chance of Asteroids
Year: 2019

Extend the Intcode computer with parameter modes, I/O, comparisons,
and conditional jumps, then run the TEST diagnostic program.
"""

from intcode import IntcodeComputer


def run_diagnostic(program, system_id):
    """Run the TEST program with a given system ID, return the diagnostic code."""
    cpu = IntcodeComputer(program, inputs=[system_id])
    cpu.run()
    return cpu.outputs[-1]


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    program = [int(x) for x in puzzle_input.strip().split(",")]

    part1 = run_diagnostic(program, 1)
    part2 = run_diagnostic(program, 5)

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    """Yield frames showing the diagnostic test runs."""
    program = [int(x) for x in puzzle_input.strip().split(",")]

    for system_id, label in [(1, "Air Conditioner"), (5, "Thermal Radiator")]:
        cpu = IntcodeComputer(program, inputs=[system_id])
        cpu.run()

        diagnostics = cpu.outputs[:-1]
        final_code = cpu.outputs[-1]

        lines = [
            f"  TEST Diagnostic — System ID {system_id} ({label})",
            "",
        ]

        if diagnostics:
            passed = sum(1 for d in diagnostics if d == 0)
            failed = sum(1 for d in diagnostics if d != 0)
            lines.append(f"  Diagnostic tests: {len(diagnostics)}")
            lines.append(f"  Passed: {passed}  Failed: {failed}")
            if failed:
                lines.append(f"  Failed outputs: {[d for d in diagnostics if d != 0]}")
            lines.append("")

        lines.append(f"  Diagnostic code: {final_code}")

        yield {"type": "text", "lines": lines, "delay": 600}

    yield {
        "type": "text",
        "lines": [
            "  ===================================",
            "  Results",
            "  ===================================",
            "",
            f"  Part 1 (AC, ID=1):  {run_diagnostic(program, 1)}",
            f"  Part 2 (TR, ID=5):  {run_diagnostic(program, 5)}",
        ],
        "delay": 500,
    }
