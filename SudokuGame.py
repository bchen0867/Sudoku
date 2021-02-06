"""Sudoku Game GUI made with pg"""

from utilities.Button import *
from utilities.Settings import Settings
from utilities.handleEvents import *
from SudokuGrid import SudokuGrid, redraw_window, loading_screen
from algorithms.generator import generate, Level
import pygame as pg
import time
from utilities.Button import Button
import numpy as np


class SudokuGame:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create resources."""
        pg.init()
        self.settings = Settings()
        self.screen = pg.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pg.display.set_caption("Sudoku Game")
        self.level = Level.EASY
        self.prob = generate(self.level)
        self.board = SudokuGrid(np.copy(self.prob), 540, 540)
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
            # currently, click quit only exit the current game.
            # If multiple games are running （new game btn was clicked), it will go back to the previous game
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

                # click events for pen or pencil mode btn
                for btn in mode_buttons:
                    if btn.is_hover():
                        remove_click_for_buttons(mode_buttons)
                        btn.clicked = True
                        if pen_btn.clicked:
                            self.board.is_pen_mode = True
                        else:
                            self.board.is_pen_mode = False
                        break

                # click events for generate btn
                if generate_btn.is_hover():
                    print("generate btn is clicked")
                    # display loading screen for 5 secs
                    for i in range(5):
                        loading_screen(self.screen)
                        pg.display.flip()
                        time.sleep(1)

                    new_game()

            button_manager.handle_hover_for_all(event)

            # keyboard events
            if event.type == pg.KEYDOWN:
                num_input_events(event, self.board)
                arrow_keys_events(event, self.board)

                if event.key == pg.K_q:
                    self.run = False

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
        self.screen.fill(self.settings.bg_color)
        redraw_window(self.screen, self.board, self.play_time, self.strikes, self.msg)
        button_manager.draw_buttons(self.screen)
        pg.display.update()


def new_game():
    pencil_btn.clicked = True
    pen_btn.clicked = False
    game = SudokuGame()
    game.run_game()


if __name__ == '__main__':

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

    new_game()
