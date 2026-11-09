"""Tests for the technique index: the data file and every Python snippet it shows."""

import importlib.util
import io
import json
import contextlib
import unittest
from functools import cmp_to_key
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DATA = REPO / "frontend" / "src" / "data"
SNIPPETS = DATA / "snippets"
TECHNIQUES = json.loads((DATA / "techniques.json").read_text())


def snippet(name):
    spec = importlib.util.spec_from_file_location(name.replace("-", "_"), SNIPPETS / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def all_meta():
    for path in sorted(REPO.glob("solutions/[0-9]*/day*/meta.json")):
        year, day = int(path.parts[-3]), int(path.parts[-2][3:])
        yield year, day, json.loads(path.read_text())


class TechniqueDataTest(unittest.TestCase):
    def test_ids_unique_and_categories_known(self):
        ids = [t["id"] for t in TECHNIQUES["techniques"]]
        self.assertEqual(len(ids), len(set(ids)))
        categories = {c["id"] for c in TECHNIQUES["categories"]}
        for technique in TECHNIQUES["techniques"]:
            self.assertIn(technique["category"], categories, technique["id"])

    def test_every_technique_has_a_snippet_and_every_snippet_a_technique(self):
        ids = {t["id"] for t in TECHNIQUES["techniques"]}
        files = {path.stem for path in SNIPPETS.glob("*.py")}
        self.assertEqual(ids, files)

    def test_every_tag_is_used_by_a_solution(self):
        used = {tag for _, _, meta in all_meta() for tag in meta.get("tags", [])}
        for technique in TECHNIQUES["techniques"]:
            for tag in technique["tags"]:
                self.assertIn(tag, used, f"{technique['id']}: unknown tag {tag!r}")

    def test_example_day_carries_one_of_the_tags(self):
        tags_by_day = {(year, day): set(meta.get("tags", [])) for year, day, meta in all_meta()}
        for technique in TECHNIQUES["techniques"]:
            example = (technique["example"]["year"], technique["example"]["day"])
            self.assertIn(example, tags_by_day, technique["id"])
            self.assertTrue(tags_by_day[example] & set(technique["tags"]), f"{technique['id']}: {example}")

    def test_no_em_dashes(self):
        for path in [DATA / "techniques.json", *SNIPPETS.glob("*.py")]:
            self.assertNotIn("—", path.read_text(), path.name)


class GraphSnippetsTest(unittest.TestCase):
    def test_bfs_on_grid(self):
        module = snippet("bfs")
        grid = ["..#", "..#", "..."]
        self.assertEqual(module.bfs((0, 0), (0, 2), module.grid_neighbors(grid)), None)
        self.assertEqual(module.bfs((0, 0), (2, 2), module.grid_neighbors(grid)), 4)

    def test_dijkstra(self):
        module = snippet("dijkstra")
        graph = {"a": [("b", 1), ("c", 5)], "b": [("c", 1)], "c": []}
        self.assertEqual(module.dijkstra("a", lambda n: n == "c", lambda n: graph[n]), 2)

    def test_dfs(self):
        module = snippet("dfs")
        graph = {"s": ["a", "b"], "a": ["b", "e"], "b": ["e"], "e": []}
        self.assertEqual(module.count_paths("s", "e", graph), 3)
        weighted = {"s": {"a": 1, "e": 10}, "a": {"e": 20}, "e": {}}
        self.assertEqual(module.longest_path("s", "e", weighted), 21)

    def test_state_search(self):
        module = snippet("state-search")
        # From 0, using +1 and *2: 0 -> 1 -> 2 -> 4 -> 5 -> 10 is the shortest route.
        steps = module.search_states(0, lambda n: n == 10, lambda n: (n + 1, n * 2))
        self.assertEqual(steps, 5)
        # A canonical key that merges states prunes them: here everything is one state.
        self.assertIsNone(module.search_states(0, lambda n: n == 10, lambda n: (n + 1,), canonical=lambda n: 0))

    def test_flood_fill_garden_example(self):
        module = snippet("flood-fill")
        grid = ["AAAA", "BBCD", "BBCC", "EEEC"]
        sizes = sorted(len(region) for region in module.regions(grid))
        self.assertEqual(sizes, [1, 3, 4, 4, 4])
        groups = module.UnionFind()
        self.assertTrue(groups.union(1, 2))
        self.assertTrue(groups.union(2, 3))
        self.assertFalse(groups.union(1, 3))

    def test_topological_sort_2018_day7_example(self):
        module = snippet("topological-sort")
        edges = [("C", "A"), ("C", "F"), ("A", "B"), ("A", "D"), ("B", "E"), ("D", "E"), ("F", "E")]
        self.assertEqual("".join(module.topological_order(list("ABCDEF"), edges)), "CABDFE")
        with self.assertRaises(ValueError):
            module.topological_order(["a", "b"], [("a", "b"), ("b", "a")])

    def test_graph_classics(self):
        module = snippet("graph-classics")
        nodes = ["a", "b", "c"]
        dist = module.all_pairs_distances(nodes, {("a", "b"): 1, ("b", "c"): 2, ("a", "c"): 9})
        self.assertEqual(dist["a"]["c"], 3)
        graph = {"a": {"b", "c", "d"}, "b": {"a", "c"}, "c": {"a", "b"}, "d": {"a"}}
        self.assertEqual(module.max_clique(graph), {"a", "b", "c"})


class GridSnippetsTest(unittest.TestCase):
    def test_grids(self):
        module = snippet("grids")
        grid = module.parse_grid("S.\n.#")
        self.assertEqual(module.find(grid, "S"), (0, 0))
        self.assertEqual(sorted(module.neighbors(grid, (0, 0))), [(0, 1), (1, 0)])
        self.assertEqual(module.rotate_clockwise(["ab", "cd"]), ["ca", "db"])
        self.assertEqual(module.transpose(["ab", "cd"]), ["ac", "bd"])
        self.assertEqual(module.turn_right(3), 0)

    def test_cellular_automaton_blinker(self):
        module = snippet("cellular-automaton")
        blinker = {(1, 0), (1, 1), (1, 2)}
        once = module.step(blinker, module.game_of_life)
        self.assertEqual(once, {(0, 1), (1, 1), (2, 1)})
        self.assertEqual(module.step(once, module.game_of_life), blinker)

    def test_manhattan_2016_day1_examples(self):
        module = snippet("manhattan")
        self.assertEqual(module.walk("R2, L3"), 5)
        self.assertEqual(module.walk("R2, R2, R2"), 2)
        self.assertEqual(module.walk("R5, L5, R5, R3"), 12)
        self.assertEqual(module.manhattan((1, 2, 3), (0, 0, 0)), 6)
        self.assertEqual(module.row_coverage([(8, 7, 9)], 10), [(2, 14)])

    def test_hex_2017_day11_examples(self):
        module = snippet("hex-grid")
        for steps, expected in [("ne,ne,ne", 3), ("ne,ne,sw,sw", 0), ("ne,ne,s,s", 2), ("se,sw,se,sw,sw", 3)]:
            self.assertEqual(module.hex_distance(module.walk(steps)), expected, steps)

    def test_polygon(self):
        module = snippet("polygon")
        square = [(0, 0), (2, 0), (2, 2), (0, 2)]
        self.assertEqual(module.shoelace_area(square), 4)
        self.assertEqual(module.lattice_points(square), (1, 8))

    def test_geometry_3d_2022_day18(self):
        module = snippet("geometry-3d")
        self.assertEqual(module.surface_area({(1, 1, 1), (2, 1, 1)}), 10)
        # a hollow 3x3x3 shell: 54 outside faces, 6 inside faces around the hole
        shell = {(x, y, z) for x in range(3) for y in range(3) for z in range(3)} - {(1, 1, 1)}
        self.assertEqual(module.surface_area(shell), 60)
        self.assertEqual(module.exterior_surface(shell), 54)


class MathSnippetsTest(unittest.TestCase):
    def test_crt_2020_day13_example(self):
        module = snippet("modular")
        buses = [(i, int(bus)) for i, bus in enumerate("7,13,x,x,59,x,31,19".split(",")) if bus != "x"]
        remainders = [-offset for offset, _ in buses]
        self.assertEqual(module.crt(remainders, [bus for _, bus in buses]), 1068781)

    def test_cycle_detection_matches_brute_force(self):
        module = snippet("cycle-detection")

        def step(x):
            return (x * x + 1) % 1009

        for n in (0, 1, 5, 50, 500, 2000):
            state = 3
            for _ in range(n):
                state = step(state)
            self.assertEqual(module.state_after(3, step, n), state, n)

    def test_linear_2024_day13_example(self):
        module = snippet("linear-algebra")
        self.assertEqual(module.solve_linear([[94, 22], [34, 67]], [8400, 5400]), [80, 40])

    def test_number_theory(self):
        module = snippet("number-theory")
        self.assertEqual(module.divisors(36), [1, 2, 3, 4, 6, 9, 12, 18, 36])
        self.assertEqual([n for n in range(20) if module.is_prime(n)], [2, 3, 5, 7, 11, 13, 17, 19])
        self.assertEqual(module.digits(1203), [1, 2, 0, 3])
        self.assertEqual(module.digits(5, base=2), [1, 0, 1])
        self.assertEqual(module.digits(0), [0])

    def test_extrapolation_2023_day9_examples(self):
        module = snippet("extrapolation")
        self.assertEqual(module.next_value([0, 3, 6, 9, 12, 15]), 18)
        self.assertEqual(module.next_value([10, 13, 16, 21, 30, 45]), 68)
        self.assertEqual(module.quadratic_at(0, 1, 4, 10), 100)

    def test_combinatorics(self):
        module = snippet("combinatorics")
        self.assertEqual(module.best_order([1, 2, 3], lambda order: order[0] * 10 + order[1]), (3, 2, 1))
        self.assertEqual(module.smallest_groups_with_sum([1, 2, 3, 4, 5, 7, 8, 9, 10, 11], 20), [(9, 11)])


class OptimizationSnippetsTest(unittest.TestCase):
    def test_memoization_2024_examples(self):
        module = snippet("memoization")
        towels = ["r", "wr", "b", "g", "bwu", "rb", "gb", "br"]
        self.assertEqual(module.count_ways("brwrr", towels), 2)
        self.assertEqual(module.count_ways("bbrgwb", towels), 0)

        def blink(stone):
            if stone == 0:
                return [1]
            text = str(stone)
            if len(text) % 2 == 0:
                half = len(text) // 2
                return [int(text[:half]), int(text[half:])]
            return [stone * 2024]

        self.assertEqual(module.evolve_counts([125, 17], blink, 25), 55312)

    def test_recursion(self):
        module = snippet("recursion")
        jobs = {"root": ("a", "+", "b"), "a": ("c", "*", "d"), "b": 3, "c": 4, "d": 5}
        self.assertEqual(module.evaluate("root", jobs), 23)
        packets = [[1, [2, [3]]], [[1], 4], [1, 1, 3], 3]
        ordered = sorted(packets, key=cmp_to_key(module.compare))
        self.assertEqual(ordered, [[1, 1, 3], [1, [2, [3]]], [[1], 4], 3])
        self.assertLess(module.compare([[1], [2, 3, 4]], [[1], 4]), 0)  # 2022 day 13, pair 2

    def test_binary_search(self):
        module = snippet("binary-search")
        self.assertEqual(module.first_true(0, 1000, lambda x: x * x >= 200), 15)
        self.assertEqual(module.first_true(0, 10, lambda x: True), 0)

    def test_greedy_2025_day3_examples(self):
        module = snippet("greedy")
        self.assertEqual(module.largest_subsequence("987654321111111", 2), "98")
        self.assertEqual(module.largest_subsequence("811111111111119", 2), "89")
        self.assertEqual(module.largest_subsequence("234234234234278", 2), "78")

    def test_constraint_elimination(self):
        module = snippet("constraint-satisfaction")
        solved = module.resolve({"row": {0, 1}, "class": {1}, "seat": {0, 1, 2}})
        self.assertEqual(solved, {"class": 1, "row": 0, "seat": 2})
        with self.assertRaises(ValueError):
            module.resolve({"a": {1, 2}, "b": {1, 2}})


class RangeSnippetsTest(unittest.TestCase):
    def test_intervals(self):
        module = snippet("intervals")
        self.assertEqual(module.merge([(5, 8), (0, 2), (3, 4), (10, 12)]), [(0, 8), (10, 12)])
        self.assertEqual(module.overlap((0, 5), (3, 9)), (3, 5))
        self.assertIsNone(module.overlap((0, 2), (3, 9)))
        moved, leftovers = module.apply_shift((79, 92), 50, 97, 2)  # 2023 day 5: seed-to-soil
        self.assertEqual((moved, leftovers), ((81, 94), []))
        moved, leftovers = module.apply_shift((0, 10), 3, 5, 100)
        self.assertEqual((moved, leftovers), ((103, 105), [(0, 2), (6, 10)]))

    def test_prefix_sums(self):
        module = snippet("prefix-sums")
        sums = module.prefix_sums([3, 1, 4, 1, 5])
        self.assertEqual(sums[4] - sums[1], 1 + 4 + 1)
        self.assertEqual(module.first_distinct_window("mjqjpqmgbljsphdztnvjfqwrcgsmlb", 4), 7)
        self.assertEqual(module.first_distinct_window("mjqjpqmgbljsphdztnvjfqwrcgsmlb", 14), 19)
        total = module.summed_area([[1, 2], [3, 4]])
        self.assertEqual(module.area_sum(total, 0, 0, 1, 1), 10)
        self.assertEqual(module.area_sum(total, 1, 0, 1, 1), 7)


class MachineSnippetsTest(unittest.TestCase):
    def test_interpreter_2016_day12_example(self):
        module = snippet("interpreter")
        program = ["cpy 41 a", "inc a", "inc a", "dec a", "jnz a 2", "dec a"]
        self.assertEqual(module.run(program, {"a": 0, "b": 0, "c": 0, "d": 0})["a"], 42)

    def test_reverse_engineering_hot_spots(self):
        module = snippet("reverse-engineering")
        program = ["dec", "jnz -1"]

        def step(program, state):
            if program[state["pc"]] == "dec":
                return {"pc": state["pc"] + 1, "x": state["x"] - 1}
            return {"pc": state["pc"] - 1 if state["x"] else state["pc"] + 1, "x": state["x"]}

        with contextlib.redirect_stdout(io.StringIO()):
            counts = module.hot_spots(program, step, {"pc": 0, "x": 5})
        self.assertEqual(counts, {0: 5, 1: 5})

    def test_circular_buffer(self):
        module = snippet("circular-buffer")
        ring = module.ring_after_inserts(3, 2017)  # 2017 day 17 example: value after 2017 is 638
        self.assertEqual(ring[0], 638)
        after = module.make_ring([3, 8, 9, 1, 2, 5, 4, 6, 7])
        module.move_after(after, 3, 3, 2)  # 2020 day 23 first move: 3 (8) (9) (1) -> after 2
        order, label = [], 3
        for _ in range(9):
            order.append(label)
            label = after[label]
        self.assertEqual(order, [3, 2, 8, 9, 1, 5, 4, 6, 7])

    def test_stack(self):
        module = snippet("stack")
        self.assertEqual(module.first_illegal("{([(<{}[<>[]}>{[]{[(<()>"), "}")
        self.assertIsNone(module.first_illegal("[({(<(())[]>[[{[]{<()<>>"))
        self.assertEqual(len(module.react("dabAcCaCBAcCcaDA")), 10)

    def test_bit_mask_2020_day14_example(self):
        module = snippet("bit-manipulation")
        mask = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X"
        self.assertEqual(module.apply_mask(11, mask), 73)
        self.assertEqual(module.apply_mask(101, mask), 101)
        self.assertEqual(module.apply_mask(0, mask), 64)

    def test_hashing(self):
        module = snippet("hashing")
        self.assertEqual(module.holiday_hash("HASH"), 52)
        self.assertTrue(module.md5_hex("abcdef609043").startswith("00000"))
        n = module.first_index_with_prefix("abc", "000")
        self.assertTrue(module.md5_hex(f"abc{n}").startswith("000"))
        self.assertFalse(any(module.md5_hex(f"abc{i}").startswith("000") for i in range(n)))

    def test_parsing(self):
        module = snippet("parsing")
        self.assertEqual(module.ints("x=-3, y=12"), [-3, 12])
        self.assertEqual(module.sections("a\nb\n\nc\n"), ["a\nb", "c"])
        memory = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"
        self.assertEqual(module.sum_of_products(memory), 48)
        self.assertEqual(module.nested("[1,[2,[3]]]"), [1, [2, [3]]])


if __name__ == "__main__":
    unittest.main()
