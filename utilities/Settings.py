from utilities.Button import *


class Settings:

    def __init__(self):
        self.screen_width, self.screen_height = 700, 700
        self.bg_color = (209, 207, 203)


# initialize the buttons
btn_width = 130
btn_height = 50

BUTTON_STYLE = {"font": pg.font.SysFont("constantia", 20),
                "hover_color": BROWN,
                "clicked_color": ORANGE,
                "font_color": OFF_WHITE}

btn_rect = pg.Rect(Settings().screen_width - btn_width - 10, btn_height, btn_width, btn_height)
pencil_btn = Button(btn_rect, BLUE, "Pencil Mode", **BUTTON_STYLE)
pen_btn = pencil_btn.duplicate(0, 150, "Pen Mode")
generate_btn = Button(btn_rect.inflate(10, 0).move(0, 450), GREEN, "New Problem", **BUTTON_STYLE)

button_manager = ButtonManager((pencil_btn, pen_btn, generate_btn))
mode_buttons = [pencil_btn, pen_btn]
