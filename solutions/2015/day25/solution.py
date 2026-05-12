"""
Day 25 - Let It Snow
Year: 2015

Find the code at a given row/column on an infinite diagonal grid,
where each code is generated via modular exponentiation.
"""

import re


def rc_to_index(row, col):
    """Convert (row, col) to the 1-based sequence index on the diagonal grid."""
    # Diagonal number (1-based): row+col-1
    # Position within diagonal: col
    diag = row + col - 1
    return diag * (diag - 1) // 2 + col


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    nums = list(map(int, re.findall(r'\d+', puzzle_input)))
    row, col = nums[0], nums[1]

    n = rc_to_index(row, col)
    # code(n) = 20151125 * 252533^(n-1) mod 33554393
    code = 20151125 * pow(252533, n - 1, 33554393) % 33554393

    # Day 25 has no Part 2 — completing all other stars unlocks it
    return str(code), "Merry Christmas!"


def visualize(puzzle_input: str):
    """Yield frames showing the diagonal code generation."""
    nums = list(map(int, re.findall(r'\d+', puzzle_input)))
    target_row, target_col = nums[0], nums[1]
    target_n = rc_to_index(target_row, target_col)

    yield {
        "type": "text",
        "lines": [
            "  Let It Snow - Code Generator",
            "",
            f"  Target: row {target_row}, col {target_col}",
            f"  Sequence index: {target_n:,}",
            "",
            "  Building the diagonal grid...",
        ],
        "delay": 800,
    }

    # Show a small portion of the grid being filled
    grid_size = 6
    grid = [["  .....  " for _ in range(grid_size)] for _ in range(grid_size)]
    code = 20151125

    for n in range(1, grid_size * (grid_size + 1) // 2 + 1):
        # Find row, col for index n by walking diagonals
        diag = 1
        while diag * (diag + 1) // 2 < n:
            diag += 1
        col = n - diag * (diag - 1) // 2
        row = diag - col + 1

        if row <= grid_size and col <= grid_size:
            grid[row - 1][col - 1] = f"{code:>9d}"

        if n < target_n:
            code = code * 252533 % 33554393

        if n <= 21 and n % 3 == 0:
            header = "     " + "".join(f"{c:>10d}" for c in range(1, grid_size + 1))
            sep = "  ---+" + "---------+" * grid_size
            lines = ["  Filling diagonals...", "", header, sep]
            for r in range(grid_size):
                row_str = f"  {r+1:>2d} | " + " ".join(grid[r])
                lines.append(row_str)
            yield {"type": "text", "lines": lines, "delay": 300}

    # Show final small grid
    header = "     " + "".join(f"{c:>10d}" for c in range(1, grid_size + 1))
    sep = "  ---+" + "---------+" * grid_size
    lines = ["  Complete 6x6 grid:", "", header, sep]
    for r in range(grid_size):
        row_str = f"  {r+1:>2d} | " + " ".join(grid[r])
        lines.append(row_str)
    yield {"type": "text", "lines": lines, "delay": 600}

    # Compute final answer with progress
    code = 20151125 * pow(252533, target_n - 1, 33554393) % 33554393

    yield {
        "type": "text",
        "lines": [
            "  Computing code via modular exponentiation:",
            "",
            f"  code = 20151125 * 252533^{target_n - 1:,} mod 33554393",
            f"       = {code}",
            "",
            f"  Answer: {code}",
            "",
            "  Merry Christmas!",
        ],
        "delay": 800,
    }