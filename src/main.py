import pygame as pg


def cheats(key_counter, incoming_event):
    """
    Funkcja testująca przychodzące wydarzenie z klawiatury tak, aby odczytać kombinację "xyzzy".
    :param key_counter: Liczba wciśniętych do tej pory klawiszy
    :param incoming_event: Przychodzące wydarzenie
    :return: Liczbę wciśniętych klawiszy zwiększoną o jeden w wypadku wciśnięcia dobrego guzika w kombinacji, bądź 0
    jako wyzerowanie kombinacji "xyzzy".
    """
    if key_counter == 0 and pg.key.name(incoming_event.key) == "x":
        key_counter = 1
    elif key_counter == 1 and pg.key.name(incoming_event.key) == "y":
        key_counter = 2
    elif (key_counter == 2 or key_counter == 3) and pg.key.name(incoming_event.key) == "z":
        key_counter += 1
    elif key_counter == 4 and pg.key.name(incoming_event.key) == "y":
        key_counter = 5
    else:
        key_counter = 0
    return key_counter


if __name__ == '__main__':
    from src import interface
    from src import logic

    # Zdefiniowane podstawowe elementy
    background_color = (200, 200, 200)
    fields_color = (120, 60, 40)
    screen = interface.set_window((395, 590), "Minesweeper", background_color)
    font = pg.font.SysFont('timesnewroman.ttf', 24)
    clock = pg.time.Clock()

    # Inicjacja domyślnej gry oraz pierwsze wygenerowanie interfejsu
    game = logic.Game(6, 6, 4, screen, fields_color)
    display = interface.Interface(screen, font, game, background_color)
    display.display()

    # Wyrażenie lambda zwracający czy podany event jest warty obsłużenia
    event_handler = lambda x: x.type == pg.MOUSEBUTTONDOWN or x.type == pg.KEYDOWN \
                              or x.type == pg.MOUSEMOTION or x.type == pg.MOUSEBUTTONUP

    pressed_keys = 0
    running = True
    while running:
        attributes_list = []

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

            if event.type == pg.KEYDOWN:
                pressed_keys = cheats(pressed_keys, event)
                if pressed_keys == 5:
                    pressed_keys = 0
                    game.set_cheat()
                    display.display()

            if event_handler(event):
                attributes_list = display.event_handler(event)

                # Sprawdzanie czy przychodzą do nas dane zebrane ze wszystkich 3 pól.
                if len(attributes_list) == 3:
                    game = logic.Game(attributes_list[0], attributes_list[1],
                                      attributes_list[2], screen, fields_color)
                    display.set_game(game)

                game.event_handler(event)

                # Część decyzyjna czy potrzebne jest odświeżanie całego ekranu czy tylko krytycznych elementów.
                # Znaczący wpływ na płynność rozgrywki oraz liczbę FPS'ów, szczególnie dla dużych plansz np. 15x15.
                if event.type == pg.MOUSEBUTTONUP or not display.areTextBoxesEmpty():
                    display.display()
                else:
                    display.display_nonstop(True)

        clock.tick(60)

    pg.quit()
