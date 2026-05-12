import random

# Hàm lấy các hướng có thể đi
def P_moves(x, y):
    moves = []
    if x < 3: moves.append('D')
    if x > 0: moves.append('U')
    if y < 3: moves.append('R')
    if y > 0: moves.append('L')
    return moves

# Hàm di chuyển
k = {'D': (1, 0), 'U': (-1, 0), 'R': (0, 1), 'L': (0, -1)}

def move(x, y, dir):
    return x + k[dir][0], y + k[dir][1]

# In ma trận
def output(grid):
    for i in range(4):
        for j in range(4):
            print(grid[i][j], end=" ")
        print()

# Hàm tạo ma trận random
def random_grid(size):
    grid = []
    for i in range(size):
        row = []
        for j in range(size):
            row.append(random.randint(0,1))
        grid.append(row)
    return grid

# Hàm tạo vị trí random
def random_position(size):
    x = random.randint(0, size-1)
    y = random.randint(0, size-1)
    return x, y

def vacuum(grid, x, y):

    # Nếu đang đứng ở vị trí dơ thì hút bụi
    state = grid[x][y]

    if state == 1:
        print("Robot hút bụi tại:", (x, y))
        grid[x][y] = 0

    # Các hướng có thể đi
    moves = P_moves(x, y)

    found = False
    for dir in moves:
        nx, ny = move(x, y, dir)
        nextstate = grid[nx][ny]

        # Nếu nextstate dơ thì đi tới đó
        if nextstate == 1:
            action = dir
            found = True
            break

    # Nếu không dơ thì random
    if found == False:
        action = random.choice(moves)
    
    print("Robot di chuyển:", action)

    # Cập nhật vị trí mới
    x, y = move(x, y, action)

    # Trả về vị trí mới
    return x, y

# Ma trận
grid = random_grid(4)

# Vị trí
x, y = random_position(4)

# Ma trận kết quả
result_grid = [
    [0,0,0,0],
    [0,0,0,0],
    [0,0,0,0],
    [0,0,0,0]
]


print("Vị trí đầu tiên:", x, y)
print()


for i in range(10):
    if grid == result_grid:
        print("done")
        break
    else:
        output(grid)
        x, y = vacuum(grid, x, y)
        print("Vị trí hiện tại:", x, y)