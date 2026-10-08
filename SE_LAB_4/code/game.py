from board import Board
from rules import valid_move, completed_boxes, parse_board_size, MIN_SIZE, MAX_SIZE

class DotsAndBoxes:
    def __init__(self, rows=2, cols=2):
        self.board = Board(rows, cols)
        self.current = 0
        self.scores = [0, 0]

    def choose_board_size(self):
        while True:
            raw = input(f"Board size as 'rows cols' ({MIN_SIZE}-{MAX_SIZE}, Enter for 2 2): ")
            size = parse_board_size(raw)
            if size:
                self.board = Board(*size)
                return
            print(f"Please enter two numbers between {MIN_SIZE} and {MAX_SIZE}, e.g. 3 3.")

    def run(self):
        print("Dots and Boxes")
        print("Enter moves as H row col or V row col.")
        print("Rows and columns start at 0.")
        print("Example: H 0 1")
        self.choose_board_size()

        while not self.board.is_complete():
            self.board.display(self.scores, self.current)
            raw = input(f"Player {self.current + 1}, move: ").strip().upper()
            parts = raw.split()

            if len(parts) != 3:
                print("Invalid format.")
                continue

            orientation, row, col = parts
            if not row.isdigit() or not col.isdigit():
                print("Row and column must be numbers.")
                continue

            row, col = int(row), int(col)
            if not valid_move(self.board, orientation, row, col):
                print("Invalid or already-used move.")
                continue

            before = set(self.board.completed)
            self.board.add_line(orientation, row, col, self.current)
            newly_completed = completed_boxes(self.board, before)

            if newly_completed:
                self.scores[self.current] += newly_completed
                print(f"Player {self.current + 1} completed {newly_completed} box(es) and plays again.")
            else:
                self.current = 1 - self.current

        self.board.display(self.scores, self.current)
        print("Game over!")
        if self.scores[0] == self.scores[1]:
            print("The game is a draw.")
        else:
            winner = 1 if self.scores[0] > self.scores[1] else 2
            print(f"Player {winner} wins!")