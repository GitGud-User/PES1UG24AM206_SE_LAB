from board import Board
from rules import completed_boxes, parse_board_size, parse_move, MIN_SIZE, MAX_SIZE

HELP_TEXT = """Commands:
  H row col   draw a horizontal line (e.g. H 0 1)
  V row col   draw a vertical line   (e.g. V 1 0)
  help        show this help
  quit        end the game"""


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

    def play_move(self, orientation, row, col):
        """Apply a validated move and update score/turn. Returns boxes completed."""
        before = set(self.board.completed)
        self.board.add_line(orientation, row, col, self.current)
        newly_completed = completed_boxes(self.board, before)

        if newly_completed:
            self.scores[self.current] += newly_completed
        else:
            self.current = 1 - self.current
        return newly_completed

    def run(self):
        print("Dots and Boxes")
        print("Enter moves as H row col or V row col.")
        print("Rows and columns start at 0.")
        print("Example: H 0 1   (type 'help' for commands, 'quit' to exit)")
        try:
            self.choose_board_size()
            self.game_loop()
        except (EOFError, KeyboardInterrupt):
            print("\nGame ended by user.")

    def game_loop(self):
        while not self.board.is_complete():
            self.board.display(self.scores, self.current)
            raw = input(f"Player {self.current + 1}, move: ").strip()

            if raw.lower() in {"q", "quit", "exit"}:
                print("Game ended by user.")
                return
            if raw.lower() in {"h", "help", "?"}:
                print(HELP_TEXT)
                continue

            move, error = parse_move(self.board, raw)
            if error:
                print(error)
                continue

            player = self.current
            newly_completed = self.play_move(*move)
            if newly_completed:
                print(f"Player {player + 1} completed {newly_completed} box(es) and plays again.")

        self.board.display(self.scores, self.current)
        print("Game over!")
        if self.scores[0] == self.scores[1]:
            print("The game is a draw.")
        else:
            winner = 1 if self.scores[0] > self.scores[1] else 2
            print(f"Player {winner} wins!")