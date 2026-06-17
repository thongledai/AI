from Algorithms_8Puzzle.ConstraintSatisfactionProblems.Ultis import *
from copy import deepcopy
import random

states = []

#Forward Checking
def FC():
    states.clear()
    current_state = deepcopy(STATE)
    states.append(deepcopy(current_state))
    domains = init_domains()
    
    result = recursive_forward_checking(current_state, domains)
    return result, states

def recursive_forward_checking(state, domains):
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
            
            removed = forward_check(domains, var, value)
            if removed is not None:
                result = recursive_forward_checking(state, domains)
                if result is not None:
                    return result
                restore(domains, removed)
                
            state[i][j] = None
            states.append(deepcopy(state))
            
    return None

#thu hẹp domain các ô còn lại
def forward_check(domains, var, value):
    removed = []
    for other in domains:
        if other == var:
            continue
        if value in domains[other]:
            domains[other].remove(value)
            removed.append((other, value))
            if len(domains[other]) == 0:
                restore(domains, removed)
                return None
    return removed




