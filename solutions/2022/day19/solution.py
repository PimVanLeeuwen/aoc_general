"""
Day 19 - Not Enough Minerals
Year: 2022

Optimize robot-building strategies to maximize geode production
under time constraints.
"""

import re
from math import ceil


def parse_blueprints(text):
    """Parse blueprints into cost tuples."""
    blueprints = []
    for line in text.strip().split("\n"):
        nums = list(map(int, re.findall(r"\d+", line)))
        blueprints.append({
            "id": nums[0],
            "ore_robot": nums[1],
            "clay_robot": nums[2],
            "obsidian_robot": (nums[3], nums[4]),
            "geode_robot": (nums[5], nums[6]),
        })
    return blueprints


def max_geodes(bp, time_limit):
    """Find maximum geodes producible with this blueprint."""
    max_ore_needed = max(
        bp["ore_robot"], bp["clay_robot"], bp["obsidian_robot"][0], bp["geode_robot"][0]
    )
    best = 0

    def dfs(minute, robots, ores):
        nonlocal best
        ore_r, clay_r, obs_r, geo_r = robots
        ore, clay, obs, geo = ores
        remaining = time_limit - minute + 1

        # Upper bound: current geodes + current geo robots * remaining + triangle number
        upper = geo + geo_r * remaining + remaining * (remaining - 1) // 2
        if upper <= best:
            return

        best = max(best, geo + geo_r * remaining)

        # Try building each robot type (skip to when we can afford it)
        # Geode robot
        if obs_r > 0:
            t_ore = max(0, ceil((bp["geode_robot"][0] - ore) / ore_r)) if ore < bp["geode_robot"][0] else 0
            t_obs = max(0, ceil((bp["geode_robot"][1] - obs) / obs_r)) if obs < bp["geode_robot"][1] else 0
            t = max(t_ore, t_obs) + 1
            if minute + t <= time_limit:
                dfs(
                    minute + t,
                    (ore_r, clay_r, obs_r, geo_r + 1),
                    (
                        ore + ore_r * t - bp["geode_robot"][0],
                        clay + clay_r * t,
                        obs + obs_r * t - bp["geode_robot"][1],
                        geo + geo_r * t,
                    ),
                )

        # Obsidian robot
        if clay_r > 0 and obs_r < bp["geode_robot"][1]:
            t_ore = max(0, ceil((bp["obsidian_robot"][0] - ore) / ore_r)) if ore < bp["obsidian_robot"][0] else 0
            t_clay = max(0, ceil((bp["obsidian_robot"][1] - clay) / clay_r)) if clay < bp["obsidian_robot"][1] else 0
            t = max(t_ore, t_clay) + 1
            if minute + t <= time_limit:
                dfs(
                    minute + t,
                    (ore_r, clay_r, obs_r + 1, geo_r),
                    (
                        ore + ore_r * t - bp["obsidian_robot"][0],
                        clay + clay_r * t - bp["obsidian_robot"][1],
                        obs + obs_r * t,
                        geo + geo_r * t,
                    ),
                )

        # Clay robot
        if clay_r < bp["obsidian_robot"][1]:
            t = max(0, ceil((bp["clay_robot"] - ore) / ore_r)) + 1 if ore < bp["clay_robot"] else 1
            if minute + t <= time_limit:
                dfs(
                    minute + t,
                    (ore_r, clay_r + 1, obs_r, geo_r),
                    (
                        ore + ore_r * t - bp["clay_robot"],
                        clay + clay_r * t,
                        obs + obs_r * t,
                        geo + geo_r * t,
                    ),
                )

        # Ore robot
        if ore_r < max_ore_needed:
            t = max(0, ceil((bp["ore_robot"] - ore) / ore_r)) + 1 if ore < bp["ore_robot"] else 1
            if minute + t <= time_limit:
                dfs(
                    minute + t,
                    (ore_r + 1, clay_r, obs_r, geo_r),
                    (
                        ore + ore_r * t - bp["ore_robot"],
                        clay + clay_r * t,
                        obs + obs_r * t,
                        geo + geo_r * t,
                    ),
                )

    dfs(1, (1, 0, 0, 0), (0, 0, 0, 0))
    return best


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    blueprints = parse_blueprints(puzzle_input)

    # Part 1: quality levels with 24 minutes
    part1 = sum(bp["id"] * max_geodes(bp, 24) for bp in blueprints)

    # Part 2: product of first 3 blueprints with 32 minutes
    part2 = 1
    for bp in blueprints[:3]:
        part2 *= max_geodes(bp, 32)

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    """Yield frames showing blueprint optimization."""
    blueprints = parse_blueprints(puzzle_input)

    yield {
        "type": "text",
        "lines": [
            "  Not Enough Minerals",
            "",
            f"  Blueprints: {len(blueprints)}",
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
            f"  Part 1: {part1} (quality level sum)",
            f"  Part 2: {part2} (product of first 3)",
        ],
        "delay": 500,
    }
