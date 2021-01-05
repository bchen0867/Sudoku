import pygame
import copy


def cell_center(curr_x, curr_y, num, grid_size):
    """
    :param curr_y:
    :param curr_x:
    :param num: integer from 1 to 9
    :param grid_size:
    :return: the center of the corresponding cell in sketch grid
    """
    col_i = (num - 1) % 3
    row_i = (num - 1) // 3
    gap = grid_size / 3
    center_x = col_i * gap + gap / 2 + curr_x
    center_y = row_i * gap + gap / 2 + curr_y
    return center_x, center_y


def draw_num(win, fnt, num, color, center_pos):
    text = fnt.render(str(num), True, color)
    text_rect = text.get_rect(center=center_pos)
    win.blit(text, text_rect)


class SudokuCell:
    rows = 9
    cols = 9

    def __init__(self, value, row, col, width, height):
        self._value = value
        self.temp = []
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = False
        self.is_provided = copy.copy(value) > 0

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        self._value = val

    def update_temp(self, val):
        if val in self.temp:
            self.temp.remove(val)
        else:
            self.temp.append(val)

    def clear_temp(self):
        self.temp = []

    def update_cell(self, val, mode):
        if mode:
            self.clear_temp()
            self.value = val
        else:
            self.update_temp(val)

    def draw(self, win):
        fnt = pygame.font.SysFont("comicsansms", 40)
        sml_fnt = pygame.font.SysFont("comicsansms", 30)
        # change the margin value if needed in the future
        left_margin = 0
        gap = self.width / 9
        x = self.col * gap + left_margin
        y = self.row * gap

        if self.value > 0:
            if self.is_provided:
                draw_num(win, fnt, self.value, (139, 0, 0), (x + gap / 2, y + gap / 2))
            else:
                draw_num(win, fnt, self.value, (0, 0, 0), (x + gap / 2, y + gap / 2))
        elif self.temp:
            # display temp values using gray font
            for num in self.temp:
                draw_num(win, sml_fnt, num, (128, 128, 128), cell_center(x, y, num, gap))

        if self.selected:
            # draw a red outline for the selected cell
            pygame.draw.rect(win, (255, 0, 0), (x, y, gap, gap), 3)
