"""
Day 21 - RPG Simulator 20XX
Year: 2015

Find the optimal equipment loadout for a boss fight — cheapest win and
most expensive loss.
"""

from itertools import combinations
import math

WEAPONS = [
    (8, 4, 0),   # Dagger
    (10, 5, 0),  # Shortsword
    (25, 6, 0),  # Warhammer
    (40, 7, 0),  # Longsword
    (74, 8, 0),  # Greataxe
]

ARMORS = [
    (0, 0, 0),    # No armor
    (13, 0, 1),   # Leather
    (31, 0, 2),   # Chainmail
    (53, 0, 3),   # Splintmail
    (75, 0, 4),   # Bandedmail
    (102, 0, 5),  # Platemail
]

RINGS = [
    (25, 1, 0),   # Damage +1
    (50, 2, 0),   # Damage +2
    (100, 3, 0),  # Damage +3
    (20, 0, 1),   # Defense +1
    (40, 0, 2),   # Defense +2
    (80, 0, 3),   # Defense +3
]


def parse_boss(text):
    """Parse boss stats from puzzle input."""
    nums = []
    for line in text.strip().splitlines():
        nums.append(int(line.split(": ")[1]))
    return nums[0], nums[1], nums[2]


def player_wins(player_hp, player_dmg, player_armor, boss_hp, boss_dmg, boss_armor):
    """Returns True if player wins. Player goes first."""
    player_dpt = max(1, player_dmg - boss_armor)
    boss_dpt = max(1, boss_dmg - player_armor)
    player_turns_to_kill = math.ceil(boss_hp / player_dpt)
    boss_turns_to_kill = math.ceil(player_hp / boss_dpt)
    return player_turns_to_kill <= boss_turns_to_kill


def all_loadouts():
    """Generate all valid (cost, damage, armor) loadouts."""
    ring_combos = [()]
    ring_combos += [(r,) for r in RINGS]
    ring_combos += list(combinations(RINGS, 2))

    for w_cost, w_dmg, w_arm in WEAPONS:
        for a_cost, a_dmg, a_arm in ARMORS:
            for ring_set in ring_combos:
                cost = w_cost + a_cost + sum(r[0] for r in ring_set)
                dmg = w_dmg + a_dmg + sum(r[1] for r in ring_set)
                arm = w_arm + a_arm + sum(r[2] for r in ring_set)
                yield cost, dmg, arm


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    boss_hp, boss_dmg, boss_armor = parse_boss(puzzle_input)

    min_cost_win = float('inf')
    max_cost_lose = 0

    for cost, dmg, arm in all_loadouts():
        if player_wins(100, dmg, arm, boss_hp, boss_dmg, boss_armor):
            min_cost_win = min(min_cost_win, cost)
        else:
            max_cost_lose = max(max_cost_lose, cost)

    return str(min_cost_win), str(max_cost_lose)


def visualize(puzzle_input: str):
    """Yield frames showing the equipment optimization search."""
    boss_hp, boss_dmg, boss_armor = parse_boss(puzzle_input)

    loadouts = list(all_loadouts())
    wins = []
    losses = []

    for cost, dmg, arm in loadouts:
        if player_wins(100, dmg, arm, boss_hp, boss_dmg, boss_armor):
            wins.append((cost, dmg, arm))
        else:
            losses.append((cost, dmg, arm))

    wins.sort(key=lambda x: x[0])
    losses.sort(key=lambda x: -x[0])

    yield {
        "type": "text",
        "lines": [
            "  RPG Simulator 20XX",
            "",
            f"  Boss: {boss_hp} HP, {boss_dmg} DMG, {boss_armor} ARM",
            f"  Player: 100 HP + equipment",
            "",
            f"  Total loadouts to evaluate: {len(loadouts)}",
        ],
        "delay": 800,
    }

    checked = 0
    best_win = float('inf')
    worst_lose = 0
    step = max(1, len(loadouts) // 30)

    for cost, dmg, arm in loadouts:
        checked += 1
        win = player_wins(100, dmg, arm, boss_hp, boss_dmg, boss_armor)
        if win:
            best_win = min(best_win, cost)
        else:
            worst_lose = max(worst_lose, cost)

        if checked % step == 0:
            pct = checked * 100 // len(loadouts)
            bar_w = 30
            fill = checked * bar_w // len(loadouts)
            bar = "=" * fill + ">" + " " * (bar_w - fill - 1)

            lines = [
                "  Searching equipment combinations...",
                "",
                f"  [{bar}] {pct}%",
                f"  Checked: {checked} / {len(loadouts)}",
                "",
            ]
            if best_win < float('inf'):
                lines.append(f"  Cheapest win so far:     {best_win:>3} gold")
            else:
                lines.append(f"  Cheapest win so far:       ---")
            if worst_lose > 0:
                lines.append(f"  Most expensive loss:     {worst_lose:>3} gold")
            else:
                lines.append(f"  Most expensive loss:       ---")

            yield {"type": "text", "lines": lines, "delay": 80}

    yield {
        "type": "text",
        "lines": [
            "  ===================================",
            "  Top 5 cheapest WINNING loadouts:",
            "  -----------------------------------",
        ]
        + [f"    {c:>3}g  ->  {d} DMG, {a} ARM" for c, d, a in wins[:5]]
        + [
            "",
            "  Top 5 most expensive LOSING loadouts:",
            "  -----------------------------------",
        ]
        + [f"    {c:>3}g  ->  {d} DMG, {a} ARM" for c, d, a in losses[:5]],
        "delay": 600,
    }

    yield {
        "type": "text",
        "lines": [
            "  ===================================",
            "  Results",
            "  ===================================",
            "",
            f"  Part 1: {wins[0][0]} gold (cheapest win)",
            f"  Part 2: {losses[0][0]} gold (priciest loss)",
        ],
        "delay": 500,
    }
