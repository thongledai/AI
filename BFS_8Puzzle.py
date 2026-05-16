import random
from collections import deque

class Node:
    def __init__(self, state, parent=None, action=None, path_cost=0):
        self.state = state  # Ma trận 3x3
        self.parent = parent
        self.action = action
        self.path_cost = path_cost

    def show_state(self):
        for row in self.state:
            print(row)
        print()

    def __eq__(self, other):
        return self.state == other.state


def get_empty(state):
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                return i, j

def get_actions(state):
    x, y = get_empty(state)
    actions = []
    if x < 2: actions.append('D')
    if x > 0: actions.append('U')
    if y < 2: actions.append('R')
    if y > 0: actions.append('L')
    return actions

mapping = { 'D': (1, 0), 
            'U': (-1, 0), 
            'R': (0, 1), 
            'L': (0, -1)}

def swap(a, b):
    return b, a

# Hàm tạo state con
def child_state(state, action):
    # Sao chép ma trận
    new_state = [row[:] for row in state]
    x, y = get_empty(state)
    
    dx, dy = mapping[action]
    new_x, new_y = x + dx, y + dy
    
    # Hoán đổi vị trí
    new_state[x][y], new_state[new_x][new_y] = swap(new_state[x][y], new_state[new_x][new_y])
    return new_state

goal = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 0]
]

def goal_test(state):
    return state == goal

# Lấy đường đi từ star đến goal
def solution(node):
    path = []
    n = node
    while n.parent:
        path.append(n.action)
        n = n.parent
    return path[::-1]

# Bread First Search
def BFS(star):
    node = Node(state=star)
    
    if goal_test(node.state):
        return solution(node)
    
    # frontier dùng FIFO
    frontier = deque([node])

    # các node.state cần xét
    frontier_set=set()
    frontier_set.add(tuple(map(tuple, node.state)))

    
    # các node.state đã xét
    explored = set()
    
    while frontier:
        node = frontier.popleft()

        state_parent = tuple(map(tuple, node.state))
        explored.add(state_parent)
        frontier_set.discard(state_parent)

        # Random các action
        actions = random.sample(get_actions(node.state), len(get_actions(node.state)))
        
        for action in actions:
            child = Node(state=child_state(node.state, action), 
                         parent=node, 
                         action=action, 
                         path_cost=node.path_cost + 1)
            state_child = tuple(map(tuple, child.state))
            if state_child not in explored and state_child not in frontier_set:               
                if goal_test(child.state):
                    return solution(child)
                else:
                    frontier.append(child)
                    frontier_set.add(state_child)

    return "failure"

# In mảng
def output(a):
    for row in a:
        print(*(row))
    print()

# Tạo mảng random
def random_start():
    nums = list(range(9))
    random.shuffle(nums)
    return [nums[0:3], nums[3:6], nums[6:9]]

# State bắt đầu
# start = random_start()
# output(start)

# res = BFS(start)
# print("Path:", res)


# Tạo GUI
from tkinter import *

window = Tk()
window.title("BFS - 8 Puzzle")
window.geometry('1000x600+250+150') 

# Trạng thái của GUI
current_states_list = []  # Lưu danh sách ma trận
current_index = 0         # Vị trí bước hiện tại

# Khung ma trận
grid_frame = Frame(window, bg='gray', bd=5)
grid_frame.place(x=350, y=50, width=300, height=300)

# Mảng 2 chiều chứa các Label
labels_matrix = [[None for _ in range(3)] for _ in range(3)]

for i in range(3):
    for j in range(3):
        lbl = Label(grid_frame, text="", font=('Arial', 24, 'bold'), 
                    bg='white', fg='black', bd=2, relief="solid")
        lbl.grid(row=i, column=j, padx=5, pady=5, sticky="nsew")
        labels_matrix[i][j] = lbl

# Các ô trong grid đều nhau
for i in range(3):
    grid_frame.rowconfigure(i, weight=1)
    grid_frame.columnconfigure(i, weight=1)

# Hàm cập nhật ma trận
def update_gui_matrix(state):
    for i in range(3):
        for j in range(3):
            val = state[i][j]
            if val == 0:
                labels_matrix[i][j].config(text="", bg='lightgray') # Ô trống
            else:
                labels_matrix[i][j].config(text=str(val), bg='white')

# Random
def handle_random():
    global current_states_list, current_index
    
    A = random_start()
    path = BFS(A)
    
    # Xóa dữ liệu cũ
    entry_path.config(state=NORMAL)
    entry_path.delete(0, END)
    
    if path == "failure":
        entry_path.insert(0, "Failure")
        entry_path.config(state=DISABLED)
        update_gui_matrix(A)
        current_states_list = [A]
        current_index = 0
        return
        
    else:
        path_str = " ".join(path)
        entry_path.insert(0, path_str)
        entry_path.config(state=DISABLED)

        # Danh sách state ở PATH
        current_states_list = [A]
        temp_state = A
        for action in path:
            temp_state = child_state(temp_state, action)
            current_states_list.append(temp_state)
            
        # Cập nhật ma trận
        current_index = 0
        update_gui_matrix(current_states_list[current_index])

# Next Step
def handle_next():
    global current_index
    if not current_states_list:
        return
    if current_index < len(current_states_list) - 1:
        current_index += 1
        update_gui_matrix(current_states_list[current_index])

# Last Step
def handle_last():
    global current_index
    if not current_states_list:
        return
    if current_index > 0:
        current_index -= 1
        update_gui_matrix(current_states_list[current_index])

# UI
btn_rd = Button(window, text="Random", bg='lightgray', fg='black',     
                font=('Arial', 20), command=handle_random)
btn_rd.place(x=250, y=520)

btn_last = Button(window, text="Last Step", bg='lightgray', fg='black',     
                 font=('Arial', 20), command=handle_last)
btn_last.place(x=441, y=520)

btn_next = Button(window, text="Next Step", bg='lightgray', fg='black',     
                 font=('Arial', 20), command=handle_next)
btn_next.place(x=645, y=520)

lb_path = Label(window, text="Path:", font=('Arial', 20))
lb_path.place(x=30, y=450)

entry_path = Entry(window, width=58, font=('Arial', 20))
entry_path.place(x=100, y=450)

window.mainloop()