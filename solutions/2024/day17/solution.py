"""
Day 17 - Chronospatial Computer
Year: 2024

Simulate a 3-bit computer with 3 registers and 8 opcodes.
Part 2 finds the register A value that makes the program output itself.
"""

import re


def combo(operand, a, b, c):
    if operand <= 3:
        return operand
    if operand == 4:
        return a
    if operand == 5:
        return b
    if operand == 6:
        return c
    raise ValueError(f"Invalid combo operand: {operand}")


def run_program(a, b, c, program):
    output = []
    ip = 0

    while ip < len(program) - 1:
        opcode = program[ip]
        operand = program[ip + 1]

        if opcode == 0:  # adv
            a = a >> combo(operand, a, b, c)
        elif opcode == 1:  # bxl
            b = b ^ operand
        elif opcode == 2:  # bst
            b = combo(operand, a, b, c) % 8
        elif opcode == 3:  # jnz
            if a != 0:
                ip = operand
                continue
        elif opcode == 4:  # bxc
            b = b ^ c
        elif opcode == 5:  # out
            output.append(combo(operand, a, b, c) % 8)
        elif opcode == 6:  # bdv
            b = a >> combo(operand, a, b, c)
        elif opcode == 7:  # cdv
            c = a >> combo(operand, a, b, c)

        ip += 2

    return output


def find_quine(program, b_init, c_init):
    """Find the smallest A that makes the program output itself.

    The program divides A by 8 each iteration (right-shift by 3 bits),
    so we build A recursively from the last output digit backwards,
    trying each 3-bit value (0-7) for each position.
    """
    def search(target_idx, a_so_far):
        if target_idx < 0:
            return a_so_far

        for bits in range(8):
            candidate = (a_so_far << 3) | bits
            if candidate == 0 and target_idx == 0:
                # A=0 would halt before producing output
                continue
            output = run_program(candidate, b_init, c_init, program)
            if output and output[0] == program[target_idx]:
                result = search(target_idx - 1, candidate)
                if result is not None:
                    return result
        return None

    return search(len(program) - 1, 0)


def solve(puzzle_input: str) -> tuple[str, str]:
    nums = list(map(int, re.findall(r"\d+", puzzle_input)))
    a, b, c = nums[0], nums[1], nums[2]
    program = nums[3:]

    # Part 1: run the program
    output = run_program(a, b, c, program)
    part1 = ",".join(str(x) for x in output)

    # Part 2: find A that produces a quine
    part2 = find_quine(program, b, c)

    return part1, str(part2)


def visualize(puzzle_input: str):
    nums = list(map(int, re.findall(r"\d+", puzzle_input)))
    a, b, c = nums[0], nums[1], nums[2]
    program = nums[3:]

    yield {
        "type": "text",
        "lines": [
            "  Chronospatial Computer",
            "",
            f"  Register A: {a}",
            f"  Register B: {b}",
            f"  Register C: {c}",
            f"  Program: {program}",
            f"  Program length: {len(program)} instructions",
        ],
        "delay": 600,
    }

    part1, part2 = solve(puzzle_input)

    yield {
        "type": "text",
        "lines": [
            "  ===================================",
            "  Results",
            "  ===================================",
            "",
            f"  Part 1: {part1}",
            f"  Part 2: {part2}",
        ],
        "delay": 500,
    }
