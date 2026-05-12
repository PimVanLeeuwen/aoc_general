"""
Day 25 - Cryostasis
Year: 2019

Explore Santa's ship as a text adventure via Intcode, collect items,
and find the right combination to pass the pressure-sensitive floor.
"""

import re
from collections import deque
from itertools import combinations
from intcode import IntcodeComputer

REVERSE = {"north": "south", "south": "north", "east": "west", "west": "east"}

# Items that cause instant game over or infinite loops
DANGEROUS = {
    "infinite loop", "giant electromagnet", "molten lava",
    "photons", "escape pod",
}


def send_command(cpu, command):
    """Send a text command to the Intcode computer and return the text output."""
    for ch in command + "\n":
        cpu.inputs.append(ord(ch))
    cpu.run_until_block()
    text = "".join(chr(c) for c in cpu.outputs)
    cpu.outputs.clear()
    return text


def parse_room(text):
    """Parse room name, doors, and items from Intcode ASCII output."""
    name = None
    doors = []
    items = []

    name_match = re.search(r"== (.+) ==", text)
    if name_match:
        name = name_match.group(1)

    in_doors = False
    in_items = False
    for line in text.split("\n"):
        if line == "Doors here lead:":
            in_doors = True
            in_items = False
        elif line == "Items here:":
            in_items = True
            in_doors = False
        elif line.startswith("- "):
            val = line[2:]
            if in_doors:
                doors.append(val)
            elif in_items:
                items.append(val)
        elif line == "":
            in_doors = False
            in_items = False

    return name, doors, items


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    program = [int(x) for x in puzzle_input.strip().split(",")]

    cpu = IntcodeComputer(program)
    cpu.run_until_block()
    initial_text = "".join(chr(c) for c in cpu.outputs)
    cpu.outputs.clear()

    # BFS to explore all rooms, collect safe items, and map the ship
    start_name, start_doors, start_items = parse_room(initial_text)

    # Collect safe items in the starting room
    collected = []
    for item in start_items:
        if item not in DANGEROUS:
            send_command(cpu, f"take {item}")
            collected.append(item)

    # BFS exploration
    visited = {start_name}
    # Queue: (direction_to_go, path_back_to_here)
    queue = deque()
    checkpoint_path = None
    checkpoint_dir = None

    for door in start_doors:
        queue.append((door, []))

    while queue:
        direction, path_from_start = queue.popleft()

        # Navigate from start to the parent room
        for step in path_from_start:
            send_command(cpu, step)

        # Move in the new direction
        text = send_command(cpu, direction)
        name, doors, items = parse_room(text)

        current_path = path_from_start + [direction]

        if name and name not in visited:
            visited.add(name)

            # Collect safe items
            for item in items:
                if item not in DANGEROUS:
                    send_command(cpu, f"take {item}")
                    collected.append(item)

            # Check if this is the security checkpoint
            if name == "Security Checkpoint":
                checkpoint_path = current_path
                # Find which door leads to the pressure floor
                for d in doors:
                    if d != REVERSE[direction]:
                        checkpoint_dir = d
            else:
                # Enqueue unexplored doors
                for door in doors:
                    if door != REVERSE[direction]:
                        queue.append((door, current_path))

        # Navigate back to start
        for step in reversed(current_path):
            send_command(cpu, REVERSE[step])

    # Navigate to the security checkpoint
    for step in checkpoint_path:
        send_command(cpu, step)

    # Drop all items
    for item in collected:
        send_command(cpu, f"drop {item}")

    # Try all combinations of items to find the right weight
    password = None
    for r in range(len(collected) + 1):
        for combo in combinations(collected, r):
            # Pick up this combination
            for item in combo:
                send_command(cpu, f"take {item}")

            # Try the pressure floor
            text = send_command(cpu, checkpoint_dir)

            if "ejected" not in text:
                # Success! Extract the password
                match = re.search(r"(\d+)", text)
                if match:
                    password = match.group(1)
                break

            # Drop items for next attempt
            for item in combo:
                send_command(cpu, f"drop {item}")

        if password:
            break

    return str(password), "50 stars"


def visualize(puzzle_input: str):
    """Yield frames showing the text adventure exploration."""
    program = [int(x) for x in puzzle_input.strip().split(",")]

    cpu = IntcodeComputer(program)
    cpu.run_until_block()
    initial_text = "".join(chr(c) for c in cpu.outputs)
    cpu.outputs.clear()

    start_name, start_doors, start_items = parse_room(initial_text)

    yield {
        "type": "text",
        "lines": [
            "  Cryostasis — Text Adventure",
            "",
            f"  Starting room: {start_name}",
            f"  Doors: {', '.join(start_doors)}",
            f"  Items: {', '.join(start_items) if start_items else 'none'}",
        ],
        "delay": 800,
    }

    # Collect safe items in starting room
    collected = []
    for item in start_items:
        if item not in DANGEROUS:
            send_command(cpu, f"take {item}")
            collected.append(item)

    # BFS exploration
    visited = {start_name}
    rooms_found = [start_name]
    queue = deque()
    checkpoint_path = None
    checkpoint_dir = None

    for door in start_doors:
        queue.append((door, []))

    while queue:
        direction, path_from_start = queue.popleft()
        for step in path_from_start:
            send_command(cpu, step)
        text = send_command(cpu, direction)
        name, doors, items = parse_room(text)
        current_path = path_from_start + [direction]

        if name and name not in visited:
            visited.add(name)
            rooms_found.append(name)
            for item in items:
                if item not in DANGEROUS:
                    send_command(cpu, f"take {item}")
                    collected.append(item)
            if name == "Security Checkpoint":
                checkpoint_path = current_path
                for d in doors:
                    if d != REVERSE[direction]:
                        checkpoint_dir = d
            else:
                for door in doors:
                    if door != REVERSE[direction]:
                        queue.append((door, current_path))

        for step in reversed(current_path):
            send_command(cpu, REVERSE[step])

    yield {
        "type": "text",
        "lines": [
            "  Exploration complete!",
            "",
            f"  Rooms discovered: {len(rooms_found)}",
            f"  Items collected: {len(collected)}",
            "",
            "  Items: " + ", ".join(collected),
        ],
        "delay": 600,
    }

    # Navigate to checkpoint and find correct combo
    for step in checkpoint_path:
        send_command(cpu, step)
    for item in collected:
        send_command(cpu, f"drop {item}")

    yield {
        "type": "text",
        "lines": [
            "  At Security Checkpoint",
            "",
            f"  Testing {2**len(collected)} item combinations",
            "  to find correct weight...",
        ],
        "delay": 600,
    }

    password = None
    attempts = 0
    for r in range(len(collected) + 1):
        for combo in combinations(collected, r):
            attempts += 1
            for item in combo:
                send_command(cpu, f"take {item}")
            text = send_command(cpu, checkpoint_dir)
            if "ejected" not in text:
                match = re.search(r"(\d+)", text)
                if match:
                    password = match.group(1)
                break
            for item in combo:
                send_command(cpu, f"drop {item}")
        if password:
            break

    yield {
        "type": "text",
        "lines": [
            "  ===================================",
            "  Results",
            "  ===================================",
            "",
            f"  Attempts: {attempts}",
            f"  Part 1: {password}",
            "  Part 2: Merry Christmas!",
        ],
        "delay": 500,
    }
