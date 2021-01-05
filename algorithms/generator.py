from algorithms.solver import *
from utilities import global_var
import random
from enum import Enum
import time


class Level(Enum):
    EASY = 1
    MEDIUM = 2


def fill_grid(grid, arr):
    for i in range(81):
        row = i // 9
        col = i % 9
        if grid[row][col] == 0:
            np.random.shuffle(arr)
            for value in arr:
                if is_valid(grid, col, row, value):
                    grid[row][col] = value
                    if check_grid(grid):
                        return True
                    elif fill_grid(grid, arr):
                        return True
            break
    grid[row][col] = 0


def generate(diff_lel):
    # record the start time
    start = time.time()

    # change the amount of clues according to the difficulty level given
    if diff_lel == Level.EASY:
        clue_goal = random.randint(31, 33)
    elif diff_lel == Level.MEDIUM:
        clue_goal = random.randint(28, 30)

    print("clue amount: ", clue_goal)

    # initiate a completed grid follows the sudoku rule
    grid = np.zeros((9, 9), dtype=int)
    arr = np.random.permutation(np.arange(1, 10))
    fill_grid(grid, arr)
    print(np.array(grid))

    # Start Removing Numbers one by one
    clue_count = 81
    pos_list = [(x, y) for x in range(9) for y in range(9)]
    while clue_count > clue_goal:
        # Select a random cell that is not already empty
        row, col = random.choice(pos_list)

        # Remember its cell value in case we need to put it back
        backup = grid[row][col]
        grid[row][col] = 0
        pos_list.remove((row, col))
        clue_count -= 1
        # Take a full copy of the grid
        copy_grid = np.copy(grid)

        # Count the number of solutions that this grid has (using a backtracking approach implemented in the
        # solveGrid() function)
        global_var.ans_counter = 0
        solve(copy_grid)
        # If the number of solution is different from 1 then we need to cancel the change by putting the value we
        # took away back in the grid
        if global_var.ans_counter != 1:
            grid[row][col] = backup
            pos_list.append((row, col))
            clue_count += 1

    run_time = time.time() - start
    print("time took to run this generate fuc: %s" % run_time)
    print("This sudoku puzzle contains %s numbers as the starting clues." % clue_count)
    print(np.array(grid))
    return grid


if __name__ == '__main__':
    choose_level = Level.MEDIUM
    new_prob = generate(choose_level)
