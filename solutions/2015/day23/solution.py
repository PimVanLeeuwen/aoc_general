"""
Day 23 - Opening the Turing Lock
Year: 2015

Simulate a simple two-register computer with six instructions.
"""


def parse_program(text):
    """Parse instructions into (opcode, args) tuples."""
    program = []
    for line in text.strip().splitlines():
        parts = line.replace(",", "").split()
        op = parts[0]
        args = parts[1:]
        program.append((op, args))
    return program


def run(program, registers):
    """Execute program, return registers when PC goes out of bounds."""
    pc = 0
    while 0 <= pc < len(program):
        op, args = program[pc]
        if op == "hlf":
            registers[args[0]] //= 2
            pc += 1
        elif op == "tpl":
            registers[args[0]] *= 3
            pc += 1
        elif op == "inc":
            registers[args[0]] += 1
            pc += 1
        elif op == "jmp":
            pc += int(args[0])
        elif op == "jie":
            pc += int(args[1]) if registers[args[0]] % 2 == 0 else 1
        elif op == "jio":
            pc += int(args[1]) if registers[args[0]] == 1 else 1
    return registers


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    program = parse_program(puzzle_input)

    regs1 = run(program, {"a": 0, "b": 0})
    part1 = regs1["b"]

    regs2 = run(program, {"a": 1, "b": 0})
    part2 = regs2["b"]

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    """Yield frames showing the computer executing step by step."""
    program = parse_program(puzzle_input)
    source_lines = puzzle_input.strip().splitlines()

    for initial_a, label in [(0, "Part 1 (a=0)"), (1, "Part 2 (a=1)")]:
        registers = {"a": initial_a, "b": 0}
        pc = 0
        steps = 0
        step_interval = 1

        yield {
            "type": "text",
            "lines": [
                f"  === {label} ===",
                "",
                f"  Program: {len(program)} instructions",
                f"  Registers: a={registers['a']}, b={registers['b']}",
            ],
            "delay": 600,
        }

        while 0 <= pc < len(program):
            op, args = program[pc]
            old_pc = pc

            if op == "hlf":
                registers[args[0]] //= 2
                pc += 1
            elif op == "tpl":
                registers[args[0]] *= 3
                pc += 1
            elif op == "inc":
                registers[args[0]] += 1
                pc += 1
            elif op == "jmp":
                pc += int(args[0])
            elif op == "jie":
                pc += int(args[1]) if registers[args[0]] % 2 == 0 else 1
            elif op == "jio":
                pc += int(args[1]) if registers[args[0]] == 1 else 1

            steps += 1

            # Adaptive frame rate: show more at start, less as it speeds up
            if steps <= 20 or steps % step_interval == 0:
                # Build a window of source lines around current PC
                window_start = max(0, old_pc - 2)
                window_end = min(len(source_lines), old_pc + 5)
                code_lines = []
                for i in range(window_start, window_end):
                    marker = " >> " if i == old_pc else "    "
                    code_lines.append(f"  {marker}{i:2d}: {source_lines[i]}")

                lines = [
                    f"  === {label} — Step {steps} ===",
                    "",
                ] + code_lines + [
                    "",
                    f"  Registers:  a = {registers['a']:<12,}  b = {registers['b']:<12,}",
                    f"  PC: {old_pc} -> {pc}",
                ]

                delay = 150 if steps <= 20 else 40
                yield {"type": "text", "lines": lines, "delay": delay}

            if steps == 20:
                step_interval = 5
            if steps == 100:
                step_interval = 50
            if steps == 500:
                step_interval = 200

        yield {
            "type": "text",
            "lines": [
                f"  === {label} — Complete ===",
                "",
                f"  Total steps: {steps:,}",
                f"  Final registers:  a = {registers['a']:,}  b = {registers['b']:,}",
                "",
                f"  Answer: b = {registers['b']}",
            ],
            "delay": 800,
        }