import random

# Hàm in ma trận
def output(board):
    for i in range(3):
        for j in range(3):
            print(board[i][j], end=" ")
        print()
    print()

# Hàm tìm vị trí ô trống
def find_zero(board):
    for i in range(3):
        for j in range(3):
            if board[i][j] == 0:
                return i, j

# Hàm tạo ma trận random 3x3
def random_board():
    nums = [0,1,2,3,4,5,6,7,8]
    random.shuffle(nums)
    board = []
    k = 0
    for i in range(3):
        row = []
        for j in range(3):
            row.append(nums[k])

            k += 1

        board.append(row)

    return board

# Hàm lấy các bước có thể đi
def P_moves(x, y):

    moves = []

    if x > 0:
        moves.append('U')

    if x < 2:
        moves.append('D')

    if y > 0:
        moves.append('L')

    if y < 2:
        moves.append('R')

    return moves

# Hàm di chuyển
k = {
    'U': (-1, 0),
    'D': (1, 0),
    'L': (0, -1),
    'R': (0, 1)
}

def move(board, x, y, action):

    nx = x + k[action][0]
    ny = y + k[action][1]

    # Đổi chỗ ô trống với ô kế bên
    board[x][y], board[nx][ny] = board[nx][ny], board[x][y]

    return nx, ny

# Hàm loại bỏ nước đi ngược
def opposite(action):

    if action == 'U':
        return 'D'

    if action == 'D':
        return 'U'

    if action == 'L':
        return 'R'

    if action == 'R':
        return 'L'

# Model-Based Reflex Agent
def agent(board, x, y, oldaction):

    # Các bước có thể đi
    moves = P_moves(x, y)

    # Từ bước 2 trở đi loại bỏ nước đi cũ
    if oldaction != None:

        back = opposite(oldaction)

        if back in moves:
            moves.remove(back)

    # Rule = random
    action = random.choice(moves)

    print("Action:", action)

    # Di chuyển
    x, y = move(board, x, y, action)

    # Lưu action cũ
    oldaction = action

    return x, y, oldaction

# Tạo ma trận random
board = random_board()

# Tìm vị trí ban đầu của ô trống
x, y = find_zero(board)

# Action cũ
oldaction = None

print("Ma trận ban đầu:")
output(board)

print("Vị trí ô trống:", (x, y))
print()

# Chạy agent
for step in range(10):

    print("Bước", step + 1)

    x, y, oldaction = agent(board, x, y, oldaction)

    output(board)

    print("Vị trí ô trống:", (x, y))

    print("Old Action:", oldaction)

    print("-------------------")