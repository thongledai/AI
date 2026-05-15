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
def random_star():
    nums = list(range(9))
    random.shuffle(nums)
    return [nums[0:3], nums[3:6], nums[6:9]]

# State bắt đầu
start = random_star()
output(start)

res = BFS(start)
print("Path:", res)
