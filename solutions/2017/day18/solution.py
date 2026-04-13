"""
Day 18 - Duet
Year: 2017

Simulate a small assembly-like language (Part 1) and two communicating programs (Part 2).
"""

def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    lines = puzzle_input.strip().split("\n")

    # Helper to get value (register or integer)
    def val(x, regs):
        return regs[x] if x.isalpha() else int(x)

    regs = {chr(c): 0 for c in range(ord('a'), ord('z') + 1)}
    last_sound = None
    ip = 0  # instruction pointer

    while 0 <= ip < len(lines):
        parts = lines[ip].split()
        op = parts[0]
        X = parts[1]

        if op == "snd":
            last_sound = val(X, regs)
            ip += 1

        elif op == "set":
            regs[X] = val(parts[2], regs)
            ip += 1

        elif op == "add":
            regs[X] += val(parts[2], regs)
            ip += 1

        elif op == "mul":
            regs[X] *= val(parts[2], regs)
            ip += 1

        elif op == "mod":
            regs[X] %= val(parts[2], regs)
            ip += 1

        elif op == "rcv":
            if val(X, regs) != 0:
                part1 = last_sound
                break
            ip += 1

        elif op == "jgz":
            if val(X, regs) > 0:
                ip += val(parts[2], regs)
            else:
                ip += 1

    def run_duet(pid):
        regs = {chr(c): 0 for c in range(ord('a'), ord('z') + 1)}
        regs["p"] = pid
        return regs

    regs0 = run_duet(0)
    regs1 = run_duet(1)

    q0 = []
    q1 = []

    ip0 = 0
    ip1 = 0

    send_count_1 = 0

    waiting0 = False
    waiting1 = False

    def step(ip, regs, inbox, outbox, is_p1):
        nonlocal send_count_1

        if not (0 <= ip < len(lines)):
            return ip, True  # terminated

        parts = lines[ip].split()
        op = parts[0]
        X = parts[1]

        if op == "snd":
            outbox.append(val(X, regs))
            if is_p1:
                send_count_1 += 1
            return ip + 1, False

        elif op == "set":
            regs[X] = val(parts[2], regs)
            return ip + 1, False

        elif op == "add":
            regs[X] += val(parts[2], regs)
            return ip + 1, False

        elif op == "mul":
            regs[X] *= val(parts[2], regs)
            return ip + 1, False

        elif op == "mod":
            regs[X] %= val(parts[2], regs)
            return ip + 1, False

        elif op == "rcv":
            if inbox:
                regs[X] = inbox.pop(0)
                return ip + 1, False
            else:
                return ip, True  # waiting

        elif op == "jgz":
            if val(X, regs) > 0:
                return ip + val(parts[2], regs), False
            else:
                return ip + 1, False

    # Run until deadlock
    while True:
        ip0_new, wait0 = step(ip0, regs0, q0, q1, False)
        ip1_new, wait1 = step(ip1, regs1, q1, q0, True)

        waiting0 = wait0
        waiting1 = wait1

        ip0 = ip0_new
        ip1 = ip1_new

        if waiting0 and waiting1:
            break

    part2 = send_count_1

    return str(part1), str(part2)




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
