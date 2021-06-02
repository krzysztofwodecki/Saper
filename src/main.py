if __name__ == '__main__':
    import pygame as pg
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

    running = True
    while running:
        attributes_list = []

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

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

            # print(pg.event.event_name(event.type))
            #
            # if event.type == pg.K_x:
            #     if pg.event.get() == pg.K_y:
            #         if pg.event.get() == pg.K_z:
            #             if pg.event.get() == pg.K_z:
            #                 if pg.event.get() == pg.K_y:
            #                     game.cheat()

        print(clock.get_fps())
        clock.tick(60)

    pg.quit()
