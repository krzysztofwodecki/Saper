if __name__ == '__main__':
    import pygame as pg
    import interface

    background_color = (200, 200, 200)
    window = interface.set_window((400, 600), "Minesweeper", background_color)
    font = pg.font.SysFont('timesnewroman.ttf', 24)
    clock = pg.time.Clock()

    box1 = interface.TextBox(5, 23, 45, 25, font)
    box2 = interface.TextBox(75, 23, 45, 25, font)
    box3 = interface.TextBox(5, 73, 115, 25, font)
    boxes = [box1, box2, box3]

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
        interface.write_text(font, window, "x", (59, 27))

        mouse = pg.mouse.get_pos()

        pg.draw.line(window, (0, 0, 0), (0, 105), (400, 105), 2)
        if 300 <= mouse[0] <= 395 and 5 <= mouse[1] <= 100:
            pg.draw.rect(window, (160, 160, 160), (300, 5, 95, 95))
        else:
            pg.draw.rect(window, (150, 150, 150), (300, 5, 95, 95))

        pg.draw.polygon(window, (0, 220, 0), [(330, 27), (330, 77), (370, 50)])

        pg.display.update()
        clock.tick(60)

    pg.quit()
