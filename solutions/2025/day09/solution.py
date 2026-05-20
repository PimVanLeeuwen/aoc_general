"""
Day 9 - Polygon Rectangles
Year: 2025

Given polygon vertices, find the largest axis-aligned rectangle
from vertex pairs (part 1: by area, part 2: fully inside polygon).
"""


def precompute_inside_set(polygon, vertex_set, query_xs, query_ys):
    """Precompute which (x, y) combinations from query_xs × query_ys
    are inside or on the boundary of the polygon.

    Uses ray-casting with precomputed x-crossings per y-value for speed.
    """
    n = len(polygon)
    inside = set()

    # For each unique query y-value, compute all x-crossings of polygon edges
    for py in query_ys:
        # Compute x-intercepts using standard ray-cast rules
        crossings = []
        for i in range(n):
            j = (i + 1) % n
            y1, y2 = polygon[i][1], polygon[j][1]
            x1, x2 = polygon[i][0], polygon[j][0]
            # Standard rule: count edge if it straddles py
            # (one endpoint strictly above, one at or below)
            if y1 == y2:
                # Horizontal edge: check if py matches and if query x is on it
                if y1 == py:
                    lo_x, hi_x = (x1, x2) if x1 <= x2 else (x2, x1)
                    for px in query_xs:
                        if lo_x <= px <= hi_x:
                            inside.add((px, py))
                continue
            if not ((y1 <= py < y2) or (y2 <= py < y1)):
                continue
            # x-intercept at py
            t = (py - y1) / (y2 - y1)
            x_cross = x1 + t * (x2 - x1)
            crossings.append(x_cross)

        crossings.sort()

        # For each query x at this y, count crossings to the right
        for px in query_xs:
            if (px, py) in inside:
                continue  # Already marked from horizontal edge
            count = 0
            for cx in crossings:
                if cx > px + 1e-9:
                    count += 1
                elif abs(cx - px) < 1e-9:
                    inside.add((px, py))
                    count = -1  # Signal: on boundary
                    break
            if count >= 0 and count % 2 == 1:
                inside.add((px, py))

    # Add all polygon vertices
    inside.update(vertex_set)
    return inside


def segments_intersect(ax1, ay1, ax2, ay2, bx1, by1, bx2, by2):
    """Check if two line segments properly intersect (crossing, not touching)."""
    d1 = (bx2 - bx1) * (ay1 - by1) - (by2 - by1) * (ax1 - bx1)
    d2 = (bx2 - bx1) * (ay2 - by1) - (by2 - by1) * (ax2 - bx1)
    d3 = (ax2 - ax1) * (by1 - ay1) - (ay2 - ay1) * (bx1 - ax1)
    d4 = (ax2 - ax1) * (by2 - ay1) - (ay2 - ay1) * (bx2 - ax1)
    if ((d1 > 0 and d2 < 0) or (d1 < 0 and d2 > 0)) and \
       ((d3 > 0 and d4 < 0) or (d3 < 0 and d4 > 0)):
        return True
    return False


def solve(puzzle_input: str) -> tuple[str, str]:
    lines = puzzle_input.strip().split("\n")
    points = [tuple(map(int, line.strip().split(","))) for line in lines]
    polygon = list(points)
    vertex_set = set(points)
    n = len(points)

    # Precompute polygon edges with bounding boxes
    poly_edges = []
    for i in range(n):
        j = (i + 1) % n
        px1, py1 = polygon[i]
        px2, py2 = polygon[j]
        poly_edges.append((px1, py1, px2, py2,
                           min(px1, px2), min(py1, py2),
                           max(px1, px2), max(py1, py2)))

    # Part 1: largest rectangle area from any two vertex pairs
    part1 = 0
    for i in range(n):
        x1, y1 = points[i]
        for j in range(i + 1, n):
            x2, y2 = points[j]
            area = (abs(x1 - x2) + 1) * (abs(y1 - y2) + 1)
            if area > part1:
                part1 = area

    # Part 2: largest rectangle fully inside the polygon
    # Precompute which (x_i, y_j) combinations are inside the polygon
    xs = sorted(set(px for px, _ in points))
    ys_pts = sorted(set(py for _, py in points))
    inside_cache = precompute_inside_set(polygon, vertex_set, xs, ys_pts)

    # Build candidates sorted by area descending
    candidates = []
    for i in range(n):
        x1, y1 = points[i]
        for j in range(i + 1, n):
            x2, y2 = points[j]
            min_x = x1 if x1 < x2 else x2
            max_x = x2 if x1 < x2 else x1
            min_y = y1 if y1 < y2 else y2
            max_y = y2 if y1 < y2 else y1
            # All 4 corners must be inside — check via precomputed cache
            if (min_x, min_y) not in inside_cache or \
               (max_x, min_y) not in inside_cache or \
               (max_x, max_y) not in inside_cache or \
               (min_x, max_y) not in inside_cache:
                continue
            area = (max_x - min_x + 1) * (max_y - min_y + 1)
            candidates.append((area, min_x, min_y, max_x, max_y))

    candidates.sort(reverse=True)

    part2 = 0
    for area, min_x, min_y, max_x, max_y in candidates:
        if area <= part2:
            break

        # Check no polygon edge crosses any rect edge
        valid = True
        rect_edges = [
            (min_x, min_y, max_x, min_y),
            (max_x, min_y, max_x, max_y),
            (max_x, max_y, min_x, max_y),
            (min_x, max_y, min_x, min_y),
        ]
        for px1, py1, px2, py2, e_min_x, e_min_y, e_max_x, e_max_y in poly_edges:
            if e_max_x < min_x or e_min_x > max_x or \
               e_max_y < min_y or e_min_y > max_y:
                continue
            for rx1, ry1, rx2, ry2 in rect_edges:
                if segments_intersect(px1, py1, px2, py2, rx1, ry1, rx2, ry2):
                    valid = False
                    break
            if not valid:
                break

        if valid:
            part2 = area
            break

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    lines = puzzle_input.strip().split("\n")
    points = [tuple(map(int, line.strip().split(","))) for line in lines]

    yield {
        "type": "text",
        "lines": [
            "  Polygon Rectangles",
            "",
            f"  Vertices: {len(points)}",
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
            f"  Part 1: {part1} (max rectangle area)",
            f"  Part 2: {part2} (max inscribed area)",
        ],
        "delay": 500,
    }
