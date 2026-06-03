import heapq
from Support_Functions.CheckSolve import check_solve
from Support_Functions.SupportFunctions import *
from Support_Functions.CalculateCost import difference_cost, manhattan_cost

class Node:
    def __init__(self, state, parent=None, action=None, g=0, h=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.g = g  
        self.h = h  
        self.f = g + h  

    def __eq__(self, other):
        return self.state == other.state

    def __lt__(self, other):
        return self.f < other.f
    
# A*
# f(n)=g(n)+h(n)
# g(n): manhattan, h(n): difference
def AStar(start, goal):
    if not check_solve(start):
        return "failure", "N/A"
    
    # khởi tạo
    node = Node(state=start, parent=None, action=None, g=0, h=difference_cost(start))

    if check_goal(node.state, goal):
        return get_path(node), node.f
    
    # frontier dùng hàng đợi ưu tiên
    frontier = []
    heapq.heappush(frontier, node)
    # Dùng dict va g(m) cũ ra so sánh
    frontier_dict = {tuple(map(tuple, node.state)): node}
    #các node đã xét
    reached = {}
    
    while frontier:
        node = heapq.heappop(frontier)

        #Lazy Deletion
        state_parent = tuple(map(tuple, node.state))
        if state_parent not in frontier_dict or frontier_dict[state_parent] != node:
            continue

        if check_goal(node.state, goal):
            return get_path(node), node.f
        
        del frontier_dict[state_parent]
        reached[state_parent] = node
        
        #các action
        actions = get_actions(node.state)
        for action in actions:
            new_state = child_state(node.state, action)
            g_new = node.g + manhattan_cost(new_state)
            h_new = difference_cost(new_state)
            
            state_child = tuple(map(tuple, new_state))
            if state_child in reached:
                current_node = reached[state_child]
                if g_new >= current_node.g:
                    continue  # Bỏ qua new_state
                else:
                    del reached[state_child] #Xóa current_node
                    new_node = Node(state=new_state, parent=node, action=action, g=g_new, h=h_new)
                    heapq.heappush(frontier, new_node)
                    frontier_dict[state_child] = new_node #cập nhật lại dict
            
            elif state_child in frontier_dict:
                current_node = frontier_dict[state_child]
                if g_new < current_node.g: 
                    new_node = Node(state=new_state, parent=node, action=action, g=g_new, h=h_new)
                    frontier_dict[state_child] = new_node #cập nhập cấu hình mới trong dict
                    heapq.heappush(frontier, new_node) #thêm vào frontier
                    #current_node vẫn để đấy và dùng Lazy dectection xử lí

            else:
                new_node = Node(state=new_state, parent=node, action=action, g=g_new, h=h_new)
                heapq.heappush(frontier, new_node)
                frontier_dict[state_child] = new_node
                
    return "failure", "N/A"