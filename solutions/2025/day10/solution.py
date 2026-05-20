"""
Day 10 - Light Machines
Year: 2025

Machines with toggle lights and joltage counters controlled by
buttons. Part 1: BFS for minimum presses to light all LEDs.
Part 2: minimum presses to reach target joltage values (ILP).
"""

import re
from collections import deque


def parse_machine(line):
    lights = re.search(r"\[([^\]]+)\]", line).group(1)
    wirings = [list(map(int, w.split(","))) for w in re.findall(r"\(([^)]+)\)", line)]
    joltages = list(map(int, re.search(r"\{([^}]+)\}", line).group(1).split(",")))
    return lights, wirings, joltages


def min_presses_lights(lights, wirings):
    """BFS to find minimum button presses to turn all lights on."""
    n = len(lights)
    target = tuple(1 if c == "#" else 0 for c in lights)
    start = tuple([0] * n)

    if start == target:
        return 0

    queue = deque([(start, 0)])
    visited = {start}

    while queue:
        state, presses = queue.popleft()

        for wiring in wirings:
            next_state = list(state)
            for i in wiring:
                next_state[i] = 1 - next_state[i]
            next_state = tuple(next_state)

            if next_state == target:
                return presses + 1

            if next_state not in visited:
                visited.add(next_state)
                queue.append((next_state, presses + 1))

    return -1


def min_presses_joltage(joltages, wirings):
    """Solve Ax = b for non-negative integers x, minimizing sum(x).

    Uses Gaussian elimination (float) then verifies integer solutions.
    For underdetermined systems, enumerates over free variables.
    """
    n_counters = len(joltages)
    n_buttons = len(wirings)

    # Build augmented matrix [A | b] in float
    aug = [[0.0] * (n_buttons + 1) for _ in range(n_counters)]
    for i in range(n_counters):
        aug[i][n_buttons] = float(joltages[i])
    for j, wiring in enumerate(wirings):
        for i in wiring:
            aug[i][j] += 1.0

    # Also keep integer copy for verification
    A_int = [[0] * n_buttons for _ in range(n_counters)]
    for j, wiring in enumerate(wirings):
        for i in wiring:
            A_int[i][j] += 1

    # Gaussian elimination with partial pivoting (RREF)
    pivot_cols = []
    row = 0
    for col in range(n_buttons):
        # Find best pivot (largest absolute value)
        best_row = None
        best_val = 1e-10
        for r in range(row, n_counters):
            if abs(aug[r][col]) > best_val:
                best_val = abs(aug[r][col])
                best_row = r
        if best_row is None:
            continue
        aug[row], aug[best_row] = aug[best_row], aug[row]
        pivot_cols.append((row, col))
        pivot_val = aug[row][col]
        for c in range(n_buttons + 1):
            aug[row][c] /= pivot_val
        for r in range(n_counters):
            if r != row and abs(aug[r][col]) > 1e-12:
                factor = aug[r][col]
                for c in range(n_buttons + 1):
                    aug[r][c] -= factor * aug[row][c]
        row += 1

    pivot_col_set = {col for _, col in pivot_cols}
    free_vars = [j for j in range(n_buttons) if j not in pivot_col_set]
    col_to_row = {col: r for r, col in pivot_cols}

    def solve_and_verify(free_vals):
        """Compute solution for given free variable values, verify with integers."""
        x = [0.0] * n_buttons
        for idx, fv in enumerate(free_vars):
            x[fv] = float(free_vals[idx])
        for _, col in pivot_cols:
            r = col_to_row[col]
            val = aug[r][n_buttons]
            for fv in free_vars:
                val -= aug[r][fv] * x[fv]
            x[col] = val

        # Round and verify
        x_int = [round(v) for v in x]
        if any(v < 0 for v in x_int):
            return None
        # Verify Ax = b exactly
        for i in range(n_counters):
            total = sum(A_int[i][j] * x_int[j] for j in range(n_buttons))
            if total != joltages[i]:
                return None
        return sum(x_int)

    if not free_vars:
        result = solve_and_verify([])
        return result if result is not None else -1

    # Enumerate over free variables
    max_target = max(joltages) if joltages else 0
    best = float("inf")

    if len(free_vars) <= 3:
        # Convert RREF to scaled integer form for fast search
        # For each pivot row: pivot_col = rhs_frac - sum(coeff_frac * fv)
        # Multiply by LCM of denominators to get integer equation:
        # pivot_col * D = RHS_int - sum(C_int * fv)
        from fractions import Fraction
        from math import gcd

        # Redo RREF with exact Fraction arithmetic
        aug_e = [[Fraction(0)] * (n_buttons + 1) for _ in range(n_counters)]
        for i in range(n_counters):
            aug_e[i][n_buttons] = Fraction(joltages[i])
        for j, wiring in enumerate(wirings):
            for i in wiring:
                aug_e[i][j] += 1
        row_e = 0
        pivot_cols_e = []
        for col in range(n_buttons):
            pr = None
            for r in range(row_e, n_counters):
                if aug_e[r][col] != 0:
                    pr = r
                    break
            if pr is None:
                continue
            aug_e[row_e], aug_e[pr] = aug_e[pr], aug_e[row_e]
            pivot_cols_e.append((row_e, col))
            pv = aug_e[row_e][col]
            for c in range(n_buttons + 1):
                aug_e[row_e][c] /= pv
            for r in range(n_counters):
                if r != row_e and aug_e[r][col] != 0:
                    f = aug_e[r][col]
                    for c in range(n_buttons + 1):
                        aug_e[r][c] -= f * aug_e[row_e][c]
            row_e += 1

        col_to_row_e = {col: r for r, col in pivot_cols_e}
        n_free = len(free_vars)

        # Convert to integer form: for each pivot row, find LCM of denominators
        # then store (denom, rhs_int, [coeff_int for each free var])
        def lcm(a, b):
            return a * b // gcd(a, b)

        int_rows = []  # (denom, rhs_int, [coeff_ints])
        for _, col in pivot_cols_e:
            r = col_to_row_e[col]
            # Collect all relevant fractions
            fracs = [aug_e[r][n_buttons]] + [aug_e[r][fv] for fv in free_vars]
            d = 1
            for f in fracs:
                d = lcm(d, f.denominator)
            rhs_int = int(aug_e[r][n_buttons] * d)
            coeff_ints = [int(aug_e[r][fv] * d) for fv in free_vars]
            int_rows.append((d, rhs_int, coeff_ints))

        n_pivots = len(int_rows)

        def search_int(depth, vals, partial_sum):
            nonlocal best
            if partial_sum >= best:
                return
            if depth == n_free:
                x_sum = partial_sum
                for pi in range(n_pivots):
                    d, rhs_int, coeff_ints = int_rows[pi]
                    num = rhs_int
                    for k in range(n_free):
                        num -= coeff_ints[k] * vals[k]
                    if num < 0 or num % d != 0:
                        return
                    x_sum += num // d
                if x_sum < best:
                    best = x_sum
                return

            # Compute tight upper bound for this free var
            upper = min(max_target, best - partial_sum - 1)
            for pi in range(n_pivots):
                d, rhs_int, coeff_ints = int_rows[pi]
                res = rhs_int
                for k in range(depth):
                    res -= coeff_ints[k] * vals[k]
                c = coeff_ints[depth]
                if c > 0:
                    # Account for remaining free vars with negative coefficients
                    # They can increase the residual
                    slack = 0
                    for k in range(depth + 1, n_free):
                        if coeff_ints[k] < 0:
                            slack -= coeff_ints[k] * max_target
                    bound = (res + slack) // c
                    if bound < upper:
                        upper = bound

            if upper < 0:
                return

            for v in range(upper + 1):
                if partial_sum + v >= best:
                    break
                vals[depth] = v
                search_int(depth + 1, vals, partial_sum + v)

        search_int(0, [0] * n_free, 0)
    else:
        # Too many free vars — try setting all to 0 first
        result = solve_and_verify([0] * len(free_vars))
        if result is not None:
            best = result

    return best if best < float("inf") else -1


def solve(puzzle_input: str) -> tuple[str, str]:
    lines = puzzle_input.strip().split("\n")
    machines = [parse_machine(line) for line in lines]

    part1 = sum(min_presses_lights(m[0], m[1]) for m in machines)
    part2 = sum(min_presses_joltage(m[2], m[1]) for m in machines)

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    lines = puzzle_input.strip().split("\n")
    machines = [parse_machine(line) for line in lines]

    yield {
        "type": "text",
        "lines": [
            "  Light Machines",
            "",
            f"  Machines: {len(machines)}",
            f"  Sample lights: {machines[0][0]}",
            f"  Buttons per machine: {len(machines[0][1])}",
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
            f"  Part 1: {part1} (min presses for lights)",
            f"  Part 2: {part2} (min presses for joltage)",
        ],
        "delay": 500,
    }
