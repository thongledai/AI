from Algorithms_8Puzzle.ConstraintSatisfactionProblems.Ultis import *
from copy import deepcopy
import random

#Lưu state đã đi
states=[]

def BS():
    states.clear()

    current_state = deepcopy(STATE)
    states.append(deepcopy(current_state))
    result = recursive_backtracking(current_state)
    return result, states

def recursive_backtracking(state):
    if is_complete(state):
        return state

    i, j = select_unassigned_variable(state)

    values = list(DOMAIN)
    random.shuffle(values)
    for value in values:
        state[i][j] = value
        states.append(deepcopy(state))
        if constraint(state):
            result = recursive_backtracking(state)
            if result is not None:
                return result

        state[i][j] = None
        states.append(deepcopy(state))
    return None

