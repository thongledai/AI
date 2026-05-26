from Support_Functions.SupportFunctions import goal

# số ô sai, khác nhau
def difference_cost(state):
    cost=0
    for i in range(3):
        for j in range(3):
            if state[i][j] != goal[i][j]:
                cost+=1
    return cost


# kc manhattan (có tính số 0)
def manhattan_cost(state):
    cost =0
    for i in range(3):
        for j in range(3):
            match state[i][j]:
                case 1: cost+= abs(i-0) + abs(j-0)
                case 2: cost+= abs(i-0) + abs(j-1)
                case 3: cost+= abs(i-0) + abs(j-2)
                case 4: cost+= abs(i-1) + abs(j-0)
                case 5: cost+= abs(i-1) + abs(j-1)
                case 6: cost+= abs(i-1) + abs(j-2)
                case 7: cost+= abs(i-2) + abs(j-0)
                case 8: cost+= abs(i-2) + abs(j-1)
                case 0: cost+= abs(i-2) + abs(j-2)
    return cost

# kc euclid
def euclid_cost(state):
    cost =0
    for i in range(3):
        for j in range(3):
            match state[i][j]:
                case 1: cost+= ((i-0)**2 + (j-0)**2)**0.5
                case 2: cost+= ((i-0)**2 + (j-1)**2)**0.5
                case 3: cost+= ((i-0)**2 + (j-2)**2)**0.5
                case 4: cost+= ((i-1)**2 + (j-0)**2)**0.5
                case 5: cost+= ((i-1)**2 + (j-1)**2)**0.5
                case 6: cost+= ((i-1)**2 + (j-2)**2)**0.5
                case 7: cost+= ((i-2)**2 + (j-0)**2)**0.5
                case 8: cost+= ((i-2)**2 + (j-1)**2)**0.5 
                case 0: cost+= ((i-2)**2 + (j-2)**2)**0.5
    return cost

#kc chebyshev
def chebyshev_cost(state):
    cost =0
    for i in range(3):
        for j in range(3):
            match state[i][j]:
                case 1: cost+= max(abs(i-0), abs(j-0))
                case 2: cost+= max(abs(i-0), abs(j-1))
                case 3: cost+= max(abs(i-0), abs(j-2))
                case 4: cost+= max(abs(i-1), abs(j-0))
                case 5: cost+= max(abs(i-1), abs(j-1))
                case 6: cost+= max(abs(i-1), abs(j-2))
                case 7: cost+= max(abs(i-2), abs(j-0))
                case 8: cost+= max(abs(i-2), abs(j-1)) 
                case 0: cost+= max(abs(i-2), abs(j-2))
    return cost

# số dãy giảm không liên tiếp (bỏ số 0 ra)
def desubsequence_cost(state):
    lst=[]
    for i in range(3):
        for j in range(3):
            if state[i][j] != 0:
                lst.append(state[i][j])
    dp = [1] * 8
    for i in range(8):
        for j in range(i):
            if lst[i] < lst[j]:
                dp[i] += dp[j]
    cost = sum(dp) - 8
    return cost