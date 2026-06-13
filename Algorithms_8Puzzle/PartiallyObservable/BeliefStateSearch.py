from collections import deque
from Support_Functions.SupportFunctions import *
from Support_Functions.Node import Node

# trang thai niem tin ban dau pbss
INITIAL_BELIEF = [
    [[1, 2, 3], [4, 0, 6], [7, 5, 8]],
    [[1, 2, 3], [0, 4, 6], [7, 5, 8]]
]

def state_to_tuple(state):
    return tuple(map(tuple, state))

def belief_to_tuple(belief):
    return tuple(sorted(state_to_tuple(s) for s in belief))

def is_goal(belief):
    goal_tuples = set(state_to_tuple(g) for g in BSS_GOALS)
    return all(state_to_tuple(s) in goal_tuples for s in belief)

def BSS():
    node = Node(state=INITIAL_BELIEF)
    if is_goal(node.state):
        return get_path(node), node.path_cost
        
    # frontier dung fifo
    frontier = deque([node])
    # cac node state can xet
    frontier_set = set()
    frontier_set.add(belief_to_tuple(node.state))
    # cac node state da xet
    explored = set()
    
    while frontier:
        node = frontier.popleft()
        
        state_parent = belief_to_tuple(node.state)
        explored.add(state_parent)
        frontier_set.discard(state_parent)
        
        # cac action
        actions = set()
        for s in node.state:
            actions.update(get_actions(s))
            
        for action in actions:
            next_belief = []
            changed = False
            for s in node.state:
                if action in get_actions(s):
                    next_belief.append(child_state(s, action))
                    changed = True
                else:
                    next_belief.append([row[:] for row in s])
                    
            if not changed:
                continue
                
            child = Node(state=next_belief,
                         parent=node,
                         action=action,
                         path_cost=node.path_cost + 1)
                         
            state_child = belief_to_tuple(child.state)
            if state_child not in explored and state_child not in frontier_set:
                if is_goal(child.state):
                    return get_path(child), child.path_cost
                else:
                    frontier.append(child)
                    frontier_set.add(state_child)
                    
    return "failure", "N/A"