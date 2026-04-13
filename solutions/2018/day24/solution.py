"""
Day 24 - Immune System Simulator 20XX
Year: 2018

It’s a battle simulation between two armies, Immune System and Infection,
each made of groups with units, hit points, attack types, weaknesses, and initiative.
Every round, groups first select targets based on how much damage they could deal,
then attack in order of initiative, killing units according to calculated damage.
The fight repeats until one army has no units left, and your task is to run this simulation
using your input and report how many units survive on the winning side.
"""

import re
from copy import deepcopy


class Group:
    """Class representing a single group in an army"""
    def __init__(self, army, units, hp, weak, immune, dmg, dmg_type, init):
        self.army = army
        self.units = units
        self.hp = hp
        self.weak = weak
        self.immune = immune
        self.dmg = dmg
        self.dmg_type = dmg_type
        self.init = init

    @property
    def power(self):
        return self.units * self.dmg

    def damage_to(self, other):
        if self.dmg_type in other.immune:
            return 0
        dmg = self.power
        if self.dmg_type in other.weak:
            dmg *= 2
        return dmg

    def __repr__(self):
        return f"{self.army}({self.units}u, {self.power}p, init {self.init})"

def apply_boost(armies, boost):
    copy_army = deepcopy(armies)
    for g in copy_army["Immune System"]:
        g.dmg += boost
    return copy_army

def parse_armies(lines):
    armies = {"Immune System": [], "Infection": []}
    army = None
    pattern = re.compile(
        r"(\d+) units each with (\d+) hit points(?: \((.*?)\))?"
        r" with an attack that does (\d+) (\w+) damage at initiative (\d+)"
    )

    for line in lines:
        if line.endswith(":"):
            army = line[:-1]
            continue
        if not line.strip():
            continue

        m = pattern.match(line)
        units, hp = int(m.group(1)), int(m.group(2))
        special = m.group(3)
        dmg, dmg_type = int(m.group(4)), m.group(5)
        init = int(m.group(6))

        weak, immune = set(), set()
        if special:
            for part in special.split("; "):
                if part.startswith("weak to "):
                    weak = set(part[len("weak to "):].split(", "))
                elif part.startswith("immune to "):
                    immune = set(part[len("immune to "):].split(", "))

        armies[army].append(Group(army, units, hp, weak, immune, dmg, dmg_type, init))

    return armies

def fight(armies):
    """Simulate battle. Returns (winner, total_units) or (None, None) if stalemated."""
    armies = deepcopy(armies)

    while True:
        all_groups = [g for army in armies.values() for g in army if g.units > 0]

        # Target selection
        all_groups.sort(key=lambda g: (-g.power, -g.init))
        chosen = set()
        targets = {}

        for g in all_groups:
            enemies = [e for e in all_groups if e.army != g.army and e not in chosen and e.units > 0]
            if not enemies:
                continue

            # Choose best target
            enemies.sort(
                key=lambda e: (g.damage_to(e), e.power, e.init),
                reverse=True
            )
            if g.damage_to(enemies[0]) > 0:
                targets[g] = enemies[0]
                chosen.add(enemies[0])

        # Attacking
        before_units = sum(g.units for g in all_groups)
        for g in sorted(all_groups, key=lambda g: -g.init):
            if g.units <= 0 or g not in targets:
                continue
            target = targets[g]
            dmg = g.damage_to(target)
            killed = min(target.units, dmg // target.hp)
            target.units -= killed

        after_units = sum(g.units for g in all_groups)
        if after_units == before_units:
            return None, None  # stalemate

        # Check victory
        alive_armies = {g.army for g in all_groups if g.units > 0}
        if len(alive_armies) == 1:
            winner = alive_armies.pop()
            total = sum(g.units for g in all_groups if g.units > 0)
            return winner, total

def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    lines = puzzle_input.strip().split("\n")

    armies = parse_armies(lines)

    # Part 1
    _, part1_units = fight(armies)
    part1 = str(part1_units)

    lo, hi = 1, 2000
    part2 = None

    while lo <= hi:
        mid = (lo + hi) // 2
        winner, units = fight(apply_boost(armies, mid))
        if winner == "Immune System":
            part2 = units
            hi = mid - 1
        else:
            lo = mid + 1

    return part1, str(part2)


# ── Optional visualizer ────────────────────────────────────────────────────────
# Uncomment and implement to enable the Visualization tab in the portfolio.
#
# def visualize(puzzle_input: str):
#     """Yield visualization frames (up to ~500 recommended)."""
#     lines = puzzle_input.strip().split("\n")
#
#     # Grid frame – renders as a pixel canvas:
#     yield {
#         "type": "grid",
#         "cells": [list(row) for row in lines],
#         "colors": {"#": "#00ff41", ".": "#0f0f23"},   # cell → hex color
#         "delay": 100,   # ms before advancing to next frame
#     }
#
#     # Text frame – renders as monospace text:
#     yield {
#         "type": "text",
#         "lines": ["Step 1", "Value: 42"],
#         "delay": 300,
#     }
