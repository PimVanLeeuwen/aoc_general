"""
Day 02 - I Was Told There Would Be No Math
Year: 2015

Calculate wrapping paper and ribbon needed for a list of box dimensions.
"""
from dataclasses import dataclass


@dataclass
class Box:
    w: int
    h: int
    l: int

    def sides(self) -> tuple[int, int, int]:
        return self.w * self.h, self.w * self.l, self.h * self.l

    def paper_needed(self) -> int:
        areas = self.sides()
        return 2 * sum(areas) + min(areas)

    def ribbon_needed(self) -> int:
        dims = sorted([self.w, self.h, self.l])
        return 2 * (dims[0] + dims[1]) + self.w * self.h * self.l


def solve(puzzle_input: str) -> tuple[str, str]:
    lines = puzzle_input.strip().split("\n")
    boxes = [Box(*map(int, line.split("x"))) for line in lines]

    part1 = sum(b.paper_needed() for b in boxes)
    part2 = sum(b.ribbon_needed() for b in boxes)

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    """Show a running tally of paper and ribbon as each box is processed."""
    lines = puzzle_input.strip().split("\n")
    boxes = [Box(*map(int, line.split("x"))) for line in lines]

    total_paper = 0
    total_ribbon = 0
    total_boxes = len(boxes)

    # Sample at most 200 frames
    step = max(1, total_boxes // 200)

    for i, box in enumerate(boxes):
        total_paper += box.paper_needed()
        total_ribbon += box.ribbon_needed()

        if i % step != 0 and i != total_boxes - 1:
            continue

        progress = (i + 1) / total_boxes
        bar_width = 40
        filled = int(bar_width * progress)
        progress_bar = "█" * filled + "░" * (bar_width - filled)

        yield {
            "type": "text",
            "lines": [
                f"Box {i + 1:>5} / {total_boxes}",
                f"  Dimensions : {box.w}x{box.h}x{box.l}",
                f"  Paper      : {box.paper_needed():>8} sq ft",
                f"  Ribbon     : {box.ribbon_needed():>8} ft",
                "",
                f"[{progress_bar}] {progress * 100:.1f}%",
                "",
                f"  Total paper  : {total_paper:>10} sq ft",
                f"  Total ribbon : {total_ribbon:>10} ft",
            ],
            "delay": 30,
        }
