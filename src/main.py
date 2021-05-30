if __name__ == '__main__':
    import pygame as pg
    import interface

    background_color = (182, 182, 182)
    window = interface.set_window((400, 600), "Minesweeper", background_color)
    font = pg.font.SysFont('timesnewroman.ttf', 24)
    clock = pg.time.Clock()

    box1 = interface.TextBox(5, 23, 40, 25, font)
    box2 = interface.TextBox(75, 23, 40, 25, font)
    box3 = interface.TextBox(5, 73, 100, 25, font)
    boxes = [box1, box2, box3]
    pg.display.flip()

    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            for box in boxes:
                box.handle_event(event)

        window.fill(background_color)

        for box in boxes:
            box.draw(window)

        interface.write_text(font, window, "Rozmiar planszy:", (5, 5))
        interface.write_text(font, window, "Liczba min:", (5, 55))
        interface.write_text(font, window, "x", (55.5, 27))

        pg.display.update()
        clock.tick(60)

    pg.quit()
