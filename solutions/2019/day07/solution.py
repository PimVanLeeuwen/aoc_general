"""
Day 7 - Amplification Circuit
Year: 2019

Find the phase setting permutation that maximizes thruster signal,
first in series mode, then in a feedback loop.
"""

from itertools import permutations
from intcode import IntcodeComputer


def run_series(program, phases):
    """Run 5 amplifiers in series, return final output signal."""
    signal = 0
    for phase in phases:
        cpu = IntcodeComputer(program, inputs=[phase, signal])
        cpu.run()
        signal = cpu.outputs[-1]
    return signal


def run_feedback(program, phases):
    """Run 5 amplifiers in a feedback loop until all halt."""
    amps = [IntcodeComputer(program, inputs=[phase]) for phase in phases]

    signal = 0
    while True:
        for i, amp in enumerate(amps):
            amp.add_input(signal)
            amp.run_until_block()
            signal = amp.outputs[-1]

        if amps[-1].halted:
            return signal


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    program = [int(x) for x in puzzle_input.strip().split(",")]

    part1 = max(run_series(program, p) for p in permutations(range(5)))
    part2 = max(run_feedback(program, p) for p in permutations(range(5, 10)))

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    """Yield frames showing the amplifier optimization search."""
    program = [int(x) for x in puzzle_input.strip().split(",")]

    yield {
        "type": "text",
        "lines": [
            "  Amplification Circuit",
            "",
            "  Part 1: Series mode (phases 0-4)",
            "  Part 2: Feedback loop (phases 5-9)",
            "",
            "  Testing all 120 permutations each...",
        ],
        "delay": 600,
    }

    # Part 1
    best_signal_1 = 0
    best_phases_1 = None
    for phases in permutations(range(5)):
        signal = run_series(program, phases)
        if signal > best_signal_1:
            best_signal_1 = signal
            best_phases_1 = phases

    yield {
        "type": "text",
        "lines": [
            "  Part 1: Series mode",
            "",
            f"  0 -> [A] -> [B] -> [C] -> [D] -> [E] -> {best_signal_1}",
            f"  Best phases: {list(best_phases_1)}",
            f"  Max signal: {best_signal_1}",
        ],
        "delay": 600,
    }

    # Part 2
    best_signal_2 = 0
    best_phases_2 = None
    best_loops = 0
    for phases in permutations(range(5, 10)):
        amps = [IntcodeComputer(program, inputs=[phase]) for phase in phases]
        signal = 0
        loops = 0
        while True:
            for amp in amps:
                amp.add_input(signal)
                amp.run_until_block()
                signal = amp.outputs[-1]
            loops += 1
            if amps[-1].halted:
                break
        if signal > best_signal_2:
            best_signal_2 = signal
            best_phases_2 = phases
            best_loops = loops

    yield {
        "type": "text",
        "lines": [
            "  Part 2: Feedback loop mode",
            "",
            "  0 -+-> [A] -> [B] -> [C] -> [D] -> [E] -+--> thrusters",
            "     |                                      |",
            "     +--------------------------------------+",
            "",
            f"  Best phases: {list(best_phases_2)}",
            f"  Feedback loops: {best_loops}",
            f"  Max signal: {best_signal_2}",
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
            f"  Part 1: {best_signal_1}",
            f"  Part 2: {best_signal_2}",
        ],
        "delay": 500,
    }
