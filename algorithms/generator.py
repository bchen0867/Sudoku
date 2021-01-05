from algorithms.solver import *
from utilities import global_var
import random


def fill_grid(grid):
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
                    elif fill_grid(grid):
                        return True
            break
    grid[row][col] = 0


if __name__ == '__main__':
    clue_goal = 29
    arr = np.random.permutation(np.arange(1, 10))
    grid = np.zeros((9, 9), dtype=int)
    fill_grid(grid)
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

    print("This sudoku puzzle contains %s numbers as the starting clues." % clue_count)
    print(np.array(grid))
    # global_var.ans_counter = 0
    # print(get_ans(grid))
    # print("number of ans: ", global_var.ans_counter)
