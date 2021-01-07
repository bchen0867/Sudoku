"""Sudoku Game GUI made with PyGame"""

import sys
import pygame
import time
from utilities.settings import Settings
from SudokuGrid import SudokuGrid, redraw_window


class SudokuGame:
    """Overall class to manage game assets and behavior."""

    def __init__(self, problem):
        """Initialize the game, and create resources."""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
                (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Sudoku Game")

        # TODO: init sudoku grid
        self.sudoku_grid = SudokuGrid(self, problem, self.settings.screen_width, self.settings.screen_height)
        self.key = None
        self.run = True
        self.start = time.time()
        self.play_time = 0
        self.strikes = 0

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            # record play time
            self.play_time = round(time.time() - self.start)

            self._check_events()
            self._update_screen()

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    sys.exit()
                if pygame.K_1 <= event.key <= pygame.K_9:
                    self.key = int(pygame.key.name(event.key))
                if pygame.K_KP1 <= event.key <= pygame.K_KP9:
                    self.key = int(pygame.key.name(event.key)[1])
                if event.key == pygame.K_DELETE:
                    self.sudoku_grid.clear_selected()
                    self.key = None
                if event.key == pygame.K_RETURN:
                    i, j = self.sudoku_grid.selected
                    if self.sudoku_grid.cells[i][j].temp != 0:
                        if self.sudoku_grid.place(self.sudoku_grid.cells[i][j].temp):
                            print("Success")
                        else:
                            print("Wrong")
                            self.strikes += 1
                        self.key = None
                        if self.sudoku_grid.is_finished():
                            print("Game over")
                            self.run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                clicked = self.sudoku_grid.click(pos)
                if clicked:
                    self.sudoku_grid.select(clicked[0], clicked[1])
                    self.key = None

    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)

        if self.sudoku_grid.selected and self.key is not None:
            self.sudoku_grid.sketch(self.key)

        # Draw a row of black pieces.
        for index, piece in enumerate(self.chess_set.pieces[:6]):
            piece.x = index * 100
            piece.blitme()

        # Draw a row of white pieces.
        for index, piece in enumerate(self.chess_set.pieces[6:]):
            piece.x = index * 100
            piece.y = 100
            piece.blitme()

        redraw_window(self.screen, self.sudoku_grid, self.play_time, self.strikes)
        pygame.display.update()


if __name__ == '__main__':
    board = [
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

    # sudoku_game = SudokuGame(board)
    # sudoku_game.run_game()