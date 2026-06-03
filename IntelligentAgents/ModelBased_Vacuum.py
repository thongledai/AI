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

#Hàm hành động đối ngược
def opposite_action(action):
    opposites = {'U': 'D', 
                 'D': 'U', 
                 'L': 'R', 
                 'R': 'L'}
    return opposites.get(action, None)

def vacuum(grid, x, y, last_action):
    #Nếu đang đứng ở vị trí dơ thì hút bụi
    state = grid[x][y]
    if state == 1:
        print("Robot hút bụi tại:", (x, y))
        grid[x][y] = 0

    #Cập nhật
    moves = P_moves(x, y)
    
    #Loại bỏ hành động trc đó
    forbidden_move = opposite_action(last_action)
    filtered_moves = [m for m in moves if m != forbidden_move]
    
    #Ưu tiên chọn ô bẩn trong các ô có thể đi
    for dir in filtered_moves:
        nx, ny = move(x, y, dir)
        nextstate = grid[nx][ny]

        # Nếu nextstate dơ thì đi tới đó
        if nextstate == 1:
            action = dir
            break
        else:
            action = random.choice(filtered_moves)
    
    print("Robot di chuyển:", action)
    nx, ny = move(x, y, action)
    
    return nx, ny, action

def model_vacuum(grid, x, y, result_grid):
    last_action = None
    for i in range(16): 
        if grid == result_grid:
            print("done")
            output(grid)
            return True
        
        print("Step", i+1)
        output(grid)
        x, y, last_action = vacuum(grid, x, y, last_action)
        print("Vị trí hiện tại:", x, y)
        print()
        
    print("false")
    return False


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
print("Vị trí đầu tiên:", (x, y))
print("Ma trận ban đầu:")
model_vacuum(grid, x, y, result_grid)