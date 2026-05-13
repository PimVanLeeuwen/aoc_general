"""
Day 22 - Monkey Map
Year: 2022

Follow a path on a map with flat wrapping (part 1)
and cube-surface wrapping (part 2).
"""

import re
from collections import deque


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    parts = puzzle_input.split("\n\n")
    grid_lines = parts[0].split("\n")
    path_str = parts[1].strip()

    max_w = max(len(line) for line in grid_lines)
    grid = [line.ljust(max_w) for line in grid_lines]
    rows, cols = len(grid), max_w

    instructions = []
    for token in re.findall(r"\d+|[LR]", path_str):
        instructions.append(int(token) if token.isdigit() else token)

    DR = [0, 1, 0, -1]
    DC = [1, 0, -1, 0]

    def walk(wrap_fn):
        r, c, d = 0, grid[0].index("."), 0
        for instr in instructions:
            if isinstance(instr, str):
                d = (d + (1 if instr == "R" else 3)) % 4
            else:
                for _ in range(instr):
                    nr, nc, nd = wrap_fn(r, c, d)
                    if grid[nr][nc] == "#":
                        break
                    r, c, d = nr, nc, nd
        return 1000 * (r + 1) + 4 * (c + 1) + d

    # Part 1: flat wrapping
    def flat_wrap(r, c, d):
        nr = (r + DR[d]) % rows
        nc = (c + DC[d]) % cols
        while grid[nr][nc] == " ":
            nr = (nr + DR[d]) % rows
            nc = (nc + DC[d]) % cols
        return nr, nc, d

    part1 = walk(flat_wrap)

    # Part 2: cube wrapping
    non_space = sum(1 for r in range(rows) for c in range(cols) if grid[r][c] != " ")
    S = int((non_space // 6) ** 0.5)

    face_pos = []
    face_at = {}
    for fr in range(rows // S):
        for fc in range(cols // S):
            if fr * S < rows and fc * S < cols and grid[fr * S][fc * S] != " ":
                face_at[(fr, fc)] = len(face_pos)
                face_pos.append((fr, fc))

    def neg(v):
        return (-v[0], -v[1], -v[2])

    # BFS to assign 3D orientation to each face
    orient = [None] * 6
    orient[0] = ((0, 0, 1), (0, -1, 0), (1, 0, 0))
    q = deque([0])
    while q:
        fi = q.popleft()
        n, u, ri = orient[fi]
        fr, fc = face_pos[fi]
        for d, (dfr, dfc) in enumerate([(0, 1), (1, 0), (0, -1), (-1, 0)]):
            nfr, nfc = fr + dfr, fc + dfc
            if (nfr, nfc) in face_at:
                nfi = face_at[(nfr, nfc)]
                if orient[nfi] is None:
                    if d == 0:
                        orient[nfi] = (ri, u, neg(n))
                    elif d == 1:
                        orient[nfi] = (neg(u), n, ri)
                    elif d == 2:
                        orient[nfi] = (neg(ri), u, n)
                    else:
                        orient[nfi] = (u, neg(n), ri)
                    q.append(nfi)

    normal_to_fi = {orient[i][0]: i for i in range(6)}

    def cube_wrap(r, c, d):
        nr, nc = r + DR[d], c + DC[d]
        fr, fc = r // S, c // S

        # Check if we stay on the same face
        if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != " ":
            nfr, nfc = nr // S, nc // S
            if (nfr, nfc) == (fr, fc):
                return nr, nc, d

        # Crossed a face boundary — use 3D orientation to find target
        fi = face_at[(fr, fc)]
        n, u, ri = orient[fi]

        dir_3d = [ri, neg(u), neg(ri), u][d]
        tfi = normal_to_fi[dir_3d]
        tn, tu, tr = orient[tfi]

        enter_3d = n  # original face's normal direction on the target face
        t_dirs = [tr, neg(tu), neg(tr), tu]
        enter_d = t_dirs.index(enter_3d)
        nd = (enter_d + 2) % 4

        lr, lc = r % S, c % S
        if d == 0: ep = lr
        elif d == 1: ep = lc
        elif d == 2: ep = S - 1 - lr
        else: ep = S - 1 - lc

        edge_along = [neg(u), ri, u, neg(ri)]
        target_along = [neg(tu), tr, tu, neg(tr)]
        if edge_along[d] != target_along[enter_d]:
            ep = S - 1 - ep

        if enter_d == 0: new_lr, new_lc = ep, S - 1
        elif enter_d == 1: new_lr, new_lc = S - 1, ep
        elif enter_d == 2: new_lr, new_lc = S - 1 - ep, 0
        else: new_lr, new_lc = 0, S - 1 - ep

        tfr, tfc = face_pos[tfi]
        return tfr * S + new_lr, tfc * S + new_lc, nd

    part2 = walk(cube_wrap)

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    """Yield frames showing the map."""
    parts = puzzle_input.split("\n\n")
    grid_lines = parts[0].split("\n")

    yield {
        "type": "text",
        "lines": [
            "  Monkey Map",
            "",
            f"  Grid: {len(grid_lines)} rows",
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
            f"  Part 1: {part1} (flat wrapping)",
            f"  Part 2: {part2} (cube wrapping)",
        ],
        "delay": 500,
    }
