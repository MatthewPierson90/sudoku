import tkinter as tk
import numpy as np
from sudoku_functions import check_valid, SolveTimeOut, tt
from gui_puzzle_solution import Solution_pop_up
# from gui_save_load_puzzle import Save_load_pop_up
from unique_solution import check_unique
from premade_puzzles import Premade_puzzles
from generate_puzzle import generate_puzzle

class sudoku(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Sudoku')
        self.geometry("620x712")
        tk.IntVar()
        self.intro_screen()
        self.make_menu()
        self.puzzle_made = False
        self.current_state = 0
        self.solution_time_out = 1.
        self.premade_puzzles = Premade_puzzles()



    def make_menu(self):
        menu = tk.Menu(self, tearoff=False)
        self.config(menu = menu)
        file_menu = tk.Menu(menu, tearoff=False)
        menu.add_cascade(label = 'Menu', menu = file_menu)
        file_menu.add_separator()
        file_menu.add_separator()
        file_menu.add_command(label = 'Solver Time Limit', command = self.set_time_limit)
        file_menu.add_separator()
        file_menu.add_separator()
        file_menu.add_command(label = 'Main Menu', command = lambda: self.intro_screen(True))


    def intro_screen(self, from_back = False):
        self.current_state = 1
        if from_back:
            for widget in self.winfo_children():
                if type(widget) != tk.Menu:
                    widget.destroy()
        self.intro_frame = tk.Frame(self)
        self.intro_frame.pack(fill=tk.BOTH, expand=True)
        new = tk.Button(self.intro_frame,
                        text = 'New Puzzle',
                        font = ('DejaVu Sans',10),
                        width = 25,
                        command = self.select_grid_size
                        ).pack(fill=tk.BOTH, expand=True)
        premade = tk.Button(self.intro_frame,
                        text = 'Pre-made Puzzles',
                        font = ('DejaVu Sans', 10),
                        width = 25,
                        command = self.select_premade_puzzle
                        ).pack(fill = tk.BOTH, expand = True)

        
    def select_premade_puzzle(self):
        self.current_state = 2
        self.intro_frame.destroy()
        self.select_frame = tk.Frame(self)
        self.select_frame.pack(fill = tk.BOTH, expand = True)
        message = tk.Label(self.select_frame, text = 'Select puzzle size:').pack(fill = tk.BOTH, expand = True)

        easy = tk.Button(self.select_frame,
                       text = 'Easy',
                       width = 25,
                       command = lambda:self.premade_button_press(self.premade_puzzles.easy)
                       ).pack(fill = tk.BOTH, expand = True)

        med = tk.Button(self.select_frame,
                       text = 'Medium',
                       width = 25,
                       command = lambda:self.premade_button_press(self.premade_puzzles.medium)
                       ).pack(fill = tk.BOTH, expand = True)
        hard = tk.Button(self.select_frame,
                       text = 'Hard',
                       width = 25,
                       command = lambda:self.premade_button_press(self.premade_puzzles.hard)
                       ).pack(fill = tk.BOTH, expand = True)

        evil1 = tk.Button(self.select_frame,
                       text = 'Evil 1',
                       width = 25,
                       command = lambda:self.premade_button_press(self.premade_puzzles.evil1)
                       ).pack(fill = tk.BOTH, expand = True)
        evil2 = tk.Button(self.select_frame,
                       text = 'Evil 2',
                       width = 25,
                       command = lambda:self.premade_button_press(self.premade_puzzles.evil2)
                       ).pack(fill = tk.BOTH, expand = True)

        evil3 = tk.Button(self.select_frame,
                       text = 'Evil 3',
                       width = 25,
                       command = lambda:self.premade_button_press(self.premade_puzzles.evil3)
                       ).pack(fill = tk.BOTH, expand = True)
        evil4 = tk.Button(self.select_frame,
                          text = 'Evil 4',
                          width = 25,
                          command = lambda:self.premade_button_press(self.premade_puzzles.evil4)
                          ).pack(fill = tk.BOTH, expand = True)
        evil5 = tk.Button(self.select_frame,
                          text = 'Evil 5',
                          width = 25,
                          command = lambda:self.premade_button_press(self.premade_puzzles.evil5)
                          ).pack(fill = tk.BOTH, expand = True)

        evil6 = tk.Button(self.select_frame,
                          text = 'Evil 6',
                          width = 25,
                          command = lambda:self.premade_button_press(self.premade_puzzles.evil6)
                          ).pack(fill = tk.BOTH, expand = True)

        back = tk.Button(self.select_frame,
                         text = 'Back',
                         width = 25,
                         command = lambda:self.intro_screen(True)
                         ).pack(fill = tk.BOTH, expand = True)

    def premade_button_press(self, puzzle):
        self.game_board = puzzle
        self.sqrt_size = int(self.game_board.shape[1] ** .5)
        self.var_list = []
        for n in range(self.game_board.shape[1]):
            self.var_list.append([])
            for m in range(self.game_board.shape[1]):
                var = tk.StringVar()
                if self.game_board[0, n, m] != 0:
                    var.set(self.game_board[0, n, m])
                self.var_list[-1].append(var)
        self.make_game_board()

    def select_grid_size(self):
        self.current_state = 2
        for widget in self.winfo_children():
            if type(widget) != tk.Menu:
                widget.destroy()
        self.select_frame = tk.Frame(self)
        self.select_frame.pack(fill = tk.BOTH, expand=True)
        message = tk.Label(self.select_frame, text = 'Select puzzle size:').pack(fill = tk.BOTH, expand=True)

        s4 = tk.Button(self.select_frame,
                       text = '4x4',
                       width = 25,
                       command = lambda : self.generate_or_enter_frame(4)
                       ).pack(fill = tk.BOTH, expand=True)

        s9 = tk.Button(self.select_frame,
                       text = '9x9',
                       width = 25,
                       command = lambda : self.generate_or_enter_frame(9)
                       ).pack(fill = tk.BOTH, expand=True)

        back = tk.Button(self.select_frame,
                         text = 'Back',
                         width = 25,
                         command = lambda :self.intro_screen(True)
                         ).pack(fill = tk.BOTH, expand=True)
    
    def generate_or_enter_frame(self, grid_size):
        self.current_state = 6
        for widget in self.winfo_children():
            if type(widget) != tk.Menu:
                widget.destroy()
        self.generate_or_enter = tk.Frame(self)
        self.generate_or_enter.pack(fill=tk.BOTH, expand=True)
        enter = tk.Button(self.generate_or_enter,
                        text = 'Enter Values',
                        font = ('DejaVu Sans',10),
                        width = 25,
                        command = lambda : self.make_setup_gird(grid_size)
                        ).pack(fill=tk.BOTH, expand=True)
        generate = tk.Button(self.generate_or_enter,
                        text = 'Generate Random \n(This may take a moment)',
                        font = ('DejaVu Sans', 10),
                        width = 25,
                        command = lambda: self.generate_button_press(grid_size)
                        ).pack(fill = tk.BOTH, expand = True)
        back = tk.Button(self.generate_or_enter,
                         text = 'Back',
                         width = 25,
                         command = lambda:self.select_grid_size()
                         ).pack(fill = tk.BOTH, expand = True)

    def generate_button_press(self, grid_size):
        puzzle = np.zeros((2,grid_size,grid_size), dtype = np.int8)
        puzzle[0] = generate_puzzle(grid_size)
        puzzle[1, puzzle[0] > 0] = 0
        self.premade_button_press(puzzle)

    def make_setup_gird(self, size):
        self.current_state = 3
        for widget in self.winfo_children():
            if type(widget) != tk.Menu:
                widget.destroy()
        self.game_frame = tk.Frame(self)
        self.game_frame.pack(fill = tk.BOTH, expand=True)
        self.game_board = np.zeros((2,size,size), dtype = int)
        self.sqrt_size = int(size ** .5)
        message_frame = tk.Frame(self.game_frame)
        message_frame.pack(pady=10)
        message = tk.Label(message_frame,
                           text = 'Enter given numbers. When finished, press set:').pack()
        self.entry_frame = tk.Canvas(self.game_frame, bg = 'white')
        self.entry_frame.pack(fill = tk.BOTH, expand=True)
        set_frame = tk.Frame(self.game_frame)
        set_frame.pack(pady=10, fill = 'x')
        set_button = tk.Button(set_frame,
                               text = 'Set Puzzle',
                               width = 10,
                               command = lambda : self.set_press())
        # set_button.pack(side = 'left', fill = 'x', expand = True)
        set_button.grid(row = 0, column = 1, sticky = 'NSEW')

        check_unique_button = tk.Button(set_frame,
                                        text = 'Check Uniqueness',
                                        width = 10,
                                        command = lambda : self.check_uniqueness())
        # check_unique_button.pack(side = 'left', fill = 'x', expand = True)
        uniqueness_time_limit_label = tk.Label(set_frame,text = 'Check for uniqueness\n time limit (seconds):')
        uniqueness_time_limit_label.grid(row = 0, column = 2, padx = 20, sticky = 'NSEW')
        uniqueness_time_limit_entry = tk.Entry(set_frame, width = 2)
        self.uniqueness_time_limit_var = tk.StringVar(uniqueness_time_limit_entry)
        self.uniqueness_time_limit_var.set(str(10.0))
        uniqueness_time_limit_entry.config(textvariable = self.uniqueness_time_limit_var)
        uniqueness_time_limit_entry.grid(row = 0, column = 3, sticky = 'NSEW')
        check_unique_button.grid(row = 0, column = 4, padx = 20, sticky = 'NSEW')
        set_frame.columnconfigure(0, weight = 1)
        set_frame.columnconfigure(1, weight = 2)
        set_frame.columnconfigure(2, weight = 3)
        set_frame.columnconfigure(3, weight = 1)
        set_frame.columnconfigure(4, weight = 4)
        self.var_list = []
        for n in range(0,size):
            self.var_list.append([])
            for m in range(0,size):
                self.var_list[n].append(tk.StringVar())
                tk.Entry(self.entry_frame,
                         width = 1,
                         justify = tk.CENTER,
                         highlightbackground = 'white',
                         font = ('DejaVu Sans',16),
                         bd = 1,
                         textvariable = self.var_list[n][m]
                         ).grid(row = 2*n+1,
                                column = 2*m+1,
                                sticky=tk.N+tk.S+tk.E+tk.W)
        self.vlines = []
        self.hlines = []
        ef_height = self.entry_frame.winfo_height()
        ef_width = self.entry_frame.winfo_width()

        for k in range(1, self.sqrt_size):
            vline = self.entry_frame.create_line(k*ef_width/self.sqrt_size+(1/2-k/self.sqrt_size)*10*ef_width/31,
                                                 0,
                                                 k*ef_width/self.sqrt_size+(1/2-k/self.sqrt_size)*10*ef_width/31,
                                                 ef_height,
                                                 width = 3)
            self.vlines.append(vline)
            hline = self.entry_frame.create_line(0,
                                                 k*ef_height/self.sqrt_size+(1/2-k/self.sqrt_size)*5,
                                                 ef_width,
                                                 k*ef_height/self.sqrt_size+(1/2-k/self.sqrt_size)*5,
                                                 width = 3)
            self.hlines.append(hline)
        for k in range(0, 2*size+1):
            if k%2 == 0:
                if 0 < k < 2*size:
                    self.entry_frame.rowconfigure(k, weight = 2)
                    self.entry_frame.columnconfigure(k, weight = 2)
                else:
                    self.entry_frame.rowconfigure(k, weight = 1)
                    self.entry_frame.columnconfigure(k, weight = 1)
            else:
                self.entry_frame.rowconfigure(k, weight = 8)
                self.entry_frame.columnconfigure(k, weight = 8)
        self.entry_frame.bind('<Configure>', lambda x:self.update_entry_text())

    def update_entry_text(self):
        for vline in self.vlines:
            self.entry_frame.delete(vline)
        for hline in self.hlines:
            self.entry_frame.delete(hline)
        ef_height = self.entry_frame.winfo_height()
        ef_width = self.entry_frame.winfo_width()
        num = int(self.sqrt_size**2)
        fs = int(ef_height/(10*num)+16)
        self.vlines = []
        self.hlines = []
        for k in range(1, int(self.sqrt_size**2)):
            if k%self.sqrt_size == 0:
                vline = self.entry_frame.create_line(k*ef_width/self.sqrt_size**2,
                                                     0,
                                                     k*ef_width/self.sqrt_size**2,
                                                     ef_height,
                                                     width = 4)
                hline = self.entry_frame.create_line(0,
                                                     k*ef_height/self.sqrt_size**2,
                                                     ef_width,
                                                     k*ef_height/self.sqrt_size**2,
                                                     width = 4)
            else:
                vline = self.entry_frame.create_line(k*ef_width/self.sqrt_size**2,
                                                     0,
                                                     k*ef_width/self.sqrt_size**2,
                                                     ef_height,
                                                     width = 2)
                hline = self.entry_frame.create_line(0,
                                                     k*ef_height/self.sqrt_size**2,
                                                     ef_width,
                                                     k*ef_height/self.sqrt_size**2,
                                                     width = 2)
            self.vlines.append(vline)
            self.hlines.append(hline)
        for widget in self.entry_frame.winfo_children():
             if type(widget) == tk.Entry or type(widget) == tk.Label :
                 widget.config(font = ('DejaVu Sans',fs))

    def set_press(self):
        invalid_entry = self.update_game_board(from_board_setup = True)
        if invalid_entry:
            invalid_puzzle = tk.Tk()
            invalid_puzzle.geometry('350x100')
            invalid_puzzle.geometry(f'+{self.winfo_rootx()+200}+{self.winfo_rooty()+200}')
            invalid_puzzle.title('Invalid!')
            time_out_message = tk.Label(invalid_puzzle,
                                        text = 'You have an invalid entry!!',
                                        font = ('DejaVu Sans', 12))
            time_out_message.pack(fill = 'both', expand = True)
        else:
            valid_puzzle, _ = check_valid(self.game_board[0])
            if valid_puzzle:
                self.make_game_board()
            else:
                invalid_puzzle = tk.Tk()
                invalid_puzzle.geometry('350x100')
                invalid_puzzle.geometry(f'+{self.winfo_rootx()+200}+{self.winfo_rooty()+200}')
                invalid_puzzle.title('Invalid!')
                time_out_message = tk.Label(invalid_puzzle,
                                            text = 'Puzzle Invalid!',
                                            font = ('DejaVu Sans', 12))
                time_out_message.pack(fill = 'both', expand = True)

    def update_game_board(self, from_board_setup = True):
        board = self.game_board
        invalid_entry = False
        for n in range(self.game_board.shape[1]):
            for m in range(self.game_board.shape[1]):
                x = self.var_list[n][m].get()
                x = x.lower()
                if x == '':
                    board[0, n, m] = 0
                else:
                    if self.sqrt_size == 2:
                        if x in '1 2 3 4' and x != ' ':
                            board[0, n, m] = int(x)
                        else:
                            invalid_entry = True
                    elif self.sqrt_size == 3:
                        if x in '1 2 3 4 5 6 7 8 9' and x != ' ':
                            board[0, n, m] = int(x)
                        else:
                            invalid_entry = True
                    elif self.sqrt_size == 4:
                        if x == 'a':
                            board[0, n, m] = 10
                        elif x == 'b':
                            board[0, n, m] = 11
                        elif x == 'c':
                            board[0, n, m] = 12
                        elif x == 'd':
                            board[0, n, m] = 13
                        elif x == 'e':
                            board[0, n, m] = 14
                        elif x == 'f':
                            board[0, n, m] = 15
                        elif x == 'g':
                            board[0, n, m] = 16
                        elif x in '1 2 3 4 5 6 7 8 9' and x != ' ':
                            board[0, n, m] = int(x)
                        else:
                            invalid_entry = True

        if from_board_setup:
            self.game_board[1,self.game_board[0] == 0] = 1
        return invalid_entry




    def make_game_board(self):
        self.current_state = 4

        for widget in self.winfo_children():
            if type(widget) != tk.Menu:
                widget.destroy()
        self.game_frame = tk.Frame(self)
        self.game_frame.pack(fill = tk.BOTH, expand = True)
        self.entry_frame = tk.Canvas(self.game_frame, bg = 'white')
        self.entry_frame.pack(side = tk.LEFT,fill = tk.BOTH, expand = True)
        solvers_frame = tk.Frame(self.game_frame)
        solvers_frame.pack(side = tk.LEFT, fill = tk.Y)

        valid_button = tk.Button(solvers_frame,
                                 text = 'Check Validity',
                                 width = 20,
                                 command = lambda:self.valid_press())

        valid_button.pack(fill = tk.BOTH, expand = True)

        brute_button = tk.Button(solvers_frame,
                                 text = 'Solve With Brute Force',
                                 width = 20,
                                 command = lambda:self.brute_press())
        brute_button.pack(fill = tk.BOTH, expand = True)

        alg1_button = tk.Button(solvers_frame,
                                 text = 'Solve With Algorithm 1',
                                 command = lambda:self.alg1_press())
        alg1_button.pack(fill = tk.BOTH, expand = True)

        alg2_button = tk.Button(solvers_frame,
                                 text = 'Solve With Algorithm 2',
                                 command = lambda:self.alg2_press())
        alg2_button.pack(fill = tk.BOTH, expand = True)

        size = int(self.sqrt_size**2)
        for n in range(0, size):
            for m in range(0, size):
                if self.game_board[0, n, m] == 0:
                    tk.Entry(self.entry_frame,
                             width = 1,
                             justify = tk.CENTER,
                             font = ('DejaVu Sans', 16),
                             bd = 0,
                             selectborderwidth = 0,
                             relief = 'flat',
                             textvariable = self.var_list[n][m]
                             ).grid(row = 2*n+1,
                                    column = 2*m+1,
                                    sticky = tk.N+tk.S+tk.E+tk.W)
                elif self.game_board[1, n, m] == 0:
                    tk.Label(self.entry_frame,
                             width = 1,
                             justify = tk.CENTER,
                             text = str(int(self.game_board[0, n, m])),
                             font = ('DejaVu Sans', 16),
                             bg = 'white',
                             bd = 0).grid(row = 2*n+1,
                                          column = 2*m+1,
                                          sticky = tk.N+tk.S+tk.E+tk.W)
                elif self.game_board[1, n, m] == 1:
                    tk.Entry(self.entry_frame,
                             width = 1,
                             justify = tk.CENTER,
                             font = ('DejaVu Sans', 16),
                             bd = 0,
                             selectborderwidth = 0,
                             relief = 'flat',
                             textvariable = self.var_list[n][m]
                             ).grid(row = 2*n+1,
                                    column = 2*m+1,
                                    sticky = tk.N+tk.S+tk.E+tk.W)
                    self.var_list[n][m].set(self.game_board[0, n, m])
        self.vlines = []
        self.hlines = []
        ef_height = self.entry_frame.winfo_height()
        ef_width = self.entry_frame.winfo_width()

        for k in range(1, self.sqrt_size):
            vline = self.entry_frame.create_line(k*ef_width/self.sqrt_size+(1/2-k/self.sqrt_size)*10*ef_width/31,
                                                 0,
                                                 k*ef_width/self.sqrt_size+(1/2-k/self.sqrt_size)*10*ef_width/31,
                                                 ef_height,
                                                 width = 3)
            self.vlines.append(vline)
            hline = self.entry_frame.create_line(0,
                                                 k*ef_height/self.sqrt_size+(1/2-k/self.sqrt_size)*5,
                                                 ef_width,
                                                 k*ef_height/self.sqrt_size+(1/2-k/self.sqrt_size)*5,
                                                 width = 3)
            self.hlines.append(hline)
        for k in range(0, 2*size+1):
            if k%2 == 0:
                if 0 < k < 2*size:
                    self.entry_frame.rowconfigure(k, weight = 2)
                    self.entry_frame.columnconfigure(k, weight = 2)
                else:
                    self.entry_frame.rowconfigure(k, weight = 1)
                    self.entry_frame.columnconfigure(k, weight = 1)
            else:
                self.entry_frame.rowconfigure(k, weight = 8)
                self.entry_frame.columnconfigure(k, weight = 8)

        self.entry_frame.bind('<Configure>', lambda x:self.update_entry_text())

    def valid_press(self):
        n = 0
        invalid_entry = self.update_game_board(from_board_setup = False)
        if invalid_entry:
            invalid_puzzle = tk.Tk()
            invalid_puzzle.geometry('350x100')
            invalid_puzzle.geometry(f'+{self.winfo_rootx()+200}+{self.winfo_rooty()+200}')
            invalid_puzzle.title('Solver Timeout')
            time_out_message = tk.Label(invalid_puzzle,
                                        text = 'You have an invalid entry!!',
                                        font = ('DejaVu Sans', 12))
            time_out_message.pack(fill = 'both', expand = True)
        else:
            is_valid, sol = check_valid(self.game_board[0].astype(int))
            valid_window = tk.Tk()
            valid_window.title('Is it valid?!')
            valid_window.geometry('300x50')
            valid_window.geometry(f'+{self.winfo_rootx()+200}+{self.winfo_rooty()+200}')
            if is_valid:
                tk.Label(valid_window, text = 'Currently Valid!').pack(expand = True, fill = 'both')
            else:
                tk.Label(valid_window, text = 'Puzzle Invalid, Logic error!').pack(expand = True, fill = 'both')


    def brute_press(self):
        self.update_game_board(from_board_setup = False)
        is_valid, sol = check_valid(self.game_board[0].astype(int))
        if is_valid:
            game_board_copy = self.game_board[0].astype(int)
        else:
            game_board_copy = self.game_board[0]*(1-self.game_board[1])
        Solution_pop_up(game_board = game_board_copy,
                        alg_name = 'Smart Brute Force',
                        sqrt_size = self.sqrt_size,
                        window_x = self.winfo_rootx(),
                        window_y = self.winfo_rooty(),
                        time_out = self.solution_time_out)

    def alg1_press(self):
        n = 0
        self.update_game_board(False)
        is_valid, sol = check_valid(self.game_board[0].astype(int))
        if is_valid:
            game_board_copy = self.game_board[0].astype(int)
        else:
            game_board_copy = self.game_board[0]*(1-self.game_board[1])
            game_board_copy  = game_board_copy.astype(int)
        Solution_pop_up(game_board = game_board_copy,
                        alg_name = 'Algorithm 1',
                        sqrt_size = self.sqrt_size,
                        window_x = self.winfo_rootx(),
                        window_y = self.winfo_rooty(),
                        time_out = self.solution_time_out)


    def alg2_press(self):
        self.update_game_board(from_board_setup = False)
        is_valid, sol = check_valid(self.game_board[0].astype(int))
        if is_valid:
            game_board_copy = self.game_board[0].astype(int)
        else:
            game_board_copy = self.game_board[0]*(1-self.game_board[1])
            game_board_copy = game_board_copy.astype(int)
        Solution_pop_up(game_board = game_board_copy,
                        alg_name = 'Algorithm 2',
                        sqrt_size = self.sqrt_size,
                        window_x = self.winfo_rootx(),
                        window_y = self.winfo_rooty(),
                        time_out = self.solution_time_out)

    def set_time_limit(self):
        self.set_time_limit_window = tk.Tk()
        self.set_time_limit_window.geometry('400x150')
        self.set_time_limit_window.geometry(f'+{self.winfo_rootx()+200}+{self.winfo_rooty()+200}')
        self.set_time_limit_window.title('Save Error')
        self.set_time_limit_window_message = tk.Label(self.set_time_limit_window,
                                     text = f'Current solver time limit: {self.solution_time_out} seconds.\nEnter new limit below.',
                                     font = ('DejaVu Sans', 12))
        self.set_time_limit_window_message.pack(fill = 'x', expand = True)
        limit_entry_frame = tk.Frame(self.set_time_limit_window)
        limit_entry_frame.pack(fill = 'both', expand = True)
        tk.Label(limit_entry_frame, text = '  ').pack(side = 'bottom', fill = 'x')
        tk.Label(limit_entry_frame, text = '  ').pack(side = 'left')
        tk.Label(limit_entry_frame, text = '  ').pack(side = 'right')
        limit_entry = tk.Entry(limit_entry_frame, justify = 'right',width = 4, font = ('DejaVu Sans',16))
        self.time_var = tk.StringVar(limit_entry)
        limit_entry.config(textvariable = self.time_var)
        limit_entry.pack(side = 'left',fill = 'both', expand = True)
        limit_button = tk.Button(limit_entry_frame, width = 4,text = 'Set limit', command = self.set_limit_press)
        limit_button.pack(side = 'right',fill = 'both', expand = True)


    def set_limit_press(self):
        try:
            self.solution_time_out = float(self.time_var.get())
            self.set_time_limit_window.destroy()
        except ValueError:
            self.set_time_limit_window.destroy()

    def check_uniqueness(self):
        invalid_entry = self.update_game_board(from_board_setup = True)
        if invalid_entry:
            invalid_puzzle = tk.Tk()
            invalid_puzzle.geometry('350x100')
            invalid_puzzle.geometry(f'+{self.winfo_rootx()+200}+{self.winfo_rooty()+200}')
            invalid_puzzle.title('Invalid!')
            time_out_message = tk.Label(invalid_puzzle,
                                        text = 'You have an invalid entry!!',
                                        font = ('DejaVu Sans', 12))
            time_out_message.pack(fill = 'both', expand = True)
        else:
            valid_puzzle, _ = check_valid(self.game_board[0])
            if valid_puzzle:
                unique_puzzle = tk.Tk()
                unique_puzzle.geometry('350x100')
                unique_puzzle.geometry(f'+{self.winfo_rootx()+200}+{self.winfo_rooty()+200}')
                unique_puzzle.title('Puzzle Unique?')
                try:
                    # print(float(self.uniqueness_time_limit_var.get()))
                    start = tt()
                    is_unique = check_unique(self.game_board[0],
                                             time_out = float(self.uniqueness_time_limit_var.get()),
                                             start = start)
                    if is_unique == 0:
                        unique_message = tk.Label(unique_puzzle,
                                                  text = 'Puzzle has multiple solutions!',
                                                  font = ('DejaVu Sans', 12))
                        unique_message.pack(fill = 'both', expand = True)
                    elif is_unique == 1:
                        unique_message = tk.Label(unique_puzzle,
                                                  text = 'Puzzle has a unique solution!!',
                                                  font = ('DejaVu Sans', 12))
                        unique_message.pack(fill = 'both', expand = True)
                    elif is_unique == -1:
                        unique_message = tk.Label(unique_puzzle,
                                                  text = 'Puzzle has no solution!!',
                                                  font = ('DejaVu Sans', 12))
                        unique_message.pack(fill = 'both', expand = True)
                except SolveTimeOut:
                    unique_message = tk.Label(unique_puzzle,
                                              text = 'Uniqueness solver timed out!!',
                                              font = ('DejaVu Sans', 12))
                    unique_message.pack(fill = 'both', expand = True)
            else:
                invalid_puzzle = tk.Tk()
                invalid_puzzle.geometry('350x100')
                invalid_puzzle.geometry(f'+{self.winfo_rootx()+200}+{self.winfo_rooty()+200}')
                invalid_puzzle.title('Invalid!')
                time_out_message = tk.Label(invalid_puzzle,
                                            text = 'Puzzle Invalid!',
                                            font = ('DejaVu Sans', 12))
                time_out_message.pack(fill = 'both', expand = True)


if __name__ == '__main__':
    s = sudoku()
    s.mainloop()

