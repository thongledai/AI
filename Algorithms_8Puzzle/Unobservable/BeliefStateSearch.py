import copy
from Support_Functions.SupportFunctions import get_actions, child_state

def state_to_tuple(state):
    """Chuyển đổi ma trận 2D thành tuple để có thể băm (hash)."""
    return tuple(tuple(row) for row in state)

def belief_to_tuple(belief_state):
    """
    Chuyển đổi tập hợp các trạng thái thành một tuple duy nhất đại diện cho Belief State.
    Sử dụng sorted() để đảm bảo (State1, State2) và (State2, State1) được coi là cùng 1 Node.
    """
    return tuple(sorted([state_to_tuple(s) for s in belief_state]))

def is_goal(belief_state, goals):
    """
    Kiểm tra Goal Test: TẤT CẢ các ma trận trong Belief State đều phải nằm trong danh sách 10 Goals.
    """
    goal_tuples = [state_to_tuple(g) for g in goals]
    for s in belief_state:
        if state_to_tuple(s) not in goal_tuples:
            return False
    return True

def BSS(initial_belief_state, goals):
    """
    Thuật toán Belief State Search (Breadth-First Search trên không gian Belief State).
    Input:
      - initial_belief_state: list chứa các trạng thái ban đầu, ví dụ: [state1, state2]
      - goals: list chứa 10 trạng thái đích
    Output:
      - Trả về tuple: (path, final_belief_state, cost) hoặc "failure"
    """
    
    # Khởi tạo Node gốc
    start_node = {
        'belief': initial_belief_state,
        'path': [],
        'cost': 0
    }
    
    # Hàng đợi cho BFS
    queue = [start_node]
    visited = set()
    visited.add(belief_to_tuple(initial_belief_state))
    
    while queue:
        current = queue.pop(0)
        
        # Kiểm tra xem trạng thái niềm tin hiện tại đã thỏa mãn mục tiêu chưa
        if is_goal(current['belief'], goals):
            return current['path'], current['belief'], current['cost']
            
        # Lấy tất cả các hành động có thể thực hiện từ TẤT CẢ các ma trận trong Belief State hiện tại
        possible_actions = set()
        for state in current['belief']:
            possible_actions.update(get_actions(state))
            
        # Thử áp dụng từng hành động để sinh ra Belief State mới
        for action in possible_actions:
            next_belief = []
            action_caused_change = False
            
            for state in current['belief']:
                # Logic cốt lõi (giống hệt GUI): 
                # Nếu hành động hợp lệ với state này -> Di chuyển
                # Nếu hành động không hợp lệ (ví dụ đụng tường) -> Đứng yên (copy lại)
                if action in get_actions(state):
                    next_belief.append(child_state(state, action))
                    action_caused_change = True
                else:
                    next_belief.append(copy.deepcopy(state))
            
            # Tối ưu: Nếu hành động này không làm thay đổi BẤT KỲ state nào, ta bỏ qua nhánh này
            if not action_caused_change:
                continue
                
            next_belief_tup = belief_to_tuple(next_belief)
            
            # Tránh vòng lặp (lặp lại trạng thái niềm tin đã duyệt)
            if next_belief_tup not in visited:
                visited.add(next_belief_tup)
                queue.append({
                    'belief': next_belief,
                    'path': current['path'] + [action],
                    'cost': current['cost'] + 1
                })
                
    # Nếu hàng đợi rỗng mà vẫn chưa tìm thấy đích
    return "failure"