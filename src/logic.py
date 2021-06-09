import numpy as np
from src import interface

# Wyrażenia lambda decydujące o dopuszczalnych rozmiarach planszy czy liczby min
size_condition = lambda n, m: n > 15 or n < 2 or m > 15 or m < 2
mines_condition = lambda mines, n, m: mines < 0 or mines > m * n

# Domyślna plansza
default_board = (6, 6, 4)
white = (255, 255, 255)

def create_field_arrays(n, m, mines, color="white"):
    """
    Funckja tworząca plansze pod postacią macierzy pól zarówno z jak i bez min. Funkcja korzysta z biblioteki numpy
    celem optymalizacji czasu pracy oraz potrzeby wykorzystania bardziej zaawansowanych wariantów generatora range()
    i funkcji generujących liczby pseudolosowe.
    :param n: pierwszy rozmiar planszy
    :param m: drugi rozmiar planszy
    :param mines: liczba min na planszy
    :param color: kolor pól
    :return: macierz pól
    """
    starting_points = (5, 160)
    size_board = (385, 385)
    size_field = (size_board[0] / n, size_board[1] / m)

    # Utworzenie macierzy z samymi polami bez min
    mines_array = np.array([[interface.Field(x, y, size_field[0], size_field[1], color)
                             for x in np.arange(starting_points[0], starting_points[0] + size_board[0], size_field[0])]
                            for y in np.arange(starting_points[1], starting_points[1] + size_board[1], size_field[1])])

    # Pętla losująca położenia zadanej liczby min
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
    """
    Funkcja wyliczająca dla każdego pola na planszy liczbę min jaka je otacza.
    :param n: pierwszy rozmiar planszy
    :param m: drugi rozmiar planszy
    :param mines_array: macierz pól
    :return: macierz liczby min w każdym polu
    """
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
    """
    Wyjątek rzucany w momencie otrzymania niepoprawnego rozmiaru planszy.
    """
    pass


class IncorrectMinesValue(Exception):
    """
    Wyjątek rzucany w momencie otrzymania niepoprawnej liczby min.
    """
    pass


class Game:
    """
    Klasa definiująca logiczną część gry.
    """
    def __init__(self, n, m, mines, screen=None, color=white):
        self._screen = screen
        self._color = color
        self._game_over = False
        self._cheat = False
        self._message = None

        # Część decydująca o poprawności nadchodzących danych.
        try:
            if size_condition(n, m):
                raise IncorrectBoardSize
            elif mines_condition(mines, n, m):
                raise IncorrectMinesValue
        except IncorrectBoardSize:
            # Niepoprawny rozmiar planszy. Ustawia odpowiednią wiadomość do wysłania do interfejsu i inicjuje
            # domyślną grę.
            self._message = 0
            self._n, self._m, self._mines = default_board
        except IncorrectMinesValue:
            # Niepoprawna liczba min. Ustawia odpowiednią wiadomość do wysłania do interfejsu i inicjuje
            # domyślną grę.
            self._message = 1
            self._n, self._m, self._mines = default_board
        else:
            self._n = n
            self._m = m
            self._mines = mines
        finally:
            # Wywoływane są funkcje tworzące macierz pól oraz macierz liczby sąsiednich min.
            self._fields = create_field_arrays(self._n, self._m, self._mines, self._color)
            self._border_values = border_values(self._n, self._m, self._fields)

    def display(self):
        """
        Metoda wywołująca dla każdego pola z macierzy pól metodę draw.
        """
        for i, row in enumerate(self._fields):
            for j, field in enumerate(row):
                field.set_border_mines(self._border_values[i][j])
                field.draw(self._screen, 0, True)

    def reveal_nearby(self, i, j):
        """
        Metoda rekurencyjnie odkrywająca sąsiednie pola jeśli są spełnione do tego warunki.
        :param i: pozycja x pola
        :param j: pozycja y pola
        """
        for q in range(i - 1 if i > 0 else 0, i + 2 if i + 2 <= self._m else i + 1):
            for p in range(j - 1 if j > 0 else 0, j + 2 if j + 2 <= self._n else j + 1):
                if self._fields[q][p].activation():
                    self.reveal_nearby(q, p)

    def change_mines_color(self, color):
        """
        Metoda zmieniająca kolor min. Przydatna w momencie pokazania wygranej, przegranej, bądź wykorzystania kodu.
        :param color: na jaki kolor chcemy zmienić
        """
        for i, row in enumerate(self._fields):
            for j, field in enumerate(row):
                if isinstance(field, interface.FieldWithMine):
                    field.set_color(color)

    def reset_mines_flag(self):
        """
        Metoda resetująca flagi dla pól z minami.
        """
        for i, row in enumerate(self._fields):
            for j, field in enumerate(row):
                if isinstance(field, interface.FieldWithMine):
                    while field.get_right_clicks() != 0:
                        field.right_click()

    def event_handler(self, event):
        if not self._game_over:
            for i, row in enumerate(self._fields):
                for j, field in enumerate(row):
                    if isinstance(field, interface.FieldWithMine):
                        # W wypadku, gdy kliknięte pole jest miną gra się kończy.
                        field.event_handler(event)
                        self.check_lose_condition()
                    else:
                        # W momencie, gdy kliknięte pole nie jest miną sprawdzane jest czy sąsiaduje z polami z miną.
                        # Jeśli tak to nie dzieje się nic, jeśli nie to odkrywane są pola sąsiadujące.
                        # Sprawdzany jest również warunek wygranej.
                        is_empty = field.event_handler(event)
                        if is_empty:
                            self.reveal_nearby(i, j)
                        self.check_win_condition()

    def check_lose_condition(self):
        click_count = 0
        for i, row in enumerate(self._fields):
            for j, field in enumerate(row):
                if isinstance(field, interface.FieldWithMine):
                    if field.get_clicked():
                        click_count += 1
        if click_count > 0:
            self.reset_mines_flag()
            self.change_mines_color("red")
            self._game_over = True
            self._message = 2

    def check_win_condition(self):
        """
        Metoda sprawdzająca dwa niezależne od siebie warunki wygranej rozgrywki.
        """
        counter_clicked = 0
        counter_flags = 0
        not_mine_clicked = True
        for row in self._fields:
            for field in row:
                if not isinstance(field, interface.FieldWithMine):
                    if field.get_clicked():
                        counter_clicked += 1
                    elif field.get_right_clicks() == 1:
                        not_mine_clicked = False
                elif isinstance(field, interface.FieldWithMine) and field.get_right_clicks() == 1:
                    counter_flags += 1

        if counter_clicked == self._n * self._m - self._mines:
            # Wariant z kliknięciem wszystkich pól niebędących minami
            self.change_mines_color("green")
            self.reset_mines_flag()
            self._game_over = True
            self._message = 3
        elif not_mine_clicked and counter_flags == self._mines:
            # Wariant z zaznaczeniem flagami wszystkich pól z minami
            self._game_over = True
            self._message = 3

    def get_flags_count(self):
        """
        Metoda zliczająca ilość postawionych flag "Tu jest mina" oraz "Tu może być mina".
        :return: (liczba flag "Tu jest mina", liczba flag "Tu może być mina")
        """
        mine_flag_counter = 0
        predicted_flag_counter = 0
        for row in self._fields:
            for field in row:
                if field.get_right_clicks() == 1:
                    mine_flag_counter += 1
                elif field.get_right_clicks() == 2:
                    predicted_flag_counter += 1
        return mine_flag_counter, predicted_flag_counter

    def get_field(self, i, j):
        return self._fields[i][j]

    def get_message(self):
        return self._message

    def get_game_over(self):
        return self._game_over

    def get_color(self):
        return self._color

    def get_mines(self):
        return self._mines

    def set_cheat(self):
        """
        Metoda ustawiająca cheaty do gry po wciśnięciu kombinacji "xyzzy" oraz zmieniająca kolor pól z minami.
        """
        if not self._cheat:
            self._cheat = True
            r, g, b = self._color
            self.change_mines_color((r - 30 if r >= 30 else 0, g - 20 if g >= 20 else 0, b - 10 if b >= 10 else 0))
