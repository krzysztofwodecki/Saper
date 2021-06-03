import numpy as np
from src import interface

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
            for q in range(i - 1 if i > 0 else 0, i + 2 if i + 2 <= m else i + 1):
                for p in range(j - 1 if j > 0 else 0, j + 2 if j + 2 <= n else j + 1):
                    if isinstance(mines_array[q][p], interface.FieldWithMine):
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
        self.game_over = False
        self.cheat = False
        self.cheat_counter = 0
        self.message = None
        try:
            if size_condition(n, m):
                raise IncorrectBoardSize
            elif mines_condition(mines, n, m):
                raise IncorrectMinesValue
        except IncorrectBoardSize:
            self.message = 0
            self.n, self.m, self.mines = default_board
        except IncorrectMinesValue:
            self.message = 1
            self.n, self.m, self.mines = default_board
        else:
            self.n = n
            self.m = m
            self.mines = mines
        finally:
            self.fields = create_field_arrays(self.n, self.m, self.mines, self.color)
            self.border_values = border_values(self.n, self.m, self.fields)

    def display(self):
        for i, row in enumerate(self.fields):
            for j, field in enumerate(row):
                field.set_border_mines(self.border_values[i][j])
                field.draw(self.screen, 0, True)

    def reveal_nearby(self, i, j):
        for q in range(i - 1 if i > 0 else 0, i + 2 if i + 2 <= self.m else i + 1):
            for p in range(j - 1 if j > 0 else 0, j + 2 if j + 2 <= self.n else j + 1):
                if self.fields[q][p].activation():
                    self.reveal_nearby(q, p)

    def change_mines_color(self, color):
        for i, row in enumerate(self.fields):
            for j, field in enumerate(row):
                if isinstance(field, interface.FieldWithMine):
                    field.set_color(color)

    def reset_mines_flag(self):
        for i, row in enumerate(self.fields):
            for j, field in enumerate(row):
                if isinstance(field, interface.FieldWithMine):
                    while field.get_right_clicks() != 0:
                        field.right_click()

    def event_handler(self, event):
        if not self.game_over:
            for i, row in enumerate(self.fields):
                for j, field in enumerate(row):
                    if isinstance(field, interface.FieldWithMine):
                        clicked = field.event_handler(event)
                        if clicked:
                            self.reset_mines_flag()
                            self.change_mines_color("red")
                            self.game_over = True
                            self.message = 2
                    else:
                        is_empty = field.event_handler(event)
                        if is_empty:
                            self.reveal_nearby(i, j)
                        self.check_win_condition()

    def check_win_condition(self):
        counter_clicked = 0
        counter_flags = 0
        not_mine_clicked = True
        for row in self.fields:
            for field in row:
                if not isinstance(field, interface.FieldWithMine):
                    if field.get_clicked():
                        counter_clicked += 1
                    elif field.get_right_clicks() == 1:
                        not_mine_clicked = False
                elif isinstance(field, interface.FieldWithMine) and field.get_right_clicks() == 1:
                    counter_flags += 1
        if counter_clicked == self.n * self.m - self.mines:
            self.change_mines_color("green")
            self.game_over = True
            self.message = 3
        elif not_mine_clicked and counter_flags == self.mines:
            self.game_over = True
            self.message = 3

    def get_flags_count(self):
        mine_flag_counter = 0
        predicted_flag_counter = 0
        for row in self.fields:
            for field in row:
                if field.get_right_clicks() == 1:
                    mine_flag_counter += 1
                elif field.get_right_clicks() == 2:
                    predicted_flag_counter += 1
        return mine_flag_counter, predicted_flag_counter

    def get_message(self):
        return self.message

    def get_color(self):
        return self.color

    def get_mines(self):
        return self.mines

    def set_cheat(self):
        if not self.cheat:
            self.cheat = True
            r, g, b = self.color
            self.change_mines_color((r - 30 if r >= 30 else 0, g - 20 if g >= 20 else 0, b - 10 if b >= 10 else 0))
