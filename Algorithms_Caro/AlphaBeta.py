from Utils import is_terminal, utility, actions, result

def alpha_beta_minimax(state, depth, alpha, beta, maximizing_player):
   if is_terminal(state) or depth == 0:
       return utility(state)
   if maximizing_player:
       value = float('-inf')
       for action in actions(state):
           value = max(value, alpha_beta_minimax(result(state, action), depth-1, alpha, beta, False))
           alpha = max(alpha, value)
           if beta <= alpha:
               break
       return value
   else:
       value = float('inf')
       for action in actions(state):
           value = min(value, alpha_beta_minimax(result(state, action), depth-1, alpha, beta, True))
           beta = min(beta, value)
           if beta <= alpha:
               break
       return value