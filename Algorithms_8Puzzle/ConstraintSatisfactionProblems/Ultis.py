import random

#tập giá trị
DOMAIN = {0, 1, 2, 3, 4, 5, 6, 7, 8}
STATE= [
        [None, None, None],
        [None, None, None],
        [None, None, None]
    ]
def is_complete(state):
    for row in state:
        for value in row:
            if value is None:
                return False
    return True

#Thứ tự các giá trj
order = [
    (2, 2),
    (0, 0),
    (0, 1),
    (0, 2),
    (1, 0),
    (1, 1),
    (1, 2),
    (2, 0),
    (2, 1)
]

# ràng buộc số trước nhỏ hơn số sau và số cuối nhỏ nhất
def constraint(state):
    for i in range(8):
        s1 = state[order[i][0]][order[i][1]]
        s2 = state[order[i+1][0]][order[i+1][1]]

        if s1 is not None and s2 is not None:
            if s1 >= s2:
                return False

    return True

#chọn giá trị chưa được gán
def select_unassigned_variable(state):
    for i in range(3):
        for j in range(3):
            if state[i][j] is None:
                return i, j
    return None

# Khởi tạo domain cho các biến
def init_domains():

    domains = {}

    for i in range(3):
        for j in range(3):
            domains[(i, j)] = DOMAIN.copy()

    return domains

# Lấy các biến kề
def neighbors(var):
    idx = order.index(var)
    result = []
    if idx > 0:
        result.append(order[idx-1])

    if idx < len(order)-1:
        result.append(order[idx+1])

    return result

# Tạo mảng random
def random_start():
    nums = list(range(9))
    random.shuffle(nums)
    return [nums[0:3], nums[3:6], nums[6:9]]

def count_conflicts(state):
    conflicts = 0
    for i in range(8):
        s1 = state[order[i][0]][order[i][1]]
        s2 = state[order[i+1][0]][order[i+1][1]]
        if s1 is not None and s2 is not None:
            if s1 >= s2:  # Nếu vi phạm điều kiện tăng dần
                conflicts += 1
    return conflicts

# Tìm biến đang vi phạm
def conflicted_variables(state):
    variables = set() # Dùng set để không bị thêm trùng lặp 1 ô nhiều lần
    for i in range(8):
        pos1 = order[i]
        pos2 = order[i+1]
        
        s1 = state[pos1[0]][pos1[1]]
        s2 = state[pos2[0]][pos2[1]]
        
        if s1 is not None and s2 is not None:
            if s1 >= s2: # Nếu 2 ô này vi phạm, đưa cả 2 vị trí vào danh sách lỗi
                variables.add(pos1)
                variables.add(pos2)
                
    return list(variables)


# Chọn giá trị gây ít xung đột nhất
def min_conflict_value(state, var):
    i, j = var
    current = state[i][j]
    best = []
    minimum = float('inf')

    for value in DOMAIN:
        state[i][j] = value
        c = count_conflicts(state)
        if c < minimum:
            minimum = c
            best = [value]
        elif c == minimum:
            best.append(value)

    state[i][j] = current
    return random.choice(best)

# Khôi phục domain
def restore(domains, removed):

    for var, value in removed:
        domains[var].add(value)

# Kiểm tra tính hợp lệ
def consistent(var, value, state):
    state[var[0]][var[1]] = value
    res = constraint(state)
    state[var[0]][var[1]] = None
    return res