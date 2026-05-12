"""
Day 2 - 1202 Program Alarm
Year: 2019

Run an Intcode program, then brute-force the noun/verb pair that
produces a target output.
"""

from intcode import IntcodeComputer


def run_with(program, noun, verb):
    """Run program with given noun/verb, return value at address 0."""
    cpu = IntcodeComputer(program)
    cpu.memory[1] = noun
    cpu.memory[2] = verb
    cpu.run()
    return cpu.memory[0]


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    program = [int(x) for x in puzzle_input.strip().split(",")]

    part1 = run_with(program, 12, 2)

    part2 = 0
    for noun in range(100):
        for verb in range(100):
            if run_with(program, noun, verb) == 19690720:
                part2 = 100 * noun + verb
                break

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    """Yield frames showing Intcode execution and the noun/verb search."""
    program = [int(x) for x in puzzle_input.strip().split(",")]

    # Show program info
    yield {
        "type": "text",
        "lines": [
            "  1202 Program Alarm",
            "",
            f"  Program length: {len(program)} integers",
            f"  Opcodes: 1 (ADD), 2 (MUL), 99 (HALT)",
        ],
        "delay": 600,
    }

    # Part 1: step through execution
    cpu = IntcodeComputer(program)
    cpu.memory[1] = 12
    cpu.memory[2] = 2
    steps = 0

    while not cpu.halted:
        old_pc = cpu.pc
        op = cpu.memory[cpu.pc]

        if steps < 10:
            if op in (1, 2):
                a, b, c = cpu.memory[cpu.pc + 1 : cpu.pc + 4]
                op_name = "ADD" if op == 1 else "MUL"
                result = cpu.memory[a] + cpu.memory[b] if op == 1 else cpu.memory[a] * cpu.memory[b]
                yield {
                    "type": "text",
                    "lines": [
                        f"  Part 1: noun=12, verb=2",
                        "",
                        f"  Step {steps + 1} @ PC={old_pc}:",
                        f"  {op_name} mem[{a}]({cpu.memory[a]}) {'+'if op==1 else '*'} mem[{b}]({cpu.memory[b]}) -> mem[{c}] = {result}",
                    ],
                    "delay": 200,
                }

        cpu.step()
        steps += 1

    yield {
        "type": "text",
        "lines": [
            f"  Part 1: HALT after {steps} steps",
            f"  mem[0] = {cpu.memory[0]}",
        ],
        "delay": 500,
    }

    # Part 2: search for target output
    target = 19690720
    found_noun, found_verb = 0, 0
    checked = 0

    for noun in range(100):
        for verb in range(100):
            result = run_with(program, noun, verb)
            checked += 1
            if result == target:
                found_noun, found_verb = noun, verb
                break
        else:
            if checked % 500 == 0:
                yield {
                    "type": "text",
                    "lines": [
                        f"  Part 2: searching for output {target:,}",
                        "",
                        f"  Checked {checked:,} / 10,000 pairs",
                        f"  Current: noun={noun}, verb={verb}",
                    ],
                    "delay": 40,
                }
            continue
        break

    yield {
        "type": "text",
        "lines": [
            "  ===================================",
            "  Results",
            "  ===================================",
            "",
            f"  Part 1: {run_with(program, 12, 2)}",
            f"  Part 2: noun={found_noun}, verb={found_verb}",
            f"          100 * {found_noun} + {found_verb} = {100 * found_noun + found_verb}",
        ],
        "delay": 500,
    }
