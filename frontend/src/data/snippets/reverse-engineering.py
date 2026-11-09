from collections import Counter


def hot_spots(program, step, state, max_steps=1_000_000, top=10):
    """
    When the program would run for ages, find the loop it spends its time in:
    run it for a while and count how often each instruction executes. Then read
    that loop, work out what it computes (often: sum of divisors, multiplication
    by repeated addition) and replace it with Python.
    step(program, state) executes one instruction; state['pc'] is the pointer.
    """
    counts = Counter()
    for _ in range(max_steps):
        pc = state["pc"]
        if not 0 <= pc < len(program):
            break
        counts[pc] += 1
        state = step(program, state)
    for pc, count in counts.most_common(top):
        print(f"{pc:4} {count:>9}  {program[pc]}")
    return counts
