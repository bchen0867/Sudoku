"""classes of Sudoku Grid"""
from algorithms.solver import get_ans
from algorithms.generator import generate, Level
import time
from datetime import timedelta
from SudokuCell import SudokuCell
from utilities.Button import *
from utilities.colors import *
from utilities.handleEvents import *
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
        self.is_pen_mode = False

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
            self.cells[row][col].update_cell(val, self.is_pen_mode)
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


def loading_screen(win):
    win.fill(OFF_WHITE)
    fnt = pg.font.SysFont("arial", 28)
    msg_wait = "Please wait patiently for the new problem to be generated..."
    text = fnt.render(msg_wait, True, (0, 0, 0))
    win.blit(text, (20, 250))


def format_time(secs):
    return str(timedelta(seconds=secs))


