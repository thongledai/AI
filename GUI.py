import tkinter as tk
import copy 
from tkinter import ttk, messagebox
from Support_Functions.SupportFunctions import *
from Algorithms_8Puzzle.UninformedSearch.BreadthFirstSearch                  import BFS
from Algorithms_8Puzzle.UninformedSearch.DepthFirstSearch                    import DFS
from Algorithms_8Puzzle.UninformedSearch.IterativeDeepeningSearch            import IDS
from Algorithms_8Puzzle.UninformedSearch.UniformCostSearch                   import UCS
from Algorithms_8Puzzle.InformedSearch.GreedySearch                          import GS
from Algorithms_8Puzzle.InformedSearch.AStar                                 import AStar
from Algorithms_8Puzzle.InformedSearch.IterativeDeepeningAStar               import IDAStar
from Algorithms_8Puzzle.LocalSearch.HillClimbing.SimpleHillClimbing          import SHC as SimpleHC
from Algorithms_8Puzzle.LocalSearch.HillClimbing.SteepestAscentHillClimbing  import SAHC
from Algorithms_8Puzzle.LocalSearch.HillClimbing.StochasticHillClimbing      import SHC as StochasticHC
from Algorithms_8Puzzle.LocalSearch.HillClimbing.RandomRestartHillClimbing   import RRHC
from Algorithms_8Puzzle.LocalSearch.LocalBeamSearch                          import LBS
from Algorithms_8Puzzle.LocalSearch.SimulatedAnnealing                       import SA
class PuzzleGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("8-Puzzle Solver")
        self.root.geometry('950x600+250+200')
        self.root.configure(bg='#f4f4f4')

        # danh sách các trạng thái ma trận
        self.current_states_list = []
        self.current_index = 0
        self.path_actions = []

        self.setup_styles()
        self.create_widgets()
        self.handle_reset()

    def setup_styles(self):
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TCombobox', fieldbackground='white', background='#e0e0e0', font=('Arial', 12))

    # chọn thuật toán
    def create_widgets(self):
        
        top_frame = tk.Frame(self.root, bg='#f4f4f4')
        top_frame.pack(side=tk.TOP, fill=tk.X, padx=40, pady=20)

        lbl_algo = tk.Label(top_frame, text="Chọn thuật toán:", font=('Arial', 13, 'bold'), bg='#f4f4f4', fg='#333333')
        lbl_algo.pack(side=tk.LEFT, padx=5)

        algorithms = [
            "Bread First Search",
            "Depth First Search",
            "Iterative Deepening Search",
            "Uniform Cost Search",
            "Greedy Search",
            "A*",
            "IDA*",
            "Simple Hill Climbing",
            "Steepest Ascent Hill Climbing",
            "Stochastic Hill Climbing",
            "Random Restart Hill Climbing",
            "Local Beam Search",
            "Simulated Annealing"
        ]

        max_width = max(len(x) for x in algorithms)

        self.algo_box = ttk.Combobox(
            top_frame,
            values=algorithms,
            state="readonly",
            width=max_width
        )
        self.algo_box.configure(height=15)
        self.algo_box.current(0)
        self.algo_box.pack(side=tk.LEFT, padx=10)

        # hiển thị ma trận
        matrix_container = tk.Frame(self.root, bg='#7f8c8d', bd=4, relief="ridge")
        matrix_container.place(x=150, y=100, width=360, height=360)

        self.matrix_entries = [[None for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                entry = tk.Entry(matrix_container, font=('Arial', 28, 'bold'), justify='center',
                                 bg='white', fg='#2c3e50', bd=1, relief="solid")
                entry.grid(row=i, column=j, padx=4, pady=4, sticky="nsew")
                matrix_container.rowconfigure(i, weight=1)
                matrix_container.columnconfigure(j, weight=1)
                self.matrix_entries[i][j] = entry

        # bảng điều khiển
        btn_frame = tk.Frame(self.root, bg='#e0e0e0', bd=2, relief="groove")
        btn_frame.place(x=620, y=100, width=220, height=360)

        lbl_control = tk.Label(btn_frame, text="BẢNG ĐIỀU KHIỂN", font=('Arial', 11, 'bold'), bg='#e0e0e0', fg='#555555')
        lbl_control.pack(fill=tk.X, pady=10)

        buttons_config = [
            ("Random", self.handle_random),
            ("Execute", self.handle_execute),
            ("Next Step", self.handle_next),
            ("Last Step", self.handle_last),
            ("Reset", self.handle_reset)
        ]

        for text, command in buttons_config:
            bg_color = '#bdc3c7' 
            fg_color = 'black'
            
            btn = tk.Button(btn_frame, text=text, font=('Arial', 12, 'bold'), bg=bg_color, fg=fg_color,
                            activebackground='#95a5a6', relief="raised", bd=2, command=command)
            btn.pack(fill=tk.X, padx=15, pady=8, ipady=4)

        # path, cost
        info_frame = tk.Frame(self.root, bg='#f4f4f4')
        info_frame.place(x=50, y=490, width=900, height=120)

        lbl_path = tk.Label(info_frame, text="Path:", font=('Arial', 13, 'bold'), bg='#f4f4f4', fg='#333333')
        lbl_path.grid(row=0, column=0, sticky=tk.W, pady=5)
        
        self.entry_path = tk.Entry(info_frame, font=('Arial', 12), bg='white', fg='black', bd=2, relief="sunken")
        self.entry_path.grid(row=0, column=1, sticky="ew", padx=10, pady=5)
        self.entry_path.config(state=tk.DISABLED)

        lbl_cost = tk.Label(info_frame, text="Cost:", font=('Arial', 13, 'bold'), bg='#f4f4f4', fg='#333333')
        lbl_cost.grid(row=1, column=0, sticky=tk.W, pady=5)

        self.entry_cost = tk.Entry(info_frame, font=('Arial', 12), bg='white', fg='#c0392b', bd=2, relief="sunken", width=15)
        self.entry_cost.grid(row=1, column=1, sticky=tk.W, padx=10, pady=5)
        self.entry_cost.config(state=tk.DISABLED)

        info_frame.columnconfigure(1, weight=1)

    # đọc xuất ma trận
    # tự nhập
    def get_state_from_gui(self):
        
        state = []
        for i in range(3):
            row = []
            for j in range(3):
                val = self.matrix_entries[i][j].get().strip()
                if val == "" or val == "0":
                    row.append(0)
                else:
                    try:
                        row.append(int(val))
                    except ValueError:
                        return None
            state.append(row)
        return state

    def update_gui_matrix(self, state):
        for i in range(3):
            for j in range(3):
                val = state[i][j]
                self.matrix_entries[i][j].config(state=tk.NORMAL)
                self.matrix_entries[i][j].delete(0, tk.END)
                if val == 0:
                    self.matrix_entries[i][j].insert(0, "")
                    self.matrix_entries[i][j].config(bg='#e0e0e0')
                else:
                    self.matrix_entries[i][j].insert(0, str(val))
                    self.matrix_entries[i][j].config(bg='white')

    def update_info_fields(self, path_text, cost_text):
        for entry, text in [(self.entry_path, path_text), (self.entry_cost, cost_text)]:
            entry.config(state=tk.NORMAL)
            entry.delete(0, tk.END)
            entry.insert(0, text)
            entry.config(state=tk.DISABLED)

    def validate_matrix(self, state):
        if not state: return False
        flat_list = [cell for row in state for cell in row]
        return sorted(flat_list) == list(range(9))

    # xử lý nút
    def handle_random(self): # tạo ma trận random
        random_state = random_start()
        self.current_states_list = [random_state]
        self.current_index = 0
        self.path_actions = []
        self.update_gui_matrix(random_state)
        self.update_info_fields("", "")

    def handle_execute(self):
        current_input = self.get_state_from_gui()
        
        if not self.validate_matrix(current_input):
            messagebox.showerror("Ma trận không hợp lệ!", "Vui lòng nhập đủ các số từ 1-8 và 1 ô trống.")
            return

        algo = self.algo_box.get()
        self.update_info_fields("Searching...", "Calculating...")
        self.root.update()

        try:
            if algo == "Bread First Search":
                result = BFS(current_input, goal)
            elif algo == "Depth First Search":
                result = DFS(current_input, goal)
            elif algo == "Iterative Deepening Search":
                result = IDS(current_input, goal)
            elif algo == "Uniform Cost Search":
                result = UCS(current_input, goal)
            elif algo == "Greedy Search":
                result = GS(current_input, goal)
            elif algo == "A*":
                result = AStar(current_input, goal)
            elif algo == "IDA*":
                result = IDAStar(current_input, goal)
            elif algo == "Simple Hill Climbing":
                result = SimpleHC(current_input, goal)
            elif algo == "Steepest Ascent Hill Climbing":
                result = SAHC(current_input, goal)
            elif algo == "Stochastic Hill Climbing":
                result = StochasticHC(current_input, goal)
            elif algo == "Random Restart Hill Climbing":
                result = RRHC(current_input, goal)
            elif algo == "Local Beam Search":
                result = LBS(current_input, goal)
            elif algo == "Simulated Annealing":
                result = SA(current_input, goal)
        except Exception as e:
            messagebox.showerror(
                "Lỗi Cấu Trúc File",
                f"Không thể chạy thuật toán:\n\n{type(e).__name__}: {str(e)}"
            )
            self.update_info_fields("Error", "N/A")
            print(type(e).__name__, ":", e)
            return


        # Xử lý kết quả
        if result is None:
            self.update_info_fields("Failure", "N/A")
            return

        if isinstance(result, tuple):
            path, cost = result

            if path == "failure":
                self.update_info_fields("Failure", "N/A")
                self.current_states_list = [current_input]
                self.current_index = 0
                self.path_actions = []
                return
        else:
            self.update_info_fields("Failure", "N/A")
            return

        # Lưu danh sách hành động
        self.path_actions = path
        self.current_states_list = [current_input]
        
        # Dựng chuỗi ma trận di chuyển qua từng bước
        temp_state = copy.deepcopy(current_input)
        for action in path:
            temp_state = child_state(temp_state, action)
            self.current_states_list.append(temp_state)

        self.current_index = 0
        self.update_gui_matrix(self.current_states_list[self.current_index])
        
        # In chuỗi hành động ra ô Path và hiển thị Cost thực tế
        path_str = " - ".join(path) if path else "Goal!"
        self.update_info_fields(path_str, str(cost))

    def handle_next(self):
        if not self.current_states_list: return
        if self.current_index < len(self.current_states_list) - 1:
            self.current_index += 1
            self.update_gui_matrix(self.current_states_list[self.current_index])
            if self.path_actions:
                path_str = " - ".join(self.path_actions)
                self.update_info_fields(path_str, f" {self.current_index} / {len(self.path_actions)}")

    def handle_last(self):
        if not self.current_states_list: return
        if self.current_index > 0:
            self.current_index -= 1
            self.update_gui_matrix(self.current_states_list[self.current_index])
            if self.path_actions:
                path_str = " - ".join(self.path_actions)
                self.update_info_fields(path_str, f" {self.current_index} / {len(self.path_actions)}")

    def handle_reset(self):
        self.current_states_list = []
        self.current_index = 0
        self.path_actions = []
        for i in range(3):
            for j in range(3):
                self.matrix_entries[i][j].config(state=tk.NORMAL)
                self.matrix_entries[i][j].delete(0, tk.END)
                self.matrix_entries[i][j].config(bg='white')
        self.update_info_fields("", "")