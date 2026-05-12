"""
Day 23 - Amphipod
Year: 2021

Organize amphipods into their home rooms with minimum energy
using Dijkstra's algorithm on the game state space.
"""

import heapq


COST = {"A": 1, "B": 10, "C": 100, "D": 1000}
HOME_COL = {"A": 3, "B": 5, "C": 7, "D": 9}
HALL_STOPS = [1, 2, 4, 6, 8, 10, 11]  # valid hallway resting positions


def parse_grid(text):
    """Extract amphipod positions from the grid as a frozen state."""
    lines = text.split("\n")
    pods = []
    for r, line in enumerate(lines):
        for c, ch in enumerate(line):
            if ch in "ABCD":
                pods.append((r, c, ch))
    return tuple(sorted(pods)), len(lines)


def is_goal(state, room_depth):
    """Check if all amphipods are in their home rooms."""
    for r, c, ch in state:
        if c != HOME_COL[ch] or r < 2 or r > 1 + room_depth:
            return False
    return True


def occupants(state):
    """Build a dict of (r, c) -> amphipod type."""
    return {(r, c): ch for r, c, ch in state}


def solve_amphipods(initial_state, room_depth):
    """Dijkstra over game states. Return minimum energy."""
    heap = [(0, initial_state)]
    visited = set()

    while heap:
        energy, state = heapq.heappop(heap)

        if state in visited:
            continue
        visited.add(state)

        if is_goal(state, room_depth):
            return energy

        occ = occupants(state)

        for i, (r, c, ch) in enumerate(state):
            home_col = HOME_COL[ch]

            # Generate all possible moves for this amphipod
            moves = []

            if r >= 2:
                # In a room — can move to hallway
                # Check path out of the room is clear
                if any((rr, c) in occ for rr in range(2, r)):
                    continue  # blocked above

                # But first: check if already home and settled
                if c == home_col:
                    # Home if all below are also correct type
                    if all(occ.get((rr, c)) == ch for rr in range(r, 2 + room_depth)):
                        continue  # already settled

                # Try each hallway position
                for hc in HALL_STOPS:
                    # Check hallway path is clear
                    step = 1 if hc > c else -1
                    if any((1, cc) in occ for cc in range(c + step, hc + step, step)):
                        continue
                    dist = (r - 1) + abs(hc - c)
                    moves.append((1, hc, dist))

            else:
                # In hallway (r == 1) — can only move into home room
                # Check hallway path to home column is clear
                step = 1 if home_col > c else -1
                if any((1, cc) in occ for cc in range(c + step, home_col + step, step)):
                    continue

                # Check room: must be empty or contain only correct type
                room_occ = [occ.get((rr, home_col)) for rr in range(2, 2 + room_depth)]
                if any(x is not None and x != ch for x in room_occ):
                    continue  # room has wrong types

                # Move to deepest available spot in the room
                target_row = 2
                for rr in range(1 + room_depth, 1, -1):
                    if (rr, home_col) not in occ:
                        target_row = rr
                        break

                dist = abs(home_col - c) + (target_row - 1)
                moves.append((target_row, home_col, dist))

            for nr, nc, dist in moves:
                cost = dist * COST[ch]
                # Build new state
                new_pods = list(state)
                new_pods[i] = (nr, nc, ch)
                new_state = tuple(sorted(new_pods))

                if new_state not in visited:
                    heapq.heappush(heap, (energy + cost, new_state))

    return -1


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    state1, _ = parse_grid(puzzle_input.strip())
    part1 = solve_amphipods(state1, 2)

    # Part 2: insert two extra rows between row 2 and row 3
    lines = puzzle_input.strip().split("\n")
    extra = ["  #D#C#B#A#", "  #D#B#A#C#"]
    lines2 = lines[:3] + extra + lines[3:]
    state2, _ = parse_grid("\n".join(lines2))
    part2 = solve_amphipods(state2, 4)

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    """Yield frames showing amphipod organization."""
    lines = puzzle_input.strip().split("\n")

    grid_display = [list(line.ljust(13)) for line in lines]
    colors = {
        "A": "#00ff41", "B": "#ffff00",
        "C": "#ff6600", "D": "#ff0000",
        "#": "#666666", ".": "#1a1a2e",
        " ": "#0f0f23",
    }

    yield {
        "type": "grid",
        "cells": grid_display,
        "colors": colors,
        "delay": 800,
    }

    part1, part2 = solve(puzzle_input)

    yield {
        "type": "text",
        "lines": [
            "  ===================================",
            "  Results",
            "  ===================================",
            "",
            f"  Part 1: {part1} (2-deep rooms)",
            f"  Part 2: {part2} (4-deep rooms)",
        ],
        "delay": 500,
    }
