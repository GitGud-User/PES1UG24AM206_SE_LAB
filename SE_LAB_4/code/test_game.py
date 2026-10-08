import unittest

from board import Board
from game import DotsAndBoxes
from rules import parse_move, parse_board_size


def play(game, *moves):
    """Play a list of moves like 'H 0 0' through the real validation + game logic."""
    for text in moves:
        move, error = parse_move(game.board, text)
        if error:
            raise AssertionError(f"{text!r} rejected: {error}")
        game.play_move(*move)


class TestMoves(unittest.TestCase):
    def setUp(self):
        self.game = DotsAndBoxes(2, 2)

    def test_valid_horizontal_move(self):
        play(self.game, "H 0 1")
        self.assertTrue(self.game.board.horizontal[0][1])
        self.assertEqual(self.game.current, 1)  # no box -> turn passes
        self.assertEqual(self.game.scores, [0, 0])

    def test_valid_vertical_move(self):
        play(self.game, "V 1 2")
        self.assertTrue(self.game.board.vertical[1][2])
        self.assertEqual(self.game.current, 1)

    def test_lowercase_move_accepted(self):
        play(self.game, "v 0 0")
        self.assertTrue(self.game.board.vertical[0][0])

    def test_repeated_move_rejected(self):
        play(self.game, "H 0 0")
        move, error = parse_move(self.game.board, "H 0 0")
        self.assertIsNone(move)
        self.assertIn("already", error)

    def test_invalid_inputs_rejected(self):
        for text in ["", "hello", "X 0 0", "H a b", "H -1 0", "H 3 0", "V 0 3", "H 0 0 0"]:
            move, error = parse_move(self.game.board, text)
            self.assertIsNone(move, text)
            self.assertTrue(error, text)

    def test_invalid_input_does_not_change_state(self):
        play(self.game, "H 0 0")
        snapshot = ([r[:] for r in self.game.board.horizontal],
                    [r[:] for r in self.game.board.vertical],
                    self.game.scores[:], self.game.current)
        for text in ["H 0 0", "H 9 9", "junk"]:
            parse_move(self.game.board, text)
        self.assertEqual(snapshot, ([r[:] for r in self.game.board.horizontal],
                                    [r[:] for r in self.game.board.vertical],
                                    self.game.scores, self.game.current))

    def test_board_rejects_illegal_add_line(self):
        board = Board(2, 2)
        board.add_line("H", 0, 0)
        with self.assertRaises(ValueError):
            board.add_line("H", 0, 0)
        with self.assertRaises(ValueError):
            board.add_line("V", 5, 5)


class TestBoxes(unittest.TestCase):
    def test_completing_a_box_scores_and_keeps_turn(self):
        game = DotsAndBoxes(2, 2)
        play(game, "H 0 0", "V 0 0", "H 1 0")  # P1, P2, P1
        self.assertEqual(game.current, 1)       # P2 to move
        play(game, "V 0 1")                     # P2 closes box (0,0)
        self.assertEqual(game.scores, [0, 1])
        self.assertEqual(game.current, 1)       # P2 plays again
        self.assertEqual(game.board.completed, {(0, 0): 1})

    def test_one_line_completing_two_boxes(self):
        game = DotsAndBoxes(2, 1)
        play(game, "H 0 0", "V 0 0", "V 0 1", "H 2 0", "V 1 0", "V 1 1")
        player = game.current
        play(game, "H 1 0")  # middle line closes both boxes
        self.assertEqual(game.scores[player], 2)
        self.assertEqual(game.current, player)


class TestEndOfGame(unittest.TestCase):
    def test_game_ends_when_all_lines_drawn(self):
        game = DotsAndBoxes(1, 1)
        play(game, "H 0 0", "H 1 0", "V 0 0")
        self.assertFalse(game.board.is_complete())
        play(game, "V 0 1")
        self.assertTrue(game.board.is_complete())
        self.assertEqual(sum(game.scores), 1)

    def test_no_moves_after_board_complete(self):
        game = DotsAndBoxes(1, 1)
        play(game, "H 0 0", "H 1 0", "V 0 0", "V 0 1")
        move, error = parse_move(game.board, "H 0 0")
        self.assertIsNone(move)
        self.assertIn("complete", error)

    def test_full_2x2_game_scores_add_up(self):
        game = DotsAndBoxes(2, 2)
        play(game, "H 0 0", "H 0 1", "H 1 0", "H 1 1", "H 2 0", "H 2 1",
             "V 0 0", "V 0 1", "V 0 2", "V 1 0", "V 1 1", "V 1 2")
        self.assertTrue(game.board.is_complete())
        self.assertEqual(sum(game.scores), 4)


class TestBoardSize(unittest.TestCase):
    def test_parse_board_size(self):
        self.assertEqual(parse_board_size(""), (2, 2))
        self.assertEqual(parse_board_size("3 4"), (3, 4))
        self.assertEqual(parse_board_size("3x3"), (3, 3))
        for bad in ["0 2", "9 9", "a b", "3"]:
            self.assertIsNone(parse_board_size(bad), bad)


if __name__ == "__main__":
    unittest.main()
