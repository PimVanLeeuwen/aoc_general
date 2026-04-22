"""
Day 25 - Clock Signal
Year: 2016

Find the lowest initial value for register a that causes the assembunny
program to emit an infinite alternating 0, 1, 0, 1, … clock signal.
"""

_TOGGLE = {"inc": "dec", "dec": "inc", "tgl": "inc", "cpy": "jnz", "jnz": "cpy"}


def parse(puzzle_input):
    return [line.split() for line in puzzle_input.strip().splitlines()]


def run(instructions, init_a, max_output=100, max_steps=2_000_000):
    """Run the program and collect up to max_output 'out' values.

    Uses a step limit rather than state-tuple tracking — state sets become
    unmanageably large when registers hold values in the hundreds.
    Includes the multiply-loop optimiser from day 23 to collapse inner
    accumulation loops (e.g. cpy 633 b / inc d / dec b / jnz b -2 / ...).
    """
    prog = [list(i) for i in instructions]
    regs = {"a": init_a, "b": 0, "c": 0, "d": 0}
    ip = 0
    outputs = []
    steps = 0

    def val(x):
        return regs[x] if x in regs else int(x)

    while 0 <= ip < len(prog) and steps < max_steps:
        steps += 1

        # ── Multiply-loop optimisation ────────────────────────────────────────
        # Pattern: cpy X c / inc A / dec c / jnz c -2 / dec D / jnz D -5
        # Semantics: A += val(X) * D;  c = 0;  D = 0
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
                d_val = regs.get(D)
                if multiplier is not None and d_val is not None:
                    regs[A] = regs.get(A, 0) + multiplier * d_val
                    regs[p[0][2]] = 0
                    regs[D] = 0
                    ip += 6
                    continue

        op, *args = prog[ip]

        if op == "cpy":
            if args[1] in regs:
                regs[args[1]] = val(args[0])
        elif op == "inc":
            if args[0] in regs:
                regs[args[0]] += 1
        elif op == "dec":
            if args[0] in regs:
                regs[args[0]] -= 1
        elif op == "jnz":
            if val(args[0]) != 0:
                ip += val(args[1])
                continue
        elif op == "tgl":
            t = ip + val(args[0])
            if 0 <= t < len(prog):
                prog[t][0] = _TOGGLE[prog[t][0]]
        elif op == "out":
            outputs.append(val(args[0]))
            if len(outputs) == max_output:
                return outputs

        ip += 1

    return outputs


def is_clock(outputs):
    return all(v == i % 2 for i, v in enumerate(outputs))


def find_clock_signal(instructions):
    for a in range(1, 10_000):
        outputs = run(instructions, a)
        if len(outputs) >= 20 and is_clock(outputs):
            return a
    return -1


def solve(puzzle_input: str) -> tuple[str, str]:
    instructions = parse(puzzle_input)
    part1 = find_clock_signal(instructions)
    # Day 25 has no part 2 — the 50th star is awarded for completing the year.
    return str(part1), "⭐"


def visualize(puzzle_input: str):
    """Show the search for the winning 'a' value, then display its output stream."""
    instructions = parse(puzzle_input)

    # Scan candidate values and show progress
    winner = None
    attempts = []
    for a in range(1, 10_000):
        outputs = run(instructions, a, max_output=20)
        ok = len(outputs) >= 20 and is_clock(outputs)
        attempts.append((a, outputs[:8], ok))

        if a % 10 == 0 or ok:
            lines = [
                "  Searching for clock signal…",
                f"  Trying a = {a}",
                "",
            ]
            for av, outs, valid in attempts[-8:]:
                symbol = "✓" if valid else "✗"
                lines.append(f"  {symbol} a={av:>5}  output: {' '.join(map(str, outs))}")
            yield {"type": "text", "lines": lines, "delay": 60}

        if ok:
            winner = a
            break

    if winner is None:
        yield {"type": "text", "lines": ["  No solution found."], "delay": 500}
        return

    # Collect a longer output stream for the winner
    full_output = run(instructions, winner, max_output=80)

    rows = []
    for chunk_start in range(0, len(full_output), 20):
        chunk = full_output[chunk_start: chunk_start + 20]
        rows.append("  " + " ".join(str(v) for v in chunk))

    yield {
        "type": "text",
        "lines": [
            f"  Winner: a = {winner}",
            "",
            f"  First {len(full_output)} output values:",
            *rows,
            "",
            "  Pattern: 0 1 0 1 0 1 … repeating ✓",
        ],
        "delay": 1000,
    }
