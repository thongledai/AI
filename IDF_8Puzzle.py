import random
from collections import deque

class Node:
    def __init__(self, state, parent=None, action=None, depth=0):
        self.state = state  # Ma trận 3x3
        self.parent = parent
        self.action = action
        self.depth = depth

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
    if y < 2: actions.append('R')
    if x > 0: actions.append('U')
    if y > 0: actions.append('L')
    return actions

mapping = { 'D': (1, 0), 
            'U': (-1, 0), 
            'R': (0, 1), 
            'L': (0, -1)}

# Hàm tạo state con
def child_state(state, action):
    # Sao chép ma trận
    new_state = [row[:] for row in state]
    x, y = get_empty(state)
    
    dx, dy = mapping[action]
    new_x, new_y = x + dx, y + dy
    
    # Hoán đổi vị trí
    new_state[x][y], new_state[new_x][new_y] = new_state[new_x][new_y], new_state[x][y]
    return new_state

def childs(node):
    childs = []
    for action in get_actions(node.state):
        child = Node(state=child_state(node.state, action), 
                     parent=node, 
                     action=action, 
                     depth=node.depth + 1)
        childs.append(child)
    return childs

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


# Iterative Deepening Search
def IDS(start):
    for depth in range(100): 
        result = DLS(start, depth)
        if result != "cutoff":
            return result
    return "failure"
         

def DLS(start, limit):
    node = Node(state=start)

    frontier = deque([node])
    frontier_set = set() # Lưu note.state tìm kiếm cho nhanh
    frontier_set.add(tuple(map(tuple, node.state))) 
    explored = set() # Lưu note.state đã xét

    result = "failure"
    while frontier:
        node = frontier.pop()
        state_parent = tuple(map(tuple, node.state))
        frontier_set.discard(state_parent)

        if goal_test(node.state):
            return solution(node)

        explored.add(state_parent)

        if node.depth >= limit:
            result = "cutoff"
        else:
            for child in childs(node):
                state_child = tuple(map(tuple, child.state))
                if state_child not in explored and state_child not in frontier_set:
                    frontier.append(child)
                    frontier_set.add(state_child)

    return result
       
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
#start = random_start()
start = [
    [0, 1, 3],
    [4, 2, 6],
    [7, 5, 8]
]
# output(start)

# res = IDS(start)
# print("Path:", res)


# Tạo GUI
from tkinter import *

window = Tk()
window.title("IDS - 8 Puzzle")
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

    # Hiện state ngay lập tức
    update_gui_matrix(A)

    # Hiện Searching...
    entry_path.config(state=NORMAL)
    entry_path.delete(0, END)
    entry_path.insert(0, "Searching...")
    entry_path.config(state=DISABLED)

    # Ép GUI cập nhật ngay
    window.update()

    # Bắt đầu tìm path
    path = IDS(A)
    
    # Xóa dữ liệu cũ
    entry_path.config(state=NORMAL)
    entry_path.delete(0, END)
    
    if path == "failure":
        entry_path.insert(0, "Failure")
        entry_path.config(state=DISABLED)

        current_states_list = [A]
        current_index = 0
        return
        
    else:
        # Hiện path cuối cùng
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