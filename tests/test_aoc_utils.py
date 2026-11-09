"""Tests for the shared solution helpers in solutions/aoc_utils.py."""

import contextlib
import io
import sys
import unittest
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "solutions"))

import aoc_utils as u  # noqa: E402

MAZE = """\
#####
#S..#
#.#.#
#..E#
#####"""


def maze_neighbors(grid):
    return lambda p: (n for n in u.neighbors(p, grid) if grid[n] != "#")


class ParsingTest(unittest.TestCase):
    def test_ints_lines_sections(self):
        self.assertEqual(u.ints("p=0,4 v=-3,12"), [0, 4, -3, 12])
        self.assertEqual(u.lines("a\nb\n"), ["a", "b"])
        self.assertEqual(u.sections("a\nb\n\nc\n"), ["a\nb", "c"])


class GridTest(unittest.TestCase):
    def setUp(self):
        self.grid = u.parse_grid(MAZE)

    def test_parse_and_find(self):
        self.assertEqual(len(self.grid), 25)
        self.assertEqual(u.grid_find(self.grid, "S"), (1, 1))
        self.assertIsNone(u.grid_find(self.grid, "X"))
        self.assertEqual(len(u.grid_find_all(self.grid, "#")), 17)

    def test_neighbors(self):
        self.assertEqual(sorted(u.neighbors((0, 0), self.grid)), [(0, 1), (1, 0)])
        self.assertEqual(len(list(u.neighbors((5, 5)))), 4)
        self.assertEqual(len(list(u.neighbors((1, 1), dirs=u.DIRS_8))), 8)
        self.assertEqual(u.add((1, 2), u.ARROWS[">"]), (1, 3))
        self.assertEqual(u.DIRS_4[(0 + 1) % 4], (0, 1))  # turning right from up faces right

    def test_rotate_transpose(self):
        self.assertEqual(u.rotate_clockwise(["ab", "cd"]), ["ca", "db"])
        self.assertEqual(u.transpose(["ab", "cd"]), ["ac", "bd"])

    def test_grid_to_str(self):
        self.assertEqual(u.grid_to_str({(-1, -1), (0, 1)}), "#..\n..#")
        self.assertEqual(u.grid_to_str(u.parse_grid("ab\ncd")), "ab\ncd")
        self.assertEqual(u.grid_to_str(set()), "")
        with contextlib.redirect_stdout(io.StringIO()) as output:
            u.print_grid({(0, 0)})
        self.assertEqual(output.getvalue(), "#\n")

    def test_manhattan(self):
        self.assertEqual(u.manhattan((3, -4)), 7)
        self.assertEqual(u.manhattan((1, 1, 1), (2, 3, 4)), 6)


class SearchTest(unittest.TestCase):
    def setUp(self):
        self.grid = u.parse_grid(MAZE)
        self.start, self.end = u.grid_find(self.grid, "S"), u.grid_find(self.grid, "E")

    def test_bfs(self):
        steps = maze_neighbors(self.grid)
        self.assertEqual(u.bfs(self.start, self.end, steps), 4)
        self.assertEqual(u.bfs(self.start, lambda p: self.grid[p] == "E", steps), 4)
        path = u.bfs_path(self.start, self.end, steps)
        self.assertEqual((path[0], path[-1], len(path)), (self.start, self.end, 5))
        self.assertIsNone(u.bfs(self.start, (0, 0), steps))
        distances = u.bfs_distances(self.start, steps)
        self.assertEqual((len(distances), distances[self.end]), (8, 4))  # 8 open cells

    def test_dijkstra_and_astar_agree(self):
        # 2021 day 15 example grid: lowest total risk is 40
        risk = u.parse_grid(
            "1163751742\n1381373672\n2136511328\n3694931569\n7463417111\n"
            "1319128137\n1359912421\n3125421639\n1293138521\n2311944581"
        )
        target = (9, 9)

        def steps(p):
            return ((n, int(risk[n])) for n in u.neighbors(p, risk))

        self.assertEqual(u.dijkstra((0, 0), target, steps), 40)
        self.assertEqual(u.dijkstra((0, 0), target, steps, heuristic=lambda p: u.manhattan(p, target)), 40)
        cost, path = u.shortest_path((0, 0), target, steps)
        self.assertEqual(cost, sum(int(risk[p]) for p in path[1:]))
        self.assertEqual(u.dijkstra_costs((0, 0), steps)[target], 40)

    def test_dijkstra_with_uncomparable_nodes(self):
        graph = {0: [(1j, 1), (1, 1)], 1j: [(1 + 1j, 1)], 1: [(1 + 1j, 5)], 1 + 1j: []}
        self.assertEqual(u.dijkstra(0, 1 + 1j, lambda n: graph[n]), 2)
        self.assertIsNone(u.dijkstra(1 + 1j, 0, lambda n: graph[n]))

    def test_regions_2024_day12_example(self):
        garden = u.parse_grid("AAAA\nBBCD\nBBCC\nEEEC")
        self.assertEqual(sorted(len(r) for r in u.regions(garden)), [1, 3, 4, 4, 4])

    def test_union_find(self):
        groups = u.UnionFind(range(5))
        self.assertTrue(groups.union(0, 1))
        self.assertTrue(groups.union(1, 2))
        self.assertFalse(groups.union(0, 2))
        self.assertEqual((groups.groups(), groups.size(2), groups.size(4)), (3, 3, 1))
        self.assertEqual(groups.find(0), groups.find(2))

    def test_topological_sort_2018_day7_example(self):
        edges = [("C", "A"), ("C", "F"), ("A", "B"), ("A", "D"), ("B", "E"), ("D", "E"), ("F", "E")]
        self.assertEqual("".join(u.topological_sort("ABCDEF", edges)), "CABDFE")
        with self.assertRaises(ValueError):
            u.topological_sort("ab", [("a", "b"), ("b", "a")])


class MathTest(unittest.TestCase):
    def test_crt_2020_day13_example(self):
        buses = [(i, int(b)) for i, b in enumerate("7,13,x,x,59,x,31,19".split(",")) if b != "x"]
        self.assertEqual(u.crt([-i for i, _ in buses], [b for _, b in buses]), 1068781)
        self.assertEqual(u.crt([2, 0], [4, 6]), 6)  # non-coprime moduli
        with self.assertRaises(ValueError):
            u.crt([1, 0], [2, 4])

    def test_state_after_matches_brute_force(self):
        def step(x):
            return (x * x + 1) % 1009

        for n in (0, 1, 7, 100, 3000):
            state = 3
            for _ in range(n):
                state = step(state)
            self.assertEqual(u.state_after(3, step, n), state)

    def test_extrapolation(self):
        self.assertEqual(u.extrapolate([10, 13, 16, 21, 30, 45]), 68)  # 2023 day 9
        self.assertEqual(u.extrapolate([45, 30, 21, 16, 13, 10]), 5)   # part 2: reversed
        self.assertEqual(u.quadratic_at(0, 1, 4, 10), 100)

    def test_polygon(self):
        square = [(0, 0), (2, 0), (2, 2), (0, 2)]
        self.assertEqual(u.shoelace_area(square), 4)
        self.assertEqual(u.lattice_points(square), (1, 8))

    def test_solve_linear_2024_day13_example(self):
        self.assertEqual(u.solve_linear([[94, 22], [34, 67]], [8400, 5400]), [80, 40])
        a, b = u.solve_linear([[26, 67], [66, 21]], [12748, 12176])
        self.assertTrue(a.denominator != 1 or b.denominator != 1)  # second machine: no whole presses
        self.assertEqual(u.solve_linear([[0, 1], [1, 0]], [3, 4]), [Fraction(4), Fraction(3)])  # needs a pivot swap
        with self.assertRaises(ValueError):
            u.solve_linear([[1, 2], [2, 4]], [1, 2])

    def test_number_theory(self):
        self.assertEqual(u.divisors(28), [1, 2, 4, 7, 14, 28])
        self.assertEqual([n for n in range(15) if u.is_prime(n)], [2, 3, 5, 7, 11, 13])


class RangesTest(unittest.TestCase):
    def test_intervals(self):
        self.assertEqual(u.merge_intervals([(10, 14), (3, 5), (16, 20), (12, 18)]), [(3, 5), (10, 20)])
        self.assertEqual(u.merge_intervals([(1, 2), (3, 4)]), [(1, 4)])  # touching ranges merge
        self.assertEqual(u.total_length([(3, 5), (10, 14), (16, 20), (12, 18)]), 14)  # 2025 day 5
        self.assertEqual(u.overlap((1, 5), (4, 9)), (4, 5))
        self.assertIsNone(u.overlap((1, 3), (4, 9)))
        self.assertEqual(u.subtract((0, 10), (3, 5)), [(0, 2), (6, 10)])
        self.assertEqual(u.subtract((0, 10), (20, 30)), [(0, 10)])
        self.assertEqual(u.subtract((3, 5), (0, 10)), [])

    def test_prefix_sums(self):
        sums = u.prefix_sums([3, 1, 4, 1, 5])
        self.assertEqual(sums[5] - sums[2], 10)


if __name__ == "__main__":
    unittest.main()
