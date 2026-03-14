"""
Day 06 - Chronal Coordinates
Year: 2018

Find the largest finite Voronoi region using Manhattan distance,
then find the region where the total distance to all coordinates is under a threshold.
"""


def parse(puzzle_input: str):
    coords = []
    for line in puzzle_input.strip().split("\n"):
        x, y = line.split(", ")
        coords.append((int(x), int(y)))
    return coords


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    coords = parse(puzzle_input)

    min_x = min(x for x, y in coords)
    max_x = max(x for x, y in coords)
    min_y = min(y for x, y in coords)
    max_y = max(y for x, y in coords)

    # Part 1: largest finite Voronoi region
    area = {}
    infinite = set()

    for gx in range(min_x, max_x + 1):
        for gy in range(min_y, max_y + 1):
            dists = sorted(
                (abs(gx - x) + abs(gy - y), i)
                for i, (x, y) in enumerate(coords)
            )
            if dists[0][0] != dists[1][0]:  # unique closest
                owner = dists[0][1]
                area[owner] = area.get(owner, 0) + 1
                if gx in (min_x, max_x) or gy in (min_y, max_y):
                    infinite.add(owner)

    part1 = max(v for k, v in area.items() if k not in infinite)

    # Part 2: region where sum of distances to all coords < 10000
    threshold = 10000
    part2 = sum(
        1
        for gx in range(min_x, max_x + 1)
        for gy in range(min_y, max_y + 1)
        if sum(abs(gx - x) + abs(gy - y) for x, y in coords) < threshold
    )

    return str(part1), str(part2)


# ── Optional visualizer ────────────────────────────────────────────────────────

def visualize(puzzle_input: str):
    """Yield visualization frames for Day 06."""
    coords = parse(puzzle_input)

    min_x = min(x for x, y in coords)
    max_x = max(x for x, y in coords)
    min_y = min(y for x, y in coords)
    max_y = max(y for x, y in coords)

    width = max_x - min_x + 1
    height = max_y - min_y + 1

    # --- Build Voronoi ownership grid ---
    owner_grid = []   # None = tie, else index
    infinite = set()
    area = {}

    for gy in range(min_y, max_y + 1):
        row = []
        for gx in range(min_x, max_x + 1):
            dists = sorted(
                (abs(gx - x) + abs(gy - y), i)
                for i, (x, y) in enumerate(coords)
            )
            if dists[0][0] == dists[1][0]:
                row.append(None)
            else:
                owner = dists[0][1]
                row.append(owner)
                area[owner] = area.get(owner, 0) + 1
                if gx in (min_x, max_x) or gy in (min_y, max_y):
                    infinite.add(owner)
        owner_grid.append(row)

    # A palette of distinct colors for up to ~50 coords
    PALETTE = [
        "#e63946", "#457b9d", "#2a9d8f", "#e9c46a", "#f4a261",
        "#264653", "#8ecae6", "#a8dadc", "#c77dff", "#80b918",
        "#f77f00", "#d62828", "#023e8a", "#48cae4", "#b5e48c",
        "#ffb703", "#fb8500", "#6d6875", "#b5838d", "#e5989b",
        "#00b4d8", "#90e0ef", "#caf0f8", "#d4e09b", "#f6f4d2",
        "#cbdfbd", "#f19c79", "#a44a3f", "#3d405b", "#81b29a",
    ]

    def owner_color(owner):
        if owner is None:
            return "#1a1a2e"
        if owner in infinite:
            # muted version
            base = PALETTE[owner % len(PALETTE)]
            return base + "88"  # semi-transparent feel via darker tone
        return PALETTE[owner % len(PALETTE)]

    # Frame 1: show all coordinate points on blank grid
    intro_cells = [["." for _ in range(width)] for _ in range(height)]
    for i, (x, y) in enumerate(coords):
        cx, cy = x - min_x, y - min_y
        intro_cells[cy][cx] = str(i % 10)

    yield {
        "type": "text",
        "lines": [
            "Part 1 — Chronal Coordinates",
            "",
            f"Grid size : {width} × {height}",
            f"Coords    : {len(coords)}",
            "",
            "Computing Voronoi regions (Manhattan distance)...",
        ],
        "delay": 800,
    }

    # Frame 2: full Voronoi grid colored
    color_map = {}
    cells = []
    for gy in range(height):
        row = []
        for gx in range(width):
            owner = owner_grid[gy][gx]
            # Check if this is an actual coordinate point
            real_x = gx + min_x
            real_y = gy + min_y
            if (real_x, real_y) in coords:
                ch = "■"
                color_map["■"] = "#ffffff"
            elif owner is None:
                ch = "·"
                color_map["·"] = "#1a1a2e"
            else:
                ch = chr(ord("a") + (owner % 26))
                color_map[ch] = owner_color(owner)
            row.append(ch)
        cells.append(row)

    yield {
        "type": "grid",
        "cells": cells,
        "colors": color_map,
        "delay": 1200,
    }

    # Frame 3: highlight only finite regions
    finite_cells = []
    for gy in range(height):
        row = []
        for gx in range(width):
            owner = owner_grid[gy][gx]
            real_x = gx + min_x
            real_y = gy + min_y
            if (real_x, real_y) in coords:
                ch = "■"
            elif owner is None or owner in infinite:
                ch = "·"
            else:
                ch = chr(ord("a") + (owner % 26))
            row.append(ch)
        finite_cells.append(row)

    finite_color_map = dict(color_map)
    finite_color_map["·"] = "#0d0d1a"

    yield {
        "type": "grid",
        "cells": finite_cells,
        "colors": finite_color_map,
        "delay": 1200,
    }

    best_owner = max((k for k in area if k not in infinite), key=lambda k: area[k])
    best_area = area[best_owner]

    yield {
        "type": "text",
        "lines": [
            "Part 1 — Voronoi complete",
            "",
            f"Total regions   : {len(area)}",
            f"Infinite regions: {len(infinite)}",
            f"Finite regions  : {len(area) - len(infinite)}",
            "",
            f"Largest finite area: {best_area}",
            "",
            f"Answer: {best_area}",
        ],
        "delay": 1500,
    }

    # --- Part 2: total distance region ---
    threshold = 10000

    yield {
        "type": "text",
        "lines": [
            "Part 2 — Safe Region",
            "",
            f"Threshold: sum of distances < {threshold:,}",
            "",
            "Computing total-distance grid...",
        ],
        "delay": 800,
    }

    # Build safe region grid
    safe_cells = []
    safe_count = 0
    for gy in range(min_y, max_y + 1):
        row = []
        for gx in range(min_x, max_x + 1):
            total = sum(abs(gx - x) + abs(gy - y) for x, y in coords)
            real_x, real_y = gx, gy
            if (real_x, real_y) in coords:
                row.append("■")
            elif total < threshold:
                row.append("#")
                safe_count += 1
            else:
                row.append("·")
        safe_cells.append(row)

    safe_color_map = {
        "#": "#00ff41",
        "·": "#0d0d1a",
        "■": "#ffffff",
    }

    yield {
        "type": "grid",
        "cells": safe_cells,
        "colors": safe_color_map,
        "delay": 1500,
    }

    yield {
        "type": "text",
        "lines": [
            "Part 2 — Safe Region complete",
            "",
            f"Threshold       : < {threshold:,}",
            f"Safe locations  : {safe_count:,}",
            "",
            f"Answer: {safe_count}",
        ],
        "delay": 2000,
    }
