from itertools import product


def all_pairs_distances(nodes, edges):
    """Floyd-Warshall: shortest distance between every pair. edges = {(a, b): weight}."""
    infinity = float("inf")
    dist = {a: {b: 0 if a == b else edges.get((a, b), infinity) for b in nodes} for a in nodes}
    for via, a, b in product(nodes, repeat=3):  # 'via' must be the outer loop
        if dist[a][via] + dist[via][b] < dist[a][b]:
            dist[a][b] = dist[a][via] + dist[via][b]
    return dist


def max_clique(graph):
    """Bron-Kerbosch: the largest group of nodes that are all connected. graph[n] = set of neighbours."""
    best = set()

    def expand(clique, candidates, excluded):
        nonlocal best
        if not candidates and not excluded:
            if len(clique) > len(best):
                best = clique
            return
        for node in list(candidates):
            expand(clique | {node}, candidates & graph[node], excluded & graph[node])
            candidates = candidates - {node}
            excluded = excluded | {node}

    expand(set(), set(graph), set())
    return best
