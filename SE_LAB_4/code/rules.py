MIN_SIZE = 1
MAX_SIZE = 5


def valid_move(board, orientation, row, col):
    if orientation not in {"H", "V"}:
        return False

    if orientation == "H":
        return (
            0 <= row <= board.rows
            and 0 <= col < board.cols
            and not board.horizontal[row][col]
        )

    return (
        0 <= row < board.rows
        and 0 <= col <= board.cols
        and not board.vertical[row][col]
    )


def completed_boxes(board, before):
    return len(set(board.completed) - set(before))


def parse_board_size(text):
    """Parse 'rows cols' (e.g. '3 3'). Returns (rows, cols) or None if invalid.
    Empty input means the default 2x2 board."""
    text = text.strip().lower().replace("x", " ")
    if not text:
        return 2, 2
    parts = text.split()
    if len(parts) != 2 or not all(p.isdigit() for p in parts):
        return None
    rows, cols = int(parts[0]), int(parts[1])
    if not (MIN_SIZE <= rows <= MAX_SIZE and MIN_SIZE <= cols <= MAX_SIZE):
        return None
    return rows, cols