if __name__ == '__main__':
    import pygame as pg
    import interface
    import logic

    background_color = (200, 200, 200)
    screen = interface.set_window((395, 550), "Minesweeper", background_color)
    font = pg.font.SysFont('timesnewroman.ttf', 24)
    clock = pg.time.Clock()

    display = interface.Interface(screen, font, background_color)

    game = logic.InitializeNewGame(6, 6, 4, screen)

    running = True
    while running:
        attributes_list = []

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            attributes_list = display.event_handler(event)

        if len(attributes_list) == 3:
            print(attributes_list)

        display.display()

        game.display()

        pg.display.update()
        clock.tick(60)

    pg.quit()
