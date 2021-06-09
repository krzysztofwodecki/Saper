import unittest
import numpy as np
from src import main
from src import logic
from src import interface


class StartNewGame(unittest.TestCase):
    def test_1x1_1(self):
        n, m, mines = (1, 1, 1)
        logic.Game(n, m, mines)
        self.assertRaises(logic.IncorrectBoardSize)

    def test_5x1_2(self):
        n, m, mines = (5, 1, 2)
        logic.Game(n, m, mines)
        self.assertRaises(logic.IncorrectBoardSize)

    def test_4x1_2(self):
        n, m, mines = (4, 1, 2)
        logic.Game(n, m, mines)
        self.assertRaises(logic.IncorrectBoardSize)

    def test_20x200_12(self):
        n, m, mines = (20, 200, 12)
        logic.Game(n, m, mines)
        self.assertRaises(logic.IncorrectBoardSize)

    def test_5x6_minus4(self):
        n, m, mines = (5, 6, -4)
        logic.Game(n, m, mines)
        self.assertRaises(logic.IncorrectMinesValue)

    def test_3x3_10(self):
        n, m, mines = (3, 3, 10)
        logic.Game(n, m, mines)
        self.assertRaises(logic.IncorrectMinesValue)

    def test_1x10_5(self):
        n, m, mines = (1, 10, 5)
        logic.Game(n, m, mines)
        self.assertRaises(logic.IncorrectBoardSize)


class FieldLeftClick(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        n, m, mines = (8, 8, 12)
        cls._game = logic.Game(n, m, mines)

    def test_DisplayMinesCountNearby(self):
        field = None
        zero_mines = True
        while zero_mines:
            i, j = (np.random.randint(0, 8), np.random.randint(0, 8))
            field = self._game.get_field(i, j)
            if not isinstance(field, interface.FieldWithMine):
                zero_mines = field.activation()
        self.assertEqual(zero_mines, False)
        self.assertEqual(field.get_clicked(), True)

    def test_ClickMineGameOver(self):
        field = None
        while not isinstance(field, interface.FieldWithMine):
            i, j = (np.random.randint(0, 8), np.random.randint(0, 8))
            field = self._game.get_field(i, j)
        field.left_click()
        self._game.check_lose_condition()
        self.assertEqual(self._game.get_game_over(), True)

    def test_IfNoMinesNearbyClickSurrounding(self):
        i, j = (None, None)
        field = None
        empty = False
        while not isinstance(field, interface.FieldWithMine) and not empty:
            i, j = (np.random.randint(1, 7), np.random.randint(1, 7))
            field = self._game.get_field(i, j)
            empty = field.activation()
        self._game.reveal_nearby(i, j)
        count = 0
        for a in range(i - 1, i + 2):
            for b in range(j - 1, j + 2):
                if self._game.get_field(a, b).get_clicked():
                    count += 1
        self.assertEqual(9, count)


if __name__ == '__main__':
    unittest.main()
