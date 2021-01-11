import pygame as pg


class Button:
    pg.font.init()

    def __init__(self, rect, color, text="", fnt=pg.font.SysFont("constantia", 20), clicked=False):
        self.rect = pg.Rect(rect)
        self.text = text
        self.font = fnt
        self.clicked = clicked
        self.color = color

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, new_color):
        self._color = new_color

    def draw(self, win):
        pg.draw.rect(win, self.color, self.rect, 0)

        if self.clicked:
            outline_clr = pg.Color("#BD6042")
            pg.draw.rect(win, outline_clr, self.rect.inflate(-2, +4), 3)
            pg.draw.rect(win, outline_clr, self.rect, 0)

        if self.text != "":
            text = self.font.render(self.text, True, pg.Color("#FCFCFC"))
            text_rect = text.get_rect(center=self.rect.center)
            win.blit(text, text_rect)

    def is_hover(self):
        if self.rect.collidepoint(pg.mouse.get_pos()):
            return True
        return False


def update_screen():
    win.fill((255, 255, 255))
    pencil_btn.draw(win)
    pen_btn.draw(win)


if __name__ == '__main__':

    pg.init()
    win_size = (700, 600)
    btn_width = 125
    btn_height = 50
    win = pg.display.set_mode(win_size)
    win.fill((255, 255, 255))

    run = True
    btn_color = pg.Color("#477EB8")
    hover_color = pg.Color("#B88147")

    pencil_rect = win_size[0]-btn_width-10, btn_height, btn_width, btn_height
    pencil_btn = Button(pencil_rect, btn_color, text="Pencil Mode", clicked=True)

    pen_rect = win_size[0]-btn_width-10, btn_height*3, btn_width, btn_height
    pen_btn = Button(pen_rect, btn_color, text="Pen Mode")

    while run:
        update_screen()
        pg.display.update()

        for event in pg.event.get():
            pos = pg.mouse.get_pos()

            if event.type == pg.QUIT:
                run = False

            if event.type == pg.MOUSEBUTTONDOWN:
                if pencil_btn.is_hover():
                    pencil_btn.clicked = True
                    pen_btn.clicked = False
                elif pen_btn.is_hover():
                    pencil_btn.clicked = False
                    pen_btn.clicked = True

            if event.type == pg.MOUSEMOTION:
                if pencil_btn.is_hover():
                    pencil_btn.color = hover_color
                else:
                    pencil_btn.color = btn_color

                if pen_btn.is_hover():
                    pen_btn.color = hover_color
                else:
                    pen_btn.color = btn_color
