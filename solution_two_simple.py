import numpy as np
import time
from copy import deepcopy
from solution_one import solution_one
from sudoku_functions import print_puzzle, timer

tt = time.perf_counter


def lst_char_len(lst):
    length = 0
    try:
        for item in lst:
            length += len(str(item))
        return (length)
    except:
        return (100000000000000000000000000)


def print_lst(lst, indt_lvl = 0):
    if lst_char_len(lst) < 100:
        print('\t'*indt_lvl, lst)
    else:
        print('\t'*(indt_lvl), '-'*50)
        for item in lst:
            if type(item) == dict:
                print_dct(item, indt_lvl+1)
            elif type(item) == list:
                print_lst(item, indt_lvl+1)
            else:
                print('\t'*indt_lvl, item)
        print('\t'*(indt_lvl), '-'*50)


def print_dct(dct, indt_lvl = 0):
    print('\t'*(indt_lvl), '-'*50)
    for key in dct.keys():
        if type(dct[key]) == dict:
            print('\t'*indt_lvl, key, ':{', '    ')
            print_dct(dct[key], indt_lvl+1)
        elif type(dct[key]) == list:
            print('\t'*indt_lvl, key, ':')
            print_lst(dct[key], (indt_lvl+1))
        else:
            print('\t'*indt_lvl, key, ':', dct[key])
    print('\t'*(indt_lvl), '-'*50)


def print_dct_lst(lst):
    print('-'*5000)
    for dct in lst:
        print_dct(dct)


def make_initial_value_arrays(puzzle,
                              length,
                              length_sqrt):
    rows = np.zeros((length, length), dtype = int)
    cols = np.zeros((length, length), dtype = int)
    blocks = np.zeros((length, length), dtype = int)
    filled_spots = np.zeros((length, length), dtype = int)
    info = {}
    all_spots = np.zeros((length+1, length, length), dtype = int)
    all_spots[0, :, :] = puzzle.copy()
    for n in range(length):
        for m in range(length):
            puzzle_number = puzzle[n, m]
            if puzzle_number == 0:
                continue
            else:
                filled_spots[n, m] = -1
                index = puzzle_number-1
                if rows[n, index] == 1:
                    return all_spots, info, -1
                else:
                    rows[n, index] = 1
                if cols[m, index] == 1:
                    return all_spots, info, -1
                else:
                    cols[m, index] = 1
                block_index = length_sqrt*(n//length_sqrt)+m//length_sqrt
                if blocks[block_index, index] == 1:
                    return all_spots, info, -1
                else:
                    blocks[block_index, index] = 1

    counts = []
    for n in range(length):
        n_rows = []
        n_cols = []
        n_blocks = []
        count = 0
        for m in range(length):
            if rows[m, n] == 0:
                n_rows.append(m)
                count += 1
            if cols[m, n] == 0:
                n_cols.append(m)
            if blocks[m, n] == 0:
                n_blocks.append(m)
        info[n+1] = {'count':count,
                     'rows':n_rows,
                     'columns':n_cols,
                     'blocks':n_blocks,
                     'available':[],
                     'available_by_row':{k:[] for k in range(length)},
                     'available_by_col':{k:[] for k in range(length)},
                     'available_by_block':{k:[] for k in range(length)},
                     'available_by_row_count':np.array([0 for k in range(length)]),
                     'available_by_col_count':np.array([0 for k in range(length)]),
                     'available_by_block_count':np.array([0 for k in range(length)])}
        counts.append(count)
    # return info
    for n in range(length):
        for (row, col) in [(row, col) for row in info[n+1]['rows'] for col in info[n+1]['columns']]:
            block_index = length_sqrt*(row//length_sqrt)+col//length_sqrt
            if block_index in info[n+1]['blocks'] and puzzle[row, col] == 0:
                info[n+1]['available'].append((row, col))
                info[n+1]['available_by_row'][row].append((row, col))
                info[n+1]['available_by_col'][col].append((row, col))
                info[n+1]['available_by_block'][block_index].append((row, col))
                info[n+1]['available_by_row_count'][row] += 1
                info[n+1]['available_by_col_count'][col] += 1
                info[n+1]['available_by_block_count'][block_index] += 1
                all_spots[n+1, row, col] = 1
    return all_spots, info, 1


def update_all_spots(all_spots, info, length, length_sqrt):
    changed_value = 1
    times_through = 0
    while changed_value == 1:
        # print(times_through)
        times_through += 1
        changed_value = 0
        for value in range(1, length+1):
            for n in range(length):
                if info[value]['available_by_row_count'][n] == 1:
                    (row, col) = info[value]['available_by_row'][n][0]
                    if all_spots[0, row, col] == 0:
                        changed_value = 1
                        all_spots[0, row, col] = value
                        block = length_sqrt*(row//length_sqrt)+col//length_sqrt
                        all_spots, info = update_info(all_spots, info, value, row, col, block, length, length_sqrt)
                    elif all_spots[0, row, col] == value:
                        print('here')
                        # continue
                    else:
                        return all_spots, info, -1
                if info[value]['available_by_col_count'][n] == 1:
                    (row, col) = info[value]['available_by_col'][n][0]
                    if all_spots[0, row, col] == 0:
                        changed_value = 1
                        all_spots[0, row, col] = value
                        block = length_sqrt*(row//length_sqrt)+col//length_sqrt
                        all_spots, info = update_info(all_spots, info, value, row, col, block, length, length_sqrt)
                    elif all_spots[0, row, col] == value:
                        print('here')
                        continue
                    else:
                        return all_spots, info, -1
                if info[value]['available_by_block_count'][n] == 1:
                    (row, col) = info[value]['available_by_block'][n][0]
                    if all_spots[0, row, col] == 0:
                        changed_value = 1
                        all_spots[0, row, col] = value
                        block = length_sqrt*(row//length_sqrt)+col//length_sqrt
                        all_spots, info = update_info(all_spots, info, value, row, col, block, length, length_sqrt)
                    elif all_spots[0, row, col] == value:
                        print('here')
                        continue
                    else:
                        return all_spots, info, -1
        sum_array = all_spots[1:].sum(axis = 0)
        for (row, col) in [(row, col) for row in range(length) for col in range(length)]:
            if sum_array[row, col] == 1:
                for value in range(1, length+1):
                    if all_spots[value, row, col] == 1:
                        changed_value = 1
                        all_spots[0, row, col] = value
                        block = length_sqrt*(row//length_sqrt)+col//length_sqrt
                        all_spots, info = update_info(all_spots, info, value, row, col, block, length, length_sqrt)
                        break
    return all_spots, info, 1

def update_info(all_spots, info, value, row, col, block, length, length_sqrt):
    block_indices = [(n_row, n_col) for n_row in range(length) for n_col in range(length)
                     if ((length_sqrt*(n_row//length_sqrt)+n_col//length_sqrt == block)
                         and (all_spots[value, n_row, n_col] == 1))]

    for n in range(length):
        if all_spots[value, n, col] == 1 and n != row:
            info[value]['available_by_row'][n].remove((n, col))
            info[value]['available_by_row_count'][n] -= 1
            block_index = length_sqrt*(n//length_sqrt)+col//length_sqrt
            info[value]['available_by_block'][block_index].remove((n, col))
            info[value]['available_by_block_count'][block_index] -= 1
            all_spots[value, n, col] = 0
        if all_spots[value, row, n] == 1 and n != col:
            info[value]['available_by_col'][n].remove((row, n))
            info[value]['available_by_col_count'][n] -= 1
            block_index = length_sqrt*(row//length_sqrt)+n//length_sqrt
            info[value]['available_by_block'][block_index].remove((row, n))
            info[value]['available_by_block_count'][block_index] -= 1
            all_spots[value, row, n] = 0
        if all_spots[n+1, row, col] == 1 and n+1 != value:
            info[n+1]['available_by_row'][row].remove((row, col))
            info[n+1]['available_by_row_count'][row] -= 1
            info[n+1]['available_by_col'][col].remove((row, col))
            info[n+1]['available_by_col_count'][col] -= 1
            info[n+1]['available_by_block'][block].remove((row, col))
            info[n+1]['available_by_block_count'][block] -= 1
            all_spots[n+1, row, col] = 0
    for (n_row, n_col) in block_indices:
        if all_spots[value, n_row, n_col] == 1 and (n_row, n_col) != (row, col):
            info[value]['available_by_row'][n_row].remove((n_row, n_col))
            info[value]['available_by_row_count'][n_row] -= 1
            info[value]['available_by_col'][n_col].remove((n_row, n_col))
            info[value]['available_by_col_count'][n_col] -= 1
            all_spots[value, n_row, n_col] = 0
    info[value]['available_by_row_count'][row] = 0
    info[value]['available_by_row'][row] = []
    info[value]['available_by_col_count'][col] = 0
    info[value]['available_by_col'][col] = []
    info[value]['available_by_block_count'][block] = 0
    info[value]['available_by_block'][block] = []
    all_spots[value, row, col] = 0
    return all_spots, info





def update_incorrect_guess(all_spots, info, length, length_sqrt, value, row, col):
    block = length_sqrt*(row//length_sqrt)+col//length_sqrt
    info[value]['available_by_row'][row].remove((row, col))
    info[value]['available_by_row_count'][row] -= 1
    info[value]['available_by_col'][col].remove((row, col))
    info[value]['available_by_col_count'][col] -= 1
    info[value]['available_by_block'][block].remove((row, col))
    info[value]['available_by_block_count'][block] -= 1
    all_spots[value, row, col] = 0
    return all_spots, info




def check_valid(all_spots, length):
    zero_count = 0
    no_error = 1
    for (row, col) in [(row, col) for row in range(length) for col in range(length)]:
        if all_spots[0, row, col] == 0:
            zero_count += 1
            no_error = 0
            for value in range(1, length+1):
                if all_spots[value, row, col] > 0:
                    no_error = 1
                    break
            if no_error == 0:
                return -1
    if zero_count == 0:
        return 1
    else:
        return 0


def choose_guess(all_spots, info, length, depth, loop_count):
    guess_value = 0
    guess_row = length
    guess_column = length
    spot_counts = all_spots[1:].sum(axis = 0)
    spot_min = spot_counts[spot_counts>0].min()
    min_count = spot_min
    row_counts = all_spots[1:].sum(axis = 2)
    row_min = row_counts[row_counts>0].min()
    if row_min < min_count:
        min_count = row_min
    col_counts = all_spots[1:].sum(axis = 1)
    col_min = col_counts[col_counts>0].min()
    if col_min < min_count:
        min_count = col_min
    if min_count == spot_min:
        rows, cols = np.where(spot_counts == spot_min)
        if len(rows) == 1:
            val = np.where(all_spots[:,rows[0],cols[0]] != 0)[0]
            return val[0], rows[0], cols[0]
        min_all_count = np.inf
        for (row,col) in zip(rows,cols):
            vals = np.where(all_spots[:,row,col] != 0)[0]
            for val in vals:
                # print(val)
                # print(row_counts[val,row])
                # print(col_counts[val,col])
                all_count = row_counts[val-1,row]+col_counts[val-1,col]
                # print(all_count)
                if all_count < min_all_count:
                    min_all_count = all_count
                    guess_value = val
                    guess_row = row
                    guess_column = col
        return guess_value, guess_row, guess_column
    elif min_count == row_min:
        vals, rows = np.where(row_counts == row_min)
        vals = vals + 1
        # print(vals)
        # print(rows)
        if len(vals) == 1:
            cols = np.where(all_spots[vals[0], rows[0], :] != 0)[0]
            # print(cols)
            return vals[0], rows[0], cols[0]
        min_all_count = np.inf
        for (val, row) in zip(vals, rows):
            cols = np.where(all_spots[val, row, :] != 0)[0]
            for col in cols:
                all_count = spot_counts[row, col]+col_counts[val-1, col]
                if all_count < min_all_count:
                    min_all_count = all_count
                    guess_value = val
                    guess_row = row
                    guess_column = col
        return guess_value, guess_row, guess_column
    elif min_count == col_min:
        vals, cols = np.where(col_counts == col_min)
        vals = vals + 1
        if len(vals) == 1:
            rows = np.where(all_spots[vals[0], :, cols[0]] != 0)[0]
            return vals[0], rows[0], cols[0]
        min_all_count = np.inf
        for (val, col) in zip(vals, cols):
            rows = np.where(all_spots[val, :, col] != 0)[0]
            for row in rows:
                all_count = spot_counts[row, col]+row_counts[val-1, row]
                if all_count < min_all_count:
                    min_all_count = all_count
                    guess_value = val
                    guess_row = row
                    guess_column = col
        return guess_value, guess_row, guess_column



def solution_two(puzzle,
                 length = None,
                 length_sqrt = None,
                 all_spots = None,
                 info = None,
                 depth = 0,
                 depth_dct = {}):
    # print(depth)
    if length is None:
        length = puzzle.shape[0]
        length_sqrt = int(np.sqrt(length))
    if np.all(all_spots == None):
        all_spots, info, init_valid = make_initial_value_arrays(puzzle, length, length_sqrt)
        if init_valid == -1:
            return -1, all_spots[0]
    all_spots, info, update_valid = update_all_spots(all_spots, info, length, length_sqrt)
    if update_valid == -1:
        return -1, all_spots[0]
    check_if_valid = check_valid(all_spots, length)
    if check_if_valid == -1:
        return -1, all_spots[0]
    elif check_if_valid == 1:
        return 1, all_spots[0]
    loop_count = 0
    while check_if_valid == 0:
        loop_count += 1
        value, row, col = choose_guess(all_spots, info, length, depth, loop_count)
        all_spots_copy = all_spots.copy()
        info_copy = deepcopy(info)
        block = length_sqrt*(row//length_sqrt)+col//length_sqrt
        all_spots_copy[0, row, col] = value
        # print('before update')
        # print(all_spots_copy[0])
        all_spots_copy, info_copy = update_info(all_spots_copy,
                                                info_copy,
                                                value,
                                                row,
                                                col,
                                                block,
                                                length,
                                                length_sqrt)
        # print('after update')
        # print(all_spots_copy[0])
        check, as0 = solution_two(all_spots_copy[0], length, length_sqrt, all_spots_copy, info_copy, depth+1)
        if check == -1:
            all_spots, info = update_incorrect_guess(all_spots, info, length, length_sqrt, value, row, col)
        else:
            return 1, as0
        check_if_valid = check_valid(all_spots, length)
    if check_if_valid == -1:
        return -1, all_spots[0]
    else:
        # print('here 3')
        return 1, all_spots[0]


if __name__ == '__main__':

    test = np.array([
            [1, 0, 0, 4],
            [3, 0, 0, 0],
            [0, 0, 4, 0],
            [0, 3, 0, 2],
    ])
    test1 = np.array([
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
    test2 = np.array([
            [0, 6, 3, 0, 0, 0, 9, 0, 2],
            [0, 0, 9, 6, 0, 0, 0, 1, 0],
            [0, 7, 0, 0, 4, 0, 0, 0, 0],
            [0, 0, 6, 4, 5, 2, 0, 0, 0],
            [5, 0, 0, 0, 3, 0, 0, 0, 6],
            [0, 0, 0, 9, 7, 6, 1, 0, 0],
            [0, 0, 0, 0, 9, 0, 0, 8, 0],
            [0, 4, 0, 0, 0, 3, 7, 0, 0],
            [9, 0, 5, 0, 0, 0, 6, 2, 0],
    ])

    test3 = np.array([
            [2, 0, 0, 4, 0, 3, 0, 0, 6],
            [0, 7, 0, 0, 0, 6, 0, 4, 0],
            [0, 4, 0, 0, 0, 7, 0, 0, 1],
            [0, 0, 0, 0, 0, 0, 5, 9, 0],
            [0, 0, 0, 2, 0, 9, 0, 0, 0],
            [0, 3, 2, 0, 0, 0, 0, 0, 0],
            [4, 0, 0, 6, 0, 0, 0, 3, 0],
            [0, 1, 0, 3, 0, 0, 0, 2, 0],
            [6, 0, 0, 9, 0, 4, 0, 0, 7],
    ])
    test4 = np.array([
            [4, 0, 0, 0, 0, 1, 0, 3, 0],
            [0, 0, 5, 0, 0, 8, 0, 7, 0],
            [0, 1, 0, 0, 6, 0, 0, 9, 0],
            [0, 0, 9, 0, 0, 4, 0, 0, 3],
            [0, 4, 0, 0, 0, 0, 0, 5, 0],
            [6, 0, 0, 3, 0, 0, 2, 0, 0],
            [0, 5, 0, 0, 8, 0, 0, 4, 0],
            [0, 2, 0, 7, 0, 0, 9, 0, 0],
            [0, 3, 0, 1, 0, 0, 0, 0, 8],
    ])

    test4 = np.array([
            [4, 0, 0, 0, 0, 1, 0, 3, 0],
            [0, 0, 5, 0, 0, 8, 0, 7, 0],
            [0, 1, 0, 0, 6, 0, 0, 9, 0],
            [0, 0, 9, 0, 0, 4, 0, 0, 3],
            [0, 4, 0, 0, 0, 0, 0, 5, 0],
            [6, 0, 0, 3, 0, 0, 2, 0, 0],
            [0, 5, 0, 0, 8, 0, 0, 4, 0],
            [0, 2, 0, 7, 0, 0, 9, 0, 0],
            [0, 3, 0, 1, 0, 0, 0, 0, 8],
    ])
    test5 = np.array([
            [0, 0, 0, 8, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 4, 3],
            [5, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 7, 0, 8, 0, 0],
            [0, 0, 0, 0, 0, 0, 1, 0, 0],
            [0, 2, 0, 0, 3, 0, 0, 0, 0],
            [6, 0, 0, 0, 0, 0, 0, 7, 5],
            [0, 0, 3, 4, 0, 0, 0, 0, 0],
            [0, 0, 0, 2, 0, 0, 6, 0, 0],
    ])

    test6 = np.array([
            [1, 2, 0, 4, 0, 0, 3, 0, 0],
            [3, 0, 0, 0, 1, 0, 0, 5, 0],
            [0, 0, 6, 0, 0, 0, 1, 0, 0],
            [7, 0, 0, 0, 9, 0, 0, 0, 0],
            [0, 4, 0, 6, 0, 3, 0, 0, 0],
            [0, 0, 3, 0, 0, 2, 0, 0, 0],
            [5, 0, 0, 0, 8, 0, 7, 0, 0],
            [0, 0, 7, 0, 0, 0, 0, 0, 5],
            [0, 0, 0, 0, 0, 0, 0, 9, 8],
    ])

    test7 = np.array([
            [1, 2, 0, 3, 0, 0, 0, 0, 0],
            [3, 4, 0, 0, 0, 0, 1, 0, 0],
            [0, 0, 5, 0, 0, 0, 0, 0, 0],
            [6, 0, 2, 4, 0, 0, 5, 0, 0],
            [0, 0, 0, 0, 6, 0, 0, 7, 0],
            [0, 0, 0, 0, 0, 8, 0, 0, 6],
            [0, 0, 4, 2, 0, 0, 3, 0, 0],
            [0, 0, 0, 0, 7, 0, 0, 0, 9],
            [0, 0, 0, 0, 0, 9, 0, 8, 0],
    ])

    test8 = np.array([
            [0, 2, 0, 0, 5, 0, 7, 0, 0],
            [4, 0, 0, 1, 0, 0, 0, 0, 6],
            [8, 0, 0, 0, 0, 3, 0, 0, 0],
            [2, 0, 0, 0, 0, 8, 0, 0, 3],
            [0, 4, 0, 0, 2, 0, 5, 0, 0],
            [0, 0, 0, 6, 0, 0, 0, 1, 0],
            [0, 0, 2, 0, 9, 0, 0, 0, 0],
            [0, 9, 0, 0, 0, 0, 0, 0, 5],
            [7, 0, 4, 0, 0, 0, 9, 0, 0],
    ])

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

    test10 = np.array([
            [0, 6, 3, 0, 0, 0, 9, 0, 2],
            [0, 0, 9, 6, 0, 0, 0, 1, 0],
            [0, 7, 0, 0, 4, 0, 0, 0, 0],
            [0, 0, 6, 4, 5, 2, 0, 0, 0],
            [5, 0, 0, 0, 3, 0, 0, 0, 6],
            [0, 0, 0, 9, 7, 6, 1, 0, 0],
            [0, 0, 0, 0, 9, 0, 0, 8, 0],
            [0, 4, 0, 0, 0, 3, 7, 0, 0],
            [9, 0, 5, 0, 0, 0, 6, 2, 0],
    ])
    # print(6)
    # all, info, valid = make_initial_value_arrays(puzzle = test6,
    #                           length = 9,
    #                           length_sqrt = 3)
    # print_dct(info)
    s1 = tt()
    s = tt()
    solution_two(test1)
    print(1,f'{tt()-s:.5f}')
    s = tt()
    solution_two(test2)
    print(2,f'{tt()-s:.5f}')
    s = tt()
    solution_two(test3)
    print(3,f'{tt()-s:.5f}')
    s = tt()
    solution_two(test4)
    print(4,f'{tt()-s:.5f}')
    s = tt()
    solution_two(test5)
    print(5,f'{tt()-s:.5f}')
    s = tt()
    solution_two(test6)
    print(6,f'{tt()-s:.5f}')
    s = tt()
    solution_two(test7)
    print(7,f'{tt()-s:.5f}')
    s = tt()
    solution_two(test8)
    print(8,f'{tt()-s:.5f}')
    s = tt()
    solution_two(test9)
    print(9,f'{tt()-s:.5f}')
    s = tt()
    solution_two(test10)
    print(10, f'{tt()-s:.5f}')
    print(f'total: {tt()-s1:.5f}')
    #
    # s1 = tt()
    # s = tt()
    # solution_one(test1)
    # print(1,f'{tt()-s:.5f}')
    # s = tt()
    # solution_one(test2)
    # print(2,f'{tt()-s:.5f}')
    # s = tt()
    # solution_one(test3)
    # print(3,f'{tt()-s:.5f}')
    # s = tt()
    # solution_one(test4)
    # print(4,f'{tt()-s:.5f}')
    # s = tt()
    # solution_one(test5)
    # print(5,f'{tt()-s:.5f}')
    # s = tt()
    # solution_one(test6)
    # print(6,f'{tt()-s:.5f}')
    # s = tt()
    # solution_one(test7)
    # print(7,f'{tt()-s:.5f}')
    # s = tt()
    # solution_one(test8)
    # print(8,f'{tt()-s:.5f}')
    # s = tt()
    # solution_one(test9)
    # print(9,f'{tt()-s:.5f}')
    # print(f'total: {tt()-s1:.5f}')




