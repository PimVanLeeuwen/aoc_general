from collections import deque


def ring_after_inserts(steps, inserts):
    """deque.rotate(k) moves the 'current' position around a circle cheaply."""
    ring = deque([0])
    for value in range(1, inserts + 1):
        ring.rotate(-steps)
        ring.append(value)  # the new value becomes the current one (at the right end)
    return ring


def make_ring(order):
    """Circular linked list as a dict: after[label] = next label. O(1) cut and splice."""
    return {a: b for a, b in zip(order, order[1:] + order[:1])}


def move_after(after, start, count, target):
    """Cut the `count` items following start and re-insert them right after target."""
    first = last = after[start]
    for _ in range(count - 1):
        last = after[last]
    after[start] = after[last]
    after[last] = after[target]
    after[target] = first
