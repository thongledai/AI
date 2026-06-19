from Utils import is_terminal, utility, actions, result

def minimax(state, depth, maximizing_player):
   if is_terminal(state) or depth == 0:
       return utility(state)
   if maximizing_player:
       max_eval = float('-inf')
       for action in actions(state):
           eval = minimax(result(state, action), depth - 1, False)
           max_eval = max(max_eval, eval)
       return max_eval
   else:
       min_eval = float('inf')
       for action in actions(state):
           eval = minimax(result(state, action), depth - 1, True)
           min_eval = min(min_eval, eval)
       return min_eval