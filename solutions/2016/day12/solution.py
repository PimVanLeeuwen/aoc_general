"""
Day 12 - Leonardo's Monorail
Year: 2016

Execute assembunny code on four registers and report register a's final value.
"""


def parse(puzzle_input):
    return [line.split() for line in puzzle_input.strip().splitlines()]


def run(instructions, registers):
    ip = 0
    while 0 <= ip < len(instructions):
        op, *args = instructions[ip]

        def val(x, regs=registers):
            return regs[x] if x in regs else int(x)

        if op == "cpy":
            registers[args[1]] = val(args[0])
        elif op == "inc":
            registers[args[0]] += 1
        elif op == "dec":
            registers[args[0]] -= 1
        elif op == "jnz":
            if val(args[0]) != 0:
                ip += val(args[1])
                continue
        ip += 1
    return registers


def solve(puzzle_input: str) -> tuple[str, str]:
    instructions = parse(puzzle_input)

    part1 = run(instructions, {"a": 0, "b": 0, "c": 0, "d": 0})["a"]
    part2 = run(instructions, {"a": 0, "b": 0, "c": 1, "d": 0})["a"]

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    """Step through the assembunny program showing the instruction pointer and registers."""
    instructions = parse(puzzle_input)
    registers = {"a": 0, "b": 0, "c": 0, "d": 0}
    ip = 0
    step = 0
    max_steps = 400

    while 0 <= ip < len(instructions) and step < max_steps:
        op, *args = instructions[ip]

        def val(x, regs=registers):
            return regs[x] if x in regs else int(x)

        lines = []
        for i, instr in enumerate(instructions):
            prefix = ">>>" if i == ip else "   "
            lines.append(f"  {prefix} {' '.join(instr)}")

        lines.append("")
        lines.append(f"  Step: {step:>6}    ip: {ip}")
        lines.append(
            f"  a={registers['a']:>8}  b={registers['b']:>8}"
            f"  c={registers['c']:>8}  d={registers['d']:>8}"
        )

        yield {"type": "text", "lines": lines, "delay": 80}

        if op == "cpy":
            registers[args[1]] = val(args[0])
        elif op == "inc":
            registers[args[0]] += 1
        elif op == "dec":
            registers[args[0]] -= 1
        elif op == "jnz":
            if val(args[0]) != 0:
                ip += val(args[1])
                step += 1
                continue
        ip += 1
        step += 1

    yield {
        "type": "text",
        "lines": [
            f"  Halted after {step} steps (visualization capped at {max_steps}).",
            "",
            f"  a={registers['a']}  b={registers['b']}"
            f"  c={registers['c']}  d={registers['d']}",
        ],
        "delay": 500,
    }
