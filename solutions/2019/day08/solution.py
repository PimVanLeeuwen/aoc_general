"""
Day 8 - Space Image Format
Year: 2019

Decode a layered image format: verify integrity then flatten layers
to reveal the hidden message.
"""

W, H = 25, 6


def parse_layers(digits):
    """Split digit string into layers of W*H pixels."""
    size = W * H
    return [digits[i:i + size] for i in range(0, len(digits), size)]


def flatten(layers):
    """Stack layers front-to-back; first non-transparent pixel wins."""
    result = ['2'] * (W * H)
    for layer in layers:
        for i, pixel in enumerate(layer):
            if result[i] == '2':
                result[i] = pixel
    return result


def render(image):
    """Convert flat image to readable lines (block for 1, space for 0)."""
    lines = []
    for row in range(H):
        line = ""
        for col in range(W):
            line += "#" if image[row * W + col] == '1' else " "
        lines.append(line)
    return lines


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    digits = puzzle_input.strip()
    layers = parse_layers(digits)

    # Part 1: layer with fewest 0s -> count(1) * count(2)
    best_layer = min(layers, key=lambda l: l.count('0'))
    part1 = best_layer.count('1') * best_layer.count('2')

    # Part 2: flatten and render
    image = flatten(layers)
    part2 = "\n".join(render(image))

    return str(part1), part2


def visualize(puzzle_input: str):
    """Yield frames showing layers being composited into the final image."""
    digits = puzzle_input.strip()
    layers = parse_layers(digits)

    yield {
        "type": "text",
        "lines": [
            "  Space Image Format",
            "",
            f"  Image: {W}x{H} pixels, {len(layers)} layers",
            f"  Total digits: {len(digits)}",
        ],
        "delay": 600,
    }

    # Show layers being composited one at a time
    composite = ['2'] * (W * H)
    step = max(1, len(layers) // 20)

    for li, layer in enumerate(layers):
        for i, pixel in enumerate(layer):
            if composite[i] == '2':
                composite[i] = pixel

        if li < 5 or li % step == 0 or li == len(layers) - 1:
            cells = []
            for row in range(H):
                r = []
                for col in range(W):
                    p = composite[row * W + col]
                    r.append(p)
                cells.append(r)

            resolved = sum(1 for p in composite if p != '2')
            pct = resolved * 100 // (W * H)

            yield {
                "type": "grid",
                "cells": cells,
                "colors": {
                    "0": "#0f0f23",
                    "1": "#ffffff",
                    "2": "#333355",
                },
                "delay": 150 if li < 10 else 60,
            }

    # Final clean render
    cells = []
    for row in range(H):
        r = []
        for col in range(W):
            p = composite[row * W + col]
            r.append(p)
        cells.append(r)

    yield {
        "type": "grid",
        "cells": cells,
        "colors": {
            "0": "#0f0f23",
            "1": "#00ff41",
            "2": "#333355",
        },
        "delay": 800,
    }
