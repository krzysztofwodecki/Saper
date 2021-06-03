import pygame as pg


def cheats(key_counter, incoming_event):
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

    event_handler = lambda x: x.type == pg.MOUSEBUTTONDOWN or x.type == pg.KEYDOWN \
                              or x.type == pg.MOUSEMOTION or x.type == pg.MOUSEBUTTONUP

    background_color = (200, 200, 200)
    fields_color = (120, 60, 40)
    screen = interface.set_window((395, 590), "Minesweeper", background_color)
    font = pg.font.SysFont('timesnewroman.ttf', 24)
    clock = pg.time.Clock()

    game = logic.InitializeNewGame(6, 6, 4, screen, fields_color)
    display = interface.Interface(screen, font, game, background_color)

    display.display()

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
                if len(attributes_list) == 3:
                    game = logic.InitializeNewGame(attributes_list[0], attributes_list[1],
                                                   attributes_list[2], screen, fields_color)
                    display.set_game(game)
                game.event_handler(event)

                if event.type == pg.MOUSEBUTTONUP or not display.areTextBoxesEmpty():
                    display.display()
                else:
                    display.display_nonstop(True)

        clock.tick(60)

    pg.quit()
