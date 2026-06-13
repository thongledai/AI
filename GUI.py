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
from Algorithms_8Puzzle.LocalSearch.HillClimbing.SimpleHillClimbing          import SHC         as SimpleHC
from Algorithms_8Puzzle.LocalSearch.HillClimbing.SteepestAscentHillClimbing  import SAHC
from Algorithms_8Puzzle.LocalSearch.HillClimbing.StochasticHillClimbing      import SHC         as StochasticHC
from Algorithms_8Puzzle.LocalSearch.HillClimbing.RandomRestartHillClimbing   import RRHC
from Algorithms_8Puzzle.LocalSearch.LocalBeamSearch                          import LBS
from Algorithms_8Puzzle.LocalSearch.SimulatedAnnealing                       import SA
from Algorithms_8Puzzle.Stochastic.AndOrGraphSearch                          import AOGS
from Algorithms_8Puzzle.PartiallyObservable.BeliefStateSearch                import BSS         as PBSS, INITIAL_BELIEF as PBSS_BELIEF
from Algorithms_8Puzzle.Unobservable.BeliefStateSearch                       import BSS         as UBSS, INITIAL_BELIEF as UBSS_BELIEF


class PuzzleGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("8-Puzzle Solver")
        self.root.geometry('950x600+250+200')
        self.root.configure(bg='#f4f4f4')

        self.current_states_list = []
        self.current_index = 0
        self.path_actions = []

        # BSS: danh sách từng bước cho cả 2 bảng
        self.bss_states_1 = []
        self.bss_states_2 = []
        self.bss_index = 0

        self.setup_styles()
        self.create_widgets()
        self.handle_reset()

    def setup_styles(self):
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TCombobox', fieldbackground='white', background='#e0e0e0', font=('Arial', 12))

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
            "Simulated Annealing",
            "And-Or Graph Search",
            "Partially Observable BSS",
            "Unobservable BSS",
        ]

        max_width = max(len(x) for x in algorithms)

        self.algo_box = ttk.Combobox(
            top_frame,
            values=algorithms,
            state="readonly",
            width=max_width
        )
        self.algo_box.configure(height=len(algorithms))
        self.algo_box.current(0)
        self.algo_box.pack(side=tk.LEFT, padx=10)
        self.algo_box.bind("<<ComboboxSelected>>", self._on_algo_change)

        # bảng đơn (chế độ thường)
        self.matrix_container = tk.Frame(self.root, bg='#7f8c8d', bd=4, relief="ridge")
        self.matrix_container.place(x=150, y=100, width=360, height=360)

        self.matrix_entries = [[None for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                entry = tk.Entry(self.matrix_container, font=('Arial', 28, 'bold'), justify='center',
                                 bg='white', fg='#2c3e50', bd=1, relief="solid")
                entry.grid(row=i, column=j, padx=4, pady=4, sticky="nsew")
                self.matrix_container.rowconfigure(i, weight=1)
                self.matrix_container.columnconfigure(j, weight=1)
                self.matrix_entries[i][j] = entry

        # 2 bảng BSS (ẩn mặc định)
        self._create_bss_matrices()

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
            btn = tk.Button(btn_frame, text=text, font=('Arial', 12, 'bold'), bg='#bdc3c7', fg='black',
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

    def _create_bss_matrices(self):
        # 2 bảng BSS đặt cạnh nhau, căn giữa vùng 620px
        self.bss_frame = tk.Frame(self.root, bg='#f4f4f4')
        self.bss_frame.place(x=20, y=100, width=590, height=380)
        self.bss_frame.place_forget()

        lbl1 = tk.Label(self.bss_frame, text="State 1", font=('Arial', 11, 'bold'), bg='#f4f4f4', fg='#2c3e50')
        lbl1.place(x=115, y=0)

        self.bss_container_1 = tk.Frame(self.bss_frame, bg='#7f8c8d', bd=4, relief="ridge")
        self.bss_container_1.place(x=10, y=25, width=265, height=265)

        lbl2 = tk.Label(self.bss_frame, text="State 2", font=('Arial', 11, 'bold'), bg='#f4f4f4', fg='#2c3e50')
        lbl2.place(x=420, y=0)

        self.bss_container_2 = tk.Frame(self.bss_frame, bg='#7f8c8d', bd=4, relief="ridge")
        self.bss_container_2.place(x=315, y=25, width=265, height=265)

        self.bss_entries_1 = [[None]*3 for _ in range(3)]
        self.bss_entries_2 = [[None]*3 for _ in range(3)]

        for i in range(3):
            for j in range(3):
                e1 = tk.Entry(self.bss_container_1, font=('Arial', 20, 'bold'), justify='center',
                              bg='white', fg='#2c3e50', bd=1, relief="solid")
                e1.grid(row=i, column=j, padx=3, pady=3, sticky="nsew")
                self.bss_container_1.rowconfigure(i, weight=1)
                self.bss_container_1.columnconfigure(j, weight=1)
                self.bss_entries_1[i][j] = e1

                e2 = tk.Entry(self.bss_container_2, font=('Arial', 20, 'bold'), justify='center',
                              bg='white', fg='#2c3e50', bd=1, relief="solid")
                e2.grid(row=i, column=j, padx=3, pady=3, sticky="nsew")
                self.bss_container_2.rowconfigure(i, weight=1)
                self.bss_container_2.columnconfigure(j, weight=1)
                self.bss_entries_2[i][j] = e2

    def _is_bss_mode(self):
        algo = self.algo_box.get()
        return algo in ("Partially Observable BSS", "Unobservable BSS")

    def _on_algo_change(self, event=None):
        if self._is_bss_mode():
            self.matrix_container.place_forget()
            self.bss_frame.place(x=20, y=100, width=590, height=380)
            belief = PBSS_BELIEF if self.algo_box.get() == "Partially Observable BSS" else UBSS_BELIEF
            self._update_bss_matrices(belief[0], belief[1])
        else:
            self.bss_frame.place_forget()
            self.matrix_container.place(x=150, y=100, width=360, height=360)

    # đọc/ghi ma trận đơn
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

    def _update_bss_matrix_widget(self, entries, state):
        for i in range(3):
            for j in range(3):
                val = state[i][j]
                entries[i][j].config(state=tk.NORMAL)
                entries[i][j].delete(0, tk.END)
                if val == 0:
                    entries[i][j].insert(0, "")
                    entries[i][j].config(bg='#e0e0e0')
                else:
                    entries[i][j].insert(0, str(val))
                    entries[i][j].config(bg='white')

    def _update_bss_matrices(self, state1, state2):
        self._update_bss_matrix_widget(self.bss_entries_1, state1)
        self._update_bss_matrix_widget(self.bss_entries_2, state2)

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

    def handle_random(self):
        if self._is_bss_mode():
            belief = PBSS_BELIEF if self.algo_box.get() == "Partially Observable BSS" else UBSS_BELIEF
            self._update_bss_matrices(belief[0], belief[1])
            self.update_info_fields("", "")
            self.bss_states_1 = []
            self.bss_states_2 = []
            self.bss_index = 0
            return

        random_state = random_start()
        self.current_states_list = [random_state]
        self.current_index = 0
        self.path_actions = []
        self.update_gui_matrix(random_state)
        self.update_info_fields("", "")

    def handle_execute(self):
        algo = self.algo_box.get()
        self.update_info_fields("Searching...", "Calculating...")
        self.root.update()

        if self._is_bss_mode():
            self._execute_bss(algo)
            return

        current_input = self.get_state_from_gui()
        if not self.validate_matrix(current_input):
            messagebox.showerror("Ma trận không hợp lệ!", "Vui lòng nhập đủ các số từ 1-8 và 1 ô trống.")
            return

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
            elif algo == "And-Or Graph Search":
                result = AOGS(current_input, goal)
            else:
                result = None
        except Exception as e:
            messagebox.showerror(
                "Lỗi Cấu Trúc File",
                f"Không thể chạy thuật toán:\n\n{type(e).__name__}: {str(e)}"
            )
            self.update_info_fields("Error", "N/A")
            print(type(e).__name__, ":", e)
            return

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

        self.path_actions = path
        self.current_states_list = [current_input]

        temp_state = copy.deepcopy(current_input)
        for action in path:
            temp_state = child_state(temp_state, action)
            self.current_states_list.append(temp_state)

        self.current_index = 0
        self.update_gui_matrix(self.current_states_list[self.current_index])

        path_str = " - ".join(path) if path else "Goal!"
        self.update_info_fields(path_str, str(cost))

    def _execute_bss(self, algo):
        try:
            result = PBSS() if algo == "Partially Observable BSS" else UBSS()
        except Exception as e:
            messagebox.showerror(
                "Lỗi Cấu Trúc File",
                f"Không thể chạy thuật toán:\n\n{type(e).__name__}: {str(e)}"
            )
            self.update_info_fields("Error", "N/A")
            print(type(e).__name__, ":", e)
            return

        if not isinstance(result, tuple) or result[0] == "failure":
            self.update_info_fields("Failure", "N/A")
            return

        path, cost = result
        belief = PBSS_BELIEF if algo == "Partially Observable BSS" else UBSS_BELIEF

        # xây dựng danh sách từng bước cho 2 state
        s1 = copy.deepcopy(belief[0])
        s2 = copy.deepcopy(belief[1])
        self.bss_states_1 = [copy.deepcopy(s1)]
        self.bss_states_2 = [copy.deepcopy(s2)]

        from Support_Functions.SupportFunctions import get_actions, child_state as cs
        for action in path:
            s1 = cs(s1, action) if action in get_actions(s1) else [row[:] for row in s1]
            s2 = cs(s2, action) if action in get_actions(s2) else [row[:] for row in s2]
            self.bss_states_1.append(copy.deepcopy(s1))
            self.bss_states_2.append(copy.deepcopy(s2))

        self.path_actions = path
        self.bss_index = 0
        self._update_bss_matrices(self.bss_states_1[0], self.bss_states_2[0])

        path_str = " - ".join(path) if path else "Goal!"
        self.update_info_fields(path_str, str(cost))

    def handle_next(self):
        if self._is_bss_mode():
            if self.bss_states_1 and self.bss_index < len(self.bss_states_1) - 1:
                self.bss_index += 1
                self._update_bss_matrices(self.bss_states_1[self.bss_index], self.bss_states_2[self.bss_index])
                if self.path_actions:
                    self.update_info_fields(
                        " - ".join(self.path_actions),
                        f" {self.bss_index} / {len(self.path_actions)}"
                    )
            return

        if not self.current_states_list: return
        if self.current_index < len(self.current_states_list) - 1:
            self.current_index += 1
            self.update_gui_matrix(self.current_states_list[self.current_index])
            if self.path_actions:
                self.update_info_fields(
                    " - ".join(self.path_actions),
                    f" {self.current_index} / {len(self.path_actions)}"
                )

    def handle_last(self):
        if self._is_bss_mode():
            if self.bss_states_1 and self.bss_index > 0:
                self.bss_index -= 1
                self._update_bss_matrices(self.bss_states_1[self.bss_index], self.bss_states_2[self.bss_index])
                if self.path_actions:
                    self.update_info_fields(
                        " - ".join(self.path_actions),
                        f" {self.bss_index} / {len(self.path_actions)}"
                    )
            return

        if not self.current_states_list: return
        if self.current_index > 0:
            self.current_index -= 1
            self.update_gui_matrix(self.current_states_list[self.current_index])
            if self.path_actions:
                self.update_info_fields(
                    " - ".join(self.path_actions),
                    f" {self.current_index} / {len(self.path_actions)}"
                )

    def handle_reset(self):
        self.current_states_list = []
        self.current_index = 0
        self.path_actions = []
        self.bss_states_1 = []
        self.bss_states_2 = []
        self.bss_index = 0

        for i in range(3):
            for j in range(3):
                self.matrix_entries[i][j].config(state=tk.NORMAL)
                self.matrix_entries[i][j].delete(0, tk.END)
                self.matrix_entries[i][j].config(bg='white')

        self.update_info_fields("", "")

        if self._is_bss_mode():
            belief = PBSS_BELIEF if self.algo_box.get() == "Partially Observable BSS" else UBSS_BELIEF
            self._update_bss_matrices(belief[0], belief[1])