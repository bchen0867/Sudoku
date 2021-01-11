from utilities.colors import *


class Button:
    pg.font.init()

    def __init__(self, rect, color, text="", fnt=pg.font.SysFont("constantia", 20), clicked=False, **kwargs):
        self.rect = pg.Rect(rect)
        self.text = text
        self.font = fnt
        self.clicked = clicked
        self._color = color
        self.btn_color = color
        self.process_kwargs(kwargs)

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, new_color):
        self._color = new_color

    def process_kwargs(self, kwargs):
        """Various optional customization you can change by passing kwargs."""
        settings = {"hover_color": None,
                    "clicked_color": None,
                    "font_color": None}
        for kwarg in kwargs:
            if kwarg in settings:
                settings[kwarg] = kwargs[kwarg]
            else:
                raise AttributeError("Button has no keyword: {}".format(kwarg))
        self.__dict__.update(settings)

    def draw(self, win):
        pg.draw.rect(win, self.color, self.rect)

        if self.clicked:
            pg.draw.rect(win, self.clicked_color, self.rect.inflate(2, 4))

        if self.text != "":
            text = self.font.render(self.text, True, self.font_color)
            text_rect = text.get_rect(center=self.rect.center)
            win.blit(text, text_rect)

    def is_hover(self):
        if self.rect.collidepoint(pg.mouse.get_pos()):
            return True
        return False

    def handle_hover(self, event):
        if event.type == pg.MOUSEMOTION and self.is_hover():
            self.color = self.hover_color
        else:
            self.color = self.btn_color


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
    btn_color = BLUE
    BUTTON_STYLE = {"hover_color": BROWN,
                    "clicked_color": ORANGE,
                    "font_color": OFF_WHITE}

    pencil_rect = win_size[0] - btn_width - 10, btn_height, btn_width, btn_height
    pencil_btn = Button(pencil_rect, btn_color, text="Pencil Mode", clicked=True, **BUTTON_STYLE)

    pen_rect = win_size[0] - btn_width - 10, btn_height * 3, btn_width, btn_height
    pen_btn = Button(pen_rect, btn_color, text="Pen Mode", **BUTTON_STYLE)

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

            pencil_btn.handle_hover(event)
            pen_btn.handle_hover(event)
