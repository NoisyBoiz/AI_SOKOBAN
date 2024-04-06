import Constant
def findSolution(map):
    player = None
    listBox = []
    listWall = []
    listCheckPoint = []
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

    limitX = (0, len(map))
    limitY = (0, len(map[0]))

    queue = [(player, listBox.copy())]
    visited = []
    action = [[]]
    while len(queue) > 0:
        cur = queue.pop(0)
        curAct = action.pop(0)
        if checkWin(cur[1], listCheckPoint):
            return curAct
        if cur in visited: continue
        visited.append(cur)
        for i in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            newPos = (cur[0][0] + i[0], cur[0][1] + i[1])
            if not checkInMap(newPos, limitX, limitY) or newPos in listWall: continue
            newListBox = cur[1].copy()
            if newPos in cur[1]:
                nextNewPos = (newPos[0] + i[0], newPos[1] + i[1])
                if(nextNewPos in listWall or nextNewPos in cur[1]): continue
                newListBox.remove(newPos)
                newListBox.append(nextNewPos)
                queue.append((newPos, newListBox))
                action.append(curAct + [i])
            else:
                queue.append((newPos, newListBox))
                action.append(curAct + [i])
    print("No solution")
    return []

def checkWin(listBox, listCheckPoint):
    for box in listBox:
        if box not in listCheckPoint:
            return False
    return True

def checkInMap(pos, limitX, limitY):
   if(pos[0] < limitX[0] or pos[0] >= limitX[1] or pos[1] < limitY[0] or pos[1] >= limitY[1]):
       return False
   return True

