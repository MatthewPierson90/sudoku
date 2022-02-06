import numpy as np
import tkinter as tk
from sudoku_functions import check_valid, brute_force
from solution_one import solution_one
from solution_two_simple import solution_two
from time import perf_counter as tt

class Solution_pop_up(tk.Tk):
    def __init__(self, game_board, alg_name, sqrt_size, window_x, window_y, time_out = 2):
        super().__init__()
        self.sqrt_size = sqrt_size
        self.time_out = time_out
        length = int(sqrt_size**2)
        try:
            if alg_name == 'Smart Brute Force':
                start = tt()
                valid, solution = brute_force(game_board, length, start = start, time_out = time_out)
                end = tt()
    
            elif alg_name == 'Algorithm 1':
                start = tt()
                valid, solution = solution_one(game_board, start = start, time_out = time_out)
                end = tt()
            else:
                start = tt()
                valid, solution = solution_two(game_board, start = start, time_out = time_out)
                end = tt()
    
            total_time = end - start
            self.title(f'Solution via {alg_name}')

            message_frame = tk.Frame(self)
            message_frame.pack(pady = 10)
            if total_time > 3600:
                total_time_in_mins = round(total_time/60)
                total_time = round(total_time)
                hours = int(total_time_in_mins/60)
                mins = total_time_in_mins%60
                secs = total_time%60
                time_string = f'{hours}h, {mins}m, {secs}s'
            elif total_time > 60:
                total_time = round(total_time)
                mins = int(total_time/60)
                secs = total_time%60
                time_string = f'{mins}m, {secs}s'
            elif total_time > .1:
                time_string = '{}s'.format(round(total_time, 2))
            else:
                if round(total_time*1000) == 0:
                    total_time = round(total_time*1000, 2)
                else:
                    total_time = round(total_time*1000)
                time_string = f'{total_time}ms'
            message = tk.Label(message_frame, text = f'{alg_name} completed in {time_string}').pack()
            solution_frame = tk.Canvas(self, bg = 'white')
            self.solution_frame = solution_frame
            solution_frame.pack(side = tk.LEFT, fill = tk.BOTH, expand = True)
            size = int(self.sqrt_size ** 2)
            if valid == 1:
                self.geometry("600x600")
                self.geometry(f'+{window_x+100}+{window_y}')
                for n in range(0, size):
                    for m in range(0, size):
                        tk.Label(solution_frame,
                                 width = 1,
                                 justify = tk.CENTER,
                                 text = str(int(solution[n, m])),
                                 font = ('DejaVu Sans', 16),
                                 bg = 'white',
                                 bd = 0).grid(row = 2*n+1,
                                              column = 2*m+1,
                                              sticky = tk.N+tk.S+tk.E+tk.W)
                self.vlines = []
                self.hlines = []
                ef_height = solution_frame.winfo_height()
                ef_width = solution_frame.winfo_width()

                for k in range(1, self.sqrt_size):
                    vline = solution_frame.create_line(k*ef_width/self.sqrt_size+(1/2-k/self.sqrt_size)*10*ef_width/31,
                                                       0,
                                                       k*ef_width/self.sqrt_size+(1/2-k/self.sqrt_size)*10*ef_width/31,
                                                       ef_height,
                                                       width = 3)
                    self.vlines.append(vline)
                    hline = solution_frame.create_line(0,
                                                       k*ef_height/self.sqrt_size+(1/2-k/self.sqrt_size)*5,
                                                       ef_width,
                                                       k*ef_height/self.sqrt_size+(1/2-k/self.sqrt_size)*5,
                                                       width = 3)
                    self.hlines.append(hline)
                for k in range(0, 2*size+1):
                    if k%2 == 0:
                        if 0 < k < 2*size:
                            solution_frame.rowconfigure(k, weight = 2)
                            solution_frame.columnconfigure(k, weight = 2)
                        else:
                            solution_frame.rowconfigure(k, weight = 1)
                            solution_frame.columnconfigure(k, weight = 1)
                    else:
                        solution_frame.rowconfigure(k, weight = 8)
                        solution_frame.columnconfigure(k, weight = 8)

                solution_frame.bind('<Configure>', lambda x:self.update_on_resize())
            else:
                self.geometry('600x150')
                self.geometry(f'+{window_x+200}+{window_y+200}')
                message2 = tk.Label(solution_frame,
                                    bg = 'white',
                                    text = 'No Solution!',
                                    font = ('DejaVu Sans', 32)).pack(fill = 'both', expand = True)
        except:
            self.geometry('350x100')
            self.geometry(f'+{window_x+200}+{window_y+200}')
            self.title('Solver Timeout')
            time_out_message = tk.Label(self,
                                         text = f'Solver exceeded {time_out} seconds.\nThe time limit can be changed in the menu.',
                                         font = ('DejaVu Sans', 12))
            time_out_message.pack(fill = 'both', expand = True)


    def update_on_resize(self):
        for vline in self.vlines:
            self.solution_frame.delete(vline)
        for hline in self.hlines:
            self.solution_frame.delete(hline)
        ef_height = self.solution_frame.winfo_height()
        ef_width = self.solution_frame.winfo_width()
        num = int(self.sqrt_size ** 2)
        fs = int(ef_height/(10*num)+16)
        self.vlines = []
        self.hlines = []
        for k in range(1, int(self.sqrt_size ** 2)):
            if k%self.sqrt_size == 0:
                vline = self.solution_frame.create_line(k*ef_width/self.sqrt_size ** 2,
                                                        0,
                                                        k*ef_width/self.sqrt_size ** 2,
                                                        ef_height,
                                                        width = 4)
                hline = self.solution_frame.create_line(0,
                                                        k*ef_height/self.sqrt_size ** 2,
                                                        ef_width,
                                                        k*ef_height/self.sqrt_size ** 2,
                                                        width = 4)
            else:
                vline = self.solution_frame.create_line(k*ef_width/self.sqrt_size ** 2,
                                                        0,
                                                        k*ef_width/self.sqrt_size ** 2,
                                                        ef_height,
                                                        width = 2)
                hline = self.solution_frame.create_line(0,
                                                        k*ef_height/self.sqrt_size ** 2,
                                                        ef_width,
                                                        k*ef_height/self.sqrt_size ** 2,
                                                        width = 2)
            self.vlines.append(vline)
            self.hlines.append(hline)
        for widget in self.solution_frame.winfo_children():
            if type(widget) == tk.Entry or type(widget) == tk.Label:
                widget.config(font = ('DejaVu Sans', fs))


