class Board:
    def __init__(self, rows=2, cols=2):
        self.rows = rows
        self.cols = cols
        self.horizontal = [[False] * cols for _ in range(rows + 1)]
        self.vertical = [[False] * (cols + 1) for _ in range(rows)]
        # Maps each completed box (row, col) to the player index (0 or 1) who claimed it
        self.completed = {}

    def add_line(self, orientation, row, col, player=0):
        # Defensive check: never let a bad call corrupt the board
        if orientation == "H":
            if not (0 <= row <= self.rows and 0 <= col < self.cols) or self.horizontal[row][col]:
                raise ValueError(f"Illegal move: {orientation} {row} {col}")
        elif orientation == "V":
            if not (0 <= row < self.rows and 0 <= col <= self.cols) or self.vertical[row][col]:
                raise ValueError(f"Illegal move: {orientation} {row} {col}")
        else:
            raise ValueError(f"Illegal orientation: {orientation}")

        if orientation == "H":
            self.horizontal[row][col] = True
        else:
            self.vertical[row][col] = True
        self._update_completed(player)
        
    def _update_completed(self, player):
        for r in range(self.rows):
            for c in range(self.cols):
                if (
                    (r, c) not in self.completed
                    and self.horizontal[r][c]
                    and self.horizontal[r + 1][c]
                    and self.vertical[r][c]
                    and self.vertical[r][c + 1]
                ):
                    self.completed[(r, c)] = player

    def is_complete(self):
        total = self.rows * (self.cols + 1) + self.cols * (self.rows + 1)
        used = sum(map(sum, self.horizontal)) + sum(map(sum, self.vertical))
        return used == total

    def display(self, scores, current):
        print()
        print(f"Scores: P1={scores[0]}  P2={scores[1]} | Turn: P{current + 1}")

        # Column numbers for horizontal lines
        print("   " + "".join(f"  {c} " for c in range(self.cols)))
        for r in range(self.rows + 1):
            # Draw a dot at every corner (including both ends) so lines align with walls
            line = f"{r:>2} ."
            for c in range(self.cols):
                line += ("---" if self.horizontal[r][c] else "   ") + "."
            print(line)
            if r < self.rows:
                middle = ["   "]
                for c in range(self.cols + 1):
                    wall = "|" if self.vertical[r][c] else " "
                    middle.append(wall)
                    if c < self.cols:
                        owner = self.completed.get((r, c))
                        mark = " " if owner is None else str(owner + 1)
                        middle.append(f" {mark} ")
                print("".join(middle))
        print()