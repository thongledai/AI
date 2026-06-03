import random

def Model():
    # Hoán đổi giá trị
    def swap(a, b):
        return b, a

    # Tìm vị trí ô trống 
    def find_0(a):
        for i in range(3):
            for j in range(3):
                if a[i][j] == 0:
                    return i, j
        return -1, -1

    # Lấy danh sách nước đi hợp lệ tránh vị trí cũ
    def get_moves(i, j, last):
        dx = [-1, 1, 0, 0]
        dy = [0, 0, -1, 1]
        valid = []
        for k in range(4):
            ni, nj = i + dx[k], j + dy[k]
            if 0 <= ni < 3 and 0 <= nj < 3 and (ni, nj) != last:
                valid.append((ni, nj))
        return valid

    # Chọn ngẫu nhiên
    def choose(moves):
        return random.choice(moves) if moves else None

    # Cập nhật trạng thái
    def update(a, last):
        i, j = find_0(a)
        moves = get_moves(i, j, last)
        target_pos = choose(moves)
        
        if target_pos:
            ti, tj = target_pos
            new_last = (i, j) 
            a[i][j], a[ti][tj] = swap(a[i][j], a[ti][tj])
            return a, new_last
        return a, last

    # In mảng
    def output(a):
        for row in a:
            print(*(row))
        print()

    # Tạo mảng 3x3 ngẫu nhiên
    def randomA():
        nums = list(range(9))
        random.shuffle(nums)
        return [nums[0:3], nums[3:6], nums[6:9]]


    target = [[1, 2, 3], 
              [4, 5, 6], 
              [7, 8, 0]]
    last = None 
    success = False


    A = randomA()
    output(A)

    for i in range(22):
        print("Step:", i+1)
        A, last = update(A, last)
        output(A)
        
        if A == target:
            print("done")
            success = True
            break

    if not success:
        print("false")


Model()