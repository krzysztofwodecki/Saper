import unittest
import numpy as np
from src import logic
from src import interface


class StartNewGame(unittest.TestCase):
    """
    Klasa dla testu pierwszego.
    """
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

    def test_DisplayNearbyMinesCount(self):
        """
        Test nr 2
        """
        # given
        field = None
        zero_mines = True
        while zero_mines:
            i, j = (np.random.randint(0, 8), np.random.randint(0, 8))
            field = self._game.get_field(i, j)
            if not isinstance(field, interface.FieldWithMine):
                zero_mines = field.activation()

        # then
        self.assertEqual(True, field.get_clicked())
        self.assertEqual(False, zero_mines)

    def test_IfNoMinesNearbyClickSurrounding(self):
        """
        Test nr 4
        """
        # given
        i, j = (None, None)
        field = None
        empty = False
        while not isinstance(field, interface.FieldWithMine) and not empty:
            i, j = (np.random.randint(1, 7), np.random.randint(1, 7))
            field = self._game.get_field(i, j)
            empty = field.activation()

        # when
        self._game.reveal_nearby(i, j)

        # then
        for a in range(i - 1, i + 2):
            for b in range(j - 1, j + 2):
                self.assertEqual(True, self._game.get_field(a, b).get_clicked())

    def test_WhenClickMineGameOver(self):
        """
        Test nr 3
        """
        # given
        field = None
        while not isinstance(field, interface.FieldWithMine):
            i, j = (np.random.randint(0, 8), np.random.randint(0, 8))
            field = self._game.get_field(i, j)

        # when
        field.left_click()
        self._game.check_lose_condition()

        # then
        self.assertEqual(True, self._game.get_game_over())


class FieldRightClick(unittest.TestCase):
    def test_hereIsMineCountRiseWhenClicked(self):
        """
        Test nr 5
        """
        # given
        n, m, mines = (8, 8, 12)
        game = logic.Game(n, m, mines)
        i, j = (np.random.randint(1, 8), np.random.randint(1, 8))
        field = game.get_field(i, j)

        # when
        field.right_click()
        mine_count, _ = game.get_flags_count()

        # then
        self.assertEqual(1, mine_count)

    def test_hereMightBeMineCountRiseWhenClickedTwice(self):
        """
        Test nr 6
        """
        # given
        n, m, mines = (8, 8, 12)
        game = logic.Game(n, m, mines)
        i, j = (np.random.randint(1, 8), np.random.randint(1, 8))
        field = game.get_field(i, j)

        # when
        field.right_click()
        field.right_click()
        _, might_be_count = game.get_flags_count()

        # then
        self.assertEqual(1, might_be_count)

    def test_multipleMarkingOneFieldShouldBeActualized(self):
        """
        Test nr 7
        """
        # given
        n, m, mines = (8, 8, 12)
        game = logic.Game(n, m, mines)
        i, j = (np.random.randint(1, 8), np.random.randint(1, 8))
        field = game.get_field(i, j)

        # when
        for _ in range(6):
            field.right_click()
        mine_count, might_be_count = game.get_flags_count()

        # then
        self.assertEqual(0, mine_count)
        self.assertEqual(0, might_be_count)

    def test_shouldFailToMarkCheckedField(self):
        """
        Test nr 10
        """
        # given
        n, m, mines = (8, 8, 12)
        game = logic.Game(n, m, mines)
        i, j = (np.random.randint(1, 8), np.random.randint(1, 8))
        field = game.get_field(i, j)

        # when
        field.activation()
        field.right_click()
        mine_count, _ = game.get_flags_count()

        # then
        self.assertEqual(0, mine_count)


class WinConditions(unittest.TestCase):
    def test_shouldBeWinWhenClickAllFieldsWithNoMines(self):
        """
        Test nr 8
        """
        # given
        n, m, mines = (8, 8, 12)
        game = logic.Game(n, m, mines)

        # when
        for i in range(n):
            for j in range(m):
                if not isinstance(game.get_field(i,j), interface.FieldWithMine):
                    game.get_field(i, j).activation()
        game.check_win_condition()

        # then
        self.assertEqual(True, game.get_game_over())
        self.assertEqual(3, game.get_message())

    def test_shouldBeWinWhenMarkAllFieldsWithMines(self):
        """
        Test nr 9
        """
        # given
        n, m, mines = (8, 8, 12)
        game = logic.Game(n, m, mines)

        # when
        for i in range(n):
            for j in range(m):
                if isinstance(game.get_field(i, j), interface.FieldWithMine):
                    game.get_field(i, j).right_click()
        game.check_win_condition()

        # then
        self.assertEqual(True, game.get_game_over())
        self.assertEqual(3, game.get_message())


class ResetsInNewGame(unittest.TestCase):
    def test_checkFieldShouldResetInNewGame(self):
        """
        Test nr 11 - sprawdzenie pól
        """
        # given
        n, m, mines = (8, 8, 12)
        game = logic.Game(n, m, mines)

        # when
        count = 0
        for i in range(n):
            for j in range(m):
                if not isinstance(game.get_field(i,j), interface.FieldWithMine) and count != 5:
                    game.get_field(i, j).activation()
                    count += 1
        game = logic.Game(n, m, mines)

        # then
        for i in range(n):
            for j in range(m):
                self.assertEqual(False, game.get_field(i, j).get_clicked())

    def test_fieldMarkingsShouldResetInNewGame(self):
        """
        Test nr 11 - oznaczenie pól
        """
        # given
        n, m, mines = (8, 8, 12)
        game = logic.Game(n, m, mines)

        # when
        count = 0
        for i in range(n):
            for j in range(m):
                if not isinstance(game.get_field(i,j), interface.FieldWithMine) and count != 5:
                    game.get_field(i, j).right_click()
                    count += 1
        game = logic.Game(n, m, mines)
        mine_count, _ = game.get_flags_count()

        # then
        self.assertEqual(0, mine_count)

    def test_colorShouldResetAfterCheat(self):
        """
        Test nr 12
        """
        # given
        n, m, mines = (8, 8, 12)
        game = logic.Game(n, m, mines)

        # when
        game.set_cheat()
        game = logic.Game(n, m, mines)

        # then
        for i in range(n):
            for j in range(m):
                self.assertEqual((255, 255, 255), game.get_field(i, j).get_color())


if __name__ == '__main__':
    unittest.main()
