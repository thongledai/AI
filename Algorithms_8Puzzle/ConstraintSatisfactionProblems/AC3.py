from collections import deque
from Algorithms_8Puzzle.ConstraintSatisfactionProblems.Ultis import *
from copy import deepcopy
import random

states = []

def AC3():
    states.clear()
    current_state = deepcopy(STATE)
    states.append(deepcopy(current_state))
    domains = init_domains()
    
    domains = AC_3(domains)
    
    if any(len(domains[var]) == 0 for var in domains):
        return None, states
        
    result = recursive_ac3_backtracking(current_state, domains)
    return result, states

def AC_3(csp):
    queue = deque()
    for Xi in csp:
        for Xj in neighbors(Xi):
            queue.append((Xi, Xj))

    while queue:
        Xi, Xj = queue.popleft()
        if RM_INCONSISTENT_VALUES(csp, Xi, Xj):
            for Xk in neighbors(Xi):
                queue.append((Xk, Xi))
    return csp

def RM_INCONSISTENT_VALUES(csp, Xi, Xj):
    removed = False
    for x in list(csp[Xi]):
        satisfies = False
        for y in csp[Xj]:
            idx_i = order.index(Xi)
            idx_j = order.index(Xj)
            
            if idx_i < idx_j and x < y: satisfies = True
            elif idx_i > idx_j and x > y: satisfies = True
            elif idx_i == idx_j: satisfies = True
            
            if satisfies: break
            
        if not satisfies:
            csp[Xi].remove(x)
            removed = True
    return removed

def recursive_ac3_backtracking(state, domains):
    if is_complete(state):
        return state

    i, j = select_unassigned_variable(state)
    var = (i, j)
    
    values = list(domains[var])
    random.shuffle(values)
    
    for value in values:
        if consistent(var, value, state):
            state[i][j] = value
            states.append(deepcopy(state))
            
            result = recursive_ac3_backtracking(state, domains)
            if result is not None:
                return result
                
            state[i][j] = None
            states.append(deepcopy(state))
            
    return None