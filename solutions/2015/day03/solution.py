"""
Day 03 - Perfectly Spherical Houses in a Vacuum
Year: 2015

Track which houses Santa visits on an infinite 2D grid.
"""

MOVES = {"^": (0, 1), "v": (0, -1), ">": (1, 0), "<": (-1, 0)}


def visited(directions: str) -> set[tuple[int, int]]:
    x, y = 0, 0
    houses = {(x, y)}
    for ch in directions:
        dx, dy = MOVES[ch]
        x, y = x + dx, y + dy
        houses.add((x, y))
    return houses


def solve(puzzle_input: str) -> tuple[str, str]:
    moves = puzzle_input.strip()

    # Part 1: Santa alone
    part1 = len(visited(moves))

    # Part 2: Santa and Robo-Santa alternate moves
    santa = visited(moves[0::2])
    robo  = visited(moves[1::2])
    part2 = len(santa | robo)

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    """Animate Santa's path on a grid, then replay with Robo-Santa."""
    moves = puzzle_input.strip()

    def frames(directions: str, label: str):
        x, y = 0, 0
        trail = [(x, y)]
        for ch in directions:
            dx, dy = MOVES[ch]
            x, y = x + dx, y + dy
            trail.append((x, y))

        visited_set = set()
        step = max(1, len(trail) // 200)

        for i in range(0, len(trail), step):
            pos = trail[i]
            visited_set.add(pos)

            # Build a small viewport around the bounding box of visited so far
            xs = [p[0] for p in visited_set]
            ys = [p[1] for p in visited_set]
            min_x, max_x = min(xs), max(xs)
            min_y, max_y = min(ys), max(ys)

            # Clamp viewport to 50×20
            cx, cy = pos
            vw, vh = 50, 20
            left  = cx - vw // 2
            right = left + vw
            top   = cy + vh // 2
            bot   = top - vh

            lines_out = [f"{label}  step {i + 1}/{len(trail)}  houses: {len(visited_set)}", ""]
            for row_y in range(top, bot - 1, -1):
                row = ""
                for col_x in range(left, right + 1):
                    if (col_x, row_y) == pos:
                        row += "S"
                    elif (col_x, row_y) == (0, 0):
                        row += "+"
                    elif (col_x, row_y) in visited_set:
                        row += "·"
                    else:
                        row += " "
                lines_out.append(row)

            yield {"type": "text", "lines": lines_out, "delay": 40}

        # Final frame
        yield {"type": "text", "lines": [
            f"{label}  done  houses visited: {len(visited_set)}"
        ], "delay": 800}

    yield from frames(moves, "Part 1 — Santa alone       ")
    yield from frames(moves[0::2], "Part 2 — Santa             ")
    yield from frames(moves[1::2], "Part 2 — Robo-Santa        ")