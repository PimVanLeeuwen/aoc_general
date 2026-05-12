"""
Day 24 - Arithmetic Logic Unit
Year: 2021

Find the largest and smallest valid 14-digit model numbers
by analyzing the MONAD ALU program's push/pop stack structure.
"""


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    lines = puzzle_input.strip().split("\n")

    # The MONAD program has 14 nearly identical blocks of 18 instructions.
    # Each block differs in three key parameters:
    #   - line 4:  div z {1 or 26}    (1 = push, 26 = pop)
    #   - line 5:  add x {check_val}
    #   - line 15: add y {offset_val}
    #
    # Push blocks: push (w + offset) onto a base-26 stack
    # Pop blocks:  pop the stack and require w == popped_value + check_val
    #
    # For z to equal 0 at the end, every push must be matched by a pop.

    blocks = []
    for i in range(14):
        block = lines[i * 18:(i + 1) * 18]
        div_z = int(block[4].split()[-1])
        check_val = int(block[5].split()[-1])
        offset_val = int(block[15].split()[-1])
        blocks.append((div_z, check_val, offset_val))

    # Match push/pop pairs using a stack
    # For each pair: digit[pop_idx] = digit[push_idx] + offset + check
    stack = []
    constraints = []  # (push_idx, pop_idx, delta) where d[pop] = d[push] + delta

    for i, (div_z, check_val, offset_val) in enumerate(blocks):
        if div_z == 1:
            # Push block
            stack.append((i, offset_val))
        else:
            # Pop block
            push_idx, push_offset = stack.pop()
            delta = push_offset + check_val
            constraints.append((push_idx, i, delta))

    # Find max and min valid model numbers
    max_digits = [0] * 14
    min_digits = [0] * 14

    for push_idx, pop_idx, delta in constraints:
        # digit[pop_idx] = digit[push_idx] + delta
        # Both digits must be 1-9
        if delta >= 0:
            max_digits[push_idx] = 9 - delta
            max_digits[pop_idx] = 9
            min_digits[push_idx] = 1
            min_digits[pop_idx] = 1 + delta
        else:
            max_digits[push_idx] = 9
            max_digits[pop_idx] = 9 + delta
            min_digits[push_idx] = 1 - delta
            min_digits[pop_idx] = 1

    part1 = "".join(map(str, max_digits))
    part2 = "".join(map(str, min_digits))

    return part1, part2


def visualize(puzzle_input: str):
    """Yield frames showing MONAD analysis."""
    lines = puzzle_input.strip().split("\n")

    yield {
        "type": "text",
        "lines": [
            "  Arithmetic Logic Unit",
            "",
            f"  Instructions: {len(lines)}",
            f"  Blocks: {len(lines) // 18}",
        ],
        "delay": 600,
    }

    # Show the push/pop structure
    blocks = []
    for i in range(14):
        block = lines[i * 18:(i + 1) * 18]
        div_z = int(block[4].split()[-1])
        check_val = int(block[5].split()[-1])
        offset_val = int(block[15].split()[-1])
        blocks.append((div_z, check_val, offset_val))

    structure_lines = ["  Block structure:", ""]
    for i, (dz, cv, ov) in enumerate(blocks):
        kind = "PUSH" if dz == 1 else "POP "
        structure_lines.append(f"  Digit {i:>2}: {kind}  check={cv:>4}  offset={ov:>3}")

    yield {"type": "text", "lines": structure_lines, "delay": 600}

    part1, part2 = solve(puzzle_input)

    yield {
        "type": "text",
        "lines": [
            "  ===================================",
            "  Results",
            "  ===================================",
            "",
            f"  Part 1: {part1} (largest)",
            f"  Part 2: {part2} (smallest)",
        ],
        "delay": 500,
    }
