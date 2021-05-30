import pygame as pg

black = (0, 0, 0)
white = (255, 255, 255)


def set_window(size=(400, 400), title=" ", color=(255, 255, 255)):
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


class TextBox:
    def __init__(self, x, y, w, h, font, default_color=white):
        self.width = w
        self.rect = pg.Rect(x, y, w, h)
        self.default_color = default_color
        self.color = default_color
        self.text = ""
        self.font = font
        self.txt_surface = font.render(self.text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = (0, 0, 0) if self.active else self.default_color
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.txt_surface = self.font.render(self.text, True, self.color)

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        pg.draw.rect(screen, self.color, self.rect, 2)