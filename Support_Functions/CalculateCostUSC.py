from Support_Functions.SupportFunctions import goal
# max_diff=9, min_diff=0
def cal_cost(state):
    cost=1
    for i in range(3):
        for j in range(3):
            if state[i][j] != goal[i][j]:
                cost+=1
    return cost
