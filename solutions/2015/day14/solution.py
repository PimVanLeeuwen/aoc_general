"""
Day 14 - Reindeer Olympics
Year: 2015

Race reindeer that alternate between flying and resting on fixed cycles.
"""


def parse(puzzle_input):
    reindeer = []
    for line in puzzle_input.strip().split("\n"):
        parts = line.split()
        name = parts[0]
        speed = int(parts[3])
        fly_time = int(parts[6])
        rest_time = int(parts[13])
        reindeer.append((name, speed, fly_time, rest_time))
    return reindeer


def distance_at(speed, fly_time, rest_time, t):
    cycle = fly_time + rest_time
    full_cycles = t // cycle
    remaining = min(t % cycle, fly_time)
    return speed * (full_cycles * fly_time + remaining)


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    reindeer = parse(puzzle_input)
    total_time = 2503

    # Part 1: max distance at t=2503
    part1 = max(distance_at(s, f, r, total_time) for _, s, f, r in reindeer)

    # Part 2: award 1 point per second to the leader(s)
    points = {name: 0 for name, _, _, _ in reindeer}
    for t in range(1, total_time + 1):
        distances = {name: distance_at(s, f, r, t) for name, s, f, r in reindeer}
        lead = max(distances.values())
        for name, d in distances.items():
            if d == lead:
                points[name] += 1

    part2 = max(points.values())

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    """Yield frames showing the reindeer race over time."""
    reindeer = parse(puzzle_input)
    total_time = 2503
    bar_width = 50

    points = {name: 0 for name, _, _, _ in reindeer}

    # Sample at regular intervals to keep frame count reasonable
    step = max(1, total_time // 80)
    times = list(range(step, total_time, step)) + [total_time]

    for t in times:
        # Update points for all seconds since last frame
        prev_t = t - step if t != times[0] else 0
        for sec in range(prev_t + 1, t + 1):
            distances = {name: distance_at(s, f, r, sec) for name, s, f, r in reindeer}
            lead = max(distances.values())
            for name, d in distances.items():
                if d == lead:
                    points[name] += 1

        distances = {name: distance_at(s, f, r, t) for name, s, f, r in reindeer}
        max_dist = max(distances.values()) or 1
        max_pts = max(points.values()) or 1

        lines = [
            f"  Reindeer Race — t = {t:>4d} / {total_time}",
            "",
            f"  {'Name':>10s}  {'Distance':>8s}  {'Pts':>5s}  Race",
        ]

        sorted_deer = sorted(reindeer, key=lambda r: distances[r[0]], reverse=True)
        for name, speed, fly_time, rest_time in sorted_deer:
            d = distances[name]
            p = points[name]
            bar_fill = round(d / max_dist * bar_width)
            bar = "█" * bar_fill + "░" * (bar_width - bar_fill)

            cycle_pos = t % (fly_time + rest_time)
            state = "✈" if cycle_pos < fly_time else "💤"

            lines.append(f"  {name:>10s}  {d:>7d}km  {p:>5d}  [{bar}] {state}")

        if t == total_time:
            dist_winner = max(distances, key=distances.get)
            pts_winner = max(points, key=points.get)
            lines.append("")
            lines.append(f"  ★ Part 1 (distance): {dist_winner} — {distances[dist_winner]} km")
            lines.append(f"  ★ Part 2 (points):   {pts_winner} — {points[pts_winner]} pts")

        yield {"type": "text", "lines": lines, "delay": 400 if t == total_time else 80}