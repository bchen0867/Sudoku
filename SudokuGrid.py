"""classes of Sudoku Grid"""
from algorithms.solver import get_ans
from algorithms.generator import generate, Level
import pygame
import time
from datetime import timedelta
from SudokuCell import SudokuCell
from utilities.Button import Button
import numpy as np


class SudokuGrid:

    def __init__(self, grid, width, height):
        self.grid = grid
        self.rows = len(self.grid)
        self.cols = len(self.grid[0])
        self.width = width
        self.height = height
        self.cells = [[SudokuCell(self.grid[i][j], i, j, width, height) for j in range(self.cols)] for i in range(self.rows)]
        self.model = None
        self.selected = None
        self.ans = get_ans(grid)

    def update_model(self):
        self.model = [[self.cells[i][j].value for j in range(self.cols)] for i in range(self.rows)]

    def is_ans(self, row, col):
        if self.cells[row][col].value == self.ans[row][col]:
            return True
        else:
            self.cells[row][col].value = 0
            self.cells[row][col].clear_temp()
            self.update_model()
            return False

    def update_selected_cell(self, val):
        row, col = self.selected
        # only allow change on the cell number if it's not provided by the question
        if not self.cells[row][col].is_provided:
            self.cells[row][col].update_cell(val, is_pen_mode)
            self.update_model()

    def draw(self, win):
        # Draw Grid Lines
        gap = self.width / 9
        for i in range(self.rows+1):
            if i % 3 == 0 or i % self.rows == 0:
                thick = 4
            else:
                thick = 1
            pygame.draw.line(win, (0, 0, 0), (0, i * gap), (self.width + thick/2, i * gap), thick)
            pygame.draw.line(win, (0, 0, 0), (i * gap, 0), (i * gap, self.height + thick/2), thick)

        # Draw cells
        for i in range(self.rows):
            for j in range(self.cols):
                self.cells[i][j].draw(win)

    def select(self, row, col):
        # Reset all other
        for i in range(self.rows):
            for j in range(self.cols):
                self.cells[i][j].selected = False

        self.cells[row][col].selected = True
        self.selected = (row, col)

    def clear_selected(self):
        row, col = self.selected
        if self.cells[row][col].value == 0:
            self.cells[row][col].clear_temp()
        else:
            self.cells[row][col].value = 0

    def click(self, pos):
        """
        :parameter: pos
        :return: (row, col)
        """
        if pos[0] < self.width and pos[1] < self.height:
            gap = self.width / 9
            x = pos[0] // gap
            y = pos[1] // gap
            return int(y), int(x)
        else:
            return None

    def is_finished(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.cells[i][j].value == 0:
                    return False
        return True


# other funcs
def redraw_window(win, board, run_time, strikes, msg):
    win.fill((255, 255, 255))
    # Draw time
    fnt = pygame.font.SysFont("comicsansms", 40)
    text = fnt.render("Time: " + format_time(run_time), True, (0, 0, 0))
    win.blit(text, (280, 600))
    # Draw Strikes
    text = fnt.render("X " * strikes, True, (255, 0, 0))
    win.blit(text, (20, 600))
    # Print message on the ui
    fnt = pygame.font.SysFont("arial", 28)
    text = fnt.render(msg, True, (0, 0, 0))
    win.blit(text, (10, 550))
    # Draw grid and board
    board.draw(win)
    # TODO: add a button manager to draw all the buttons added
    # Draw buttons
    pencil_btn.draw(win)
    pen_btn.draw(win)
    generate_btn.draw(win)


def format_time(secs):
    return str(timedelta(seconds=secs))


if __name__ == '__main__':
    win_size = (700, 700)
    win = pygame.display.set_mode(win_size)
    pygame.display.set_caption("Sudoku")
    pygame.font.init()
    # prob = [
    #     [0, 0, 4, 1, 0, 0, 0, 5, 0],
    #     [0, 3, 2, 9, 0, 0, 4, 8, 1],
    #     [1, 0, 0, 2, 8, 0, 0, 3, 9],
    #     [0, 0, 9, 5, 3, 0, 1, 0, 0],
    #     [0, 0, 0, 4, 0, 2, 0, 0, 0],
    #     [7, 0, 5, 0, 9, 8, 0, 4, 0],
    #     [0, 4, 0, 0, 0, 0, 0, 2, 0],
    #     [5, 0, 0, 0, 0, 0, 3, 0, 0],
    #     [0, 9, 0, 0, 0, 0, 5, 0, 0]
    # ]
    choose_level = Level.EASY
    prob = generate(choose_level)
    board = SudokuGrid(prob, 540, 540)
    key = None
    run = True
    start = time.time()
    strikes = 0

    btn_width = 125
    btn_height = 50
    btn_color = pygame.Color("#477EB8")
    hover_color = pygame.Color("#B88147")

    pencil_btn = Button(btn_color, win_size[0]-btn_width-10, btn_height, btn_width, btn_height, "Pencil Mode", True)
    pen_btn = Button(btn_color, win_size[0]-btn_width-10, btn_height*3, btn_width, btn_height, "Pen Mode")
    is_pen_mode = False

    generate_btn = \
        Button(btn_color, win_size[0] - btn_width - 10, btn_height * 5, btn_width, btn_height, "Generate New Problem")

    msg = "Press Enter key after your input to check if the value is correct. "
    while run:
        # record play time
        play_time = round(time.time() - start)

        # check events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            # mouse events
            pos = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # click events on game board
                clicked = board.click(pos)
                if clicked:
                    board.select(clicked[0], clicked[1])
                    key = None

                # click events for pen or pencil mode btn
                if pencil_btn.is_hover(pos):
                    pencil_btn.clicked = True
                    pen_btn.clicked = False
                    is_pen_mode = False
                elif pen_btn.is_hover(pos):
                    pencil_btn.clicked = False
                    pen_btn.clicked = True
                    is_pen_mode = True

                # click events for generate btn
                if generate_btn.is_hover(pos):
                    print("generate btn is clicked")

            # TODO: this event should be included in Button Class
            if event.type == pygame.MOUSEMOTION:
                if pencil_btn.is_hover(pos):
                    pencil_btn.color = hover_color
                else:
                    pencil_btn.color = btn_color

                if pen_btn.is_hover(pos):
                    pen_btn.color = hover_color
                else:
                    pen_btn.color = btn_color

                if generate_btn.is_hover(pos):
                    generate_btn.color = hover_color
                else:
                    generate_btn.color = btn_color

            # keyboard events
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    run = False

                if pygame.K_1 <= event.key <= pygame.K_9:
                    key = int(pygame.key.name(event.key))
                    # update temp info only after event
                    if board.selected and key is not None:
                        board.update_selected_cell(key)

                if pygame.K_KP1 <= event.key <= pygame.K_KP9:
                    key = int(pygame.key.name(event.key)[1])
                    # update temp info only after event
                    if board.selected and key is not None:
                        board.update_selected_cell(key)

                if board.selected:
                    i, j = board.selected
                    if event.key == pygame.K_LEFT and j > 0:
                        j -= 1
                    elif event.key == pygame.K_RIGHT and j < 8:
                        j += 1
                    elif event.key == pygame.K_UP and i > 0:
                        i -= 1
                    elif event.key == pygame.K_DOWN and i < 8:
                        i += 1
                    board.select(i, j)

                if event.key == pygame.K_DELETE:
                    board.clear_selected()
                    key = None

                # press return key to compare to the answer
                if event.key == pygame.K_RETURN:
                    i, j = board.selected
                    if board.cells[i][j].value == 0:
                        msg = "There is no value inside this cell to compare!"
                    else:
                        if board.is_ans(i, j):
                            msg = "Success!"
                        else:
                            msg = "Wrong!"
                            strikes += 1
                        key = None

                        if board.is_finished():
                            if np.array_equal(board.model, board.ans):
                                msg = "You've solved this sudoku puzzle! Good Job. Press P to exit."
                            else:
                                msg = "You've failed! Game over!"

                        if strikes > 5:
                            msg = "You got it wrong for more than 5 times! Game over!"

        redraw_window(win, board, play_time, strikes, msg)

        pygame.display.update()

