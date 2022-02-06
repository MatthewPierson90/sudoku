import numpy as np
import tkinter as tk
import os

class Save_load_pop_up(tk.Tk):
    def __init__(self, save_or_load, window_x = 0, window_y = 0, game_board = None):
        super().__init__()
        self.title(f'{save_or_load} file')
        self.geometry("300x300")
        self.geometry(f'+{window_x+100}+{window_y}')
        self.saved_games = os.listdir('saved_games')
        self.saved_games.sort()
        self.save_or_load = save_or_load
        if save_or_load == 'Save':
            self.game_board = game_board
            self.save()
        else:
            self.loaded = False
            self.game_board = np.zeros((2,4,4))
            self.load()

    def save(self):
        self.save_frame = tk.Frame(self)
        self.save_frame.pack(fill = 'both', expand = True)
        enter_frame = tk.Frame(self.save_frame)
        enter_frame.pack(fill = 'x')
        save_as_message = tk.Label(enter_frame, text = 'Save As:')
        save_as_message.pack(fill = 'x', side = 'left')
        self.file_name = tk.StringVar(self.save_frame)
        enter_name = tk.Entry(enter_frame, textvariable = self.file_name)
        enter_name.pack(padx = 5, fill = 'x', expand = True, side = 'left')
        save_button = tk.Button(enter_frame, text = 'Save', command = lambda : self.save_press())
        save_button.pack(fill = 'x', side = 'right')
        in_use_message = tk.Label(self.save_frame, text = 'Currently Used:')
        in_use_message.pack(fill = 'x')
        list_frame = tk.Frame(self.save_frame)
        tk.Label(list_frame, text = '').pack(side='left', padx = 10)
        tk.Label(list_frame, text = '').pack(side = 'right', padx = 10)
        list_frame.pack(fill = 'both', expand = True)
        files_scroll_bar = tk.Scrollbar(list_frame)
        files_scroll_bar.pack(side = tk.RIGHT, fill = tk.Y)
        list_in_use = tk.Listbox(list_frame, yscrollcommand = files_scroll_bar.set)
        for file_name in self.saved_games:
            list_in_use.insert(tk.END,file_name[:-4])
        list_in_use.pack(side = tk.LEFT, fill = tk.BOTH, expand = True)
        tk.Label(self.save_frame, text = '').pack(fill = 'x', side = 'bottom')
        files_scroll_bar.config(command = list_in_use.yview)
        list_in_use.bind('<<ListboxSelect>>', self.list_box_single_press)
        list_in_use.bind('<Double-Button-1>', self.list_box_double_press)

    def list_box_single_press(self, event):
        list_box = event.widget
        index = int(list_box.curselection()[0])
        value = list_box.get(index)
        self.file_name.set(value)

    def list_box_double_press(self, event):
        list_box = event.widget
        index = int(list_box.curselection()[0])
        value = list_box.get(index)
        self.file_name.set(value)
        if self.save_or_load == 'Save':
            self.save_press(from_save_pop_up = False)
        else:
            self.load_press()

    def save_press(self, from_save_pop_up = False):
        file_name = self.file_name.get()
        if file_name != '':
            if file_name in self.saved_games or file_name+'.npy' in self.saved_games:
                if from_save_pop_up:
                    np.save(f'saved_games/{file_name}', self.game_board)
                    self.file_in_use.destroy()
                    self.destroy()
                else:
                    root_x = self.winfo_rootx()
                    root_y = self.winfo_rooty()
                    self.file_in_use = tk.Tk()
                    self.file_in_use.title('Warning!')
                    self.file_in_use.geometry('300x100')
                    self.file_in_use.geometry(f'+{root_x+100}+{root_y+100}')
                    name_in_use_message = tk.Label(self.file_in_use,font = ('DejaVu Sans',12), text = 'File name in use, overwrite?')
                    name_in_use_message.pack(fill = 'both', expand = True)
                    button_frame = tk.Frame(self.file_in_use)
                    button_frame.pack(fill = 'both',expand = True)
                    yes_button = tk.Button(button_frame,  text = 'Yes', command = lambda: self.save_press(True))
                    yes_button.grid(row = 0, column = 1, sticky = 'NSEW')
                    no_button = tk.Button(button_frame,  text = 'No', command = lambda: self.file_in_use.destroy())
                    no_button.grid(row = 0, column = 3, sticky = 'NSEW')
                    button_frame.columnconfigure(0, weight = 1)
                    button_frame.columnconfigure(1, weight = 2)
                    button_frame.columnconfigure(2, weight = 1)
                    button_frame.columnconfigure(3, weight = 2)
                    button_frame.columnconfigure(4, weight = 1)
            else:
                np.save(f'saved_games/{file_name}', self.game_board)
                self.destroy()

    def load(self):
        self.load_frame = tk.Frame(self)
        self.load_frame.pack(fill = 'both', expand = True)
        select_message = tk.Label(self.load_frame,font = ('DejaVu Sans',12), text = 'Select a File:')
        select_message.pack(fill = 'x')
        tk.Label(self.load_frame, text = '').pack(fill = 'x')
        list_frame = tk.Frame(self.load_frame)
        tk.Label(list_frame, text = '').pack(side = 'left', padx = 10)
        tk.Label(list_frame, text = '').pack(side = 'right', padx = 10)
        list_frame.pack(fill = 'both', expand = True)
        files_scroll_bar = tk.Scrollbar(list_frame)
        files_scroll_bar.pack(side = tk.RIGHT, fill = tk.Y)
        list_in_use = tk.Listbox(list_frame, yscrollcommand = files_scroll_bar.set)
        for file_name in self.saved_games:
            list_in_use.insert(tk.END, file_name[:-4])
        list_in_use.pack(side = tk.LEFT, fill = tk.BOTH, expand = True)
        tk.Label(self.load_frame, text = '').pack(fill = 'x')
        files_scroll_bar.config(command = list_in_use.yview)
        list_in_use.bind('<<ListboxSelect>>', self.list_box_single_press)
        list_in_use.bind('<Double-Button-1>', self.list_box_double_press)
        enter_frame = tk.Frame(self.load_frame)
        enter_frame.pack(fill = 'x')
        current_selection_message = tk.Label(enter_frame, text = 'Selected:')
        current_selection_message.pack(fill = 'x', side = 'left')
        self.file_name = tk.StringVar(self.load_frame)
        selection_name = tk.Entry(enter_frame, textvariable = self.file_name)
        selection_name.pack(padx = 5, fill = 'x', expand = True, side = 'left')
        load_button = tk.Button(enter_frame, width = 10, text = 'Load', command = lambda:self.load_press())
        load_button.pack(fill = 'x', side = 'right')
        tk.Label(self.load_frame, text = '').pack(fill = 'x')

    def load_press(self):
        file_name = self.file_name.get()
        self.game_board = np.load(f'saved_games/{file_name}.npy')
        self.loaded = True
        self.destroy()

if __name__ == '__main__':
    easy = np.array([
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
    to_save = np.zeros((2, 9, 9))

    to_save[0] = easy
    test = Save_load_pop_up('Load',window_x = 2500, window_y = 300, game_board = to_save)
    test.mainloop()