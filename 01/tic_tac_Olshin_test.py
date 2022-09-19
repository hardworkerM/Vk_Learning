import unittest
from unittest.mock import patch
import tic_tac_Olshin as py


class TicTacTest(unittest.TestCase):

    @patch('builtins.input')
    def test_start_game(self, input_draw_mock):
        test_exem = py.TicTacGame()
        input_draw_mock.side_effect = ['1a', '1a', 'abs',
                                       '2b', '1b', '1c', '3a',
                                       '2a', '2c', '3b', '3c']
        self.assertFalse(test_exem.start_game())

    def test_check_winner(self):
        test_exem = py.TicTacGame()
        test_exem.board = [
            ['X', '.', 'O', '3'],
            ['.', 'X', 'O', '2'],
            ['.', '.', 'X', '1'],
            ['a', 'b', 'c']
        ]
        self.assertEqual(test_exem.check_winner(), 'X')
        test_exem.board = [
            ['O', '.', 'X', '3'],
            ['.', 'O', 'X', '2'],
            ['.', 'X', 'O', '1'],
            ['a', 'b', 'c']
        ]
        self.assertEqual(test_exem.check_winner(), 'O')
        test_exem.board = [
            ['O', '.', 'X', '3'],
            ['.', 'X', 'O', '2'],
            ['X', '.', '.', '1'],
            ['a', 'b', 'c']
        ]
        self.assertEqual(test_exem.check_winner(), 'X')
        test_exem.board = [
            ['X', '.', 'O', '3'],
            ['.', 'O', 'X', '2'],
            ['O', '.', 'X', '1'],
            ['a', 'b', 'c']
        ]
        self.assertEqual(test_exem.check_winner(), 'O')
        test_exem.board = [
            ['O', 'X', '.', '3'],
            ['O', 'X', 'O', '2'],
            ['.', 'X', '.', '1'],
            ['a', 'b', 'c']
        ]
        self.assertEqual(test_exem.check_winner(), 'X')
        test_exem.board = [
            ['X', 'O', '.', '3'],
            ['X', 'O', 'X', '2'],
            ['.', 'O', 'X', '1'],
            ['a', 'b', 'c']
        ]
        self.assertEqual(test_exem.check_winner(), 'O')
        test_exem.board = [
            ['.', '.', '.', '3'],
            ['O', 'O', '.', '2'],
            ['X', 'X', 'X', '1'],
            ['a', 'b', 'c']
        ]
        self.assertEqual(test_exem.check_winner(), 'X')
        test_exem.board = [
            ['.', 'X', 'X', '3'],
            ['X', 'X', '.', '2'],
            ['O', 'O', 'O', '1'],
            ['a', 'b', 'c']
        ]
        self.assertEqual(test_exem.check_winner(), 'O')
        test_exem.board = [
            ['O', 'X', 'O', '3'],
            ['O', 'X', 'X', '2'],
            ['X', 'O', 'X', '1'],
            ['a', 'b', 'c']
        ]
        self.assertEqual(test_exem.check_winner(), False)


if __name__ == '__main__':
    unittest.main()
