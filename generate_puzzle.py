import numpy as np
from copy import deepcopy
from sudoku_functions import print_puzzle, timer, SolveTimeOut, tt
from unique_solution import check_unique, check_valid, make_initial_value_arrays
from solution_two import solution_two

"""
This algorithm relies heavily on solution two and Unique solution.  It begins by randomly filling in 10 to 20 values,
solves the resulting puzzle with solution two, and then randomly removes values from the puzzle while a unique solution 
is still guaranteed.  It often results in easy/ mostly filled in puzzles, and could really use som work/ more thought. 
"""

def get_all_available(puzzle, length, length_sqrt):
    all_spots, info, valid = make_initial_value_arrays(puzzle,
                                                       length,
                                                       length_sqrt)
    all_available = []
    for value in range(1, length):
        for (row, col) in info[value]['available']:
            all_available.append((value, row, col))
    return all_available

def generate_puzzle(length):
    puzzle = np.zeros((length, length), dtype = np.int8)
    length_sqrt = int(length**.5)
    not_done = True
    count = 0
    if length == 9:
        num_to_add = np.random.randint(10,20)
    else:
        num_to_add = 1
    while not_done:
        count += 1
        all_available = get_all_available(puzzle, length, length_sqrt)
        # print(all_available)
        puzzle_copy = puzzle.copy()
        for n in range(num_to_add):
            to_add = np.random.randint(0, len(all_available))
            value, row, col = all_available[to_add]
            puzzle_copy = puzzle_copy.copy()
            puzzle_copy[row, col] = value
            all_available = get_all_available(puzzle_copy, length, length_sqrt)
        num_to_add = int(num_to_add/2)+1
        try:
            start = tt()
            valid, puzzle = solution_two(puzzle_copy,
                                         start = start,
                                         time_out = .5)
            if valid == 1:
                not_done = False
            else:
                puzzle = np.zeros((length, length), dtype = np.int8)
                if length == 9:
                    num_to_add = 20
                else:
                    num_to_add = 1
        except SolveTimeOut:
            puzzle = np.zeros((length, length), dtype = np.int8)
            if length == 9:
                num_to_add = 20
            else:
                num_to_add = 1
    used = []
    not_done = True
    while not_done:
        row = np.random.randint(length)
        col = np.random.randint(length)

        if (row,col) in used:
            continue
        else:
            puzzle_copy = puzzle.copy()
            puzzle_copy[row,col] = 0
            try:
                start = tt()
                unique = check_unique(puzzle_copy, time_out = .5, start = start)
                if unique == 0:
                    return puzzle
                else:
                    puzzle = puzzle_copy
            except:
                continue
            used.append((row,col))

if __name__ == '__main__':
    times = []
    sum = 0
    for n in range(20):
        start = tt()
        test = generate_puzzle(9)
        end = tt()
        times.append(end - start)
        sum += end - start
        print('\n','-'*20,'\n')
        print(n+1)
        print(test)
        print(end - start)
        print(sum / (n+1))












