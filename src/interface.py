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
        self._x = x
        self._y = y
        self._w = w
        self._h = h
        self._rect = pg.Rect(x, y, w, h)
        self._default_color = color
        self._color = color

    def draw(self, screen, thickness=0, border=False):
        """
        Funkcja rysująca na ekranie zdefiniowany prostokąt, wraz z możliwością dodania obramowania oraz wyboru
        grubości prostokąta.
        """
        pg.draw.rect(screen, self._color, self._rect, thickness)
        if border:
            pg.draw.rect(screen, black, (self._x - 1, self._y - 1,
                                         self._w + 2, self._h + 2), 3)

    def get_x(self):
        return self._x

    def get_y(self):
        return self._y

    def get_w(self):
        return self._w

    def get_h(self):
        return self._h

    def get_rect(self):
        return self._rect


class TextBox(Rectangle):
    """
    Klasa tworząca interaktywne pole do wpisywania tekstu.
    """

    def __init__(self, x, y, w, h, font, default_color=white):
        super().__init__(x, y, w, h, default_color)
        self._text = ""
        self._font = font
        self._txt_surface = font.render(self._text, True, self._color)
        self._active = False

    def event_handler(self, event):
        # Event zaznaczenia danego pola
        if event.type == pg.MOUSEBUTTONDOWN:
            if self._rect.collidepoint(event.pos):
                self._active = not self._active
            else:
                self._active = False
            self._color = (0, 0, 0) if self._active else self._default_color

        # Event wpisywania tekstu do pola
        if event.type == pg.KEYDOWN:
            if self._active:
                if event.key == pg.K_BACKSPACE:
                    self._text = self._text[:-1]
                elif event.key in [pg.K_0, pg.K_1, pg.K_2, pg.K_3, pg.K_4,
                                   pg.K_5, pg.K_6, pg.K_7, pg.K_8, pg.K_9]:
                    self._text += event.unicode
                    if len(self._text) > self._w // 10:
                        self._text = self._text[:-1]
                self._txt_surface = self._font.render(self._text, True, self._color)

    def draw(self, screen, thickness=2, border=False):
        screen.blit(self._txt_surface, (self._rect.x + 5, self._rect.y + 5))
        super().draw(screen, thickness, False)

    def get_value(self):
        try:
            value = int(self._text)
        except ValueError:
            value = 0
        return value

    def clear(self):
        self._text = ""
        self._txt_surface = self._font.render(self._text, True, self._color)

    def isEmpty(self):
        if len(self._text) == 0:
            return True
        else:
            return False


class Button(Rectangle):
    """
    Klasa definiująca duży przycisk służący do zaczęcia nowej gry.
    """
    def highlight(self, screen, thickness=0):
        mouse = pg.mouse.get_pos()

        # Odczyt pozycji myszki i ustalenie czy przycisk ma się podświetlić
        if self._rect.x <= mouse[0] <= self._rect.x + self._rect.w \
                and self._rect.y <= mouse[1] <= self._rect.y + self._rect.h:
            a, b, c = self._default_color
            self._color = (a + 10 if a < 245 else 255, b + 10 if b < 245 else 255, c + 10 if c < 245 else 255)
        else:
            self._color = self._default_color

        super().draw(screen, thickness, True)

    def event_handler(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            return self._rect.collidepoint(event.pos)


class Field(Rectangle):
    """
    Klasa definiująca podstawowy element gry, czyli pole, ale bez miny.
    """
    def __init__(self, x, y, w, h, color=white):
        super().__init__(x, y, w, h, color)
        self._clicked = False
        self._border_mines = None
        self._right_clicks = 0

    def event_handler(self, event):
        if not self._clicked:
            if event.type == pg.MOUSEBUTTONDOWN:
                if self._rect.collidepoint(event.pos):
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
        if not self._clicked:
            self._clicked = True
            r, g, b = self._color
            self._color = (r + 30 if r < 225 else 255, g + 30 if g < 225 else 255, b + 30 if b < 225 else 255)
            return self._border_mines == 0

    def draw(self, screen, thickness=2, border=False):
        super().draw(screen, thickness, border)
        font = pg.font.SysFont('timesnewroman.ttf', int(self._h // 1.5) if self._h <= self._w else int(self._w // 1.5))

        # Wyświetla cyfrę min w sąsiedztwie miny, jeżeli aktywowane
        if self._clicked and self._border_mines != 0 and not isinstance(self, FieldWithMine):
            write_text(font, screen, str(self._border_mines),
                       (self._rect.centerx - font.get_height() / 3, self._rect.centery - font.get_height() / 2))

        # Wyświetla X jako flagę "Tu jest mina", jeśli pole nieaktywowane
        elif self._right_clicks == 1 and not self._clicked:
            pg.draw.line(screen, (0, 0, 0), self._rect.bottomleft, self._rect.topright, 3)
            pg.draw.line(screen, (0, 0, 0), self._rect.bottomright, self._rect.topleft, 3)

        # Wyświetla ? jako flagę "Tu może być mina", jeśli pole nieaktywowane
        elif self._right_clicks == 2 and not self._clicked:
            write_text(font, screen, "?",
                       (self._rect.centerx - font.get_height() / 3, self._rect.centery - font.get_height() / 2))

    def set_border_mines(self, border_mines):
        self._border_mines = border_mines

    def get_clicked(self):
        return self._clicked

    def right_click(self):
        if not self._clicked:
            self._right_clicks = (self._right_clicks + 1) % 3

    def get_right_clicks(self):
        return self._right_clicks

    def get_color(self):
        return self._color

    def __repr__(self):
        return "Brak miny"


class FieldWithMine(Field):
    """
    Klasa dziedzicząca po zwykłym polu, ale zawierająca minę.
    """
    def event_handler(self, event):
        if not self._clicked:
            if event.type == pg.MOUSEBUTTONDOWN:
                if self._rect.collidepoint(event.pos):
                    left, _, right = pg.mouse.get_pressed(3)
                    if left:
                        self.left_click()
                    if right:
                        super().right_click()
        return False

    def left_click(self):
        self._clicked = True

    def set_color(self, color):
        self._color = color

    def __repr__(self):
        return "Mina"


class Interface:
    """
    Klasa opisująca interfejs naszej gry, tworzy pola oraz je potem wyświetla.
    """
    def __init__(self, screen, font, game, background_color=white):
        self._screen = screen
        self._font = font
        self._game = game
        self._background_color = background_color
        self._boxes = [TextBox(5, 23, 45, 25, font), TextBox(75, 23, 45, 25, font),
                       TextBox(5, 73, 115, 25, font)]
        self._message = None
        self._button = Button(295, 5, 95, 95, (200, 245, 200))
        self._properties = [Rectangle(5, 550, 35, 35, "red"), Rectangle(135, 550, 35, 35, self._game.get_color()),
                            Rectangle(265, 550, 35, 35, self._game.get_color())]
        self._attributes = []

    def display_nonstop(self, update=False):
        """
        Metoda wyświetlająca najważniejsze elementy na ekranie, które potrzebują rysowania za każdym razem.
        Metoda występuje samodzielnie albo jako składowa innej metody, wobec tego przyjmuje argument czy ma po sobie
        odświeżyć ekran czy jeszcze nie.
        :param update: czy metoda ma odświeżyć ekran
        """
        for box in self._boxes:
            box.draw(self._screen)

        self._button.highlight(self._screen)
        pg.draw.polygon(self._screen, (0, 220, 0), [(325, 27), (325, 77), (365, 50)])

        if update:
            pg.display.update()

    def display(self):
        """
        Metoda wyświetlająca cały ekran od nowa, odświeżająca go.
        """
        self._screen.fill(self._background_color)

        write_text(self._font, self._screen, "Rozmiar planszy:", (5, 5))
        write_text(self._font, self._screen, "Liczba min:", (5, 55))
        write_text(self._font, self._screen, "x", (59, 27))

        self.display_nonstop()

        pg.draw.line(self._screen, (0, 0, 0), (0, 105), (400, 105), 2)

        self._message = self._game.get_message()

        # Wyświetlanie komunikatów do gracza o problemach, bądź rezultacie rozgrywki
        if self._message == 0:
            write_text(self._font, self._screen, "Niepoprawny rozmiar planszy!", (5, 115))
            write_text(self._font, self._screen, "Uruchomiono grę domyślną.", (5, 135))
        elif self._message == 1:
            write_text(self._font, self._screen, "Niepoprawna liczba min.", (5, 115))
            write_text(self._font, self._screen, "Uruchomiono grę domyślną.", (5, 135))
        elif self._message == 2:
            write_text(self._font, self._screen, "Przegrałeś!", (155, 125))
        elif self._message == 3:
            write_text(self._font, self._screen, "Wygrałeś!", (157, 125))

        for prop in self._properties:
            prop.draw(self._screen, 0, True)

        rect_mine = self._properties[1].get_rect()
        pg.draw.line(self._screen, (0, 0, 0), rect_mine.bottomleft, rect_mine.topright, 3)
        pg.draw.line(self._screen, (0, 0, 0), rect_mine.bottomright, rect_mine.topleft, 3)

        rect_mine = self._properties[2].get_rect()
        write_text(self._font, self._screen, "?",
                   (rect_mine.centerx - self._font.get_height() / 3.6,
                    rect_mine.centery - self._font.get_height() / 2.4))

        flags = self._game.get_flags_count()
        write_text(self._font, self._screen, ": " + str(self._game.get_mines()), (45, 560))
        write_text(self._font, self._screen, ": " + str(flags[0]), (175, 560))
        write_text(self._font, self._screen, ": " + str(flags[1]), (305, 560))

        self._game.display()
        pg.display.update()

    def event_handler(self, event):
        """
        Handler iterujący po każdym ze zdefiniowanych elementów interfejsu; dysponujący, kumulujący oraz rozporządzający
        przychodzące wydarzenia.
        :param event: przychodzące wydarzenie
        :return: wartości rozmiaru planszy oraz liczby min odczytane po wciśnięciu nowej rozgrywki
        """
        self._attributes = []
        if self._button.event_handler(event):
            for box in self._boxes:
                if box.get_value() != 0:
                    self._attributes.append(box.get_value())
                box.clear()

        for box in self._boxes:
            box.event_handler(event)

        return self._attributes

    def set_message(self, message):
        self._message = message

    def set_game(self, game):
        # Setter ustawiający nową grę
        self._message = None
        self._game = game

    def areTextBoxesEmpty(self):
        counter = 0
        for box in self._boxes:
            if box.isEmpty():
                counter += 1
        if counter == len(self._boxes):
            return True
        else:
            return False
