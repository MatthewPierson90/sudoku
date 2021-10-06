# -*- coding: utf-8 -*-
"""
Created on Mon Oct  4 08:47:15 2021

@author: Matthew
"""

import numpy as np


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
            puzzle_number = puzzle[row,col]
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


import time
tt = time.time

def brute_force(puzzle, length = None):
    if np.all(length == None):
        length = puzzle.shape[0]
    for n in range(length):
        for m in range(length):
            if puzzle[n,m] == 0:
                for k in range(length):
                    puzzle_copy = puzzle.copy()
                    puzzle_copy[n,m] = k+1
                    valid, solution = check_valid(puzzle_copy)
                    # if (tt()-start) - int(tt()-start)<.001:
                    # print('depth,n,m,value:',depth,n,m,k+1)
                    # print(puzzle_copy)
                    if valid == 1:
                        if solution == 1:
                            return puzzle_copy
                        else:
                            to_return = brute_force(puzzle_copy,length)
                            if np.all(to_return == -1):
                                continue
                            elif check_valid(to_return) == (1,1):
                                return to_return
                return -1
    return -1

test_tic = tt()
def test_time(start):
    while tt()-start<10:
        if (tt()-start) - int(tt()-start)<.01:
            print(tt()-start)

if __name__ == '__main__':
    # test = np.zeros((9,9)).astype(int)
    # test2 = np.random.randint(0,9,(9,9))
    # print(check_valid(test))
    # print(check_valid(test2))
    # test3 = np.random.randint(0,4,(4,4))
    # test4 = np.random.randint(0,16,(16,16))
    # print_puzzle(test)
    # print_puzzle(test2)
    # print_puzzle(test3)
    # print_puzzle(test4)
    test = np.array([
            [1, 0, 0, 4],
            [3, 0, 0, 0],
            [0, 0, 4, 0],
            [0, 3, 0, 2],
    ])
    print(brute_force(test))