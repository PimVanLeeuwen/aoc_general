"""Tests for the daily workflow tooling in aoc.py (stdlib unittest, no network)."""

import contextlib
import io
import json
import shutil
import sys
import tempfile
import unittest
from datetime import datetime
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

import aoc  # noqa: E402

# Part 1 counts the lines, part 2 sums them.
SOLUTION = '''
def solve(puzzle_input):
    numbers = [int(line) for line in puzzle_input.split()]
    return len(numbers), sum(numbers)
'''


def quietly(function, *args, **kwargs):
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        return function(*args, **kwargs)


class WorkflowTestCase(unittest.TestCase):
    def setUp(self):
        self.root = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.root)
        shutil.copytree(REPO / "solutions" / "template", self.root / "solutions" / "template")
        self.puzzle = aoc.Puzzle(2026, 3, self.root)

    def write_solution(self, code=SOLUTION):
        self.puzzle.solution_dir.mkdir(parents=True, exist_ok=True)
        self.puzzle.solution.write_text(code)

    def write_input(self, name, text):
        self.puzzle.input_dir.mkdir(parents=True, exist_ok=True)
        (self.puzzle.input_dir / name).write_text(text)

    def write_expected(self, expected):
        self.write_input("day03.answers.json", json.dumps(expected))


class TodayPuzzleTest(unittest.TestCase):
    def test_during_the_event(self):
        self.assertEqual(aoc.today_puzzle(datetime(2026, 12, 5, 0, 1)), (2026, 5))

    def test_outside_the_event(self):
        self.assertIsNone(aoc.today_puzzle(datetime(2026, 11, 30)))
        self.assertIsNone(aoc.today_puzzle(datetime(2026, 12, 26)))


class ExamplesTest(WorkflowTestCase):
    def test_examples_in_natural_order(self):
        for name in ("day03.example10.txt", "day03.example2.txt", "day03.example.txt", "day04.example.txt"):
            self.write_input(name, "1\n")
        names = [aoc.example_name(path) for path in self.puzzle.examples()]
        self.assertEqual(names, ["example", "example2", "example10"])


class TodayTest(WorkflowTestCase):
    def test_scaffolds_everything(self):
        quietly(aoc.today, self.puzzle, fetch=lambda puzzle: "1\n2\n3")

        solution = self.puzzle.solution.read_text()
        self.assertIn("Day 03", solution)
        self.assertIn("Year: 2026", solution)
        self.assertTrue((self.puzzle.solution_dir / "meta.json").exists())
        self.assertEqual(self.puzzle.input.read_text(), "1\n2\n3\n")
        self.assertEqual(self.puzzle.examples()[0].read_text(), "")
        self.assertEqual(json.loads(self.puzzle.answers.read_text()), {"example": {"part1": "", "part2": ""}})

    def test_never_overwrites(self):
        self.write_solution("# my work")
        self.write_input("day03.txt", "real")
        self.write_input("day03.example.txt", "example")
        self.write_expected({"example": {"part1": "7"}})

        def fail_fetch(puzzle):
            raise AssertionError("must not download an existing input")

        quietly(aoc.today, self.puzzle, fetch=fail_fetch)

        self.assertEqual(self.puzzle.solution.read_text(), "# my work")
        self.assertEqual(self.puzzle.input.read_text(), "real")
        self.assertEqual(self.puzzle.examples()[0].read_text(), "example")
        self.assertEqual(json.loads(self.puzzle.answers.read_text()), {"example": {"part1": "7"}})

    def test_download_failure_is_reported_not_raised(self):
        def no_token(puzzle):
            raise RuntimeError("missing session")

        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            aoc.today(self.puzzle, fetch=no_token)

        self.assertFalse(self.puzzle.input.exists())
        self.assertIn("missing session", output.getvalue())
        self.assertTrue(self.puzzle.solution.exists())


class CheckTest(WorkflowTestCase):
    def setUp(self):
        super().setUp()
        self.write_solution()
        self.write_input("day03.example.txt", "1\n2\n")
        self.write_input("day03.txt", "10\n20\n30\n")

    def test_passing_examples_run_the_real_input(self):
        self.write_expected({"example": {"part1": "2", "part2": 3}})
        self.assertEqual(quietly(aoc.check, self.puzzle), (True, ("3", "60")))

    def test_blank_expected_answers_are_not_checked(self):
        self.write_expected({"example": {"part1": "", "part2": ""}})
        self.assertEqual(quietly(aoc.check, self.puzzle), (True, ("3", "60")))

    def test_failing_example_skips_the_real_input(self):
        self.write_expected({"example": {"part1": "2", "part2": "4"}})
        self.assertEqual(quietly(aoc.check, self.puzzle), (False, None))

    def test_force_runs_the_real_input_anyway(self):
        self.write_expected({"example": {"part1": "99"}})
        self.assertEqual(quietly(aoc.check, self.puzzle, force_real=True), (False, ("3", "60")))

    def test_second_example_checked_against_its_own_answers(self):
        self.write_input("day03.example2.txt", "5\n")
        self.write_expected({"example": {"part1": "2"}, "example2": {"part2": "6"}})
        self.assertEqual(quietly(aoc.check, self.puzzle), (False, None))

    def test_raising_solution_fails(self):
        self.write_solution("def solve(puzzle_input):\n    raise ValueError('boom')\n")
        self.assertEqual(quietly(aoc.check, self.puzzle), (False, None))

    def test_unfinished_part2_is_shown_as_empty(self):
        self.write_solution("def solve(puzzle_input):\n    return 1, ''\n")
        self.assertEqual(quietly(aoc.check, self.puzzle), (True, ("1", "")))


class WatchTest(WorkflowTestCase):
    def test_sees_changes_to_solution_and_examples(self):
        self.write_solution()
        before = aoc.watched_files(self.puzzle)
        self.write_input("day03.example.txt", "1\n")
        self.assertNotEqual(aoc.watched_files(self.puzzle), before)
        self.assertIn(self.puzzle.solution, before)


class SubmitTest(WorkflowTestCase):
    def setUp(self):
        super().setUp()
        self.write_solution()
        self.write_input("day03.example.txt", "1\n2\n")
        self.write_input("day03.txt", "10\n20\n30\n")
        self.sent = []

    def submit(self, part=2, reply="y", force=False):
        return quietly(
            aoc.submit, self.puzzle, part, force=force,
            confirm=lambda prompt: reply,
            send=lambda puzzle, part, answer: self.sent.append((part, answer)),
        )

    def test_sends_after_yes(self):
        self.assertTrue(self.submit(part=2, reply="y"))
        self.assertEqual(self.sent, [(2, "60")])

    def test_anything_but_yes_cancels(self):
        self.assertFalse(self.submit(reply=""))
        self.assertFalse(self.submit(reply="n"))
        self.assertEqual(self.sent, [])

    def test_failing_examples_block_unless_forced(self):
        self.write_expected({"example": {"part2": "999"}})
        self.assertFalse(self.submit())
        self.assertEqual(self.sent, [])
        self.assertTrue(self.submit(force=True))
        self.assertEqual(self.sent, [(2, "60")])

    def test_empty_answer_is_never_sent(self):
        self.write_solution("def solve(puzzle_input):\n    return 1, ''\n")
        self.assertFalse(self.submit(part=2))
        self.assertEqual(self.sent, [])


if __name__ == "__main__":
    unittest.main()
