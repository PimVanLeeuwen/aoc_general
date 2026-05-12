"""
Day 23 - Category Six
Year: 2019

Simulate a network of 50 Intcode computers exchanging packets.
A NAT device monitors for idle networks and delivers wake-up packets.
"""

from collections import deque
from intcode import IntcodeComputer


def simulate(program):
    """Run the 50-computer network. Returns (part1, part2)."""
    # Boot 50 computers, each with its network address
    computers = []
    queues = []
    for i in range(50):
        cpu = IntcodeComputer(program, inputs=[i])
        computers.append(cpu)
        queues.append(deque())

    part1 = None
    nat_packet = None
    last_nat_y = None

    while True:
        idle = True

        for i in range(50):
            cpu = computers[i]

            # Feed input: next packet from queue, or -1
            if queues[i]:
                idle = False
                x, y = queues[i].popleft()
                cpu.add_input(x)
                cpu.add_input(y)
            else:
                cpu.add_input(-1)

            # Run until it blocks on input
            cpu.run_until_block()

            # Collect output packets (groups of 3: dest, x, y)
            while len(cpu.outputs) >= 3:
                idle = False
                dest, x, y = cpu.outputs[:3]
                del cpu.outputs[:3]

                if dest == 255:
                    if part1 is None:
                        part1 = y
                    nat_packet = (x, y)
                else:
                    queues[dest].append((x, y))

        # Check if network is idle (all queues empty, no output produced)
        if idle and nat_packet is not None:
            if last_nat_y == nat_packet[1]:
                return part1, nat_packet[1]
            last_nat_y = nat_packet[1]
            queues[0].append(nat_packet)


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    program = [int(x) for x in puzzle_input.strip().split(",")]

    part1, part2 = simulate(program)

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    """Yield frames showing the network simulation."""
    program = [int(x) for x in puzzle_input.strip().split(",")]

    yield {
        "type": "text",
        "lines": [
            "  Category Six — Network Simulation",
            "",
            "  50 Intcode computers connected via packets.",
            "  Each sends (dest, X, Y) triples.",
            "  NAT monitors address 255 for idle detection.",
        ],
        "delay": 800,
    }

    # Run simulation with tracking
    computers = []
    queues = []
    for i in range(50):
        cpu = IntcodeComputer(program, inputs=[i])
        computers.append(cpu)
        queues.append(deque())

    part1 = None
    nat_packet = None
    last_nat_y = None
    total_packets = 0
    nat_sends = 0

    while True:
        idle = True

        for i in range(50):
            cpu = computers[i]
            if queues[i]:
                idle = False
                x, y = queues[i].popleft()
                cpu.add_input(x)
                cpu.add_input(y)
            else:
                cpu.add_input(-1)

            cpu.run_until_block()

            while len(cpu.outputs) >= 3:
                idle = False
                dest, x, y = cpu.outputs[:3]
                del cpu.outputs[:3]
                total_packets += 1

                if dest == 255:
                    if part1 is None:
                        part1 = y
                    nat_packet = (x, y)
                else:
                    queues[dest].append((x, y))

        if idle and nat_packet is not None:
            nat_sends += 1
            if last_nat_y == nat_packet[1]:
                part2 = nat_packet[1]
                break
            last_nat_y = nat_packet[1]
            queues[0].append(nat_packet)

    yield {
        "type": "text",
        "lines": [
            "  ===================================",
            "  Results",
            "  ===================================",
            "",
            f"  Total packets sent: {total_packets:,}",
            f"  NAT wake-ups: {nat_sends}",
            "",
            f"  Part 1: {part1} (first Y to address 255)",
            f"  Part 2: {part2} (first repeated NAT Y)",
        ],
        "delay": 500,
    }
