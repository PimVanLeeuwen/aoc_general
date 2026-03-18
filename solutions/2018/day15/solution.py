"""
Day 15 - Beverage Bandits
Year: 2018

Simulate a battle between Elves and Goblins in a cave.
Part 1: Outcome (rounds × remaining HP) of combat.
Part 2: Minimum Elf attack power for zero Elf deaths.
"""

# Reading order: up, left, right, down (sorted by (y, x))
DIRS = [(-1, 0), (0, -1), (0, 1), (1, 0)]


def parse(puzzle_input: str, elf_atk: int = 3):
    """Parse grid and units. Returns (walls, units) where units is {(y,x): [type, hp, atk]}."""
    lines = puzzle_input.strip().splitlines()
    walls = set()
    units = {}
    for y, row in enumerate(lines):
        for x, ch in enumerate(row):
            if ch == "#":
                walls.add((y, x))
            elif ch in "EG":
                atk = elf_atk if ch == "E" else 3
                units[(y, x)] = [ch, 200, atk]
    height = len(lines)
    width = max(len(row) for row in lines)
    return walls, units, height, width


def adjacent(pos):
    """Yield adjacent positions in reading order."""
    y, x = pos
    for dy, dx in DIRS:
        yield y + dy, x + dx


def find_move(start, targets, walls, occupied):
    """
    BFS to find the best move toward any target.
    Returns the first step to take, or None if no path exists.
    """
    if start in targets:
        return None  # Already at a target
    
    blocked = walls | occupied
    
    # Get all valid first moves
    first_moves = [pos for pos in adjacent(start) if pos not in blocked]
    if not first_moves:
        return None
    
    # Collect results: (first_move, distance, target_pos)
    best_moves = []
    
    for first_move in first_moves:
        # Check if first move is already adjacent to enemy
        if first_move in targets:
            best_moves.append((first_move, 1, first_move))
            continue
        
        # BFS from this first move
        seen = {start, first_move}
        stack = [pos for pos in adjacent(first_move) if pos not in blocked and pos not in seen]
        
        dist = 1
        found = False
        while stack and not found:
            dist += 1
            new_stack = []
            
            for tile in stack:
                if tile in seen:
                    continue
                seen.add(tile)
                
                if tile in targets:
                    best_moves.append((first_move, dist, tile))
                    found = True
                    continue
                
                # Add neighbors to explore next
                for nb in adjacent(tile):
                    if nb not in blocked and nb not in seen:
                        new_stack.append(nb)
            
            stack = list(set(new_stack))
    
    if not best_moves:
        return None
    
    # Sort by: (1) distance, (2) target position reading order, (3) first step reading order
    best_moves.sort(key=lambda x: (x[1], x[2], x[0]))
    
    return best_moves[0][0]


def run_combat(walls, units, stop_on_elf_death=False):
    """
    Run the combat simulation.
    Returns (rounds, total_hp, elf_died) and optionally yields frames.
    """
    units = {pos: list(u) for pos, u in units.items()}  # deep copy
    rounds = 0
    
    while True:
        # Process units in reading order
        turn_order = sorted(units.keys())
        moved_this_round = set()  # Track units that have taken their turn
        
        for pos in turn_order:
            if pos not in units:
                continue  # unit died earlier this round
            if pos in moved_this_round:
                continue  # another unit moved here; this position was already processed
            
            unit_type, hp, atk = units[pos]
            enemies = {p for p, u in units.items() if u[0] != unit_type}
            
            if not enemies:
                # Combat ends
                total_hp = sum(u[1] for u in units.values())
                return rounds, total_hp, False
            
            # Check if already in range
            in_range = [e for e in adjacent(pos) if e in enemies]
            
            if not in_range:
                # Need to move: find squares in range of enemies
                occupied = {p for p in units if p != pos}
                target_squares = set()
                for e in enemies:
                    for adj in adjacent(e):
                        if adj not in walls and adj not in occupied:
                            target_squares.add(adj)
                
                if target_squares:
                    move = find_move(pos, target_squares, walls, occupied)
                    if move:
                        # Move
                        del units[pos]
                        pos = move
                        units[pos] = [unit_type, hp, atk]
                        moved_this_round.add(pos)  # Mark new position as processed
                
                # Check again if in range after moving
                in_range = [e for e in adjacent(pos) if e in enemies]
            
            # Attack
            if in_range:
                # Select target with lowest HP, then reading order
                target = min(in_range, key=lambda e: (units[e][1], e))
                units[target][1] -= atk
                if units[target][1] <= 0:
                    killed_type = units[target][0]
                    del units[target]
                    if stop_on_elf_death and killed_type == "E":
                        return rounds, 0, True
        
        rounds += 1


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    # Part 1: Standard combat
    walls, units, _, _ = parse(puzzle_input)
    rounds, hp, _ = run_combat(walls, units)
    part1 = rounds * hp
    
    # Part 2: Find minimum elf attack power for no elf deaths
    elf_atk = 4
    while True:
        walls, units, _, _ = parse(puzzle_input, elf_atk)
        rounds, hp, elf_died = run_combat(walls, units, stop_on_elf_death=True)
        if not elf_died:
            part2 = rounds * hp
            break
        elf_atk += 1
    
    return str(part1), str(part2)


# ── Optional visualizer ────────────────────────────────────────────────────────

def visualize(puzzle_input: str):
    """Yield visualization frames for Day 15 combat."""
    walls, units_orig, height, width = parse(puzzle_input)
    units = {pos: list(u) for pos, u in units_orig.items()}
    
    COLORS = {
        "#": "#444444",  # walls
        ".": "#1a1a2e",  # floor
        "E": "#00ff41",  # elves
        "G": "#ff4444",  # goblins
        "X": "#ffaa00",  # combat highlight
    }
    
    def render(units_dict, highlight=None):
        cells = []
        for y in range(height):
            row = []
            for x in range(width):
                if (y, x) in walls:
                    row.append("#")
                elif (y, x) in units_dict:
                    row.append(units_dict[(y, x)][0])
                elif highlight and (y, x) in highlight:
                    row.append("X")
                else:
                    row.append(".")
            cells.append(row)
        return cells
    
    def unit_summary(units_dict):
        elves = [(p, u) for p, u in sorted(units_dict.items()) if u[0] == "E"]
        gobs = [(p, u) for p, u in sorted(units_dict.items()) if u[0] == "G"]
        return f"Elves: {len(elves)} ({sum(u[1] for _, u in elves)} HP)  Goblins: {len(gobs)} ({sum(u[1] for _, u in gobs)} HP)"
    
    # Initial state
    yield {
        "type": "grid",
        "cells": render(units),
        "colors": COLORS,
        "delay": 500,
    }
    
    rounds = 0
    frame_count = 1
    max_frames = 450  # Leave room for final frames
    
    while frame_count < max_frames:
        turn_order = sorted(units.keys())
        moved_this_round = set()
        combat_ended = False
        
        for pos in turn_order:
            if pos not in units:
                continue
            if pos in moved_this_round:
                continue
            
            unit_type, hp, atk = units[pos]
            enemies = {p for p, u in units.items() if u[0] != unit_type}
            
            if not enemies:
                combat_ended = True
                break
            
            in_range = [e for e in adjacent(pos) if e in enemies]
            
            if not in_range:
                occupied = {p for p in units if p != pos}
                target_squares = set()
                for e in enemies:
                    for adj in adjacent(e):
                        if adj not in walls and adj not in occupied:
                            target_squares.add(adj)
                
                if target_squares:
                    move = find_move(pos, target_squares, walls, occupied)
                    if move:
                        del units[pos]
                        pos = move
                        units[pos] = [unit_type, hp, atk]
                        moved_this_round.add(pos)
                
                in_range = [e for e in adjacent(pos) if e in enemies]
            
            if in_range:
                target = min(in_range, key=lambda e: (units[e][1], e))
                units[target][1] -= atk
                if units[target][1] <= 0:
                    del units[target]
        
        if combat_ended:
            break
        
        rounds += 1
        
        # Show every few rounds to stay under frame limit
        if rounds <= 5 or rounds % 3 == 0:
            yield {
                "type": "grid",
                "cells": render(units),
                "colors": COLORS,
                "delay": 150,
            }
            frame_count += 1
    
    # Final state
    total_hp = sum(u[1] for u in units.values())
    winner = "Elves" if any(u[0] == "E" for u in units.values()) else "Goblins"
    
    yield {
        "type": "grid",
        "cells": render(units),
        "colors": COLORS,
        "delay": 500,
    }
    
    yield {
        "type": "text",
        "lines": [
            "Combat Complete!",
            "",
            f"Winner: {winner}",
            f"Rounds: {rounds}",
            f"Remaining HP: {total_hp}",
            "",
            f"Part 1: {rounds} × {total_hp} = {rounds * total_hp}",
        ],
        "delay": 2000,
    }
    
    # Part 2 visualization
    yield {
        "type": "text",
        "lines": [
            "Part 2: Finding minimum Elf attack power...",
            "",
            "Goal: All Elves survive",
        ],
        "delay": 1000,
    }
    
    elf_atk = 4
    while elf_atk < 50:
        walls2, units2, _, _ = parse(puzzle_input, elf_atk)
        rounds2, hp2, elf_died = run_combat(walls2, units2, stop_on_elf_death=True)
        
        if not elf_died:
            yield {
                "type": "text",
                "lines": [
                    f"Success with attack power: {elf_atk}",
                    "",
                    f"Rounds: {rounds2}",
                    f"Remaining HP: {hp2}",
                    "",
                    f"Part 2: {rounds2} × {hp2} = {rounds2 * hp2}",
                ],
                "delay": 3000,
            }
            break
        
        elf_atk += 1
