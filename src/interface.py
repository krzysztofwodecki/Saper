from abc import abstractmethod, ABC


import pygame as pg

black = (0, 0, 0)
white = (255, 255, 255)


def set_window(size=(400, 400), title=" ", color=white):
    """
    Funkcja tworząca okienko.
    :param size: rozmiar okna
    :param title: tytuł okna
    :param color: kolor tła
    :return: okno
    """
    pg.init()
    screen = pg.display.set_mode(size)
    pg.display.set_caption(title)
    screen.fill(color)
    pg.display.flip()
    return screen


def write_text(font, screen, text="", position=(0, 0), color="black"):
    """
    Funkcja wypisująca zadany tekst w podanym miejscu.
    :param font: Używa wybranego przez nas fonta
    :param screen: Wyświetla tekst w zadanym oknie
    :param text: Tekst do wyświetlenia
    :param position: Pozycja tekstu na ekranie
    :param color: Kolor tekstu
    """
    img = font.render(text, True, color)
    screen.blit(img, position)


class Rectangle:
    """
    Klasa, po której dziedziczy większość dalszych klas. Definiuje najbardziej podstawowy prostokąt, dając podstawę
    dla pól do gry, guzików czy pól do wpisywania tekstu.
    """

    def __init__(self, x, y, w, h, color=white):
        self.__x = x
        self.__y = y
        self.__w = w
        self.__h = h
        self.__rect = pg.Rect(x, y, w, h)
        self.__default_color = color
        self.__color = color

    def draw(self, screen, thickness=0, border=False):
        """
        Funkcja rysująca na ekranie zdefiniowany prostokąt, wraz z możliwością dodania obramowania oraz wyboru
        grubości prostokąta.
        """
        pg.draw.rect(screen, self.color, self.__rect, thickness)
        if border:
            pg.draw.rect(screen, black, (self.__x - 1, self.__y - 1,
                                         self.__w + 2, self.__h + 2), 3)

    @abstractmethod
    def event_handler(self, event):
        raise NotImplementedError()

    @abstractmethod
    def activation(self):
        raise NotImplementedError()

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    @property
    def w(self):
        return self.__w

    @property
    def h(self):
        return self.__h

    @property
    def rect(self):
        return self.__rect

    @property
    def default_color(self):
        return self.__default_color

    @property
    def color(self):
        return self.__color

    @color.setter
    def color(self, color):
        self.__color = color


class TextBox(Rectangle, ABC):
    """
    Klasa tworząca interaktywne pole do wpisywania tekstu.
    """

    def __init__(self, x, y, w, h, font, default_color=white):
        """
        Konstruktor nowego pola.
        :param x: położenie x pola
        :param y: położenie y pola
        :param w: szerokość pola
        :param h: wysokość pola
        :param font: font, którym sie pole będzie posługiwać
        :param default_color: podstawowy kolor obramowania pola tekstowego
        """
        super().__init__(x, y, w, h, default_color)
        self.__text = ""
        self.__font = font
        self.__txt_surface = font.render(self.__text, True, self.color)
        self.__active = False

    def event_handler(self, event):
        """
        Event handler dla pola tekstowego.
        :param event: przychodzące wydarzenie
        """
        # Event zaznaczenia danego pola
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.__active = not self.__active
            else:
                self.__active = False
            self.color = (0, 0, 0) if self.__active else self.default_color

        # Event wpisywania tekstu do pola
        if event.type == pg.KEYDOWN:
            if self.__active:
                if event.key == pg.K_BACKSPACE:
                    self.__text = self.__text[:-1]
                elif event.key in [pg.K_0, pg.K_1, pg.K_2, pg.K_3, pg.K_4,
                                   pg.K_5, pg.K_6, pg.K_7, pg.K_8, pg.K_9]:
                    self.__text += event.unicode
                    if len(self.__text) > self.w // 10:
                        self.__text = self.__text[:-1]
                self.__txt_surface = self.__font.render(self.__text, True, self.color)

    def draw(self, screen, thickness=2, border=False):
        """
        Metoda wyświetlająca pole tekstowe na ekranie.
        :param screen: ekran
        :param thickness: grubość krawędzi pola
        :param border: czy ma rysować dodatkowe krawędzie
        """
        screen.blit(self.__txt_surface, (self.rect.x + 5, self.rect.y + 5))
        super().draw(screen, thickness, False)

    def get_value(self):
        """
        Parser z wpisywanego stringa w pole tekstowe na int.
        :return: wartość po parsowaniu
        """
        try:
            value = int(self.__text)
        except ValueError:
            value = -1
        return value

    def clear(self):
        """
        Metoda czyści pole tekstowe.
        """
        self.__text = ""
        self.__txt_surface = self.__font.render(self.__text, True, self.color)

    def isEmpty(self):
        """
        Metoda zwraca czy pole jest puste.
        :return: czy pole jest puste
        """
        if len(self.__text) == 0:
            return True
        else:
            return False


class Button(Rectangle, ABC):
    """
    Klasa definiująca duży przycisk służący do zaczęcia nowej gry.
    """

    def highlight(self, screen, thickness=0):
        """
        Metoda realizująca podświetlenie przycisku zaczęcia nowej gry, gdy się na nią najedzie. Daje to poczucie
        interaktywności przycisku.
        :param screen: ekran
        :param thickness: grubość ścianek domyślnie wypełnienie
        """
        mouse = pg.mouse.get_pos()

        # Odczyt pozycji myszki i ustalenie czy przycisk ma się podświetlić
        if self.rect.x <= mouse[0] <= self.rect.x + self.rect.w \
                and self.rect.y <= mouse[1] <= self.rect.y + self.rect.h:
            a, b, c = self.default_color
            self.color = (a + 10 if a < 245 else 255, b + 10 if b < 245 else 255, c + 10 if c < 245 else 255)
        else:
            self.color = self.default_color

        super().draw(screen, thickness, True)

    def event_handler(self, event):
        """
        Event handler dla wciśnięcia guzika.
        :param event: przychodzące wydarzenie
        :return: bool czy kliknięte w guzik czy nie
        """
        if event.type == pg.MOUSEBUTTONDOWN:
            return self.rect.collidepoint(event.pos)


class Field(Rectangle):
    """
    Klasa definiująca podstawowy element gry, czyli pole, ale bez miny.
    """

    def __init__(self, x, y, w, h, color=white):
        """
        Konstruktor nowego pola.
        :param x: położenie x pola
        :param y: położenie y pola
        :param w: szerokość pola
        :param h: wysokośc pola
        :param color: kolor
        """
        super().__init__(x, y, w, h, color)
        self.__clicked = False
        self.__border_mines = None
        self.__right_clicks = 0

    def event_handler(self, event):
        """
        Event handler dla pól bez min.
        :param event: przychodzące wydarzenie
        :return: bool: czy aktywowane pole graniczy z jakąś miną
        """
        if not self.__clicked:
            if event.type == pg.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    left, _, right = pg.mouse.get_pressed(3)
                    # Aktywacja pola
                    if left:
                        return self.activation()
                    # Ustawienie flagi na polu
                    if right:
                        self.right_click()
        return False

    def activation(self):
        """
        Metoda aktywująca pole pod warunkiem, że już nie zostało aktywowane.
        :return: true - pole nie graniczy z żadną miną; false - pole graniczy z jakąkolwiek miną
        """
        if not self.__clicked:
            self.__clicked = True
            r, g, b = self.color
            self.color = (r + 30 if r < 225 else 255, g + 30 if g < 225 else 255, b + 30 if b < 225 else 255)
            return self.__border_mines == 0

    def draw(self, screen, thickness=0, border=False):
        """
        Metoda rysująca pole oraz rysująca na nim znaki czy cyfry min dookoła.
        :param screen: ekran, na którym ma rysować
        :param thickness: grubość ścianek prostokąta, domyślnie zero co jest wypełnieniem
        :param border: czy rysować otoczkę dookoła
        """
        super().draw(screen, thickness, border)
        font = pg.font.SysFont('timesnewroman.ttf', int(self.h // 1.5) if self.h <= self.w else int(self.w // 1.5))

        # Wyświetla cyfrę min w sąsiedztwie miny, jeżeli aktywowane
        if self.__clicked and self.__border_mines != 0 and not isinstance(self, FieldWithMine):
            write_text(font, screen, str(self.__border_mines),
                       (self.rect.centerx - font.get_height() / 3, self.rect.centery - font.get_height() / 2))

        # Wyświetla X jako flagę "Tu jest mina", jeśli pole nieaktywowane
        elif self.__right_clicks == 1 and not self.__clicked:
            pg.draw.line(screen, (0, 0, 0), self.rect.bottomleft, self.rect.topright, 3)
            pg.draw.line(screen, (0, 0, 0), self.rect.bottomright, self.rect.topleft, 3)

        # Wyświetla ? jako flagę "Tu może być mina", jeśli pole nieaktywowane
        elif self.__right_clicks == 2 and not self.__clicked:
            write_text(font, screen, "?",
                       (self.rect.centerx - font.get_height() / 3, self.rect.centery - font.get_height() / 2))

    def set_border_mines(self, border_mines):
        self.__border_mines = border_mines

    def get_clicked(self):
        return self.__clicked

    def left_click(self):
        self.__clicked = True

    def right_click(self):
        """
        Metoda zmieniająca stan pola ze trzech możliwych: podstawowego,
        z flagą "Tu jest mina" i z flagą "Tu może być mina".
        """
        if not self.__clicked:
            self.__right_clicks = (self.__right_clicks + 1) % 3

    def set_right_clicks(self, value):
        self.__right_clicks = value % 3

    def get_right_clicks(self):
        return self.__right_clicks

    def get_color(self):
        return self.color

    def __repr__(self):
        return "Brak miny"


class FieldWithMine(Field):
    """
    Klasa dziedzicząca po zwykłym polu, ale zawierająca minę.
    """

    def event_handler(self, event):
        """
        :param event: przychodzące wydarzenie
        :return: zwraca zawsze fałsz celem zgodności zwracanego typu z metodą, po której dziedziczy
        """
        if not self.get_clicked():
            if event.type == pg.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    left, _, right = pg.mouse.get_pressed(3)
                    if left:
                        super().left_click()
                    if right:
                        super().right_click()
        return False

    def set_color(self, color):
        self.color = color


class Interface:
    """
    Klasa opisująca interfejs naszej gry, tworzy pola oraz je potem wyświetla.
    """

    def __init__(self, screen, font, game, background_color=white):
        """
        Konstruktor interfejsu tworzący wszystkie potrzebne guziki,
        :param screen: określony ekran
        :param font: określony font
        :param game: gra, z którą zaczynamy
        :param background_color: kolor tła
        """
        self.__screen = screen
        self.__font = font
        self.__game = game
        self.__background_color = background_color
        self.__boxes = [TextBox(5, 23, 45, 25, font), TextBox(75, 23, 45, 25, font),
                        TextBox(5, 73, 115, 25, font)]
        self.__message = None
        self.__button = Button(295, 5, 95, 95, (200, 245, 200))
        self.__properties = [Rectangle(5, 550, 35, 35, "red"), Rectangle(135, 550, 35, 35, self.__game.get_color()),
                             Rectangle(265, 550, 35, 35, self.__game.get_color())]
        self.__attributes = []

    def display_nonstop(self, update=False):
        """
        Metoda wyświetlająca najważniejsze elementy na ekranie, które potrzebują rysowania za każdym razem.
        Metoda występuje samodzielnie albo jako składowa innej metody, wobec tego przyjmuje argument czy ma po sobie
        odświeżyć ekran czy jeszcze nie.
        :param update: czy metoda ma odświeżyć ekran
        """
        for box in self.__boxes:
            box.draw(self.__screen)

        self.__button.highlight(self.__screen)
        pg.draw.polygon(self.__screen, (0, 220, 0), [(325, 27), (325, 77), (365, 50)])

        if update:
            pg.display.update()

    def display(self):
        """
        Metoda wyświetlająca cały ekran od nowa, odświeżająca go.
        """
        self.__screen.fill(self.__background_color)

        write_text(self.__font, self.__screen, "Rozmiar planszy:", (5, 5))
        write_text(self.__font, self.__screen, "Liczba min:", (5, 55))
        write_text(self.__font, self.__screen, "x", (59, 27))

        self.display_nonstop()

        pg.draw.line(self.__screen, (0, 0, 0), (0, 105), (400, 105), 2)

        # Wyświetlanie komunikatów do gracza o problemach, bądź rezultacie rozgrywki
        if self.__message == 0:
            write_text(self.__font, self.__screen, "Niepoprawny rozmiar planszy!", (5, 115))
        elif self.__message == 1:
            write_text(self.__font, self.__screen, "Niepoprawna liczba min.", (5, 115))
        if self.__message == 2:
            write_text(self.__font, self.__screen, "Przegrałeś!", (155, 125))
        elif self.__message == 3:
            write_text(self.__font, self.__screen, "Wygrałeś!", (157, 125))

        # Ikony liczby min i flag
        for prop in self.__properties:
            prop.draw(self.__screen, 0, True)

        # X w liczbie flag
        rect_mine = self.__properties[1].rect
        pg.draw.line(self.__screen, (0, 0, 0), rect_mine.bottomleft, rect_mine.topright, 3)
        pg.draw.line(self.__screen, (0, 0, 0), rect_mine.bottomright, rect_mine.topleft, 3)

        # Pytajnik w liczbie flag
        rect_mine = self.__properties[2].rect
        write_text(self.__font, self.__screen, "?",
                   (rect_mine.centerx - self.__font.get_height() / 3.6,
                    rect_mine.centery - self.__font.get_height() / 2.4))

        # Liczby flag
        flags = self.__game.get_flags_count()
        write_text(self.__font, self.__screen, ": " + str(self.__game.get_mines()), (45, 560))
        write_text(self.__font, self.__screen, ": " + str(flags[0]), (175, 560))
        write_text(self.__font, self.__screen, ": " + str(flags[1]), (305, 560))

        self.__game.display()
        pg.display.update()

    def event_handler(self, event):
        """
        Handler iterujący po każdym ze zdefiniowanych elementów interfejsu; dysponujący, kumulujący oraz rozporządzający
        przychodzące wydarzenia.
        :param event: przychodzące wydarzenie
        :return: wartości rozmiaru planszy oraz liczby min odczytane po wciśnięciu nowej rozgrywki
        """
        self.__attributes = []
        if self.__button.event_handler(event):
            for box in self.__boxes:
                if box.get_value() >= 0:
                    self.__attributes.append(box.get_value())
                box.clear()

        for box in self.__boxes:
            box.event_handler(event)

        return self.__attributes

    def set_message(self, message):
        self.__message = message

    def get_message(self):
        return self.__message

    def set_game(self, game):
        """
        Setter ustawiający nową grę
        :param game: nowa gra
        """
        self.__game = game
        self.__message = self.__game.get_message()

    def areTextBoxesEmpty(self):
        """
        Metoda sprawdzająca czy pola do wpisywania danych są puste.
        """
        counter = 0
        for box in self.__boxes:
            if box.isEmpty():
                counter += 1
        if counter == len(self.__boxes):
            return True
        else:
            return False
