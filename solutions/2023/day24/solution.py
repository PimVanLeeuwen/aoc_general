"""
Day 24 - Never Tell Me The Odds
Year: 2023

Find 2D hailstone path intersections and determine
a rock trajectory that hits every hailstone.
"""


def parse_hailstones(text):
    """Parse hailstones as list of ((x,y,z), (dx,dy,dz))."""
    stones = []
    for line in text.split("\n"):
        pos, vel = line.split(" @ ")
        p = tuple(int(x) for x in pos.split(", "))
        v = tuple(int(x) for x in vel.split(", "))
        stones.append((p, v))
    return stones


def intersect_2d(s1, s2, lo, hi):
    """Check if two hailstones' 2D paths intersect within [lo, hi] in the future."""
    (x1, y1, _), (dx1, dy1, _) = s1
    (x2, y2, _), (dx2, dy2, _) = s2

    # Solve: x1 + dx1*t1 = x2 + dx2*t2, y1 + dy1*t1 = y2 + dy2*t2
    det = dx1 * dy2 - dy1 * dx2
    if det == 0:
        return False  # parallel

    t1 = ((x2 - x1) * dy2 - (y2 - y1) * dx2) / det
    t2 = ((x2 - x1) * dy1 - (y2 - y1) * dx1) / det

    if t1 < 0 or t2 < 0:
        return False  # intersection in the past

    ix = x1 + dx1 * t1
    iy = y1 + dy1 * t1
    return lo <= ix <= hi and lo <= iy <= hi


def find_rock(stones):
    """Find rock position that hits all hailstones using linear algebra.

    For hailstones i and j, the equation:
      (px)(dyi-dyj) - (py)(dxi-dxj) + (vx)(yj-yi) + (vy)(xi-xj) =
      xj*dyj - xi*dyi - yj*dxj + yi*dxi
    is linear in (px, py, vx, vy). Need 4 equations (5 hailstones, 4 pairs).
    Similarly for the xz plane to find pz, vz.
    """
    def solve_4x4(equations):
        """Solve Ax = b using Gaussian elimination with partial pivoting."""
        n = len(equations)
        # Augmented matrix
        mat = [list(row) for row in equations]

        for col in range(n):
            # Partial pivot
            max_row = col
            for row in range(col + 1, n):
                if abs(mat[row][col]) > abs(mat[max_row][col]):
                    max_row = row
            mat[col], mat[max_row] = mat[max_row], mat[col]

            pivot = mat[col][col]
            if abs(pivot) < 1e-10:
                continue

            for row in range(col + 1, n):
                factor = mat[row][col] / pivot
                for k in range(col, n + 1):
                    mat[row][k] -= factor * mat[col][k]

        # Back substitution
        result = [0.0] * n
        for i in range(n - 1, -1, -1):
            result[i] = mat[i][n]
            for j in range(i + 1, n):
                result[i] -= mat[i][j] * result[j]
            result[i] /= mat[i][i]

        return result

    # Build equations for xy plane
    # Using pairs (0,1), (0,2), (0,3), (0,4)
    xy_eqs = []
    for j in range(1, 5):
        xi, yi, _ = stones[0][0]
        dxi, dyi, _ = stones[0][1]
        xj, yj, _ = stones[j][0]
        dxj, dyj, _ = stones[j][1]

        # Coefficients for [px, py, vx, vy] = rhs
        a = dyi - dyj
        b = -(dxi - dxj)
        c = yj - yi
        d = -(xj - xi)
        rhs = xi * dyi - xj * dyj - yi * dxi + yj * dxj
        xy_eqs.append([a, b, c, d, rhs])

    px, py, vx, vy = solve_4x4(xy_eqs)

    # Build equations for xz plane (same structure, swap y↔z)
    xz_eqs = []
    for j in range(1, 5):
        xi, _, zi = stones[0][0]
        dxi, _, dzi = stones[0][1]
        xj, _, zj = stones[j][0]
        dxj, _, dzj = stones[j][1]

        a = dzi - dzj
        b = -(dxi - dxj)
        c = zj - zi
        d = -(xj - xi)
        rhs = xi * dzi - xj * dzj - zi * dxi + zj * dxj
        xz_eqs.append([a, b, c, d, rhs])

    px2, pz, vx2, vz = solve_4x4(xz_eqs)

    return round(px), round(py), round(pz)


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    stones = parse_hailstones(puzzle_input.strip())

    # Part 1: count 2D intersections in test area
    n = len(stones)
    if n <= 5:
        lo, hi = 7, 27  # sample bounds
    else:
        lo, hi = 200000000000000, 400000000000000

    part1 = 0
    for i in range(n):
        for j in range(i + 1, n):
            if intersect_2d(stones[i], stones[j], lo, hi):
                part1 += 1

    # Part 2: find rock that hits all hailstones
    if n >= 5:
        px, py, pz = find_rock(stones)
        part2 = px + py + pz
    else:
        part2 = 0

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    """Yield frames showing hailstone analysis."""
    stones = parse_hailstones(puzzle_input.strip())

    yield {
        "type": "text",
        "lines": [
            "  Never Tell Me The Odds",
            "",
            f"  Hailstones: {len(stones)}",
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
            f"  Part 1: {part1} (2D intersections)",
            f"  Part 2: {part2} (rock position sum)",
        ],
        "delay": 500,
    }
