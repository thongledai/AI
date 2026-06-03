from Support_Functions.SupportFunctions import *
from Support_Functions.CheckSolve import check_solve
from Support_Functions.CalculateCost import manhattan_cost

# Local Beam Search
def LBS(start, goal, k=5):
    if not check_solve(start):
        return "failure", "N/A"
    
    # lưu (state, path)
    current_state_set = [(start, [])]
    actions = get_actions(start)
    for action in actions:
        next_state = child_state(start, action)
        current_state_set.append((next_state, [action]))
    #đã xets
    explored = set()

    for state, path in current_state_set:
        if check_goal(state, goal):
            return path, len(path)

    while True:
        neighbor_states = []
        for state, path in current_state_set:
            state_key = tuple(map(tuple, state))
            if state_key in explored:
                continue
            else:
                explored.add(state_key)

            actions = get_actions(state)
            for action in actions:
                next_state = child_state(state, action)
                next_path = path + [action]

                if next_state == goal:
                    return next_path, len(next_path)
                else:
                    neighbor_states.append((next_state, next_path))

        if not neighbor_states:
            return "failure", "N/A"

        neighbor_states.sort(key=lambda x: manhattan_cost(x[0]))
        current_state_set = neighbor_states[:k]