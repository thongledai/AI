import random
from tracemalloc import start

start()

# Lấy vị trí ô trống
def get_empty(state):
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                return i, j

# Lấy các actions có thể đi
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

# Lấy đường đi từ star đến goal
def solution(node):
    path = []
    n = node
    while n.parent:
        path.append(n.action)
        n = n.parent
    return path[::-1]

# In mảng
def output(state):
    for row in state:
        print(*(row))
    print()

# Tạo mảng random
def random_start():
    nums = list(range(9))
    random.shuffle(nums)
    return [nums[0:3], nums[3:6], nums[6:9]]

start = random_start()

goal = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 0]
]

def check_goal(state):
    return state == goal