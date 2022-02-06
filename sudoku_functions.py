from datetime import datetime
import numpy as np
import time

tt = time.perf_counter

class SolveTimeOut(Exception):
    """To stop a solver that is taking too long"""
    pass


def timer(func):
    def wrap(*args,**kwargs):
        print('Began at',datetime.now().strftime("%H:%M:%S"),'\n')
        start = tt()
        result = func(*args,**kwargs)
        end = tt()
        total_time = end-start
        if total_time > 3600:
            total_time_in_mins = round(total_time / 60)
            total_time = round(total_time)
            hours = int(total_time_in_mins / 60)
            mins = total_time_in_mins % 60
            secs = total_time % 60
            time_string = f'{hours}h, {mins}m, {secs}s'
        elif total_time > 60:
            total_time = round(total_time)
            mins = int(total_time / 60)
            secs = total_time % 60
            time_string = f'{mins}m, {secs}s'
        elif total_time > .1:
            time_string = '{}s'.format(round(total_time,2))
        else:
            if round(total_time*1000) == 0:
                total_time = round(total_time*1000,2)
            else:
                total_time = round(total_time * 1000)
            time_string = f'{total_time}ms'
        print('Time elapsed:',time_string,'\n')
        return result
    return wrap


def make_numbers_letters(number):
    """
    Turns letters into numbers for numbers greater than 10

    Parameters
    ----------
    number : TYPE int
        a number greater than or equal to 10

    Returns
    -------
    a letter, specifically 
    'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'[number - 10]

    """
    letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    index = number - 10
    return letters[index]


def print_puzzle(puzzle, length = None):
    """
    Prints a sudoku puzzle up to 49 x 49

    Parameters
    ----------
    puzzle : TYPE an np.array
        The puzzle as an np.array
    length : Type int, optional Default is None
        The length of a side, default is None
    Returns
    -------
    None. Prints the puzzle

    """
    if not length:
        length = puzzle.shape[0]
    length_sqrt = np.sqrt(length).astype(np.uint8)
    row_divider = '-+'
    for n in range(length):
        if n % length_sqrt == 0:
            row_divider += '+'
        row_divider += '+---'
        if n == length - 1:
            row_divider += '++\n'

    topbot = '-+'
    for n in range(length):
        if n % length_sqrt == 0:
            topbot += '+'
        topbot += '+-'+str(n)+'-'
        if n == length - 1:
            topbot += '++\n'
    puzzle_string = ''
    puzzle_string += topbot
    for row in range(length):
        if row % length_sqrt == 0 and row != 0:
            puzzle_string += row_divider
        puzzle_string += row_divider
        for col in range(length):
            if col == 0:
                puzzle_string += str(row)+'|'
            puzzle_string += '|'
            if col % length_sqrt == 0:
                puzzle_string += '|'
            puzzle_number = int(puzzle[row,col])
            if puzzle_number == 0:
                puzzle_string += '   '
            elif puzzle_number < 10:
                puzzle_string += ' '+str(puzzle_number)+' '
            elif puzzle_number < 62:
                puzzle_string += ' '+str(make_numbers_letters(puzzle_number))+' '
            else:
                print('Puzzle too large, write a better print function!')
                return -1
            if col == length - 1:
                puzzle_string += '||\n'
        if row == length-1:
            puzzle_string += row_divider + topbot
    print(puzzle_string)


def check_valid(puzzle, length = None):
    """
    Checks the validity of a puzzle
    :param puzzle: np.array
    :param length: int, default None
    :return: (1,1) if valid and solution, (1,0) if valid and not solution, else (0,0)
    """
    if not length:
        length = puzzle.shape[0]
    length_sqrt = np.sqrt(length).astype(np.uint8)
    rows = np.zeros((length, length))
    cols = np.zeros((length, length))
    blocks = np.zeros((length, length))
    solution = 1
    for n in range(length):
        for m in range(length):
            puzzle_number = puzzle[n,m]
            if puzzle_number == 0:
                solution = 0
                continue
            else:
                index = puzzle_number - 1
                if rows[n,index] == 1:
                    return 0, 0
                else:
                    rows[n,index] = 1
                if cols[m,index] == 1:
                    return 0, 0
                else:
                    cols[m,index] = 1
                block_index = length_sqrt * (m // length_sqrt) + n // length_sqrt
                if blocks[block_index,index] == 1:
                    return 0, 0
                else:
                    blocks[block_index, index] = 1
    return 1, solution


def brute_force(puzzle,
                length = None,
                start = tt(),
                time_out = np.inf):
    """
    Parameters
    ----------
    puzzle: np.array
    length: int, default None

    Returns: int, np.array
    -------
    """
    if np.all(length == None):
        length = puzzle.shape[0]
    for n in range(length):
        for m in range(length):
            if puzzle[n,m] == 0:
                for k in range(length):
                    if tt()-start > time_out:
                        raise SolveTimeOut
                    puzzle_copy = puzzle.copy()
                    puzzle_copy[n,m] = k+1
                    valid, solution = check_valid(puzzle_copy)
                    if valid == 1:
                        if solution == 1:
                            return 1, puzzle_copy
                        else:
                            valid, solution = brute_force(puzzle_copy,length, start, time_out)
                            if valid == -1:
                                continue
                            elif check_valid(solution) == (1,1):
                                return 1, solution
                return -1, puzzle
    return -1, puzzle







if __name__ == '__main__':
    import time
    # Valid puzzle
    test = np.array([
            [1, 0, 0, 4],
            [3, 0, 0, 0],
            [0, 0, 4, 0],
            [0, 3, 0, 2],
    ])
    print(timer(brute_force)(test))
    print(check_valid(test))
    # Invalid puzzle

    test = np.array([
            [1, 0, 4, 4],
            [3, 0, 0, 0],
            [0, 0, 4, 0],
            [0, 3, 0, 2],
    ])
    print(timer(brute_force)(test))