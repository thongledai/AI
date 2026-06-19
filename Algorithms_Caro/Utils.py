# state là 1 tuple
# ví dụ: state = ('X',   None,  'O', 
#                 None,   'X',  None, 
#                 'O',   None,  None)

# điều kiện thắng
win_conditions = [
    (0, 1, 2), 
    (3, 4, 5), 
    (6, 7, 8),
    (0, 3, 6), 
    (1, 4, 7), 
    (2, 5, 8),
    (0, 4, 8), 
    (2, 4, 6)
]

# Kiểm tra xem ván đấu đã kết thúc chưa
def is_terminal(state):
    for a, b, c in win_conditions:
        if state[a] is not None and state[a] == state[b] == state[c]:
            return True
    return all(cell is not None for cell in state)

# Tính điểm
def utility(state):
    for a, b, c in win_conditions:
        if state[a] is not None and state[a] == state[b] == state[c]:
            if state[a] == 'X':
                return 1
            elif state[a] == 'O':
                return -1
    return 0

# Tìm ô trống
def actions(state):
    return [i for i, cell in enumerate(state) if cell is None]

# Next state
def result(state, action):
    x_count = state.count('X')
    o_count = state.count('O')
    player = 'X' if x_count == o_count else 'O' #player là lượt đi của X hoặc O
    
    new_state = list(state)
    new_state[action] = player
    return tuple(new_state)
