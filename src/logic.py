import pygame as pg
import numpy as np
import interface


def create_field_arrays(n, m, mines):
    starting_points = (5, 160)
    size_board = (385, 385)
    size_field = (size_board[0] / n, size_board[1] / m)
    mines_array = np.array([interface.Field(x, y, size_field[0], size_field[1])
                            for x in np.arange(starting_points[0], starting_points[0] + size_board[0], size_field[0])
                            for y in np.arange(starting_points[1], starting_points[1] + size_board[1], size_field[1])])
    return mines_array


class IncorrectBoardSize(Exception):
    pass


class IncorrectMinesValue(Exception):
    pass


class InitializeNewGame:
    def __init__(self, n, m, mines, screen):
        self.screen = screen
        if n < 2 or n > 15 or m < 2 or m > 15:
            raise IncorrectBoardSize
        elif mines < 0 or mines > m * n:
            raise IncorrectMinesValue
        else:
            self.n = n
            self.m = m
            self.mines = mines
            self.fields = create_field_arrays(n, m, mines)

    def display(self):
        for field in self.fields:
            field.draw(self.screen, 1)
