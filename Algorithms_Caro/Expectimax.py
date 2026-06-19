def expectima(state, depth, maximizing_player):
   if is_terminal(state) or depth == 0:
       return utility(state)
   if maximizing_player:
       max_eval = float('-inf')
       for action in actions(state):
           eval = expectima(result(state, action), depth - 1, False)
           max_eval = max(max_eval, eval)
       return max_eval
   else:
       chance_eval = 0
       for action in actions(state):
           eval = expectima(result(state, action), depth - 1, True)
           chance_eval += eval
       return chance_eval / len(actions(state))