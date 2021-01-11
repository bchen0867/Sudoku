"""Sudoku Game GUI made with pg"""

import sys
import time
from utilities.Settings import Settings
from SudokuGrid import SudokuGrid, redraw_window
from algorithms.solver import get_ans
from algorithms.generator import generate, Level
import pygame as pg
import time
from datetime import timedelta
from SudokuCell import SudokuCell
from utilities.Button import Button
import numpy as np


class SudokuGame:
    """Overall class to manage game assets and behavior."""

    def __init__(self, prob):
        """Initialize the game, and create resources."""
        pg.init()
        self.settings = Settings()
        self.screen = pg.display.set_mode(
                (self.settings.screen_width, self.settings.screen_height))
        pg.display.set_caption("Sudoku Game")

        # TODO: init sudoku grid
        # self.level = Level.EASY
        # self.prob = generate(self.level)
        self.board = SudokuGrid(np.copy(prob), 540, 540)
        self.key = None
        self.run = True
        self.start = time.time()
        self.play_time = 0
        self.strikes = 0
        self.msg = "Press Enter key after your input to check if the value is correct. "

    def run_game(self):
        """Start the main loop for the game."""
        while self.run:
            # record play time
            self.play_time = round(time.time() - self.start)

            self._check_events()
            self._update_screen()

    def _check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.run = False

            # mouse events
            pos = pg.mouse.get_pos()
            if event.type == pg.MOUSEBUTTONDOWN:
                # click events on game board
                clicked = self.board.click(pos)
                if clicked:
                    self.board.select(clicked[0], clicked[1])
                    self.key = None

                # # click events for pen or pencil mode btn
                # if pencil_btn.is_hover(pos):
                #     pencil_btn.clicked = True
                #     pen_btn.clicked = False
                #     is_pen_mode = False
                # elif pen_btn.is_hover(pos):
                #     pencil_btn.clicked = False
                #     pen_btn.clicked = True
                #     is_pen_mode = True

                # # click events for generate btn
                # if generate_btn.is_hover(pos):
                #     print("generate btn is clicked")
                #     is_loading = True
                #     prob = generate(Level.EASY)
                #     board = SudokuGrid(prob, 540, 540)
                #     key = None
                #     run = True
                #     start = time.time()
                #     strikes = 0
                #     msg = "Press Enter key after your input to check if the value is correct. "

            # # TODO: this event should be included in Button Class
            # if event.type == pg.MOUSEMOTION:
            #     if pencil_btn.is_hover(pos):
            #         pencil_btn.color = hover_color
            #     else:
            #         pencil_btn.color = btn_color
            #
            #     if pen_btn.is_hover(pos):
            #         pen_btn.color = hover_color
            #     else:
            #         pen_btn.color = btn_color
            #
            #     if generate_btn.is_hover(pos):
            #         generate_btn.color = hover_color
            #     else:
            #         generate_btn.color = btn_color

            # keyboard events
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_q:
                    self.run = False

                if pg.K_1 <= event.key <= pg.K_9:
                    key = int(pg.key.name(event.key))
                    # update temp info only after event
                    if self.board.selected and key is not None:
                        self.board.update_selected_cell(key)

                if pg.K_KP1 <= event.key <= pg.K_KP9:
                    key = int(pg.key.name(event.key)[1])
                    # update temp info only after event
                    if self.board.selected and key is not None:
                        self.board.update_selected_cell(key)

                if self.board.selected:
                    i, j = self.board.selected
                    if event.key == pg.K_LEFT and j > 0:
                        j -= 1
                    elif event.key == pg.K_RIGHT and j < 8:
                        j += 1
                    elif event.key == pg.K_UP and i > 0:
                        i -= 1
                    elif event.key == pg.K_DOWN and i < 8:
                        i += 1
                    self.board.select(i, j)

                if event.key == pg.K_DELETE:
                    self.board.clear_selected()
                    self.key = None

                # press return key to compare to the answer
                if event.key == pg.K_RETURN:
                    i, j = self.board.selected
                    if self.board.cells[i][j].value == 0:
                        self.msg = "There is no value inside this cell to compare!"
                    else:
                        if self.board.is_ans(i, j):
                            self.msg = "Success!"
                        else:
                            self.msg = "Wrong!"
                            self.strikes += 1
                        self.key = None

                        if self.board.is_finished():
                            if np.array_equal(self.board.model, self.board.ans):
                                self.msg = "You've solved this sudoku puzzle! Good Job. Press P to exit."
                            else:
                                self.msg = "You've failed! Game over!"

                        if self.strikes > 5:
                            self.msg = "You got it wrong for more than 5 times! Game over!"

    def _update_screen(self):
        # self.screen.fill(self.settings.bg_color)
        redraw_window(self.screen, self.board, self.play_time, self.strikes, self.msg)
        pg.display.update()


if __name__ == '__main__':
    prob = [
        [7, 8, 0, 4, 0, 0, 1, 2, 0],
        [6, 0, 0, 0, 7, 5, 0, 0, 9],
        [0, 0, 0, 6, 0, 1, 0, 7, 8],
        [0, 0, 7, 0, 4, 0, 2, 6, 0],
        [0, 0, 1, 0, 5, 0, 9, 3, 0],
        [9, 0, 4, 0, 6, 0, 0, 0, 5],
        [0, 7, 0, 3, 0, 0, 0, 1, 2],
        [1, 2, 0, 0, 0, 7, 4, 0, 0],
        [0, 4, 9, 2, 0, 6, 0, 0, 7]
    ]

    game = SudokuGame(prob)
    game.run_game()