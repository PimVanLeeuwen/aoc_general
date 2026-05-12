"""
Day 16 - Packet Decoder
Year: 2021

Parse nested BITS packets from a hex-encoded transmission.
Sum version numbers and evaluate the expression tree.
"""

from math import prod


def parse_packet(bits, pos):
    """Parse one packet starting at pos. Return (value, version_sum, new_pos)."""
    version = int(bits[pos:pos + 3], 2)
    type_id = int(bits[pos + 3:pos + 6], 2)
    pos += 6
    version_sum = version

    if type_id == 4:
        # Literal value
        value = 0
        while True:
            group = bits[pos:pos + 5]
            value = (value << 4) | int(group[1:], 2)
            pos += 5
            if group[0] == "0":
                break
        return value, version_sum, pos

    # Operator packet — collect sub-packet values
    sub_values = []
    length_type = bits[pos]
    pos += 1

    if length_type == "0":
        total_length = int(bits[pos:pos + 15], 2)
        pos += 15
        end = pos + total_length
        while pos < end:
            val, vs, pos = parse_packet(bits, pos)
            sub_values.append(val)
            version_sum += vs
    else:
        num_packets = int(bits[pos:pos + 11], 2)
        pos += 11
        for _ in range(num_packets):
            val, vs, pos = parse_packet(bits, pos)
            sub_values.append(val)
            version_sum += vs

    # Evaluate based on type
    if type_id == 0:
        value = sum(sub_values)
    elif type_id == 1:
        value = prod(sub_values)
    elif type_id == 2:
        value = min(sub_values)
    elif type_id == 3:
        value = max(sub_values)
    elif type_id == 5:
        value = int(sub_values[0] > sub_values[1])
    elif type_id == 6:
        value = int(sub_values[0] < sub_values[1])
    elif type_id == 7:
        value = int(sub_values[0] == sub_values[1])

    return value, version_sum, pos


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    hex_str = puzzle_input.strip()
    bits = bin(int(hex_str, 16))[2:].zfill(len(hex_str) * 4)

    value, version_sum, _ = parse_packet(bits, 0)

    return str(version_sum), str(value)


def visualize(puzzle_input: str):
    """Yield frames showing packet structure."""
    hex_str = puzzle_input.strip()
    bits = bin(int(hex_str, 16))[2:].zfill(len(hex_str) * 4)

    yield {
        "type": "text",
        "lines": [
            "  Packet Decoder",
            "",
            f"  Hex input: {len(hex_str)} characters",
            f"  Binary: {len(bits)} bits",
        ],
        "delay": 600,
    }

    # Walk the packet tree and collect structure info
    depth_counts = {}

    def walk(pos, depth):
        type_id = int(bits[pos + 3:pos + 6], 2)
        pos += 6
        depth_counts[depth] = depth_counts.get(depth, 0) + 1

        if type_id == 4:
            while bits[pos] == "1":
                pos += 5
            pos += 5
            return pos

        length_type = bits[pos]
        pos += 1
        if length_type == "0":
            total = int(bits[pos:pos + 15], 2)
            pos += 15
            end = pos + total
            while pos < end:
                pos = walk(pos, depth + 1)
        else:
            n = int(bits[pos:pos + 11], 2)
            pos += 11
            for _ in range(n):
                pos = walk(pos, depth + 1)
        return pos

    walk(0, 0)

    lines = ["  Packet nesting depths:", ""]
    for d in sorted(depth_counts):
        bar = "#" * min(depth_counts[d], 40)
        lines.append(f"  Depth {d}: {bar} ({depth_counts[d]})")

    yield {"type": "text", "lines": lines, "delay": 600}

    value, version_sum, _ = parse_packet(bits, 0)

    yield {
        "type": "text",
        "lines": [
            "  ===================================",
            "  Results",
            "  ===================================",
            "",
            f"  Part 1: {version_sum} (version sum)",
            f"  Part 2: {value} (expression value)",
        ],
        "delay": 500,
    }
