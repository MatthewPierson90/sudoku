import tkinter as tk
import numpy as np
from sudoku_functions import check_valid
from gui_puzzle_solution import Solution_pop_up


class sudoku(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Sudoku')
        self.geometry("620x712")
        tk.IntVar()
        self.intro_screen()
        self.make_menu()
        self.puzzle_made = False

    def make_menu(self):
        menu = tk.Menu(self)
        self.config(menu = menu)
        filemenu = tk.Menu(menu)
        menu.add_cascade(label = 'Files', menu = filemenu)
        filemenu.add_command(label = 'New Puzzle')
        filemenu.add_command(label = 'Load Puzzle')
        filemenu.add_command(label = 'Save Puzzle')

    def intro_screen(self, from_back = False):
        if from_back:
            self.select_frame.destroy()
        self.intro_frame = tk.Frame(self)
        self.intro_frame.pack(fill=tk.BOTH, expand=True)
        new = tk.Button(self.intro_frame,
                        text = 'New Puzzle',
                        font = ('DejaVu Sans',10),
                        width = 25,
                        command = self.select_grid_size
                        ).pack(fill=tk.BOTH, expand=True)
        load = tk.Button(self.intro_frame,
                         text = 'Load Puzzle',
                         width = 25,
                         command = self.select_grid_size
                         ).pack(fill=tk.BOTH, expand=True)

    def select_grid_size(self):
        self.intro_frame.destroy()
        self.select_frame = tk.Frame(self)
        self.select_frame.pack(fill = tk.BOTH, expand=True)
        message = tk.Label(self.select_frame, text = 'Select puzzle size:').pack(fill = tk.BOTH, expand=True)

        s4 = tk.Button(self.select_frame,
                       text = '4x4',
                       width = 25,
                       command = lambda : self.make_setup_gird(4)
                       ).pack(fill = tk.BOTH, expand=True)

        s9 = tk.Button(self.select_frame,
                       text = '9x9',
                       width = 25,
                       command = lambda : self.make_setup_gird(9)
                       ).pack(fill = tk.BOTH, expand=True)

        s16 = tk.Button(self.select_frame,
                        text = '16x16',
                        width = 25,
                        command = lambda : self.make_setup_gird(16)
                        ).pack(fill = tk.BOTH, expand=True)

        back = tk.Button(self.select_frame,
                         text = 'Back',
                         width = 25,
                         command = lambda :self.intro_screen(True)
                         ).pack(fill = tk.BOTH, expand=True)


    def make_setup_gird(self, size):
        self.select_frame.destroy()
        self.game_frame = tk.Frame(self)
        self.game_frame.pack(fill = tk.BOTH, expand=True)
        self.game_board = np.zeros((2,size,size), dtype = int)
        self.sqrt_size = int(size ** .5)
        message_frame = tk.Frame(self.game_frame)
        message_frame.pack(pady=10)
        message = tk.Label(message_frame, text = 'Enter given numbers. When finished, press set:').pack()
        self.entry_frame = tk.Canvas(self.game_frame, bg = 'white')
        self.entry_frame.pack(fill = tk.BOTH, expand=True)
        set_frame = tk.Frame(self.game_frame)
        set_frame.pack(pady=10)
        set_button = tk.Button(set_frame, text = 'Set', width = 10, command = lambda : self.set_press())
        set_button.pack()
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
        n = 0
        for row in self.var_list:
            m=0
            for var in row:
                self.update_game_board(var.get(),n,m)
                m += 1
            n += 1
        # print(self.game_board)
        valid,_ = check_valid(self.game_board[0])
        if valid:
            self.make_game_board()
        else:
            pass

    def update_game_board(self, x, n, m, from_board_setup = True):
        board = self.game_board
        if from_board_setup:
            in_game_entry = 0
        else:
            in_game_entry = 1
        x = x.lower()
        if x == '':
            board[0, n, m] = 0
        else:
            if self.sqrt_size == 2:
                if x in '1 2 3 4' and x != ' ':
                    board[0, n, m] = int(x)
                    board[1, n, m] = in_game_entry
                else:
                    pass
            elif self.sqrt_size == 3:
                if x in '1 2 3 4 5 6 7 8 9' and x != ' ':
                    board[0, n, m] = int(x)
                    board[1, n, m] = in_game_entry
                else:
                    pass
            elif self.sqrt_size == 4:
                if x == 'a':
                    board[0, n, m] = 10
                    board[1, n, m] = in_game_entry
                elif x == 'b':
                    board[0, n, m] = 11
                    board[1, n, m] = in_game_entry
                elif x == 'c':
                    board[0, n, m] = 12
                    board[1, n, m] = in_game_entry
                elif x == 'd':
                    board[0, n, m] = 13
                    board[1, n, m] = in_game_entry
                elif x == 'e':
                    board[0, n, m] = 14
                    board[1, n, m] = in_game_entry
                elif x == 'f':
                    board[0, n, m] = 15
                    board[1, n, m] = in_game_entry
                elif x == 'g':
                    board[0, n, m] = 16
                    board[1, n, m] = in_game_entry
                elif x in '1 2 3 4 5 6 7 8 9' and x != ' ':
                    board[0, n, m] = int(x)
                    board[1, n, m] = in_game_entry
                else:
                    pass

    def make_game_board(self):
        self.game_frame.destroy()
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
                else:
                    tk.Label(self.entry_frame,
                             width = 1,
                             justify = tk.CENTER,
                             text = str(int(self.game_board[0, n, m])),
                             font = ('DejaVu Sans', 16),
                             bg = 'white',
                             bd = 0).grid(row = 2*n+1,
                                          column = 2*m+1,
                                          sticky = tk.N+tk.S+tk.E+tk.W)
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
        for row in self.var_list:
            m = 0
            for var in row:
                self.update_game_board(var.get(), n, m, from_board_setup = False)
                m += 1
            n += 1
        is_valid, sol = check_valid(self.game_board[0].astype(int))

        if is_valid:
            print('Valid')
        else:
            print('BAD BAD BAD')


    def brute_press(self):
        n = 0
        for row in self.var_list:
            m = 0
            for var in row:
                self.update_game_board(var.get(), n, m, from_board_setup = False)
                m += 1
            n += 1
        is_valid, sol = check_valid(self.game_board[0].astype(int))
        if is_valid:
            game_board_copy = self.game_board[0].astype(int)
        else:
            game_board_copy = self.game_board[0]*(1-self.game_board[1])
        Solution_pop_up(game_board_copy, 'Smart Brute Force', self.sqrt_size)

    def alg1_press(self):
        n = 0
        for row in self.var_list:
            m = 0
            for var in row:
                self.update_game_board(var.get(), n, m, from_board_setup = False)
                m += 1
            n += 1
        is_valid, sol = check_valid(self.game_board[0].astype(int))
        if is_valid:
            game_board_copy = self.game_board[0].astype(int)
        else:
            game_board_copy = self.game_board[0]*(1-self.game_board[1])
            game_board_copy  = game_board_copy.astype(int)
        Solution_pop_up(game_board_copy, 'Algorithm 1', self.sqrt_size)

    def alg2_press(self):
        n = 0
        for row in self.var_list:
            m = 0
            for var in row:
                self.update_game_board(var.get(), n, m, from_board_setup = False)
                m += 1
            n += 1
        is_valid, sol = check_valid(self.game_board[0].astype(int))
        if is_valid:
            game_board_copy = self.game_board[0].astype(int)
        else:
            game_board_copy = self.game_board[0]*(1-self.game_board[1])
            game_board_copy = game_board_copy.astype(int)
        Solution_pop_up(game_board_copy, 'Algorithm 2', self.sqrt_size)

    def save_puzzle_state(self):
        pass

    def load_puzzle_state(self):
        pass

    def new_puzzle_state(self):
        pass



if __name__ == '__main__':
    s = sudoku()
    s.mainloop()

# window = tk.Tk()
#
# window.title('Sudoku')
#
# grid_size = tk.IntVar(value = 0)
#
# tk.Radiobutton(window, text = ' 9x9 ', variable = grid_size, value = 9).grid(row = 2, sticky = tk.W)
# tk.Radiobutton(window, text = '16x16', variable = grid_size, value = 16).grid(row = 3, sticky = tk.W)
#
# if grid_size.get() != 0:
#     tk.Label(window, text = f'{grid_size}x{grid_size}').grid(row = 4)
#
#
# window.mainloop()