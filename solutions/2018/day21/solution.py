"""
Day 21 - Chronal Conversion
Year: 2018

The program computes a hash-like sequence and checks each value against r[0].
We reverse-engineer the algorithm and extract two input-specific constants,
then run the extracted algorithm directly (the VM inner loop is far too slow).
"""


def extract_constants(program):
    """Extract CONST_A and CONST_B from the program.

    The algorithm is always:
        r = 0
        loop:
            c = r | 65536
            r = CONST_A
            while True:
                r = ((r + (c & 255)) & 0xFFFFFF) * CONST_B & 0xFFFFFF
                if c < 256: break
                c = c // 256
            if r == r0: halt  # ← the value we intercept
            goto loop
    """
    # Find eqrr that references register 0 → gives us check_reg
    check_reg = None
    for op, a, b, c in program:
        if op == 'eqrr' and (a == 0 or b == 0):
            check_reg = b if a == 0 else a
            break

    # CONST_A: the large seti into check_reg
    const_a = None
    for op, a, b, c in program:
        if op == 'seti' and c == check_reg and a > 65536:
            const_a = a
            break

    # CONST_B: the muli of check_reg
    const_b = None
    for op, a, b, c in program:
        if op == 'muli' and a == check_reg and c == check_reg:
            const_b = b
            break

    return const_a, const_b


def generate_sequence(const_a, const_b):
    """Yield the sequence of values compared against r[0]."""
    r = 0
    while True:
        c = r | 65536
        r = const_a
        while True:
            r = ((r + (c & 255)) & 0xFFFFFF) * const_b & 0xFFFFFF
            if c < 256:
                break
            c = c >> 8
        yield r


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    lines = puzzle_input.strip().splitlines()
    program = []
    for line in lines[1:]:
        p = line.split()
        program.append((p[0], int(p[1]), int(p[2]), int(p[3])))

    const_a, const_b = extract_constants(program)

    seen = set()
    order = []
    for val in generate_sequence(const_a, const_b):
        if val in seen:
            break
        seen.add(val)
        order.append(val)

    return str(order[0]), str(order[-1])


def visualize(puzzle_input: str):
    """Show the hash sequence being computed."""
    lines = puzzle_input.strip().splitlines()
    program = []
    for line in lines[1:]:
        p = line.split()
        program.append((p[0], int(p[1]), int(p[2]), int(p[3])))

    const_a, const_b = extract_constants(program)

    yield {
        "type": "text",
        "lines": [
            "Chronal Conversion",
            "",
            f"Extracted constants: A={const_a}, B={const_b}",
            "",
            "Algorithm:",
            "  r = 0",
            "  loop:",
            "    c = r | 65536",
            f"    r = {const_a}",
            f"    r = ((r + (c & 255)) & 0xFFFFFF) * {const_b} & 0xFFFFFF",
            "    c >>= 8 (repeat while c >= 256)",
            "    if r == r0: halt",
        ],
        "delay": 3000,
    }

    seen = set()
    order = []
    for val in generate_sequence(const_a, const_b):
        if val in seen:
            break
        seen.add(val)
        order.append(val)
        if len(order) <= 300 and len(order) % 20 == 0:
            yield {
                "type": "text",
                "lines": [
                    f"Values collected: {len(order)}",
                    f"Latest: {val}",
                ],
                "delay": 60,
            }

    yield {
        "type": "text",
        "lines": [
            f"Cycle detected after {len(order)} unique values",
            "",
            f"Part 1 (first value):  {order[0]}",
            f"Part 2 (last unique):  {order[-1]}",
        ],
        "delay": 4000,
    }