"""
Day 23 - Safe Cracking
Year: 2016

Extended assembunny interpreter with the 'tgl' instruction, plus a
multiplication-loop optimizer to handle the factorial computation in part 2.
"""

TOGGLE = {"inc": "dec", "dec": "inc", "tgl": "inc", "cpy": "jnz", "jnz": "cpy"}


def parse(puzzle_input):
    return [line.split() for line in puzzle_input.strip().splitlines()]


def run(instructions, registers):
    prog = [list(instr) for instr in instructions]  # mutable copy
    ip = 0

    def val(x):
        return registers.get(x, None) if x in "abcd" else int(x)

    while 0 <= ip < len(prog):
        op, *args = prog[ip]

        # ── Multiply-loop optimisation ────────────────────────────────────────
        # Detect the pattern:
        #   cpy X c
        #   inc A
        #   dec c
        #   jnz c -2
        #   dec D
        #   jnz D -5
        # Semantics: A += val(X) * val(D); c = 0; D = 0
        if ip + 5 < len(prog):
            p = prog[ip: ip + 6]
            if (
                p[0][0] == "cpy"
                and p[1][0] == "inc"
                and p[2][0] == "dec" and p[2][1] == p[0][2]
                and p[3][0] == "jnz" and p[3][1] == p[0][2] and p[3][2] == "-2"
                and p[4][0] == "dec"
                and p[5][0] == "jnz" and p[5][1] == p[4][1] and p[5][2] == "-5"
            ):
                A, D = p[1][1], p[4][1]
                multiplier = val(p[0][1])
                if multiplier is not None and registers.get(D) is not None:
                    registers[A] = registers.get(A, 0) + multiplier * registers[D]
                    registers[p[0][2]] = 0
                    registers[D] = 0
                    ip += 6
                    continue

        # ── Normal execution ──────────────────────────────────────────────────
        if op == "cpy":
            v = val(args[0])
            if args[1] in "abcd" and v is not None:
                registers[args[1]] = v

        elif op == "inc":
            if args[0] in "abcd":
                registers[args[0]] = registers.get(args[0], 0) + 1

        elif op == "dec":
            if args[0] in "abcd":
                registers[args[0]] = registers.get(args[0], 0) - 1

        elif op == "jnz":
            v = val(args[0])
            if v is not None and v != 0:
                offset = val(args[1])
                if offset is not None:
                    ip += offset
                    continue

        elif op == "tgl":
            v = val(args[0])
            if v is not None:
                target = ip + v
                if 0 <= target < len(prog):
                    t_op = prog[target][0]
                    prog[target][0] = TOGGLE[t_op]

        ip += 1

    return registers


def solve(puzzle_input: str) -> tuple[str, str]:
    instructions = parse(puzzle_input)
    part1 = run(instructions, {"a": 7, "b": 0, "c": 0, "d": 0})["a"]
    part2 = run(instructions, {"a": 12, "b": 0, "c": 0, "d": 0})["a"]
    return str(part1), str(part2)


def visualize(puzzle_input: str):
    """Step through the assembunny program (a=7) showing tgl mutations and register state."""
    instructions = parse(puzzle_input)
    prog = [list(instr) for instr in instructions]
    registers = {"a": 7, "b": 0, "c": 0, "d": 0}
    ip = 0
    step = 0
    max_steps = 400
    toggled_log = []

    TOGGLE_local = TOGGLE

    def val(x):
        return registers.get(x, None) if x in "abcd" else int(x)

    while 0 <= ip < len(prog) and step < max_steps:
        op, *args = prog[ip]
        mutated = None

        # Multiply optimisation (same as solve)
        if ip + 5 < len(prog):
            p = prog[ip: ip + 6]
            if (
                p[0][0] == "cpy"
                and p[1][0] == "inc"
                and p[2][0] == "dec" and p[2][1] == p[0][2]
                and p[3][0] == "jnz" and p[3][1] == p[0][2] and p[3][2] == "-2"
                and p[4][0] == "dec"
                and p[5][0] == "jnz" and p[5][1] == p[4][1] and p[5][2] == "-5"
            ):
                A, D = p[1][1], p[4][1]
                multiplier = val(p[0][1])
                if multiplier is not None and registers.get(D) is not None:
                    registers[A] = registers.get(A, 0) + multiplier * registers[D]
                    registers[p[0][2]] = 0
                    registers[D] = 0
                    ip += 6
                    step += 1
                    continue

        lines = []
        for i, instr in enumerate(prog):
            prefix = ">>>" if i == ip else "   "
            lines.append(f"  {prefix} {' '.join(instr)}")
        lines.append("")
        lines.append(
            f"  Step {step:>4}  ip={ip}  "
            f"a={registers['a']:>8}  b={registers['b']:>8}  "
            f"c={registers['c']:>8}  d={registers['d']:>8}"
        )
        if toggled_log:
            lines.append(f"  Last tgl: {toggled_log[-1]}")

        yield {"type": "text", "lines": lines, "delay": 80}

        # Execute
        if op == "cpy":
            v = val(args[0])
            if args[1] in "abcd" and v is not None:
                registers[args[1]] = v
        elif op == "inc":
            if args[0] in "abcd":
                registers[args[0]] = registers.get(args[0], 0) + 1
        elif op == "dec":
            if args[0] in "abcd":
                registers[args[0]] = registers.get(args[0], 0) - 1
        elif op == "jnz":
            v = val(args[0])
            if v is not None and v != 0:
                offset = val(args[1])
                if offset is not None:
                    ip += offset
                    step += 1
                    continue
        elif op == "tgl":
            v = val(args[0])
            if v is not None:
                target = ip + v
                if 0 <= target < len(prog):
                    old = prog[target][0]
                    prog[target][0] = TOGGLE_local[old]
                    toggled_log.append(f"ip{target}: {old} → {prog[target][0]}")

        ip += 1
        step += 1

    yield {
        "type": "text",
        "lines": [
            f"  Halted after {step} steps (cap: {max_steps}).",
            "",
            f"  a={registers['a']}  b={registers['b']}"
            f"  c={registers['c']}  d={registers['d']}",
        ],
        "delay": 600,
    }
