"""
Day 10 - The Stars Align
Year: 2018

Fast-forward moving light points to the moment they spell a message; return the text and the time.
"""
import re


def parse(puzzle_input: str):
    points = []
    for line in puzzle_input.strip().split("\n"):
        x, y, vx, vy = map(int, re.findall(r'-?\d+', line))
        points.append((x, y, vx, vy))
    return points


def bounding_height(points: list, t: int) -> int:
    ys = [y + vy * t for _, y, _, vy in points]
    return max(ys) - min(ys)


def find_message_time(points: list) -> int:
    # The message appears when bounding box height is minimised — ternary search
    lo, hi = 0, 20000
    while hi - lo > 2:
        m1 = lo + (hi - lo) // 3
        m2 = hi - (hi - lo) // 3
        if bounding_height(points, m1) < bounding_height(points, m2):
            hi = m2
        else:
            lo = m1
    return min(range(lo, hi + 1), key=lambda t: bounding_height(points, t))


def render(points: list, t: int) -> list[str]:
    xs = [x + vx * t for x, _, vx, _ in points]
    ys = [y + vy * t for _, y, _, vy in points]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    lit = set(zip(xs, ys))
    return [
        "".join("#" if (min_x + c, min_y + r) in lit else "."
                for c in range(max_x - min_x + 1))
        for r in range(max_y - min_y + 1)
    ]


def solve(puzzle_input: str) -> tuple[str, str]:
    points = parse(puzzle_input)
    t = find_message_time(points)
    message_lines = render(points, t)
    # Part 1: the visual message (rendered as ASCII art block)
    part1 = "\n".join(message_lines)
    part2 = str(t)
    return part1, part2


# ── Optional visualizer ────────────────────────────────────────────────────────

def visualize(puzzle_input: str):
    points = parse(puzzle_input)
    t_msg = find_message_time(points)

    # ── Show convergence: sample a window of frames around the message ─────────
    WINDOW = 12        # frames before and after the message
    STEP   = max(1, t_msg // 20)   # coarser steps early on

    # Fast approach: show a few frames at broad intervals, then zoom in
    sample_times = (
        list(range(0, max(0, t_msg - WINDOW * 3), STEP))[:8]
        + list(range(max(0, t_msg - WINDOW), t_msg + WINDOW + 1))
    )
    sample_times = sorted(set(sample_times))

    for t in sample_times:
        xs = [x + vx * t for x, _, vx, _ in points]
        ys = [y + vy * t for _, y, _, vy in points]
        height = max(ys) - min(ys)
        width  = max(xs) - min(xs)

        if t == t_msg:
            grid_lines = render(points, t)
            yield {
                "type": "text",
                "lines": [
                    f"t = {t:,}s  ← MESSAGE APPEARS",
                    f"Bounding box: {width} × {height}",
                    "",
                ] + grid_lines,
                "delay": 3000,
            }
        else:
            # Show a downscaled dot-cloud so the user can see the convergence
            COLS, ROWS = 60, 16
            if width > 0 and height > 0:
                cell = set()
                for x, y in zip(xs, ys):
                    cx = (x - min(xs)) * (COLS - 1) // width
                    cy = (y - min(ys)) * (ROWS - 1) // height
                    cell.add((cx, cy))
                grid = [
                    "".join("█" if (c, r) in cell else " "
                            for c in range(COLS))
                    for r in range(ROWS)
                ]
            else:
                grid = ["(all points collapsed)"]

            dist_to_msg = abs(t - t_msg)
            yield {
                "type": "text",
                "lines": [
                    f"t = {t:,}s  (message at t = {t_msg:,}s,  Δ={dist_to_msg:,})",
                    f"Bounding box: {width:,} × {height:,}",
                    "",
                ] + grid,
                "delay": 150 if dist_to_msg > WINDOW else 400,
            }

    # ── Final frame: clean message render ─────────────────────────────────────
    yield {
        "type": "text",
        "lines": [
            "The Stars Align!",
            f"Message appears at t = {t_msg}s",
            "",
        ] + render(points, t_msg),
        "delay": 5000,
    }
