"""
Day 24 - Crossed Wires
Year: 2024

Simulate a circuit of logic gates. Part 1 computes the output.
Part 2 identifies swapped wires in a ripple-carry adder.
"""


def parse_input(text):
    parts = text.strip().split("\n\n")
    wires = {}
    for line in parts[0].split("\n"):
        name, val = line.split(": ")
        wires[name] = int(val)

    gates = []
    for line in parts[1].split("\n"):
        tokens = line.split()
        # input1 OP input2 -> output
        gates.append((tokens[0], tokens[1], tokens[2], tokens[4]))

    return wires, gates


def simulate(wires, gates):
    """Simulate gates until all outputs are resolved."""
    wires = dict(wires)
    remaining = list(gates)

    while remaining:
        progress = False
        next_remaining = []
        for a, op, b, out in remaining:
            if a in wires and b in wires:
                if op == "AND":
                    wires[out] = wires[a] & wires[b]
                elif op == "OR":
                    wires[out] = wires[a] | wires[b]
                elif op == "XOR":
                    wires[out] = wires[a] ^ wires[b]
                progress = True
            else:
                next_remaining.append((a, op, b, out))
        remaining = next_remaining
        if not progress:
            break

    return wires


def get_z_value(wires):
    """Extract the binary number from z-wires."""
    z_bits = []
    for name, val in sorted(wires.items()):
        if name.startswith("z"):
            z_bits.append((int(name[1:]), val))
    z_bits.sort()
    result = 0
    for bit_pos, val in z_bits:
        result |= val << bit_pos
    return result


def find_swapped_wires(gates):
    """Identify swapped output wires in a ripple-carry adder.

    In a correct ripple-carry adder, the following rules hold:
    - XOR gates that take x/y inputs should not output to z (except z00)
    - Non-XOR gates should not output to z (except the last bit)
    - XOR gates with non-x/y inputs should output to z
    - AND gates (except x00 AND y00) should feed into OR gates
    - XOR gates with x/y inputs should feed into XOR gates
    """
    # Build lookup structures
    output_gate = {}  # output_wire -> (a, op, b)
    for a, op, b, out in gates:
        output_gate[out] = (a, op, b)

    # Find which gates each wire feeds into
    feeds_into = {}
    for a, op, b, out in gates:
        feeds_into.setdefault(a, []).append((a, op, b, out))
        feeds_into.setdefault(b, []).append((a, op, b, out))

    max_z = max(int(out[1:]) for _, _, _, out in gates if out.startswith("z"))
    swapped = set()

    for a, op, b, out in gates:
        is_xy_input = (a[0] in "xy" and b[0] in "xy")
        is_z_output = out.startswith("z")
        is_first_bit = (a in ("x00", "y00") and b in ("x00", "y00"))
        is_last_z = out == f"z{max_z:02d}"

        if op == "XOR":
            if is_xy_input:
                # XOR of x/y should not output directly to z (except bit 0)
                if is_z_output and not is_first_bit:
                    swapped.add(out)
            else:
                # XOR of non-x/y (carry + half-sum) must output to z
                if not is_z_output:
                    swapped.add(out)
        elif op == "AND":
            if not is_first_bit:
                # AND gates must never output to z
                if is_z_output:
                    swapped.add(out)
                # AND gates must feed into OR (carry chain), not XOR/AND
                elif out in feeds_into:
                    fed_ops = [g[1] for g in feeds_into[out]]
                    if "OR" not in fed_ops:
                        swapped.add(out)
        elif op == "OR":
            # OR (carry propagation) must never output to z (except last bit)
            if is_z_output and not is_last_z:
                swapped.add(out)

    return sorted(swapped)


def solve(puzzle_input: str) -> tuple[str, str]:
    wires, gates = parse_input(puzzle_input)

    # Part 1: simulate the circuit
    result = simulate(wires, gates)
    part1 = get_z_value(result)

    # Part 2: find swapped wires
    swapped = find_swapped_wires(gates)
    part2 = ",".join(swapped)

    return str(part1), part2


def visualize(puzzle_input: str):
    wires, gates = parse_input(puzzle_input)

    ops = {"AND": 0, "OR": 0, "XOR": 0}
    for _, op, _, _ in gates:
        ops[op] += 1

    yield {
        "type": "text",
        "lines": [
            "  Crossed Wires",
            "",
            f"  Input wires: {len(wires)}",
            f"  Gates: {len(gates)}",
            f"    AND: {ops['AND']}  OR: {ops['OR']}  XOR: {ops['XOR']}",
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
