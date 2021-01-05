import pygame


class Button:
    def __init__(self, color, x, y, width, height, text="", clicked=False):

        # (x, y) is the top left corner of the button
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.clicked = clicked
        self.color = color

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, new_color):
        self._color = new_color

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.clicked:
            outline_clr = pygame.Color("#BD6042")
            pygame.draw.rect(win, outline_clr, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 3)
            pygame.draw.rect(win, outline_clr, (self.x, self.y, self.width, self.height), 0)

        if self.text != "":
            font = pygame.font.SysFont("constantia", 20)
            text = font.render(self.text, True, pygame.Color("#fcfcfc"))
            text_rect = text.get_rect(center=(self.x+self.width/2, self.y+self.height/2))
            win.blit(text, text_rect)

    def is_hover(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if self.x < pos[0] < self.x + self.width:
            if self.y < pos[1] < self.y + self.height:
                return True
        return False


def update_screen():
    win.fill((255, 255, 255))
    pencil_btn.draw(win)
    pen_btn.draw(win)


if __name__ == '__main__':

    pygame.init()
    win_size = (700, 600)
    btn_width = 125
    btn_height = 50
    win = pygame.display.set_mode(win_size)
    win.fill((255, 255, 255))

    run = True
    btn_color = pygame.Color("#477EB8")
    hover_color = pygame.Color("#B88147")

    pencil_btn = Button(btn_color, win_size[0]-btn_width-10, btn_height, btn_width, btn_height, "Pencil Mode", True)
    pen_btn = Button(btn_color, win_size[0]-btn_width-10, btn_height*3, btn_width, btn_height, "Pen Mode")

    while run:
        update_screen()
        pygame.display.update()

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if pencil_btn.is_hover(pos):
                    pencil_btn.clicked = True
                    pen_btn.clicked = False
                elif pen_btn.is_hover(pos):
                    pencil_btn.clicked = False
                    pen_btn.clicked = True

            if event.type == pygame.MOUSEMOTION:
                if pencil_btn.is_hover(pos):
                    pencil_btn.color = hover_color
                else:
                    pencil_btn.color = btn_color

                if pen_btn.is_hover(pos):
                    pen_btn.color = hover_color
                else:
                    pen_btn.color = btn_color
