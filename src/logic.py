import numpy as np
from src import interface

# Wyrażenia lambda decydujące o dopuszczalnych rozmiarach planszy czy liczby min
size_condition = lambda n, m: n > 15 or n < 2 or m > 15 or m < 2
mines_condition = lambda mines, n, m: mines < 0 or mines > m * n

# Domyślny kolor
white = (255, 255, 255)


def create_field_arrays(n, m, mines, color=white):
    """
    Funkcja tworząca plansze pod postacią macierzy pól zarówno z jak i bez min. Funkcja korzysta z biblioteki numpy
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
            mines_array[a][b] = interface.FieldWithMine(mines_array[a][b].x, mines_array[a][b].y,
                                                        mines_array[a][b].w, mines_array[a][b].h, color)
    return mines_array


def border_values(n, m, mines_array):
    """
    Funkcja wyliczająca dla każdego pola na planszy liczbę min jaka je otacza.
    :param n: pierwszy rozmiar planszy
    :param m: drugi rozmiar planszy
    :param mines_array: macierz pól
    :return: macierz liczby min w każdym polu
    """
    return np.array([[count_mines_nearby(n, m, mines_array, i, j) for j, field in enumerate(row)]
                     for i, row in enumerate(mines_array)])


def count_mines_nearby(n, m, mines_array, i, j):
    """
    Funkcja tworząca macierz prawdy dookoła danego pola i zliczająca liczbę wystąpień tej prawdy.
    :param n: pierwszy rozmiar planszy
    :param m: drugi rozmiar planszy
    :param mines_array: macierz pól
    :param i: pierwszy indeks pola
    :param j: drugi indeks pola
    :return:
    """
    return np.sum(np.array([[1 if isinstance(mines_array[q][p], interface.FieldWithMine) else 0
                             for p in range(j - 1 if j > 0 else 0, j + 2 if j + 2 <= n else j + 1)]
                            for q in range(i - 1 if i > 0 else 0, i + 2 if i + 2 <= m else i + 1)]))


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
        self.__screen = screen
        self.__color = color
        self.__game_over = False
        self.__cheat = False
        self.__message = None

        # Część decydująca o poprawności nadchodzących danych.
        try:
            if size_condition(n, m):
                raise IncorrectBoardSize
            elif mines_condition(mines, n, m):
                raise IncorrectMinesValue
        except IncorrectBoardSize:
            # Niepoprawny rozmiar planszy. Ustawia odpowiednią wiadomość do wysłania do interfejsu.
            self.__message = 0
        except IncorrectMinesValue:
            # Niepoprawna liczba min. Ustawia odpowiednią wiadomość do wysłania do interfejsu.
            self.__message = 1
        else:
            self.__n = n
            self.__m = m
            self.__mines = mines
            self.__fields = create_field_arrays(self.__n, self.__m, self.__mines, self.__color)
            self.__border_values = border_values(self.__n, self.__m, self.__fields)

    def display(self):
        """
        Metoda wywołująca dla każdego pola z macierzy pól metodę draw.
        """
        for i, row in enumerate(self.__fields):
            for j, field in enumerate(row):
                field.set_border_mines(self.__border_values[i][j])
                field.draw(self.__screen, 0, True)

    def reveal_nearby(self, i, j):
        """
        Metoda rekurencyjnie odkrywająca sąsiednie pola jeśli są spełnione do tego warunki.
        :param i: pozycja x pola
        :param j: pozycja y pola
        """
        for q in range(i - 1 if i > 0 else 0, i + 2 if i + 2 <= self.__m else i + 1):
            for p in range(j - 1 if j > 0 else 0, j + 2 if j + 2 <= self.__n else j + 1):
                if self.__fields[q][p].activation():
                    self.reveal_nearby(q, p)

    def change_mines_color(self, color):
        """
        Metoda zmieniająca kolor min. Przydatna w momencie pokazania wygranej, przegranej, bądź wykorzystania kodu.
        :param color: na jaki kolor chcemy zmienić
        """
        for i, row in enumerate(self.__fields):
            for j, field in enumerate(row):
                if isinstance(field, interface.FieldWithMine):
                    field.set_color(color)

    def reset_mines_flag(self):
        """
        Metoda resetująca flagi dla pól z minami.
        """
        for i, row in enumerate(self.__fields):
            for j, field in enumerate(row):
                if isinstance(field, interface.FieldWithMine):
                    field.set_right_clicks(0)

    def event_handler(self, event):
        """
        Event handler dla logiki iterujący po każdym polu w macierzy i przekazujący do każdego pola event.
        :param event: przychodzące wydarzenie
        """
        if not self.__game_over:
            for i, row in enumerate(self.__fields):
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
                        if field.get_clicked():
                            field.set_right_clicks(0)
                        if is_empty:
                            self.reveal_nearby(i, j)
                        self.check_win_condition()

    def check_lose_condition(self):
        """
        Metoda sprawdzająca czy gracz przegrał.
        """
        click_count = 0
        for i, row in enumerate(self.__fields):
            for j, field in enumerate(row):
                if isinstance(field, interface.FieldWithMine):
                    if field.get_clicked():
                        click_count += 1
        if click_count > 0:
            self.reset_mines_flag()
            self.change_mines_color("red")
            self.__game_over = True
            self.__message = 2

    def check_win_condition(self):
        """
        Metoda sprawdzająca dwa niezależne od siebie warunki wygranej rozgrywki.
        """
        counter_clicked = 0
        counter_flags = 0
        not_mine_clicked = True
        for row in self.__fields:
            for field in row:
                if not isinstance(field, interface.FieldWithMine):
                    if field.get_clicked():
                        counter_clicked += 1
                    elif field.get_right_clicks() == 1:
                        not_mine_clicked = False
                elif isinstance(field, interface.FieldWithMine) and field.get_right_clicks() == 1:
                    counter_flags += 1

        if counter_clicked == self.__n * self.__m - self.__mines:
            # Wariant z kliknięciem wszystkich pól niebędących minami
            self.change_mines_color("green")
            self.reset_mines_flag()
            self.__game_over = True
            self.__message = 3
        elif not_mine_clicked and counter_flags == self.__mines:
            # Wariant z zaznaczeniem flagami wszystkich pól z minami
            self.__game_over = True
            self.__message = 3

    def get_flags_count(self):
        """
        Metoda zliczająca ilość postawionych flag "Tu jest mina" oraz "Tu może być mina".
        :return: (liczba flag "Tu jest mina", liczba flag "Tu może być mina")
        """
        mine_flag_counter = 0
        predicted_flag_counter = 0
        for row in self.__fields:
            for field in row:
                if field.get_right_clicks() == 1:
                    mine_flag_counter += 1
                elif field.get_right_clicks() == 2:
                    predicted_flag_counter += 1
        return mine_flag_counter, predicted_flag_counter

    def get_field(self, i, j):
        return self.__fields[i][j]

    def get_message(self):
        return self.__message

    def get_game_over(self):
        return self.__game_over

    def get_color(self):
        return self.__color

    def get_mines(self):
        return self.__mines

    def set_cheat(self):
        """
        Metoda ustawiająca cheaty do gry po wciśnięciu kombinacji "xyzzy" oraz zmieniająca kolor pól z minami.
        """
        if not self.__cheat:
            self.__cheat = True
            r, g, b = self.__color
            self.change_mines_color((r - 30 if r >= 30 else 0, g - 20 if g >= 20 else 0, b - 10 if b >= 10 else 0))
