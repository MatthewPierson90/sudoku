# -*- coding: utf-8 -*-
"""
Created on Tue Oct  5 11:58:03 2021

@author: Matthew
"""
import numpy as np
from sudoku_functions import print_puzzle


# noinspection PyShadowingNames,PyUnusedLocal
def make_initial_value_arrays(puzzle, length, length_sqrt):
    rows = np.zeros((length, length))
    cols = np.zeros((length, length))
    blocks = np.zeros((length, length))
    filled_spots = np.zeros((length,length))
    for n in range(length):
        for m in range(length):
            puzzle_number = puzzle[n, m]
            if puzzle_number == 0:
                continue
            else:
                filled_spots[n,m] = -1
                index = puzzle_number - 1
                if rows[n,index] == 1:
                    return -1,  rows, cols, blocks
                else:
                    rows[n,index] = 1
                if cols[m,index] == 1:
                    return -1,  rows, cols, blocks
                else:
                    cols[m,index] = 1
                block_index = length_sqrt * (n // length_sqrt) + m // length_sqrt
                if blocks[block_index,index] == 1:
                    return -1, rows, cols, blocks
                else:
                    blocks[block_index, index] = 1
    info = {}
    counts = []

    # noinspection PyShadowingNames
    for n in range(length):
        n_rows = []
        n_cols = []
        n_blocks = []
        count = 0
        for m in range(length):
            if rows[m,n] == 0:
                n_rows.append(m)
                count += 1
            if cols[m,n] == 0:
                n_cols.append(m)
            if blocks[m,n] == 0:
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
    all_spots = np.zeros((length+1,length,length))
    all_spots[0,:,:] = puzzle.copy()
    for n in range(length):
        for (row,col) in [(row,col) for row in info[n+1]['rows'] for col in info[n+1]['columns']]:
            block_index = length_sqrt * (row // length_sqrt) + col // length_sqrt
            if block_index in info[n+1]['blocks'] and puzzle[row,col] == 0:
                info[n+1]['available'].append((row,col))
                info[n+1]['available_by_row'][row].append((row,col))
                info[n+1]['available_by_col'][col].append((row,col))
                info[n+1]['available_by_block'][block_index].append((row,col))
                info[n+1]['available_by_row_count'][row] += 1
                info[n+1]['available_by_col_count'][col] += 1
                info[n+1]['available_by_block_count'][block_index] += 1
                all_spots[n+1, row, col] = 1
    return all_spots, info, rows, cols, blocks


# noinspection PyUnusedLocal,PyShadowingNames
def update_all_spots(all_spots, info, length, length_sqrt):
    changed_value = 1
    times_through = 0
    while changed_value == 1:
        print(times_through)
        times_through += 1
        changed_value = 0
        for value in range(1,length+1):
            for n in range(length):
                if info[value]['available_by_row_count'][n] == 1:
                    (row,col) = info[value]['available_by_row'][n][0]
                    if all_spots[0,row,col] != 0 and all_spots[0,row,col] != value:
                        return -1,-1
                    changed_value = 1
                    all_spots[:,row,col] = np.array([value]+[0 for k in range(length)])
                    all_spots[value,row,:] = 0
                    all_spots[value,:,col] = 0
                    info[value]['available_by_row_count'][row] = 0
                    info[value]['available_by_row'][row] = []
                    info[value]['available_by_col_count'][col] = 0
                    info[value]['available_by_col'][col] = []
                    block = length_sqrt * (row // length_sqrt) + col // length_sqrt
                    info[value]['available_by_block_count'][block] = 0
                    info[value]['available_by_block'][block] = []
                if info[value]['available_by_col_count'][n] == 1:
                    (row,col) = info[value]['available_by_col'][n][0]
                    if all_spots[0,row,col] != 0 and all_spots[0,row,col] != value:
                        return -1,-1
                    changed_value = 1
                    all_spots[:,row,col] = np.array([value]+[0 for k in range(length)])
                    all_spots[value,row,:] = 0
                    all_spots[value,:,col] = 0
                    info[value]['available_by_row_count'][row] = 0
                    info[value]['available_by_row'][row] = []
                    info[value]['available_by_col_count'][col] = 0
                    info[value]['available_by_col'][col] = []
                    block = length_sqrt * (row // length_sqrt) + col // length_sqrt
                    info[value]['available_by_block_count'][block] = 0
                    info[value]['available_by_block'][block] = []
                if info[value]['available_by_block_count'][n] == 1:
                    (row,col) = info[value]['available_by_block'][n][0]
                    if all_spots[0,row,col] != 0 and all_spots[0,row,col] != value:
                        return -1,-1
                    changed_value = 1
                    all_spots[:,row,col] = np.array([value]+[0 for k in range(length)])
                    all_spots[value,row,:] = 0
                    all_spots[value,:,col] = 0
                    info[value]['available_by_row_count'][row] = 0
                    info[value]['available_by_row'][row] = []
                    info[value]['available_by_col_count'][col] = 0
                    info[value]['available_by_col'][col] = []
                    block = length_sqrt * (row // length_sqrt) + col // length_sqrt
                    info[value]['available_by_block_count'][block] = 0
                    info[value]['available_by_block'][block] = []
        sum_array = all_spots[1:].sum(axis = 0)
        for (row,col) in [(row,col) for row in range(length) for col in range(length)]:
            if sum_array[row,col] == 1:
                for value in range(1,length+1):
                    if all_spots[value, row, col] == 1:
                        changed_value = 1
                        all_spots[:,row,col] = np.array([value]+[0 for k in range(length)])
                        all_spots[value,row,:] = 0
                        all_spots[value,:,col] = 0
                        info[value]['available_by_row_count'][row] = 0
                        info[value]['available_by_row'][row] = []
                        info[value]['available_by_col_count'][col] = 0
                        info[value]['available_by_col'][col] = []
                        block = length_sqrt * (row // length_sqrt) + col // length_sqrt
                        info[value]['available_by_block_count'][block] = 0
                        info[value]['available_by_block'][block] = []
                        break
    return all_spots, info


# noinspection PyUnusedLocal,PyShadowingNames
def update_info(all_spots, length, length_sqrt):
    row_sum = all_spots[1:].sum(axis = 2)
    col_sum = all_spots[1:].sum(axis = 1)
    info = {}
    for n in range(length):
        info[n+1] = {'available_by_row':{k:[] for k in range(length)},
                     'available_by_col':{k:[] for k in range(length)},
                     'available_by_block':{k:[] for k in range(length)},
                     'available_by_block_count':np.array([0 for k in range(length)])}
        info[n+1]['available_by_row_count'] = row_sum[n]
        info[n+1]['available_by_col_count'] = col_sum[n]
        for (row,col) in [(row, col) for row in range(length) for col in range(length)]:
            if all_spots[n+1,row,col] == 1:
                info[n+1]['available_by_row'][row].append((row,col))
                info[n+1]['available_by_col'][col].append((row,col))
                block_index = length_sqrt * (row // length_sqrt) + col // length_sqrt
                info[n+1]['available_by_block'][block_index].append((row,col))
                info[n+1]['available_by_block_count'][block_index] += 1
                

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
    
    test3 = np.array([
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
    # info= make_initial_available_arrays(test, 4, 2)
    all_spots1, info1, rows1, cols1, blocks1 = make_initial_value_arrays(test3, 9, 3)
    all_spots1 = all_spots1.astype(int)
    a1 = all_spots1.copy()
    print_puzzle(all_spots1[0])
    print('-'*100,'\n')
    # print_puzzle(all_spots[1:].sum(axis=0))
    # for n in range(10):
    #     print_puzzle(all_spots[n])
    all_spots1, _ = update_all_spots(all_spots1, info1, 9,3)
    print_puzzle(all_spots1[0])
    print('-'*100,'\n')
    print_puzzle(all_spots1[0]-a1[0])
    print('-'*100,'\n')
    print_puzzle(all_spots1[1:].sum(axis=0))
    print('-'*100,'\n')
    for n in range(10):
        print(n)
        print_puzzle(all_spots1[n])
