# Giao diện đồ họa hiển thị và điều khiển trò chơi Caro 3x3.
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import threading
import time

import Utils
import Minimax
import AlphaBeta
import Expectimax

class CaroGUI:
    def __init__(self, root):
        self.root = root
        
        self.board = (None,) * 9
        self.algorithm = "Minimax"
        self.game_over_announced = False
        
        self.root.title("Caro")
        self.root.geometry("400x420+500+220")
        self.root.resizable(False, False)
        self.root.configure(bg="#F8F9FA")
        
        self.font_cell = ("Segoe UI", 28, "bold")
        self.font_button = ("Segoe UI", 10, "bold")
        
        self.color_bg = "#F8F9FA"          
        self.color_panel = "#FFFFFF"       
        self.color_grid_line = "#DEE2E6"   
        self.color_cell_empty = "#FFFFFF"  
        self.color_cell_hover = "#F1F3F5"  
        self.color_cell_active = "#E9ECEF" 
        self.color_text_dark = "#212529"   
        self.color_text_muted = "#868E96"  
        self.color_btn_bg = "#E9ECEF"      
        self.color_btn_hover = "#DEE2E6"   
        
        self.create_header()
        self.create_board()
        
        self.update_ui()
        self.root.after(300, self.trigger_ai_move)

    def create_header(self):
        header_frame = tk.Frame(self.root, bg=self.color_panel, bd=0, height=60)
        header_frame.pack(fill=tk.X, side=tk.TOP)
        header_frame.pack_propagate(False)
        
        algo_label = tk.Label(
            header_frame, 
            text="Algorithms:", 
            font=("Segoe UI", 10, "bold"), 
            bg=self.color_panel, 
            fg=self.color_text_dark
        )
        algo_label.pack(side=tk.LEFT, padx=(15, 5), pady=15)
        
        self.algo_combobox = ttk.Combobox(
            header_frame, 
            values=["Minimax", "AlphaBeta", "Expectimax"], 
            state="readonly",
            font=("Segoe UI", 10),
            width=12
        )
        self.algo_combobox.set(self.algorithm)
        self.algo_combobox.pack(side=tk.LEFT, padx=5, pady=15)
        self.algo_combobox.bind("<<ComboboxSelected>>", self.on_algorithm_change)
        
        self.restart_btn = tk.Button(
            header_frame,
            text="Play",
            font=self.font_button,
            bg="#BBBBBB",
            fg="#000000",
            activebackground="#BBBBBB",
            activeforeground="#000000",
            bd=0,
            relief=tk.FLAT,
            padx=15,
            pady=4,
            command=self.on_restart_click
        )
        self.restart_btn.pack(side=tk.RIGHT, padx=15, pady=15)
        
        self.restart_btn.bind("<Enter>", lambda e: self.restart_btn.config(bg="#B0B0B0"))
        self.restart_btn.bind("<Leave>", lambda e: self.restart_btn.config(bg="#E0E0E0"))

    def create_board(self):
        self.grid_frame = tk.Frame(self.root, bg=self.color_grid_line, bd=0)
        self.grid_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)
        
        for i in range(3):
            self.grid_frame.columnconfigure(i, weight=1, uniform="grid")
            self.grid_frame.rowconfigure(i, weight=1, uniform="grid")
            
        self.buttons = []
        for i in range(9):
            row = i // 3
            col = i % 3
            
            btn = tk.Button(
                self.grid_frame,
                text="",
                font=self.font_cell,
                bg=self.color_cell_empty,
                activebackground=self.color_cell_active,
                bd=0,
                relief=tk.FLAT,
                command=lambda index=i: self.on_cell_click(index)
            )
            btn.grid(row=row, column=col, padx=1, pady=1, sticky="nsew")
            
            btn.bind("<Enter>", lambda e, b=btn: self.on_cell_enter(b))
            btn.bind("<Leave>", lambda e, b=btn: self.on_cell_leave(b))
            
            self.buttons.append(btn)

    def on_algorithm_change(self, event):
        self.algorithm = self.algo_combobox.get()

    def on_cell_enter(self, btn):
        if btn["text"] == "" and not self.is_game_over() and self.get_current_player() == 'O':
            btn.config(bg=self.color_cell_hover)

    def on_cell_leave(self, btn):
        if btn["text"] == "":
            btn.config(bg=self.color_cell_empty)

    def set_board_state(self, disabled=True):
        state = tk.DISABLED if disabled else tk.NORMAL
        for btn in self.buttons:
            if btn["text"] == "":
                btn.config(state=state)

    def get_current_player(self):
        x_count = self.board.count('X')
        o_count = self.board.count('O')
        return 'X' if x_count == o_count else 'O'

    def make_move(self, action):
        if action in Utils.actions(self.board):
            self.board = Utils.result(self.board, action)
            return True
        return False

    def is_game_over(self):
        return Utils.is_terminal(self.board)

    def get_winner(self):
        val = Utils.utility(self.board)
        if val == 1:
            return 'X'
        elif val == -1:
            return 'O'
        elif self.is_game_over():
            return 'Draw'
        return None

    def get_ai_move(self):
        state = self.board
        available_actions = Utils.actions(state)
        if not available_actions:
            return None

        best_score = float('-inf')
        best_move = None

        for action in available_actions:
            next_state = Utils.result(state, action)
            depth = len(Utils.actions(next_state))

            if self.algorithm == "Minimax":
                score = Minimax.minimax(next_state, depth, False)
            elif self.algorithm == "AlphaBeta":
                score = AlphaBeta.alpha_beta_minimax(next_state, depth, float('-inf'), float('inf'), False)
            elif self.algorithm == "Expectimax":
                score = Expectimax.expectima(next_state, depth, False)
            else:
                score = 0

            if score > best_score:
                best_score = score
                best_move = action
                

        return best_move

    def update_ui(self):
        for i, val in enumerate(self.board):
            btn = self.buttons[i]
            if val is not None:
                btn.config(
                    text=val, 
                    state=tk.DISABLED, 
                    bg=self.color_cell_empty, 
                    disabledforeground=self.color_text_dark
                )
            else:
                btn.config(text="", state=tk.NORMAL, bg=self.color_cell_empty)
                
        if self.is_game_over():
            self.set_board_state(disabled=True)

    def trigger_ai_move(self):
        if self.is_game_over() or self.get_current_player() != 'X':
            return
            
        self.set_board_state(disabled=True)
        
        def run():
            time.sleep(0.2)
            ai_move = self.get_ai_move()
            self.root.after(0, lambda: self.apply_ai_move(ai_move))
            
        threading.Thread(target=run, daemon=True).start()

    def apply_ai_move(self, move):
        if move is not None:
            self.make_move(move)
        self.update_ui()
        self.set_board_state(disabled=False)
        if self.is_game_over():
            self.announce_result()

    def on_cell_click(self, index):
        if self.is_game_over() or self.get_current_player() != 'O':
            return
            
        if self.make_move(index):
            self.update_ui()
            if not self.is_game_over():
                self.trigger_ai_move()

    def on_restart_click(self):
        self.board = (None,) * 9
        self.update_ui()
        self.root.after(300, self.trigger_ai_move)
