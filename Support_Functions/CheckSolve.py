def check_solve(start):
    lst=[]
    for i in range(3):
        for j in range(3):
            if start[i][j] != 0:
                lst.append(start[i][j])
    print(lst)
    count=0
    for i in range(7): 
        for j in range(i+1,8):
            if lst[i] > lst[j]:
                count += 1
    if count % 2 == 0:
        return True
    else: 
        return False
