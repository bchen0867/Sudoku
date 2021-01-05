import numpy as np
from utilities import global_var


# A helper function to check if the grid is all filled
def check_grid(grid):
    for row in range(9):
        for col in range(9):
            if grid[row][col] == 0:
                return False
    return True


def is_valid(grid, x, y, num):
    # check row
    for i in range(len(grid)):
        if grid[i][x] == num:
            return False

    # check column
    for j in range(len(grid[0])):
        if grid[y][j] == num:
            return False

    # check box
    x0 = (x // 3) * 3
    y0 = (y // 3) * 3
    for i in range(3):
        for j in range(3):
            if grid[i + y0][j + x0] == num:
                return False
    return True


def solve(grid):

    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0:
                for num in range(1, 10):
                    if is_valid(grid, j, i, num):
                        grid[i][j] = num
                        solve(grid)
                        grid[i][j] = 0
                return

    global_var.ans_counter += 1
    global_var.ans_grid = np.copy(grid)


def get_ans(grid):
    global_var.ans_counter = 0
    solve(grid)
    return global_var.ans_grid


if __name__ == '__main__':

    grid = [
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

    global_var.ans_counter = 0
    print(get_ans(grid))
    # print(np.array(grid))
    print("number of ans: ", global_var.ans_counter)

# [[9 8 4 1 6 3 7 5 2]
#  [6 3 2 9 7 5 4 8 1]
#  [1 5 7 2 8 4 6 3 9]
#  [4 2 9 5 3 7 1 6 8]
#  [8 6 3 4 1 2 9 7 5]
#  [7 1 5 6 9 8 2 4 3]
#  [3 4 1 7 5 9 8 2 6]
#  [5 7 6 8 2 1 3 9 4]
#  [2 9 8 3 4 6 5 1 7]]
