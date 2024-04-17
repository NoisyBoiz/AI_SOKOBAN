import Constant
def findSolution(map):
    player = None
    listBox = []
    listWall = []
    listCheckPoint = []
    # duyệt map để lấy vị trí của player, box, wall, checkpoint lưu vào các mảng tương ứng
    for i in range(len(map)):
        for j in range(len(map[i])):
            if map[i][j] == Constant.WALL:
                listWall.append((i, j))
            elif map[i][j] == Constant.PLAYER:
                player = (i, j)
            elif map[i][j] == Constant.BOX:
                listBox.append((i, j))
            elif map[i][j] == Constant.CHECKPOINT:
                listCheckPoint.append((i, j))
            elif map[i][j] == Constant.BOXSOLVE:
                listBox.append((i, j))
                listCheckPoint.append((i, j))

    # lấy ra giới hạn của map
    limitX = (0, len(map))
    limitY = (0, len(map[0]))

    # tạo queue để lưu trạng thái của player và box
    queue = [(player, listBox.copy())]

    # tạo mảng visited để lưu trạng thái đã duyệt
    visited = []

    # tạo mảng action để lưu các hướng di chuyển của player
    action = [[]]

    # duyệt queue để
    while len(queue) > 0:
        # lấy ra trạng thái hiện tại của player và box
        cur = queue.pop(0)

        # lấy ra các hướng di chuyển của player trong trạng thái hiện tại
        curAct = action.pop(0)

        # kiểm tra xem trạng thái hiện tại có phải là trạng thái win không
        if checkWin(cur[1], listCheckPoint):
            # nếu là trạng thái win thì trả về hướng di chuyển để đến trạng thái win
            return curAct
        
        # kiểm tra xem trạng thái hiện tại đã được duyệt chưa nếu rồi thì bỏ qua và duyệt trạng thái tiếp theo
        if cur in visited: continue

        # thêm trạng thái hiện tại vào mảng visited
        visited.append(cur)

        # duyệt qua 4 hướng di chuyển của player
        for i in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            # tính vị trí mới của player sau khi di chuyển
            newPos = (cur[0][0] + i[0], cur[0][1] + i[1])
            # kiểm tra vị trí mới có nằm trong map hay trùng với wall không
            if not checkInMap(newPos, limitX, limitY) or newPos in listWall: continue
            # tạo mảng mới để lưu trạng thái mới của box
            newListBox = cur[1].copy()
            # kiểm tra vị trí mới có trùng với box không nếu có thì di chuyển box
            if newPos in cur[1]:
                # tính vị trí mới của box sau khi di chuyển
                nextNewPos = (newPos[0] + i[0], newPos[1] + i[1])
                # kiểm tra vị trí mới của box có nằm trong map hay trùng với wall hoặc box khác không
                if(nextNewPos in listWall or nextNewPos in cur[1]): continue
                # cập nhật vị trí của box
                newListBox.remove(newPos)
                newListBox.append(nextNewPos)

                # thêm trạng thái mới của player và box vào queue
                queue.append((newPos, newListBox))
                # thêm hướng di chuyển hiện tại vào action
                action.append(curAct + [i])
            else:
                # nếu không trùng với box thì thêm trạng thái mới của player và box vào queue
                queue.append((newPos, newListBox))
                action.append(curAct + [i])

    # nếu không tìm thấy hướng di chuyển để win thì trả về mảng rỗng
    print("No solution")
    return []

def checkWin(listBox, listCheckPoint):
    # kiểm tra xem các box đã trùng với các checkpoint chưa
    for box in listBox:
        if box not in listCheckPoint:
            return False
    return True

def checkInMap(pos, limitX, limitY):
    # kiểm tra vị trí có nằm trong map không
   if(pos[0] < limitX[0] or pos[0] >= limitX[1] or pos[1] < limitY[0] or pos[1] >= limitY[1]):
       return False
   return True

