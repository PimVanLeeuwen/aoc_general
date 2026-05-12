"""
Day 04 - Giant Squid
Year: 2021

Simulate bingo against a giant squid: find the first and last
boards to win and compute their scores.
"""


def parse_bingo(text):
    """Parse draw numbers and bingo boards from input."""
    blocks = text.strip().split("\n\n")
    draws = [int(x) for x in blocks[0].split(",")]
    boards = []
    for block in blocks[1:]:
        board = []
        for line in block.strip().split("\n"):
            board.append([int(x) for x in line.split()])
        boards.append(board)
    return draws, boards


def check_win(marked, board_size=5):
    """Check if any row or column is fully marked."""
    for i in range(board_size):
        if all(marked[i][j] for j in range(board_size)):
            return True
        if all(marked[j][i] for j in range(board_size)):
            return True
    return False


def board_score(board, marked):
    """Sum of unmarked numbers on the board."""
    total = 0
    for r in range(5):
        for c in range(5):
            if not marked[r][c]:
                total += board[r][c]
    return total


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    draws, boards = parse_bingo(puzzle_input)

    marked = [[[False] * 5 for _ in range(5)] for _ in boards]
    won = [False] * len(boards)
    first_score = None
    last_score = None

    for number in draws:
        for b, board in enumerate(boards):
            if won[b]:
                continue
            for r in range(5):
                for c in range(5):
                    if board[r][c] == number:
                        marked[b][r][c] = True

            if check_win(marked[b]):
                won[b] = True
                score = board_score(board, marked[b]) * number
                if first_score is None:
                    first_score = score
                last_score = score

    return str(first_score), str(last_score)


def visualize(puzzle_input: str):
    """Yield frames showing bingo game progression."""
    draws, boards = parse_bingo(puzzle_input)

    yield {
        "type": "text",
        "lines": [
            "  Giant Squid Bingo",
            "",
            f"  Boards: {len(boards)}",
            f"  Numbers to draw: {len(draws)}",
        ],
        "delay": 600,
    }

    marked = [[[False] * 5 for _ in range(5)] for _ in boards]
    won = [False] * len(boards)
    win_order = []

    for number in draws:
        for b, board in enumerate(boards):
            if won[b]:
                continue
            for r in range(5):
                for c in range(5):
                    if board[r][c] == number:
                        marked[b][r][c] = True
            if check_win(marked[b]) and not won[b]:
                won[b] = True
                score = board_score(board, marked[b]) * number
                win_order.append((b, number, score))

    progress = ["  Win order:", ""]
    for i, (b, num, score) in enumerate(win_order):
        if i < 5 or i >= len(win_order) - 3:
            progress.append(f"  #{i + 1:>3}: Board {b + 1:>3} on number {num:>2} (score {score})")
        elif i == 5:
            progress.append(f"  ... ({len(win_order) - 8} more boards) ...")

    yield {
        "type": "text",
        "lines": progress,
        "delay": 800,
    }

    yield {
        "type": "text",
        "lines": [
            "  ===================================",
            "  Results",
            "  ===================================",
            "",
            f"  Part 1: {win_order[0][2]} (first winner)",
            f"  Part 2: {win_order[-1][2]} (last winner)",
        ],
        "delay": 500,
    }
