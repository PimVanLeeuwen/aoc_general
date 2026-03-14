"""
Day 07 - The Sum of Its Parts
Year: 2018

Order assembly steps by their dependencies; then simulate parallel workers.
"""
import heapq
from collections import defaultdict


def parse(puzzle_input: str):
    deps = defaultdict(set)
    all_steps = set()
    for line in puzzle_input.strip().split("\n"):
        parts = line.split()
        before, after = parts[1], parts[7]
        deps[after].add(before)
        all_steps.add(before)
        all_steps.add(after)
    for s in all_steps:
        deps.setdefault(s, set())
    return all_steps, deps


def topo_sort(all_steps: set, deps: dict) -> str:
    remaining = {s: set(d) for s, d in deps.items()}
    heap = [s for s in all_steps if not remaining[s]]
    heapq.heapify(heap)
    order = []
    while heap:
        step = heapq.heappop(heap)
        order.append(step)
        for s, d in remaining.items():
            if step in d:
                d.discard(step)
                if not d and s not in order and s not in heap:
                    heapq.heappush(heap, s)
    return "".join(order)


def parallel_time(all_steps: set, deps: dict, num_workers: int = 5, base: int = 60) -> int:
    remaining = {s: set(d) for s, d in deps.items()}
    in_progress: set = set()
    completed: set = set()
    available = [s for s in all_steps if not remaining[s]]
    heapq.heapify(available)
    workers = []  # (finish_time, step)
    time = 0
    while available or workers:
        while available and len(workers) < num_workers:
            step = heapq.heappop(available)
            heapq.heappush(workers, (time + base + ord(step) - ord('A') + 1, step))
            in_progress.add(step)
        if not workers:
            break
        time = workers[0][0]
        while workers and workers[0][0] == time:
            _, done = heapq.heappop(workers)
            completed.add(done)
            in_progress.discard(done)
        for s in all_steps:
            if s not in completed and s not in in_progress:
                if remaining[s] <= completed:
                    heapq.heappush(available, s)
    return time


def solve(puzzle_input: str) -> tuple[str, str]:
    all_steps, deps = parse(puzzle_input)
    part1 = topo_sort(all_steps, deps)
    part2 = parallel_time(all_steps, deps)
    return part1, str(part2)


# ── Optional visualizer ────────────────────────────────────────────────────────

def visualize(puzzle_input: str):
    all_steps, deps = parse(puzzle_input)

    # ── Part 1: animate the topological sort ──────────────────────────────────
    remaining = {s: set(d) for s, d in deps.items()}
    heap = [s for s in all_steps if not remaining[s]]
    heapq.heapify(heap)
    order = []

    while heap:
        available_display = sorted(heap)
        step = heapq.heappop(heap)
        order.append(step)

        yield {
            "type": "text",
            "lines": [
                "Part 1 — Topological Sort",
                "",
                f"Available : {', '.join(available_display)}",
                f"Chosen    : {step}  (alphabetically first)",
                "",
                f"Order so far : {''.join(order)}",
                f"Progress     : {len(order)} / {len(all_steps)} steps",
            ],
            "delay": 350,
        }

        for s, d in remaining.items():
            if step in d:
                d.discard(step)
                if not d and s not in order and s not in heap:
                    heapq.heappush(heap, s)

    yield {
        "type": "text",
        "lines": [
            "Part 1 — Complete!",
            "",
            f"Step order : {''.join(order)}",
        ],
        "delay": 1500,
    }

    # ── Part 2: simulate workers and collect schedule ─────────────────────────
    NUM_WORKERS = 5
    BASE = 60

    remaining2 = {s: set(d) for s, d in deps.items()}
    in_progress: set = set()
    completed: set = set()
    schedule = []  # (step, start, end, worker_slot)
    worker_slots: list = [None] * NUM_WORKERS  # None or (step, start, end)
    available2 = [s for s in all_steps if not remaining2[s]]
    heapq.heapify(available2)
    workers_heap: list = []  # (finish_time, step, slot)
    time = 0
    events = []

    while available2 or workers_heap:
        # Assign available steps to free worker slots
        free_slots = [i for i in range(NUM_WORKERS) if worker_slots[i] is None]
        while available2 and free_slots:
            step = heapq.heappop(available2)
            slot = free_slots.pop(0)
            finish = time + BASE + ord(step) - ord('A') + 1
            worker_slots[slot] = (step, time, finish)
            heapq.heappush(workers_heap, (finish, step, slot))
            in_progress.add(step)

        if not workers_heap:
            break

        # Snapshot current state
        wlines = []
        for i, ws in enumerate(worker_slots):
            if ws is None:
                wlines.append(f"  Worker {i+1}: idle")
            else:
                wlines.append(f"  Worker {i+1}: {ws[0]}  (done at t={ws[2]})")

        events.append({
            "time": time,
            "lines": [
                f"Part 2 — t = {time:4d}s",
                "",
            ] + wlines + [
                "",
                f"  Done : {''.join(sorted(completed)) or '—'}",
            ],
        })

        # Advance to next completion
        time = workers_heap[0][0]
        while workers_heap and workers_heap[0][0] == time:
            _, done, slot = heapq.heappop(workers_heap)
            step, start, end = worker_slots[slot]
            schedule.append((step, start, end, slot))
            worker_slots[slot] = None
            completed.add(done)
            in_progress.discard(done)

        for s in all_steps:
            if s not in completed and s not in in_progress:
                if remaining2[s] <= completed:
                    heapq.heappush(available2, s)

    total_time = time

    # Yield worker-state snapshots (cap at ~60 frames)
    step_size = max(1, len(events) // 60)
    for i, ev in enumerate(events):
        if i % step_size == 0:
            ev["lines"][-3] = f"  Time elapsed: {ev['time']:,}s / ~{total_time:,}s"
            yield {"type": "text", "lines": ev["lines"], "delay": 150}

    # ── Gantt chart summary ───────────────────────────────────────────────────
    # Build a compact ASCII gantt per worker
    BAR_WIDTH = 50
    gantt_lines = [
        "Part 2 — Worker Timeline",
        f"Total time: {total_time}s",
        "",
    ]
    for slot in range(NUM_WORKERS):
        slot_tasks = sorted((s, st, en) for s, st, en, w in schedule if w == slot)
        bar = [" "] * BAR_WIDTH
        for step, start, end in slot_tasks:
            # Map [start,end] onto BAR_WIDTH chars
            a = round(start * BAR_WIDTH / total_time)
            b = max(a + 1, round(end * BAR_WIDTH / total_time))
            mid = (a + b) // 2
            for x in range(a, min(b, BAR_WIDTH)):
                bar[x] = "█"
            if mid < BAR_WIDTH:
                bar[mid] = step
        gantt_lines.append(f"W{slot+1} |{''.join(bar)}|")

    gantt_lines += [
        "",
        f"Answer: {total_time}s",
    ]
    yield {"type": "text", "lines": gantt_lines, "delay": 3000}
