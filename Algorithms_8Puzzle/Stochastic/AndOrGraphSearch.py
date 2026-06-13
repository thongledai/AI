from Support_Functions.SupportFunctions import *
from Support_Functions.CheckSolve import check_solve


def AOGS(start, goal):
    if not check_solve(start):
        return "failure", "N/A"
        
    path = []    
    result = OR_SEARCH(start, goal, path)
    
    if result == "failure":
        return "failure", "N/A"
    else:
        return result, len(result)


def OR_SEARCH(state, goal, path):
    if check_goal(state, goal):
        return []
    
    if state in path:
        return "failure"

    actions = get_actions(state)
    for action in actions:
        next_state = child_state(state, action)
        
        plan = AND_SEARCH([next_state], goal, path + [state])
        
        if plan != "failure":
            next_state_tuple = tuple(map(tuple, next_state))
            return [action] + plan[next_state_tuple]
            
    return "failure"


def AND_SEARCH(states, goal, path):
    plans = {}
    
    for s in states:
        plan = OR_SEARCH(s, goal, path)
        if plan == "failure":
            return "failure"
            
        plans[tuple(map(tuple, s))] = plan
        
    return plans