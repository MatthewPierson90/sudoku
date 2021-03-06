from sudoku_functions import timer, tt, SolveTimeOut
import numpy as np


"""
Solution/ Algorithm one maintains a set/list, called available, for each empty spot in the puzzle. 
The set/list is found by taking the union of the numbers in use in the same row, column, and block as the spot, 
call this union unavailable.  The available numbers that can go in the spot is the set 
difference between [1,...,length] and unavailable. So available = [1,...,length] - unavailable.  The algorithm chooses
the spot with the minimum available list, makes a copy of the board and fills in one of the available numbers in the 
copy, and recursively calls the algorithm on the copy.  If a contradiction is reached, a -1 is returned in the 
0th output place, and the puzzle copy is returned in the 1st output place.  If a solution is found, a 1 is returned in 
the 0th output place, and the solution is returned in the 1st output place.
"""

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
                # print(index)
                if rows[n,index] == 1:
                    return -1, available_array, rows, cols, blocks
                else:
                    rows[n,index] = 1
                if cols[m,index] == 1:
                    return -1, available_array, rows, cols, blocks
                else:
                    cols[m,index] = 1
                block_index = length_sqrt * (n // length_sqrt) + m // length_sqrt
                # print('ls',length_sqrt)
                # print('bi',block_index)
                # print('i',index)
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


def update(available_array, rows, cols, blocks, length, length_sqrt):
    for n in range(length):
        for m in range(length):
            if available_array[n,m,0] != -1:
                block_index = length_sqrt * (n // length_sqrt) + m // length_sqrt
                available_array[n,m,1:] = np.minimum(1, rows[n]+cols[m]+blocks[block_index])
                available_array[n, m, 0] = available_array[n,m,1:].sum()
    return available_array


def solution_one(puzzle,
                 length = 9,
                 length_sqrt = 3,
                 available_array = -1*np.ones((9,9,10)),
                 rows = -1*np.ones((9,9)),
                 cols = -1*np.ones((9,9)),
                 blocks = -1*np.ones((9,9)),
                 start = tt(),
                 time_out = np.inf):
    if tt() - start > time_out:
        raise SolveTimeOut
    if length != puzzle.shape[0]:
        length = int(puzzle.shape[0])
        length_sqrt = int(puzzle.shape[0]**.5)
        available_array = -1*np.ones((puzzle.shape[0], puzzle.shape[0], puzzle.shape[0]+1)).astype(int)
        rows = -1*np.ones((puzzle.shape[0], puzzle.shape[0])).astype(int)
        cols = -1*np.ones((puzzle.shape[0], puzzle.shape[0])).astype(int)
        blocks = -1*np.ones((puzzle.shape[0], puzzle.shape[0])).astype(int)
    if np.all(available_array == -1):
        check, available_array, rows, cols, blocks = make_initial_available_arrays(puzzle, length, length_sqrt)
        if check == -1:
            return -1, puzzle
    max_value = np.max(available_array[:,:,0])
    if max_value == length:
        return -1, puzzle
    max_row, max_col = np.unravel_index(np.argmax(available_array[:,:,0], axis=None), available_array[:,:,0].shape)
    for value in range(len(available_array[max_row,max_col,1:])):
        if tt() - start > time_out:
            raise SolveTimeOut
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
               valid, solution = solution_one(puzzle= new_puzzle,
                                               length=length,
                                               length_sqrt=length_sqrt,
                                               available_array = new_available_array,
                                               rows = new_rows,
                                               cols = new_cols,
                                               blocks = new_blocks,
                                               start = start,
                                               time_out = time_out)
               if valid == -1:
                   continue
               else:
                   break
    return valid, solution



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
    test1 = np.array([
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
    
    test3 = test = np.array([
    [2,0,0,4,0,3,0,0,6],
    [0,7,0,0,0,6,0,4,0],
    [0,4,0,0,0,7,0,0,1],
    [0,0,0,0,0,0,5,9,0],
    [0,0,0,2,0,9,0,0,0],
    [0,3,2,0,0,0,0,0,0],
    [4,0,0,6,0,0,0,3,0],
    [0,1,0,3,0,0,0,2,0],
    [6,0,0,9,0,4,0,0,7],
    ])
    test4 = np.array([
        [2,0,1,4,8,3,0,0,6],
        [0,7,5,0,0,6,3,4,0],
        [0,4,0,0,0,7,0,8,1],
        [7,6,0,0,3,1,5,9,0],
        [0,5,0,2,0,9,0,7,0],
        [0,3,2,0,4,0,1,6,0],
        [4,0,0,6,0,0,0,3,0],
        [0,1,0,3,7,0,6,2,0],
        [6,2,3,9,0,4,0,1,7],
        ])
    test5 = np.array([
        [2,0,0,4,8,3,0,0,6],
        [0,7,5,0,0,6,3,4,0],
        [0,4,0,0,0,7,0,8,1],
        [7,6,0,0,3,1,5,9,0],
        [0,5,0,2,0,9,0,7,0],
        [0,3,2,0,4,0,1,6,0],
        [4,0,0,6,0,0,0,3,0],
        [0,1,0,3,7,0,6,2,0],
        [6,2,3,9,0,4,0,1,7],
        ])
    test6 = np.array([
        [2,0,0,4,0,3,0,0,6],
        [0,7,5,0,0,6,3,4,0],
        [0,4,0,0,0,7,0,8,1],
        [7,6,0,0,3,1,5,9,0],
        [0,5,0,2,0,9,0,7,0],
        [0,3,2,0,4,0,1,6,0],
        [4,0,0,6,0,0,0,3,0],
        [0,1,0,3,7,0,6,2,0],
        [6,2,3,9,0,4,0,1,7],
        ])
    test7 = np.array([
        [2,0,1,4,0,3,0,0,6],
        [0,7,5,0,0,6,3,4,0],
        [0,4,0,0,0,7,0,8,1],
        [7,6,0,0,3,1,5,9,0],
        [0,5,0,2,0,9,0,7,0],
        [0,3,2,0,4,0,1,6,0],
        [4,0,0,6,0,0,0,3,0],
        [0,1,0,3,7,0,6,2,0],
        [6,2,3,9,0,4,0,1,7],
        ])
    test8 = np.array([
        [2,0,0,4,8,3,0,0,6],
        [0,7,5,0,0,6,0,4,0],
        [0,4,0,0,0,7,0,8,1],
        [0,6,0,0,3,1,5,9,0],
        [0,5,0,2,0,9,0,7,0],
        [0,3,2,0,4,0,1,6,0],
        [4,0,0,6,0,0,0,3,0],
        [0,1,0,3,7,0,6,2,0],
        [6,2,3,9,0,4,0,1,7],
        ])
    testend = np.array([
        [2,0,0,4,0,3,0,0,6],
        [0,7,5,0,0,6,0,4,0],
        [0,4,0,0,0,7,0,8,1],
        [0,6,0,0,0,1,5,9,0],
        [0,5,0,2,0,9,0,0,0],
        [0,3,2,0,4,0,1,6,0],
        [4,0,0,6,0,0,0,3,0],
        [0,1,0,3,0,0,6,2,0],
        [6,0,3,9,0,4,0,0,7],
        ])


    # print_puzzle(test3)
    # print_puzzle(test5)
    # print_puzzle(test4)
    # timer(print_puzzle)(solution_one(test1))
    # # timer(print_puzzle)(solution_one(test2))
    # timer(print_puzzle)(solution_one(test3))
    # timer(print_puzzle)(solution_one(test4))
    # timer(print_puzzle)(solution_one(test5))
    # timer(print_puzzle)(solution_one(test6))
    # timer(print_puzzle)(solution_one(test7))
    # timer(print_puzzle)(solution_one(test8))
    # timer(print_puzzle)(solution_one(testend))
    test9 = np.array([
            [0, 0, 0, 0, 0, 0, 0, 0, 3],
            [0, 0, 1, 0, 0, 5, 6, 0, 0],
            [0, 9, 0, 0, 4, 0, 0, 7, 0],
            [0, 0, 0, 0, 0, 9, 0, 5, 0],
            [7, 0, 0, 0, 0, 0, 0, 0, 8],
            [0, 5, 0, 4, 0, 2, 0, 0, 0],
            [0, 8, 0, 0, 2, 0, 0, 9, 0],
            [0, 0, 3, 5, 0, 0, 1, 0, 0],
            [6, 0, 0, 0, 0, 0, 0, 0, 0],
    ])
    test6 = np.array([
            [1, 2, 3, 4, 0, 0, 3, 0, 0],
            [3, 0, 0, 0, 1, 0, 0, 5, 0],
            [0, 0, 6, 0, 0, 0, 1, 0, 0],
            [7, 0, 0, 0, 9, 0, 0, 0, 0],
            [0, 4, 0, 6, 0, 3, 0, 0, 0],
            [0, 0, 3, 0, 0, 2, 0, 0, 0],
            [5, 0, 0, 0, 8, 0, 7, 0, 0],
            [0, 0, 7, 0, 0, 0, 0, 0, 5],
            [0, 0, 0, 0, 0, 0, 0, 9, 8],
    ])
    # print(timer(solution_one)(test1))
    # print(timer(solution_one)(test2))
    # print(timer(solution_one)(test3))
    # print(timer(solution_one)(test4))
    # print(timer(solution_one)(test5))
    print(timer(solution_one)(test6))
    # print(timer(solution_one)(test7))
    # print(timer(solution_one)(test8))
    # print(timer(solution_one)(test9))

    #
    # print('test4')
    # toc = tt()
    # solution_one(test4)
    # tic = tt()
    # time1 = tic - toc
    # print('solution 1',tic - toc)
    #
    # toc = tt()
    # brute_force(test4)
    # tic = tt()
    # time_brute = tic- toc
    # print('brute force', time_brute)
    # 

    # timer(print_puzzle)(solution_one(test3))


    # print('test3')
    # toc = tt()
    # print_puzzle(solution_one(test3))
    # tic = tt()
    # time1 = tic - toc
    # print('solution 1',tic - toc)
    #
    # toc = tt()
    # print_puzzle(brute_force(test3))
    # tic = tt()
    # time_brute = tic- toc
    # print('brute force', time_brute)

