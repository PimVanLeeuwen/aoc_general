"""
Day 19 - Go With The Flow
Year: 2018

Execute an assembly program with the instruction pointer bound to a register.
Part 1: register 0 when the program halts (r[0]=0 initially).
Part 2: register 0 when the program halts (r[0]=1 initially) — the program
        computes the sum of divisors of a large number N; detected analytically.
"""

OPS = {
    'addr': lambda r, a, b: r[a] + r[b],
    'addi': lambda r, a, b: r[a] + b,
    'mulr': lambda r, a, b: r[a] * r[b],
    'muli': lambda r, a, b: r[a] * b,
    'banr': lambda r, a, b: r[a] & r[b],
    'bani': lambda r, a, b: r[a] & b,
    'borr': lambda r, a, b: r[a] | r[b],
    'bori': lambda r, a, b: r[a] | b,
    'setr': lambda r, a, b: r[a],
    'seti': lambda r, a, b: a,
    'gtir': lambda r, a, b: int(a > r[b]),
    'gtri': lambda r, a, b: int(r[a] > b),
    'gtrr': lambda r, a, b: int(r[a] > r[b]),
    'eqir': lambda r, a, b: int(a == r[b]),
    'eqri': lambda r, a, b: int(r[a] == b),
    'eqrr': lambda r, a, b: int(r[a] == r[b]),
}


def parse(puzzle_input: str):
    lines = puzzle_input.strip().splitlines()
    ip_reg = int(lines[0].split()[1])
    program = [(p[0], int(p[1]), int(p[2]), int(p[3]))
               for line in lines[1:] for p in [line.split()]]
    return ip_reg, program


def run(ip_reg, program, regs):
    ip = 0
    while 0 <= ip < len(program):
        regs[ip_reg] = ip
        op, a, b, c = program[ip]
        regs[c] = OPS[op](regs, a, b)
        ip = regs[ip_reg] + 1
    return regs


def sum_divisors(n: int) -> int:
    """O(sqrt n) sum of all divisors of n."""
    total, i = 0, 1
    while i * i <= n:
        if n % i == 0:
            total += i
            if i != n // i:
                total += n // i
        i += 1
    return total


def solve(puzzle_input: str) -> tuple[str, str]:
    ip_reg, program = parse(puzzle_input)

    # Part 1: run from r[0] = 0
    part1 = run(ip_reg, program, [0] * 6)[0]

    # Part 2: r[0] = 1. Initialization sets a large N in a register; the main
    # loop then iterates O(N^2) steps summing divisors — too slow to simulate.
    # Strategy: instruction 0 jumps to init code; once init finishes the IP
    # returns to 1. At that point N is the largest register value.
    regs = [1, 0, 0, 0, 0, 0]
    ip = 0
    first = True
    while 0 <= ip < len(program):
        regs[ip_reg] = ip
        op, a, b, c = program[ip]
        regs[c] = OPS[op](regs, a, b)
        ip = regs[ip_reg] + 1
        if first:
            first = False
        elif ip == 1:
            n = max(r for i, r in enumerate(regs) if i != ip_reg)
            part2 = sum_divisors(n)
            break
    else:
        part2 = regs[0]

    return str(part1), str(part2)


# ── Optional visualizer ────────────────────────────────────────────────────────

def visualize(puzzle_input: str):
    ip_reg, program = parse(puzzle_input)

    # Show disassembly
    yield {
        "type": "text",
        "lines": [f"#ip {ip_reg}", ""] +
                 [f"  {i:2d}: {op:4s}  {a} {b} {c}"
                  for i, (op, a, b, c) in enumerate(program)],
        "delay": 1500,
    }

    # Trace first 50 steps of Part 1 execution
    regs = [0] * 6
    ip = 0
    for step in range(1, 51):
        if not (0 <= ip < len(program)):
            break
        regs[ip_reg] = ip
        op, a, b, c = program[ip]
        prev = regs[:]
        regs[c] = OPS[op](regs, a, b)
        ip = regs[ip_reg] + 1
        yield {
            "type": "text",
            "lines": [
                f"Step {step:3d}  ip={prev[ip_reg]}",
                f"  {op} {a} {b} {c}",
                f"  before: {prev}",
                f"  after : {regs}",
            ],
            "delay": 120,
        }

    # Finish Part 1
    while 0 <= ip < len(program):
        regs[ip_reg] = ip
        op, a, b, c = program[ip]
        regs[c] = OPS[op](regs, a, b)
        ip = regs[ip_reg] + 1

    yield {
        "type": "text",
        "lines": ["Part 1 — program halted", "", f"  r[0] = {regs[0]}"],
        "delay": 2000,
    }

    # Part 2: run until N is initialized, then compute analytically
    regs2 = [1, 0, 0, 0, 0, 0]
    ip = 0
    n = None
    first = True
    while 0 <= ip < len(program):
        regs2[ip_reg] = ip
        op, a, b, c = program[ip]
        regs2[c] = OPS[op](regs2, a, b)
        ip = regs2[ip_reg] + 1
        if first:
            first = False
        elif ip == 1:
            n = max(r for i, r in enumerate(regs2) if i != ip_reg)
            break

    part2 = sum_divisors(n) if n else regs2[0]
    yield {
        "type": "text",
        "lines": [
            "Part 2 — r[0]=1, analytical shortcut",
            "",
            f"  Program computes sum of divisors of N",
            f"  N       = {n:,}",
            f"  Divisors: {', '.join(str(i) for i in range(1, min(n+1, 50)) if n % i == 0)}"
            + ("…" if n >= 50 else ""),
            f"  Sum     = {part2:,}",
        ],
        "delay": 4000,
    }
