"""
Day 08 - Memory Maneuver
Year: 2018

Parse a license-file tree encoded as a flat number sequence; sum metadata and compute node values.
"""


def parse(numbers: list[int], pos: int = 0):
    """Recursively parse a node starting at pos. Returns (node, next_pos)."""
    num_children = numbers[pos]
    num_meta = numbers[pos + 1]
    pos += 2
    children = []
    for _ in range(num_children):
        child, pos = parse(numbers, pos)
        children.append(child)
    metadata = numbers[pos:pos + num_meta]
    return {"children": children, "meta": metadata}, pos + num_meta


def sum_meta(node: dict) -> int:
    return sum(node["meta"]) + sum(sum_meta(c) for c in node["children"])


def node_value(node: dict) -> int:
    if not node["children"]:
        return sum(node["meta"])
    return sum(
        node_value(node["children"][i - 1])
        for i in node["meta"]
        if 1 <= i <= len(node["children"])
    )


def solve(puzzle_input: str) -> tuple[str, str]:
    numbers = list(map(int, puzzle_input.strip().split()))
    root, _ = parse(numbers, 0)
    return str(sum_meta(root)), str(node_value(root))


# ── Optional visualizer ────────────────────────────────────────────────────────

def visualize(puzzle_input: str):
    numbers = list(map(int, puzzle_input.strip().split()))

    # ── Build the tree with depth/index metadata for display ──────────────────
    nodes = []  # (label, depth, num_children, metadata, value)

    label_counter = [0]

    def build(pos: int, depth: int):
        label = label_counter[0]
        label_counter[0] += 1
        num_children = numbers[pos]
        num_meta = numbers[pos + 1]
        pos += 2
        children = []
        for _ in range(num_children):
            child, pos = build(pos, depth + 1)
            children.append(child)
        meta = numbers[pos:pos + num_meta]
        pos += num_meta
        val = sum(meta) if not children else sum(
            children[i - 1]["value"]
            for i in meta if 1 <= i <= len(children)
        )
        node = {"label": label, "depth": depth, "children": children, "meta": meta, "value": val}
        nodes.append(node)
        return node, pos

    root, _ = build(0, 0)
    total_nodes = len(nodes)

    # ── Intro frame ───────────────────────────────────────────────────────────
    yield {
        "type": "text",
        "lines": [
            "Memory Maneuver — License File Tree",
            "",
            f"Input contains {len(numbers):,} numbers",
            f"Tree has {total_nodes:,} nodes",
            "",
            "Parsing structure...",
        ],
        "delay": 800,
    }

    # ── Animate depth-first traversal showing each node ───────────────────────
    # Flatten tree in DFS order (already built above in label order)
    # Sort nodes by label (DFS discovery order)
    dfs_nodes = sorted(nodes, key=lambda n: n["label"])
    step = max(1, total_nodes // 50)

    running_meta_sum = 0
    for i, node in enumerate(dfs_nodes):
        running_meta_sum += sum(node["meta"])
        if i % step != 0 and i != total_nodes - 1:
            continue
        indent = "  " * node["depth"]
        yield {
            "type": "text",
            "lines": [
                f"Parsing node {i + 1:,} / {total_nodes:,}",
                "",
                f"{indent}Node #{node['label']}  (depth {node['depth']})",
                f"{indent}  children : {len(node['children'])}",
                f"{indent}  metadata : {node['meta'][:8]}{'…' if len(node['meta']) > 8 else ''}",
                f"{indent}  value    : {node['value']:,}",
                "",
                f"Running metadata sum: {running_meta_sum:,}",
            ],
            "delay": 100,
        }

    part1 = sum_meta(root)
    part2 = node_value(root)

    # ── Part 1 result ─────────────────────────────────────────────────────────
    yield {
        "type": "text",
        "lines": [
            "Part 1 — Sum of all metadata",
            "",
            f"Total nodes    : {total_nodes:,}",
            f"Metadata sum   : {part1:,}",
            "",
            f"Answer: {part1}",
        ],
        "delay": 1500,
    }

    # ── Part 2: walk value computation top-down ───────────────────────────────
    # Show how node value propagates for the first few levels
    def level_summary(node, depth_limit, depth=0):
        lines = []
        indent = "  " * depth
        if not node["children"]:
            lines.append(f"{indent}Node #{node['label']}  leaf  → value = sum({node['meta']}) = {node['value']}")
        else:
            idx_refs = [i for i in node["meta"] if 1 <= i <= len(node["children"])]
            lines.append(
                f"{indent}Node #{node['label']}  refs={node['meta']}  → value = {node['value']:,}"
            )
        if depth < depth_limit:
            for child in node["children"]:
                lines.extend(level_summary(child, depth_limit, depth + 1))
        return lines

    summary = level_summary(root, depth_limit=3)[:28]
    yield {
        "type": "text",
        "lines": [
            "Part 2 — Node values (first 4 levels)",
            "  No children → value = sum(metadata)",
            "  Has children → value = sum(children[i] for i in metadata)",
            "",
        ] + summary + [
            "",
            f"Root node value: {part2:,}",
            f"Answer: {part2}",
        ],
        "delay": 3000,
    }
