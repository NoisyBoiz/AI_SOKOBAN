import Constant
from queue import Queue
    
directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]

player = None
listBox = None
listWall = None
listCheckPoint = None
deadlocks = None

def initDeadlocks(map):
    global player, listBox, listWall, listCheckPoint, deadlocks
    player = None
    listBox = set()
    listWall = set()
    listCheckPoint = set()
    deadlocks = set()

    # tạo mảng paths để lưu vị trí của player, box, checkpoint, path
    paths = set() 
    # tạo mảng dictDeadlocks để lưu khoảng cách từ checkpoint đến path
    dictDeadlocks = dict()

    # duyệt map để lấy vị trí của player, box, wall, checkpoint lưu vào các mảng tương ứng
    for i in range(len(map)):
        for j in range(len(map[i])):
            if map[i][j] == Constant.WALL:
                listWall.add((i, j))
            elif map[i][j] == Constant.PLAYER:
                player = (i, j)
                paths.add((i, j))
            elif map[i][j] == Constant.BOX:
                listBox.add((i, j))
                paths.add((i, j))
            elif map[i][j] == Constant.CHECKPOINT:
                listCheckPoint.add((i, j))
                paths.add((i, j))
            elif map[i][j] == Constant.BOXSOLVE:
                listBox.add((i, j))
                listCheckPoint.add((i, j))
                paths.add((i, j))
            elif map[i][j] == Constant.PLAYER + Constant.CHECKPOINT:
                player = (i, j)
                listCheckPoint.add((i, j))
                paths.add((i, j))
            elif map[i][j] == 0:
                paths.add((i, j))

    # tạo mảng dictDeadlocks để lưu khoảng cách từ checkpoint đến path 
    # đặt khoảng cách ban đầu từ checkpoint đến path là 1e9
    for cp in listCheckPoint:
        dictDeadlocks[cp] = dict()
        for path in paths:
            dictDeadlocks[cp][path] = 1e9

    queue = Queue()
    for cp in listCheckPoint:
        # khoảng cách từ checkpoint đến chính nó là 0
        dictDeadlocks[cp][cp] = 0
        # thêm checkpoint vào queue
        queue.put(cp)
        # duyệt queue để tìm khoảng cách từ checkpoint hiện tại đến path
        while not queue.empty():
            cur = queue.get()
            # duyệt qua 4 hướng di chuyển có thể đi đến checkpoint
            for d in directions:
                # giả sử vị trí của player và box
                boxPos = (cur[0] + d[0], cur[1] + d[1])
                playerPos = (cur[0] + 2 * d[0], cur[1] + 2 * d[1])
                # kiểm tra xem vị trí của player và box có nằm trong map không
                if boxPos in paths:
                    # kiểm tra xem khoảng cách từ checkpoint đến path có phải là vô cùng không
                    if dictDeadlocks[cp][boxPos] == 1e9:
                        # kiểm tra xem vị trí của player và box có nằm trong wall không
                        if(boxPos not in listWall and playerPos not in listWall):
                            # cập nhật khoảng cách từ checkpoint đến path
                            dictDeadlocks[cp][boxPos] = dictDeadlocks[cp][cur] + 1
                            # lưu vị trí box hiện tại vào queue để duyệt tiếp
                            queue.put(boxPos)

    # nếu khoảng cách từ checkpoint đến path là vô cùng thì nếu box ở vị trí path đó sẽ không thể di chuyển để đến checkpoint
    for path in paths:
        ok = True
        for cp in listCheckPoint:
            if dictDeadlocks[cp][path] != 1e9:
                ok = False
                break
        if ok:
            deadlocks.add(path)


def findSolution(map):
    initDeadlocks(map)
    # tạo queue để lưu trạng thái của player và box
    queue = Queue()
    queue.put((player, tuple(listBox), []))

    # tạo mảng visited để lưu trạng thái đã duyệt
    visited = set()

    # duyệt queue 
    while not queue.empty():
        # lấy ra trạng thái hiện tại của player và box
        cur = queue.get()

        # kiểm tra xem trạng thái hiện tại có phải là trạng thái win không
        if is_win(listCheckPoint, set(cur[1])):    
            # nếu là trạng thái win thì trả về hướng di chuyển để đến trạng thái win
            return cur[2]
        
        # kiểm tra xem trạng thái hiện tại đã được duyệt chưa nếu rồi thì bỏ qua và duyệt trạng thái tiếp theo
        if (cur[0], cur[1]) in visited: continue

        # thêm trạng thái hiện tại vào mảng visited
        visited.add((cur[0], cur[1]))

        # duyệt qua 4 hướng di chuyển của player
        for i in directions:
            # tính vị trí mới của player sau khi di chuyển
            newPos = (cur[0][0] + i[0], cur[0][1] + i[1])
            # kiểm tra vị trí mới có nằm trong map hay trùng với wall không
            if newPos in listWall: continue

            # kiểm tra vị trí mới có trùng với box không nếu có thì di chuyển box
            if newPos in cur[1]:
                # tính vị trí mới của box sau khi di chuyển
                nextNewPos = (newPos[0] + i[0], newPos[1] + i[1])
                # kiểm tra vị trí mới của box có nằm trong map hay trùng với wall hoặc box khác không
                if(nextNewPos in listWall) or (nextNewPos in cur[1]) or (nextNewPos in deadlocks): continue
                # cập nhật vị trí của box
                newListBox = list(cur[1])
                newListBox.remove(newPos)
                newListBox.append(nextNewPos)

                # thêm trạng thái mới của player và box vào queue
                queue.put((newPos, tuple(newListBox), cur[2] + [i]))
            else:
                # nếu không trùng với box thì thêm trạng thái mới của player và box vào queue
                queue.put((newPos, cur[1], cur[2] + [i]))  

    # nếu không tìm thấy hướng di chuyển để win thì trả về mảng rỗng
    print("No solution")
    return []

def is_win(goals, boxes):
	return goals.issubset(boxes)

