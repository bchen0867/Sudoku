from utilities.colors import *


class Button:
    pg.font.init()

    def __init__(self, rect, color, caption="", **kwargs):
        self.rect = pg.Rect(rect)
        self.caption = caption
        self.clicked = False
        self.color = color
        self.btn_color = color
        self.kwargs = kwargs
        self.process_kwargs()

    def process_kwargs(self):
        settings = {"font": pg.font.SysFont("constantia", 16),
                    "hover_color": None,
                    "clicked_color": None,
                    "font_color": None}
        for kwarg in self.kwargs:
            if kwarg in settings:
                settings[kwarg] = self.kwargs[kwarg]
            else:
                raise AttributeError("Button has no keyword: {}".format(kwarg))
        self.__dict__.update(settings)

    def duplicate(self, x, y, new_caption="", new_color=None):
        """Returns a new button having the same parameters
        and is moved by the given offset."""
        rect = self.rect.copy().move(x, y)
        caption = self.caption
        color = self.color

        if new_caption:
            caption = new_caption
        if new_color:
            color = new_color

        return Button(rect, color, caption, **self.kwargs)

    def draw(self, win):
        pg.draw.rect(win, self.color, self.rect)

        if self.clicked:
            pg.draw.rect(win, self.clicked_color, self.rect.inflate(2, 4))

        if self.caption:
            text = self.font.render(self.caption, True, self.font_color)
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


class ButtonManager:
    def __init__(self, button_list):
        self.size = len(button_list)
        # self.buttons = [Button(button_list[i]) for i in range(self.size)]
        self.buttons = button_list

    def add_button(self, button):
        """ Sets the button to manage """
        self.buttons.append(button)

    def remove_button(self, button):
        """ Remove a button from the managed buttons """
        self.buttons.remove(button)

    def clear_buttons(self):
        """ Removes all buttons """
        self.buttons.clear()

    def handle_hover_for_all(self, event):
        for btn in self.buttons:
            btn.handle_hover(event)

    def draw_buttons(self, win):
        for btn in self.buttons:
            btn.draw(win)


def update_screen():
    win.fill((255, 255, 255))
    button_manager.draw_buttons(win)


if __name__ == '__main__':

    pg.init()
    win_size = (700, 600)
    btn_width = 125
    btn_height = 50
    win = pg.display.set_mode(win_size)
    win.fill((255, 255, 255))

    run = True

    BUTTON_STYLE = {"font": pg.font.SysFont("constantia", 20),
                    "hover_color": BROWN,
                    "clicked_color": ORANGE,
                    "font_color": OFF_WHITE}

    btn_rect = pg.Rect(win_size[0] - btn_width - 10, btn_height, btn_width, btn_height)
    pencil_btn = Button(btn_rect, BLUE, "Pencil Mode", **BUTTON_STYLE)
    pencil_btn.clicked = True
    pen_btn = pencil_btn.duplicate(0, 150, "Pen Mode")

    button_manager = ButtonManager((pencil_btn, pen_btn))

    while run:
        update_screen()
        pg.display.update()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False

            if event.type == pg.MOUSEBUTTONDOWN:
                if pencil_btn.is_hover():
                    pencil_btn.clicked = True
                    pen_btn.clicked = False
                elif pen_btn.is_hover():
                    pencil_btn.clicked = False
                    pen_btn.clicked = True

            button_manager.handle_hover_for_all(event)
