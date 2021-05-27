if __name__ == '__main__':
    import pygame as pg
    import interface

    window = interface.set_window((400, 600), "Minesweeper")
    FONT = pg.font.SysFont('timesnewroman.ttf', 24)

    interface.write_text(FONT, window, "Rozmiar planszy:", (5, 5))
    interface.write_text(FONT, window, "Liczba min:", (5, 55))

    box1 = interface.TextBox(5, 23, 40, 25, FONT)
    box2 = interface.TextBox(75, 23, 40, 25, FONT)
    boxes = [box1, box2]

    running = True
    while running:
        pg.display.flip()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            for box in boxes:
                box.handle_event(event)

        window.fill((30, 30, 30))
        for box in boxes:
            box.draw(window)

    pg.quit()
