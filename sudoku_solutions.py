from sudoku_functions import print_puzzle, check_valid
import numpy as np
from numba import njit

@njit(nogil = True, cache = True)
def make_initial_available_arrays(puzzle, length, length_sqrt):
    available_array = np.zeros((length, length, length+1))
    rows = np.zeros((length, length))
    cols = np.zeros((length, length))
    blocks = np.zeros((length, length))
    for n in range(length):
        for m in range(length):
            puzzle_number = puzzle[n, m]
            if puzzle_number == 0:
                continue
            else:
                available_array[n, m, 0] = -1
                index = puzzle_number - 1
                if rows[n,index] == 1:
                    return -1, available_array, rows, cols, blocks
                else:
                    rows[n,index] = 1
                if cols[m,index] == 1:
                    return -1, available_array, rows, cols, blocks
                else:
                    cols[m,index] = 1
                block_index = length_sqrt * (n // length_sqrt) + m // length_sqrt
                if blocks[block_index,index] == 1:
                    return -1, available_array, rows, cols, blocks
                else:
                    blocks[block_index, index] = 1
    for n in range(length):
        for m in range(length):
            if available_array[n,m,0] != -1:
                block_index = length_sqrt * (n // length_sqrt) + m // length_sqrt
                available_array[n,m,1:] = np.minimum(1, rows[n]+cols[m]+blocks[block_index])
                available_array[n, m, 0] = available_array[n,m,1:].sum()
    return 1, available_array, rows, cols, blocks

@njit(nogil = True, cache = True)
def update(available_array, rows, cols, blocks, length, length_sqrt):
    for n in range(length):
        for m in range(length):
            if available_array[n,m,0] != -1:
                block_index = length_sqrt * (n // length_sqrt) + m // length_sqrt
                available_array[n,m,1:] = np.minimum(1, rows[n]+cols[m]+blocks[block_index])
                available_array[n, m, 0] = available_array[n,m,1:].sum()
    return available_array

@njit(nogil = True, cache = True)
def solution_one(puzzle,
                 length = 9,
                 length_sqrt = 3,
                 available_array = -1*np.ones((9,9,10)),
                 rows = -1*np.ones((9,9)),
                 cols = -1*np.ones((9,9)),
                 blocks = -1*np.ones((9,9))):
    if length != puzzle.shape[0]:
        print('Wrong length')
        return -1, puzzle
    if np.all(available_array == -1):
        check, available_array, rows, cols, blocks = make_initial_available_arrays(puzzle, length, length_sqrt)
        if check == -1:
            return -1, puzzle
    max_value = np.max(available_array[:,:,0])
    if max_value == length:
        return -1, puzzle
    a_max = np.argmax(available_array[:,:,0])
    max_row = a_max // length
    max_col = a_max - max_row*length
    
    for value in range(len(available_array[max_row,max_col,1:])):
        if available_array[max_row,max_col,1:][value] > 0:
            continue
        else:
            new_puzzle = puzzle.copy()
            new_available_array = available_array.copy()
            new_rows = rows.copy()
            new_cols = cols.copy()
            new_blocks = blocks.copy()
            new_puzzle[max_row,max_col] = value+1
            new_available_array[max_row, max_col, 0] = -1
            new_rows[max_row, value] = 1
            new_cols[max_col, value] = 1
            block_index = length_sqrt * (max_row // length_sqrt) + max_col // length_sqrt
            new_blocks[block_index,value] = 1
            new_available_array = update(new_available_array,
                                         new_rows,
                                         new_cols,
                                         new_blocks,
                                         length,
                                         length_sqrt)
            if np.min(new_puzzle) > 0:
                return 1, new_puzzle
            else:
                check, solution = solution_one(puzzle= new_puzzle,
                                               length=length,
                                               length_sqrt=length_sqrt,
                                               available_array = new_available_array,
                                               rows = new_rows,
                                               cols = new_cols,
                                               blocks = new_blocks)
                if check == -1:
                    continue
                else:
                    break
    return 1, solution



if __name__ == '__main__':
    import time
    tt = time.time
    # test = np.array([
    #         [1, 0, 0, 4],
    #         [3, 0, 0, 0],
    #         [0, 0, 4, 0],
    #         [0, 3, 0, 2],
    # ])
    test = np.array([
            [0, 4, 0, 1, 0, 0, 0, 3, 5],
            [0, 0, 0, 6, 7, 8, 2, 1, 0],
            [0, 7, 0, 0, 5, 3, 6, 0, 0],
            [7, 5, 0, 0, 3, 0, 0, 0, 1],
            [0, 0, 0, 0, 6, 0, 0, 0, 0],
            [4, 0, 0, 0, 9, 0, 0, 2, 3],
            [0, 0, 1, 2, 4, 0, 0, 8, 0],
            [0, 8, 7, 9, 1, 6, 0, 0, 0],
            [9, 2, 0, 0, 0, 7, 0, 5, 0],
    ])
    test = np.array([
    [0,6,3,0,0,0,9,0,2],
    [0,0,9,6,0,0,0,1,0],
    [0,7,0,0,4,0,0,0,0],
    [0,0,6,4,5,2,0,0,0],
    [5,0,0,0,3,0,0,0,6],
    [0,0,0,9,7,6,1,0,0],
    [0,0,0,0,9,0,0,8,0],
    [0,4,0,0,0,3,7,0,0],
    [9,0,5,0,0,0,6,2,0],
    ])
    print_puzzle(test)
    toc = tt()
    print_puzzle(solution_one(test)[1])
    tic = tt()
    print(tic - toc)