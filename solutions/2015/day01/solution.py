"""
Day 01 - Not Quite Lisp
Year: 2015

Santa follows a string of parentheses to navigate floors of a building.
'(' means go up one floor, ')' means go down one floor.
"""


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    line = puzzle_input.strip().split("\n")[0].strip()

    floor = 0
    part2 = 0

    for i, c in enumerate(line):
        floor += 1 if c == '(' else -1
        if floor < 0 and part2 == 0:
            part2 = i + 1

    return str(floor), str(part2)


def visualize(puzzle_input: str):
    """Animate Santa's floor journey step by step."""
    line = puzzle_input.strip().split("\n")[0].strip()

    # Sample at most 300 steps so the animation stays watchable
    step = max(1, len(line) // 300)

    floor = 0
    basement_pos = None
    history = [0]

    for i, c in enumerate(line):
        floor += 1 if c == '(' else -1
        if floor < 0 and basement_pos is None:
            basement_pos = i + 1
        history.append(floor)

    final_floor = floor

    width = 60   # chart columns
    chart_h = 12  # visible rows in the chart window

    def render_frame(up_to: int) -> list[str]:
        """Render a bar-chart style text frame up to step index `up_to`."""
        current = history[up_to]
        lines_out = [f"Step {up_to:>6} / {len(line)}   Floor: {current:>+4}", ""]

        # Sparkline: sample `width` points from history[0..up_to]
        sample_len = up_to + 1
        samples = []
        for col in range(width):
            idx = int(col * (sample_len - 1) / max(width - 1, 1)) if sample_len > 1 else 0
            samples.append(history[idx])

        # Fixed-height window centered on current floor, always including 0
        half = chart_h // 2
        win_top = max(current + half, half)        # at least show floor 0
        win_bot = win_top - chart_h + 1

        # Draw rows from win_top down to win_bot
        for row_floor in range(win_top, win_bot - 1, -1):
            row = ""
            for col, val in enumerate(samples):
                if row_floor == 0:
                    ch = "─"
                else:
                    ch = " "
                if 0 < row_floor <= val:
                    ch = "█"
                elif 0 > row_floor >= val:
                    ch = "█"
                row += ch
            label = f" {row_floor:>+3}" if row_floor % 5 == 0 or row_floor == 0 else "    "
            lines_out.append(row + label)

        lines_out.append("")
        if basement_pos is not None and up_to >= basement_pos:
            lines_out.append(f"First entered basement at step {basement_pos}.")
        if up_to == len(line):
            lines_out.append(f"Final floor: {final_floor:+d}")

        return lines_out

    # Emit frames
    for i in range(0, len(line) + 1, step):
        yield {
            "type": "text",
            "lines": render_frame(i),
            "delay": 40,
        }

    # Always emit the final frame
    yield {
        "type": "text",
        "lines": render_frame(len(line)),
        "delay": 1000,
    }
