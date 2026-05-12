"""
Day 8 - Handheld Halting
Year: 2020

Simulate a simple VM with acc/jmp/nop instructions. Detect infinite loops
and fix the program by swapping one jmp/nop instruction.
"""


def parse_program(text):
    """Parse instructions into a list of (op, arg) tuples."""
    instructions = []
    for line in text.strip().split("\n"):
        op, arg = line.split()
        instructions.append((op, int(arg)))
    return instructions


def run(instructions):
    """Execute the program. Returns (terminated, accumulator).

    terminated is True if the program exits normally (pc reaches end),
    False if an infinite loop is detected.
    """
    seen = set()
    pc = acc = 0
    while pc < len(instructions):
        if pc in seen:
            return False, acc
        seen.add(pc)
        op, arg = instructions[pc]
        if op == "acc":
            acc += arg
            pc += 1
        elif op == "jmp":
            pc += arg
        else:
            pc += 1
    return True, acc


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    instructions = parse_program(puzzle_input)

    # Part 1: accumulator value when the loop is first detected
    _, part1 = run(instructions)

    # Part 2: swap exactly one jmp<->nop to make the program terminate
    part2 = 0
    for i, (op, arg) in enumerate(instructions):
        if op == "acc":
            continue
        modified = list(instructions)
        modified[i] = ("nop" if op == "jmp" else "jmp", arg)
        terminated, acc = run(modified)
        if terminated:
            part2 = acc
            break

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    """Yield frames showing the program execution and fix."""
    instructions = parse_program(puzzle_input)

    _, part1 = run(instructions)

    yield {
        "type": "text",
        "lines": [
            "  Handheld Halting",
            "",
            f"  Program: {len(instructions)} instructions",
            f"  acc: {sum(1 for op, _ in instructions if op == 'acc')}",
            f"  jmp: {sum(1 for op, _ in instructions if op == 'jmp')}",
            f"  nop: {sum(1 for op, _ in instructions if op == 'nop')}",
        ],
        "delay": 600,
    }

    fix_idx = 0
    part2 = 0
    for i, (op, arg) in enumerate(instructions):
        if op == "acc":
            continue
        modified = list(instructions)
        modified[i] = ("nop" if op == "jmp" else "jmp", arg)
        terminated, acc = run(modified)
        if terminated:
            fix_idx = i
            part2 = acc
            break

    yield {
        "type": "text",
        "lines": [
            "  ===================================",
            "  Results",
            "  ===================================",
            "",
            f"  Part 1: {part1} (acc at loop detection)",
            f"  Part 2: {part2} (fixed instruction {fix_idx}:",
            f"          {instructions[fix_idx][0]} -> {'nop' if instructions[fix_idx][0] == 'jmp' else 'jmp'})",
        ],
        "delay": 500,
    }
