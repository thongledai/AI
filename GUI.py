# Tạo GUI
from tkinter import *

window = Tk()
window.title("UCS - 8 Puzzle")
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
    path = UCS(A)
    
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