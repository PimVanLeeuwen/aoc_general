"""
Day 04 - Repose Record
Year: 2018

Analyze guard sleep patterns to find the best time to sneak past them.
"""
import re
from collections import defaultdict


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    lines = sorted(puzzle_input.strip().split("\n"))
    
    # Parse logs and build sleep schedule per guard
    guard_minutes = defaultdict(lambda: [0] * 60)  # guard_id -> [count per minute]
    current_guard = None
    sleep_start = 0
    
    for line in lines:
        minute = int(re.search(r':(\d+)', line).group(1))
        if 'Guard' in line:
            current_guard = int(re.search(r'#(\d+)', line).group(1))
        elif 'falls asleep' in line:
            sleep_start = minute
        elif 'wakes up' in line:
            for m in range(sleep_start, minute):
                guard_minutes[current_guard][m] += 1

    # Strategy 1: Guard with most total minutes asleep × their sleepiest minute
    sleepiest_guard = max(guard_minutes, key=lambda g: sum(guard_minutes[g]))
    sleepiest_minute = guard_minutes[sleepiest_guard].index(max(guard_minutes[sleepiest_guard]))
    part1 = sleepiest_guard * sleepiest_minute

    # Strategy 2: Guard most frequently asleep on the same minute
    best_guard, best_minute, best_count = 0, 0, 0
    for guard, minutes in guard_minutes.items():
        max_count = max(minutes)
        if max_count > best_count:
            best_count = max_count
            best_guard = guard
            best_minute = minutes.index(max_count)
    part2 = best_guard * best_minute

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    """Yield visualization frames for Day 04."""
    lines = sorted(puzzle_input.strip().split("\n"))
    
    # Parse logs
    guard_minutes = defaultdict(lambda: [0] * 60)
    guard_total = defaultdict(int)
    current_guard = None
    sleep_start = 0
    events = []
    
    for line in lines:
        minute = int(re.search(r':(\d+)', line).group(1))
        date = re.search(r'\d{4}-(\d{2}-\d{2})', line).group(1)
        if 'Guard' in line:
            current_guard = int(re.search(r'#(\d+)', line).group(1))
            events.append(('shift', date, current_guard, minute))
        elif 'falls asleep' in line:
            sleep_start = minute
            events.append(('sleep', date, current_guard, minute))
        elif 'wakes up' in line:
            for m in range(sleep_start, minute):
                guard_minutes[current_guard][m] += 1
                guard_total[current_guard] += 1
            events.append(('wake', date, current_guard, minute, sleep_start))

    # Show processing of events
    total_events = len(events)
    show_every = max(1, total_events // 15)
    
    for i, event in enumerate(events):
        if i % show_every == 0 or i == total_events - 1:
            if event[0] == 'shift':
                yield {
                    "type": "text",
                    "lines": [
                        f"Processing logs... ({i+1}/{total_events})",
                        "",
                        f"Guard #{event[2]} begins shift",
                        f"Date: {event[1]}",
                        "",
                        f"Guards tracked: {len(guard_total)}",
                        f"Total sleep minutes: {sum(guard_total.values()):,}",
                    ],
                    "delay": 200,
                }
            elif event[0] == 'wake':
                sleep_duration = event[3] - event[4]
                yield {
                    "type": "text",
                    "lines": [
                        f"Processing logs... ({i+1}/{total_events})",
                        "",
                        f"Guard #{event[2]} slept: {event[4]:02d}-{event[3]:02d}",
                        f"Duration: {sleep_duration} minutes",
                        f"Date: {event[1]}",
                        "",
                        f"Guards tracked: {len(guard_total)}",
                        f"Total sleep minutes: {sum(guard_total.values()):,}",
                    ],
                    "delay": 200,
                }

    # Strategy 1 result
    sleepiest_guard = max(guard_minutes, key=lambda g: sum(guard_minutes[g]))
    sleepiest_minute = guard_minutes[sleepiest_guard].index(max(guard_minutes[sleepiest_guard]))
    total_sleep = sum(guard_minutes[sleepiest_guard])
    
    yield {
        "type": "text",
        "lines": [
            "Strategy 1: Most Total Sleep",
            "",
            f"Sleepiest guard: #{sleepiest_guard}",
            f"Total minutes asleep: {total_sleep}",
            f"Most common minute: {sleepiest_minute}",
            "",
            f"Answer: {sleepiest_guard} × {sleepiest_minute} = {sleepiest_guard * sleepiest_minute}",
        ],
        "delay": 1000,
    }

    # Strategy 2 result
    best_guard, best_minute, best_count = 0, 0, 0
    for guard, minutes in guard_minutes.items():
        max_count = max(minutes)
        if max_count > best_count:
            best_count = max_count
            best_guard = guard
            best_minute = minutes.index(max_count)

    yield {
        "type": "text",
        "lines": [
            "Strategy 2: Most Frequent Minute",
            "",
            f"Guard #{best_guard} sleeps at minute {best_minute}",
            f"Frequency: {best_count} times",
            "",
            f"Answer: {best_guard} × {best_minute} = {best_guard * best_minute}",
        ],
        "delay": 1000,
    }

    # Final summary
    yield {
        "type": "text",
        "lines": [
            "Analysis Complete!",
            "",
            f"Total guards analyzed: {len(guard_minutes)}",
            f"Total log entries: {total_events}",
            "",
            "Results:",
            f"   Part 1: {sleepiest_guard * sleepiest_minute}",
            f"   Part 2: {best_guard * best_minute}",
        ],
        "delay": 2000,
    }

