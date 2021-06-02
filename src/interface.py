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


def write_text(font, screen, text=" ", position=(0, 0), color=(0, 0, 0)):
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


class FunctionalRectangle:
    def __init__(self, x, y, w, h, color=white):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.rect = pg.Rect(x, y, w, h)
        self.default_color = color
        self.color = color

    def draw(self, screen, thickness=2, border=False):
        pg.draw.rect(screen, self.color, self.rect, thickness)
        if border:
            for i in range(4):
                pg.draw.rect(screen, black, (self.x - i, self.y - i,
                                             self.w + 2, self.h + 2), 1)

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_w(self):
        return self.w

    def get_h(self):
        return self.h


class TextBox(FunctionalRectangle):
    def __init__(self, x, y, w, h, font, default_color=white):
        super().__init__(x, y, w, h, default_color)
        self.rect = pg.Rect(x, y, w, h)
        self.text = ""
        self.font = font
        self.txt_surface = font.render(self.text, True, self.color)
        self.active = False

    def event_handler(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = (0, 0, 0) if self.active else self.default_color
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif event.key in [pg.K_0, pg.K_1, pg.K_2, pg.K_3, pg.K_4,
                                   pg.K_5, pg.K_6, pg.K_7, pg.K_8, pg.K_9]:
                    self.text += event.unicode
                    if len(self.text) > self.w // 10:
                        self.text = self.text[:-1]
                self.txt_surface = self.font.render(self.text, True, self.color)

    def draw(self, screen, thickness=2, border=False):
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        super().draw(screen, thickness, False)

    def get_value(self):
        try:
            value = int(self.text)
        except ValueError:
            value = 0
        return value

    def clear(self):
        self.text = ""
        self.txt_surface = self.font.render(self.text, True, self.color)


class Button(FunctionalRectangle):
    def __init__(self, x, y, w, h, default_color=white):
        super().__init__(x, y, w, h, default_color)

    def highlight(self, screen, thickness=0):
        mouse = pg.mouse.get_pos()

        if self.rect.x <= mouse[0] <= self.rect.x + self.rect.w \
                and self.rect.y <= mouse[1] <= self.rect.y + self.rect.h:
            a, b, c = self.default_color
            self.color = (a + 10 if a < 245 else 255, b + 10 if b < 245 else 255, c + 10 if c < 245 else 255)
            super().draw(screen, thickness, True)
        else:
            self.color = self.default_color
            super().draw(screen, thickness, True)

    def event_handler(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            return self.rect.collidepoint(event.pos)


class Field(FunctionalRectangle):
    def __init__(self, x, y, w, h, color=white):
        super().__init__(x, y, w, h, color)
        self.clicked = False
        self.border_mines = None

    def event_handler(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return self.activation()
        return False

    def activation(self):
        if not self.clicked:
            self.clicked = True
            r, g, b = self.color
            self.color = (r + 30 if r <= 225 else 255, g + 30 if g <= 225 else 255, b + 30 if b <= 225 else 255)
            return self.border_mines == 0

    def draw(self, screen, thickness=2, border=False):
        super(Field, self).draw(screen, thickness, border)
        font = pg.font.SysFont('timesnewroman.ttf', int(self.h // 1.5) if self.h <= self.w else int(self.w // 1.5))
        if self.clicked and self.border_mines != 0:
            write_text(font, screen, str(self.border_mines),
                       (self.rect.centerx - font.get_height() / 3, self.rect.centery - font.get_height() / 2))

    def set_border_mines(self, border_mines):
        self.border_mines = border_mines

    def __repr__(self):
        return "Brak miny"


class FieldWithMine(Field):
    def __init__(self, x, y, w, h, color=white):
        super().__init__(x, y, w, h, color)
        self.activated = False

    def event_handler(self, event):
        if not self.activated:
            if event.type == pg.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    return True
        return False

    def set_color(self, color):
        self.color = color

    def get_color(self):
        return self.color

    def __repr__(self):
        return "Mina"


class Interface:
    def __init__(self, screen, font, background_color):
        self.screen = screen
        self.font = font
        self.background_color = background_color
        self.boxes = [TextBox(5, 23, 45, 25, font), TextBox(75, 23, 45, 25, font),
                      TextBox(5, 73, 115, 25, font)]
        self.button = Button(295, 5, 95, 95, (200, 245, 200))
        self.attributes = []

    def display(self, game):
        self.screen.fill(self.background_color)

        for box in self.boxes:
            box.draw(self.screen)

        write_text(self.font, self.screen, "Rozmiar planszy:", (5, 5))
        write_text(self.font, self.screen, "Liczba min:", (5, 55))
        write_text(self.font, self.screen, "x", (59, 27))

        pg.draw.rect(self.screen, (0, 0, 0), pg.Rect(5, 160, 385, 385))
        pg.draw.line(self.screen, (0, 0, 0), (0, 105), (400, 105), 2)

        self.button.highlight(self.screen)

        pg.draw.polygon(self.screen, (0, 220, 0), [(325, 27), (325, 77), (365, 50)])

        game.display()

    def event_handler(self, event):
        self.attributes = []
        if self.button.event_handler(event):
            for box in self.boxes:
                if box.get_value() != 0:
                    self.attributes.append(box.get_value())
                box.clear()

        for box in self.boxes:
            box.event_handler(event)

        return self.attributes
