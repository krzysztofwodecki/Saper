import numpy as np
import interface

size_condition = lambda n, m: n > 15 or n < 2 or m > 15 or m < 2
mines_condition = lambda mines, n, m: mines < 0 or mines > m * n

default_board = (6, 6, 4)

white = (255, 255, 255)
black = (0, 0, 0)


def create_field_arrays(n, m, mines, color=white):
    starting_points = (5, 160)
    size_board = (385, 385)
    size_field = (size_board[0] / n, size_board[1] / m)
    mines_array = np.array([[interface.Field(x, y, size_field[0], size_field[1], color)
                             for x in np.arange(starting_points[0], starting_points[0] + size_board[0], size_field[0])]
                            for y in np.arange(starting_points[1], starting_points[1] + size_board[1], size_field[1])])

    i = mines
    while i > 0:
        a = np.random.randint(0, m)
        b = np.random.randint(0, n)
        if not isinstance(mines_array[a][b], interface.FieldWithMine):
            i -= 1
            mines_array[a][b] = interface.FieldWithMine(mines_array[a][b].get_x(), mines_array[a][b].get_y(),
                                                        mines_array[a][b].get_w(), mines_array[a][b].get_h(), color)
    return mines_array


def border_values(n, m, mines_array):
    border = []
    for i, row in enumerate(mines_array):
        border_sub_array = []
        for j, field in enumerate(row):
            counter = 0
            for k in range(i-1 if i > 0 else 0, i + 2 if i + 2 < n else i + 1):
                for l in range(j-1 if j > 0 else 0, j + 2 if j + 2 < m else j + 1):
                    if isinstance(mines_array[k][l], interface.FieldWithMine) and k!=l:
                        counter += 1
            border_sub_array.append(counter)
        border.append(border_sub_array)
    return np.array(border)


class IncorrectBoardSize(Exception):
    pass


class IncorrectMinesValue(Exception):
    pass


class InitializeNewGame:
    def __init__(self, n, m, mines, screen, color=white):
        self.screen = screen
        self.color = color
        try:
            if size_condition(n, m):
                raise IncorrectBoardSize
            elif mines_condition(mines, n, m):
                raise IncorrectMinesValue
        except IncorrectBoardSize:
            self.n, self.m, self.mines = default_board
        except IncorrectMinesValue:
            self.n, self.m, self.mines = default_board
        else:
            self.n = n
            self.m = m
            self.mines = mines
        finally:
            self.fields = create_field_arrays(self.n, self.m, self.mines, self.color)
            self.border_values = border_values(self.n, self.m, self.fields)
            print(self.fields)
            print(self.border_values)

    def display(self, font):
        for i, row in enumerate(self.fields):
            for j, field in enumerate(row):
                field.set_border_mines(self.border_values[i][j])
                field.draw(self.screen, 0, True)

    def event_handler(self, event):
        for row in self.fields:
            for field in row:
                field.event_handler(event)
