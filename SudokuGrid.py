"""classes of Sudoku Grid"""
from algorithms.solver import get_ans
from algorithms.generator import generate, Level
import pygame as pg
import time
from datetime import timedelta
from SudokuCell import SudokuCell
from utilities.Button import *
from utilities.colors import *
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
            pg.draw.line(win, (0, 0, 0), (0, i * gap), (self.width + thick/2, i * gap), thick)
            pg.draw.line(win, (0, 0, 0), (i * gap, 0), (i * gap, self.height + thick/2), thick)

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
    win.fill(OFF_WHITE)
    # Draw time
    fnt = pg.font.SysFont("comicsansms", 40)
    text = fnt.render("Time: " + format_time(run_time), True, (0, 0, 0))
    win.blit(text, (280, 600))
    # Draw Strikes
    text = fnt.render("X " * strikes, True, (255, 0, 0))
    win.blit(text, (20, 600))
    # Print message on the ui
    fnt = pg.font.SysFont("arial", 28)
    text = fnt.render(msg, True, (0, 0, 0))
    win.blit(text, (10, 550))
    # Draw grid and board
    board.draw(win)
    # TODO: add a button manager to draw all the buttons added
    # Draw buttons
    button_manager.draw_buttons(win)


def loading_screen(win):
    win.fill(OFF_WHITE)
    fnt = pg.font.SysFont("arial", 28)
    msg_wait = "Please wait patiently for the new problem to be generated..."
    text = fnt.render(msg_wait, True, (0, 0, 0))
    win.blit(text, (20, 250))


def format_time(secs):
    return str(timedelta(seconds=secs))


if __name__ == '__main__':
    win_size = (700, 700)
    win = pg.display.set_mode(win_size)
    pg.display.set_caption("Sudoku")
    pg.font.init()

    # use pre-generated problem for testing other features
    prob = [
        [0, 0, 4, 1, 0, 0, 0, 5, 0],
        [0, 3, 2, 9, 0, 0, 4, 8, 1],
        [1, 0, 0, 2, 8, 0, 0, 3, 9],
        [0, 0, 9, 5, 3, 0, 1, 0, 0],
        [0, 0, 0, 4, 0, 2, 0, 0, 0],
        [7, 0, 5, 0, 9, 8, 0, 4, 0],
        [0, 4, 0, 0, 0, 0, 0, 2, 0],
        [5, 0, 0, 0, 0, 0, 3, 0, 0],
        [0, 9, 0, 0, 0, 0, 5, 0, 0]
    ]

    # initialize the game
    prob = generate(Level.EASY)
    board = SudokuGrid(prob, 540, 540)
    key = None
    run = True
    start = time.time()
    strikes = 0
    msg = "Press Enter key after your input to check if the value is correct. "
    is_pen_mode = False

    # initialize the buttons
    btn_width = 130
    btn_height = 50

    BUTTON_STYLE = {"font": pg.font.SysFont("constantia", 20),
                    "hover_color": BROWN,
                    "clicked_color": ORANGE,
                    "font_color": OFF_WHITE}

    btn_rect = pg.Rect(win_size[0] - btn_width - 10, btn_height, btn_width, btn_height)
    pencil_btn = Button(btn_rect, BLUE, "Pencil Mode", **BUTTON_STYLE)
    pencil_btn.clicked = True
    pen_btn = pencil_btn.duplicate(0, 150, "Pen Mode")
    generate_btn = Button(btn_rect.inflate(10, 0).move(0, 450), GREEN, "New Problem", **BUTTON_STYLE)
    button_manager = ButtonManager((pencil_btn, pen_btn, generate_btn))
    mode_buttons = [pencil_btn, pen_btn]

    # initialize is_loading var
    is_loading = False
    while run:
        # record play time
        play_time = round(time.time() - start)

        # check events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False

            # mouse events
            pos = pg.mouse.get_pos()
            if event.type == pg.MOUSEBUTTONDOWN:
                # click events on game board
                clicked = board.click(pos)
                if clicked:
                    board.select(clicked[0], clicked[1])
                    key = None

                # click events for pen or pencil mode btn
                for btn in mode_buttons:
                    if btn.is_hover():
                        remove_click_for_buttons(mode_buttons)
                        btn.clicked = True
                        break

                # click events for generate btn
                if generate_btn.is_hover():
                    print("generate btn is clicked")

                    # TODO: print out message to let users wait for the new problem to be generated
                    is_loading = True
                    prob = generate(Level.EASY)
                    board = SudokuGrid(prob, 540, 540)
                    key = None
                    run = True
                    start = time.time()
                    strikes = 0
                    msg = "Press Enter key after your input to check if the value is correct. "

            button_manager.handle_hover_for_all(event)

            # keyboard events
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_q:
                    run = False

                if pg.K_1 <= event.key <= pg.K_9:
                    key = int(pg.key.name(event.key))
                    # update temp info only after event
                    if board.selected and key is not None:
                        board.update_selected_cell(key)

                if pg.K_KP1 <= event.key <= pg.K_KP9:
                    key = int(pg.key.name(event.key)[1])
                    # update temp info only after event
                    if board.selected and key is not None:
                        board.update_selected_cell(key)

                if board.selected:
                    i, j = board.selected
                    if event.key == pg.K_LEFT and j > 0:
                        j -= 1
                    elif event.key == pg.K_RIGHT and j < 8:
                        j += 1
                    elif event.key == pg.K_UP and i > 0:
                        i -= 1
                    elif event.key == pg.K_DOWN and i < 8:
                        i += 1
                    board.select(i, j)

                if event.key == pg.K_DELETE:
                    board.clear_selected()
                    key = None

                # press return key to compare to the answer
                if event.key == pg.K_RETURN:
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

        while is_loading:
            # TODO: make loading time dynamic
            for i in range(5):
                loading_screen(win)
                pg.display.flip()
                time.sleep(1)
            is_loading = False

        redraw_window(win, board, play_time, strikes, msg)
        pg.display.update()

