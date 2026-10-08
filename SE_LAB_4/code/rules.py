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


def parse_move(board, text):
    """Turn raw input like 'h 0 1' into (orientation, row, col).
    Returns (move, None) on success or (None, error_message) on failure.
    Never changes the board."""
    if board.is_complete():
        return None, "The board is already complete. No more moves can be made."

    parts = text.strip().upper().split()
    if len(parts) != 3:
        return None, "Invalid format. Use: H row col  or  V row col (e.g. H 0 1)."

    orientation, row_text, col_text = parts
    if orientation not in {"H", "V"}:
        return None, "Direction must be H (horizontal) or V (vertical)."

    try:
        row, col = int(row_text), int(col_text)
    except ValueError:
        return None, "Row and column must be whole numbers."

    if orientation == "H":
        max_row, max_col = board.rows, board.cols - 1
    else:
        max_row, max_col = board.rows - 1, board.cols
    if not (0 <= row <= max_row and 0 <= col <= max_col):
        return None, (f"Out of range. For {orientation} lines, row must be 0-{max_row} "
                      f"and column 0-{max_col}.")

    if not valid_move(board, orientation, row, col):
        return None, "That line has already been drawn. Choose another."

    return (orientation, row, col), None