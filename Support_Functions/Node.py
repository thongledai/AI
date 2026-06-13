from Support_Functions.SupportFunctions import child_state, get_actions


class Node:
    def __init__(self, state, parent=None, action=None, path_cost=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost

    def show_state(self):
        for row in self.state:
            print(row)
        print()

    def __eq__(self, other):
        return self.state == other.state

    def __lt__(self, other):
        return self.path_cost < other.path_cost
    
def childs(node):
    childs = []
    for action in get_actions(node.state):
        child = Node(state=child_state(node.state, action), 
                     parent=node, 
                     action=action, 
                     path_cost=node.path_cost + 1)
        childs.append(child)
    return childs
