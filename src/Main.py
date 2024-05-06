import pygame
import Constant

pygame.init()

screen = pygame.display.set_mode((Constant.SCREEN_WIDTH, Constant.SCREEN_HEIGHT))
surfaceAlpha = pygame.Surface((Constant.SCREEN_WIDTH, Constant.SCREEN_HEIGHT),pygame.SRCALPHA)
surfaceAlpha.set_alpha(50)

from HandleImage import getImage, splitSpriteImgPath
from HandleFile import readFile, saveFile
import Interact
import Player
import Solve

map = None
finishGame = False
offset = (0,0)
offsetScroll = (0,0)
scrollXRange = (0,0)
listChooseMap = []
indexMap = 0
runStep = "menu"

autoHistory = False

Image = {
    "Wall": getImage("Wall.png", Constant.BLOCK_SIZE, Constant.BLOCK_SIZE),
    "Box": getImage("Box.png", Constant.BLOCK_SIZE, Constant.BLOCK_SIZE),
    "BoxSolve": getImage("BoxSolve.png", Constant.BLOCK_SIZE, Constant.BLOCK_SIZE),
    "CheckPoint": getImage("CheckPoint.png", Constant.BLOCK_SIZE, Constant.BLOCK_SIZE),
    "Player": splitSpriteImgPath("Character", 32, 32, Constant.BLOCK_SIZE, Constant.BLOCK_SIZE, True),
    "Floor": getImage("Floor.png", Constant.BLOCK_SIZE, Constant.BLOCK_SIZE),
    "Background": getImage("background.png", Constant.SCREEN_WIDTH, Constant.SCREEN_HEIGHT)
}
Button = {}

def initButton():
    global Button, titleGame, titleGameBorder
    x = (Constant.SCREEN_WIDTH - Constant.BTN_MENU_SIZE[0])/2
    y = (Constant.SCREEN_HEIGHT - 4*(Constant.BTN_MENU_SIZE[1] + Constant.BTN_MENU_GAP))/2

    titleGame = pygame.font.SysFont(Constant.FONT_FAMILY, 60).render("Sokoban",True,(50, 255, 255))
    titleGameBorder = pygame.font.SysFont(Constant.FONT_FAMILY, 60).render("Sokoban",True,(255,255,255))

    Button["Play"] = Interact.Button2("Play", x, y + (Constant.BTN_MENU_SIZE[1] + Constant.BTN_MENU_GAP), Constant.BTN_MENU_SIZE[0], Constant.BTN_MENU_SIZE[1], 3, (239, 135, 10), "btn-sokoban-blue.png", lambda: setRunStep("chooseMap"))
    Button["CreateMap"] = Interact.Button2("Create Map", x, y + (Constant.BTN_MENU_SIZE[1] + Constant.BTN_MENU_GAP) * 2, Constant.BTN_MENU_SIZE[0], Constant.BTN_MENU_SIZE[1], 3, (239, 135, 10), "btn-sokoban-blue.png", lambda: setRunStep("chooseMapEdit"))
    Button["Exit"] = Interact.Button2("Exit", x,  y + (Constant.BTN_MENU_SIZE[1] + Constant.BTN_MENU_GAP)*3,Constant.BTN_MENU_SIZE[0], Constant.BTN_MENU_SIZE[1], 3, (239, 135, 10), "btn-sokoban-blue.png", lambda: Interact.createComfirm(500,200,"Exit","Do you want to exit",(142, 205, 221),(34, 102, 141), Interact.closeNotification, exitGame))
    Button["Back"] = Interact.Button2(None, 10, 10, 50, 50, 0, (0, 0, 0), "Back.png", lambda: Interact.createComfirm(500,200,"Back","Do you want to exit game?",(142, 205, 221),(34, 102, 141), Interact.closeNotification, lambda: setRunStep("chooseMap")))
    Button["Menu"] = Interact.Button2(None, 10, 10, 50, 50, 0, (0, 0, 0), "Home.png", lambda: setRunStep("menu"))
    Button["PlayAgain"] = Interact.Button2(None,  Constant.SCREEN_WIDTH - 120, 10, 50 , 50, 0, (0, 0, 0), "Reload.png", lambda: Interact.createComfirm(500,200,"Play Again","Do you want to play again",(142, 205, 221),(34, 102, 141), lambda: Interact.closeNotification(), lambda: setRunStep("game")))
    Button["Auto"] = Interact.Button2(None,  Constant.SCREEN_WIDTH - 60, 10, 50 , 50, 0, (0, 0, 0), "Auto.png", lambda: autoPlay())

class ToolBar:
    def __init__(self):
        self.listAction = ["quit","save","move","add","edit","delete"]
        self.listKeyAction = ["B","S","M","A","E","X"]
        self.listImageAction = []
        self.rectAction = pygame.Rect(0,0,Constant.BLOCK_SIZE*len(self.listAction),Constant.BLOCK_SIZE)
        self.listRectAction = []
        
        self.listBlock = ["character","wall","box","checkPoint", "boxSolve", "playerCP"]
        self.listImageBlock = []
        self.listImageBlockOrigin = []
        self.listKeyBlock = []
        self.rectBlock = pygame.Rect((Constant.BLOCK_SIZE*len(self.listAction)+1),0,Constant.SCREEN_WIDTH-Constant.BLOCK_SIZE*len(self.listAction),Constant.BLOCK_SIZE)
        self.listRectBlock = []
        
        self.iconSize = Constant.BLOCK_SIZE*0.6

        self.textKeyAction = []
        self.textKeyBlock = []

        self.getImage()
        self.initRectIcon()
        self.initTextKey()
        #status
        self.actionType = "move"
        self.blockType = "character"
        self.indexBlock = 0
        self.isMouseDown = False
        self.objSelected = None
        self.isQuit = False
        self.preMousePos = (0,0)
        self.offset = (Constant.SCREEN_WIDTH//2,Constant.SCREEN_HEIGHT//2)

        self.limitX = (-Constant.SCREEN_WIDTH,Constant.SCREEN_WIDTH)
        self.limitY = (-Constant.SCREEN_HEIGHT,Constant.SCREEN_HEIGHT)

        self.data = []
    def resize(self):
        self.rectBlock = pygame.Rect((Constant.BLOCK_SIZE*len(self.listAction)+1),0,Constant.SCREEN_WIDTH-Constant.BLOCK_SIZE*len(self.listAction),Constant.BLOCK_SIZE)
        self.limitPageBlock = Constant.SCREEN_WIDTH//Constant.BLOCK_SIZE - len(self.listAction)
        self.listRectAction.clear()
        self.listRectBlock.clear()
        self.initRectIcon()

    def blurImageBlock(self, screen, mousePos):
        if self.actionType == "add" or self.actionType == "edit":
            if mousePos[1]>Constant.BLOCK_SIZE:
                shift_x = self.offset[0]%Constant.BLOCK_SIZE
                shift_y = self.offset[1]%Constant.BLOCK_SIZE
                mousePoint = ((mousePos[0]-shift_x)//Constant.BLOCK_SIZE*Constant.BLOCK_SIZE + shift_x, (mousePos[1]-shift_y)//Constant.BLOCK_SIZE*Constant.BLOCK_SIZE + shift_y)
                surfaceAlpha.blit(self.listImageBlockOrigin[self.indexBlock],(mousePoint[0],mousePoint[1]))
                screen.blit(surfaceAlpha,(0,0))

    def getImage(self):
        for i in self.listAction:
            self.listImageAction.append(getImage(i+".png",self.iconSize,self.iconSize))

        for i,block in enumerate(self.listBlock):
            if block == "character":
                img = splitSpriteImgPath("Character", 32, 32, Constant.BLOCK_SIZE, Constant.BLOCK_SIZE, False)
                self.listImageBlock.append(pygame.transform.scale(img["Character"][0],(self.iconSize,self.iconSize)))
                self.listImageBlockOrigin.append(img["Character"][0])
            else:
                self.listImageBlock.append(getImage(block+".png",self.iconSize,self.iconSize))
                self.listImageBlockOrigin.append(getImage(block+".png",Constant.BLOCK_SIZE,Constant.BLOCK_SIZE))
            self.listKeyBlock.append(chr(49+i))

    # tính tọa độ để vẽ các icon
    def initRectIcon(self):
        for i in range(len(self.listAction)):
            self.listRectAction.append((i*Constant.BLOCK_SIZE,0,Constant.BLOCK_SIZE,Constant.BLOCK_SIZE))

        shift_x = len(self.listAction)*Constant.BLOCK_SIZE
        for i in range(len(self.listImageBlock)):
            self.listRectBlock.append((i*Constant.BLOCK_SIZE+shift_x,0,Constant.BLOCK_SIZE,Constant.BLOCK_SIZE))

    def initTextKey(self):
        font = pygame.font.SysFont("Arial",20,bold=True)
        for i in self.listKeyAction:
            text = font.render(i,True, (255, 36, 66))
            self.textKeyAction.append(text)

        for i in self.listKeyBlock:
            text = font.render(i,True, (255, 36, 66))
            self.textKeyBlock.append(text)

    # phím tắt
    def checkPressKey(self,key):
        for i,k in enumerate(self.listKeyAction):
            if key == ord(k.lower()) or key == ord(k):
                if(self.listAction[i] == "save"):
                    Interact.createComfirm(500,200,"Save","Do you want to save this map",(142, 205, 221),(34, 102, 141), Interact.closeNotification, saveMap)
                elif(self.listAction[i] == "back"):
                    Interact.createComfirm(500,200,"Back","Do you want to back",(142, 205, 221),(34, 102, 141),Interact.closeNotification, lambda: setRunStep("chooseMapEdit"))
                else:
                    self.actionType = self.listAction[i]
                return
            
        for i,k in enumerate(self.listKeyBlock):
            if key == ord(k):
                self.blockType = self.listBlock[i]
                self.indexBlock = i
                return

    def handleClick(self,mousePos):
        if(mousePos[1] < Constant.BLOCK_SIZE):
        # check chọn loại hành động (save,move,edit,delete)
            for i,rect in enumerate(self.listRectAction):
                if rect[0] <= mousePos[0] <= rect[0]+rect[2] and rect[1] <= mousePos[1] <= rect[1]+rect[3]:
                    if(self.listAction[i] == "save"):
                        Interact.createComfirm(500,200,"Save","Do you want to save this map",(142, 205, 221),(34, 102, 141),Interact.closeNotification, saveMap)
                    elif(self.listAction[i] == "quit"):
                        Interact.createComfirm(500,200,"Back","Do you want to back",(142, 205, 221),(34, 102, 141),Interact.closeNotification, lambda: setRunStep("chooseMapEdit"))
                    else: 
                        self.actionType = self.listAction[i]
                    return 
            # check chọn loại block
            for i,rect in enumerate(self.listRectBlock):
                if rect[0] <= mousePos[0] <= rect[0]+rect[2] and rect[1] <= mousePos[1] <= rect[1]+rect[3]:
                    self.blockType = self.listBlock[i]
                    self.indexBlock = i
                    return 

        elif self.actionType == "move":
            self.isMouseDown = True
            self.preMousePos = mousePos

        elif self.actionType == "add":
            x = (mousePos[0] - self.offset[0])//Constant.BLOCK_SIZE
            y = (mousePos[1] - self.offset[1])//Constant.BLOCK_SIZE
            if self.limitX[0] <= x*Constant.BLOCK_SIZE < self.limitX[1] and self.limitY[0] <= y*Constant.BLOCK_SIZE < self.limitY[1]:
                if self.blockType == "character" or self.blockType == "playerCP":
                    prePos = None
                    for i in self.data:
                        if i["type"] == "character" or i["type"] == "playerCP":
                            i["type"] = self.blockType
                            prePos = i["pos"]
                        if i["pos"] == (x,y):
                            return
                    if prePos != None:
                        for i in self.data:
                            if i["pos"] == prePos:
                                i["pos"] = (x,y)
                                return
                    self.data.append({"type":self.blockType,"pos":(x,y)})
                else:
                    for i in self.data:
                        if i["pos"] == (x,y):
                            return
                    self.data.append({"type":self.blockType,"pos":(x,y)})
                return
        elif self.actionType == "edit":
            x = (mousePos[0] - self.offset[0])//Constant.BLOCK_SIZE
            y = (mousePos[1] - self.offset[1])//Constant.BLOCK_SIZE

            change = False
            for i in self.data:
                if i["pos"] == (x,y):
                    self.data.remove(i)
                    self.data.append({"type":self.blockType,"pos":(x,y)})
                    change = True
                    break
            if(self.blockType == "character" and change):
                for i in self.data:
                    if i["type"] == "character":
                        self.data.remove(i)
                        break

        elif self.actionType == "delete":
            x = (mousePos[0] - self.offset[0])//Constant.BLOCK_SIZE
            y = (mousePos[1] - self.offset[1])//Constant.BLOCK_SIZE
            for i in self.data:
                if i["pos"] == (x,y):
                    self.data.remove(i)
                    return
    
    def moveAction(self, mousePos):
        if self.isMouseDown and self.actionType == "move" and mousePos[1] > Constant.BLOCK_SIZE:
            offX = mousePos[0] - self.preMousePos[0]
            offY = mousePos[1] - self.preMousePos[1]
            if(offX > 0):
                if(self.offset[0] + offX < self.limitX[1]):
                    self.offset = (self.offset[0] + offX, self.offset[1])
                else:
                    self.offset = (self.limitX[1], self.offset[1])
            elif(offX < 0):
                if(self.offset[0] + offX > self.limitX[0] + Constant.SCREEN_WIDTH):
                    self.offset = (self.offset[0] + offX, self.offset[1])
                else:
                    self.offset = (self.limitX[0] + Constant.SCREEN_WIDTH, self.offset[1])

            if(offY > 0):
                if(self.offset[1] + offY < self.limitY[1]):
                    self.offset = (self.offset[0], self.offset[1] + offY)
                else:
                    self.offset = (self.offset[0], self.limitY[1])
            elif(offY < 0):
                if(self.offset[1] + offY > self.limitY[0] + Constant.SCREEN_HEIGHT):
                    self.offset = (self.offset[0] , self.offset[1] + offY)
                else:
                    self.offset = (self.offset[0] , self.limitY[0] + Constant.SCREEN_HEIGHT)
            self.preMousePos = mousePos
                
    def convertMap(self):
        if(indexMap == None): return
        map = readFile("map.json")[indexMap]
        for i in range(len(map)):
            for j in range(len(map[i])):
                if(map[i][j] == Constant.PLAYER):
                    self.data.append({"type":"character","pos":(i,j)})
                elif(map[i][j] == Constant.BOX):
                    self.data.append({"type":"box","pos":(i,j)})
                elif(map[i][j] == Constant.CHECKPOINT):
                    self.data.append({"type":"checkPoint","pos":(i,j)})
                elif(map[i][j] == Constant.BOXSOLVE):
                    self.data.append({"type":"boxSolve","pos":(i,j)})
                elif(map[i][j] == Constant.WALL):
                    self.data.append({"type":"wall","pos":(i,j)})
                elif(map[i][j] == Constant.PLAYER + Constant.CHECKPOINT):
                    self.data.append({"type":"playerCP","pos":(i,j)})

        self.offset = (Constant.SCREEN_WIDTH//2 - (len(map)*Constant.BLOCK_SIZE)//2, Constant.SCREEN_HEIGHT//2 - (len(map[0])*Constant.BLOCK_SIZE)//2)

    def convertData(self):
        if len(self.data) == 0:
            Interact.Interact.createAlert(500,200,"Save","Map is empty",(142, 205, 221),(34, 102, 141), Interact.closeNotification)
            return None

        min_x = Constant.SCREEN_WIDTH//Constant.BLOCK_SIZE
        min_y = Constant.SCREEN_HEIGHT//Constant.BLOCK_SIZE
        max_x = 0
        max_y = 0

        haveCharacter = False
        CheckPointCount = 0
        BoxCount = 0

        for i in self.data:
            if i["type"] == "character":
                haveCharacter = True
            elif i["type"] == "checkPoint":
                CheckPointCount += 1
            elif i["type"] == "box":
                BoxCount += 1
            elif i["type"] == "playerCP":
                haveCharacter = True
                CheckPointCount += 1
            if i["pos"][0] < min_x:
                min_x = i["pos"][0]
            if i["pos"][1] < min_y:
                min_y = i["pos"][1]
            if i["pos"][0] > max_x:
                max_x = i["pos"][0]
            if i["pos"][1] > max_y:
                max_y = i["pos"][1]
        
        if not haveCharacter:
            Interact.createAlert(500,200,"Error","Map must have character",(142, 205, 221),(34, 102, 141),Interact.closeNotification)
            return None
        if CheckPointCount == 0:
            Interact.createAlert(500,200,"Error","Map must have at least one checkPoint",(142, 205, 221),(34, 102, 141),Interact.closeNotification)
            return None
        if BoxCount == 0:
            Interact.createAlert(500,200,"Error","Map must have at least one box",(142, 205, 221),(34, 102, 141),Interact.closeNotification)
            return None
        if CheckPointCount != BoxCount:
            Interact.createAlert(500,200,"Error","Number of checkPoint must equal number of box",(142, 205, 221),(34, 102, 141),Interact.closeNotification)
            return None
        
        map = [[0 for i in range(max_y - min_y + 1)] for j in range(max_x - min_x + 1)]
        
        for i in self.data:
            index = Constant.FLOOR
            if(i["type"] == "character"):
                index = Constant.PLAYER
            elif(i["type"] == "wall"):
                index = Constant.WALL
            elif(i["type"] == "box"):
                index = Constant.BOX
            elif(i["type"] == "checkPoint"):
                index = Constant.CHECKPOINT
            elif(i["type"] == "boxSolve"):
                index = Constant.BOXSOLVE
            elif(i["type"] == "playerCP"):
                index = Constant.PLAYER + Constant.CHECKPOINT
            map[i["pos"][0] - min_x][i["pos"][1] - min_y] = index
        return map
                
    def draw(self,screen):
        pygame.draw.rect(screen,(96, 150, 180),(self.rectAction))
        pygame.draw.rect(screen,(234, 199, 199),(self.rectBlock))
        for i in range(Constant.SCREEN_WIDTH//Constant.BLOCK_SIZE):
            pygame.draw.rect(screen,(0,0,0),(i*Constant.BLOCK_SIZE,0,Constant.BLOCK_SIZE,Constant.BLOCK_SIZE),1)
    
        for i,action in enumerate(self.listRectAction):
            screen.blit(self.listImageAction[i],(action[0]+((Constant.BLOCK_SIZE - self.iconSize)/2),action[1]+((Constant.BLOCK_SIZE - self.iconSize)/2)))
            if self.actionType == self.listAction[i]:
                pygame.draw.rect(screen,(199, 0, 57),(action[0],action[1],action[2],action[3]),6)
            screen.blit(self.textKeyAction[i],(action[0]+2,action[1]-3))

        for i,block in enumerate(self.listRectBlock):
            screen.blit(self.listImageBlock[i],(block[0]+((Constant.BLOCK_SIZE - self.iconSize)/2),block[1]+((Constant.BLOCK_SIZE - self.iconSize)/2)))
            if self.blockType == self.listBlock[i]:
                pygame.draw.rect(screen,(150, 210, 20),(block[0],block[1],block[2],block[3]),6)
            screen.blit(self.textKeyBlock[i],(block[0]+2,block[1]-3))

    def drawRuler(self,screen):
        shift_x = self.offset[0]%Constant.BLOCK_SIZE
        shift_y = self.offset[1]%Constant.BLOCK_SIZE
        for i in range(shift_x,Constant.SCREEN_WIDTH+shift_x,Constant.BLOCK_SIZE):
            # if(i-self.offset[0]==0): draw.line(screen,(255,0,0),(i,0),(i,contain.SCREEN_HEIGHT),2)
            # else:
                self.drawDrashedLine(screen,i,Constant.SCREEN_HEIGHT,3,"vertical")
        for j in range(shift_y,Constant.SCREEN_HEIGHT+shift_y,Constant.BLOCK_SIZE):
            # if(j-self.offset[1]==0): draw.line(screen,(255,0,0),(0,j),(contain.SCREEN_WIDTH,j),2)
            # else: 
                self.drawDrashedLine(screen,j,Constant.SCREEN_WIDTH,3,"horizontal")
        
    def drawDrashedLine(self,screen,pos,length,step,direction):
        if direction == "vertical":
            for i in range(0,length,step*3):
                pygame.draw.line(screen,(0,0,0),(pos,i),(pos,i+step))
        else:
            for i in range(0,length,step*3):
                pygame.draw.line(screen,(0,0,0),(i,pos),(i+step,pos))

    def drawData(self,screen):
        for data in self.data:
            if data["type"] == "character":
                screen.blit(self.listImageBlockOrigin[0],(data["pos"][0]*Constant.BLOCK_SIZE + self.offset[0],data["pos"][1]*Constant.BLOCK_SIZE + self.offset[1]))
            else:
                screen.blit(self.listImageBlockOrigin[self.listBlock.index(data["type"])],(data["pos"][0]*Constant.BLOCK_SIZE + self.offset[0],data["pos"][1]*Constant.BLOCK_SIZE + self.offset[1]))

def saveMap():
    global toolBar
    map = toolBar.convertData()
    if(map == None): return
    data = readFile("map.json")
    if(indexMap == None):
        data.append(map)
    else:
        data[indexMap] = map
    saveFile("map.json",data)
    toolBar.data.clear()
    setRunStep("chooseMapEdit")

def deleteMap(index):
    data = readFile("map.json")
    data.pop(index)
    saveFile("map.json",data)
    setRunStep("chooseMapEdit")

toolBar = ToolBar()

def setIndexMap(index, isEdit = False): 
    global indexMap
    mapLen = len(readFile("map.json"))
    if(index >= 0 and index < mapLen): indexMap = index
    elif(index >= mapLen): indexMap = 0
    else: indexMap = mapLen - 1
    if(isEdit): setRunStep("createMap")
    else: setRunStep("game")
    
def setRunStep(step):
    global runStep
    runStep = step
    Interact.closeNotification()
    if(step == 'game'):
        initGame()
    elif(step == 'chooseMap'):
        initChooseMap()
    elif(step == 'chooseMapEdit'):
        initChooseMap(True)
    elif(step == 'createMap'):
        toolBar.data.clear()
        toolBar.convertMap()

def exitGame():
    global running
    running = False

def initGame():
    global map, offset, totalCheckPoint, totalGoat, player, finishGame, solution, timeTook, memo_info
    totalCheckPoint = 0
    totalGoat = 0
    finishGame = False
    solution = []
    timeTook = None
    memo_info = None
    player = None
    map = readFile("map.json")[indexMap]

    for i in range(len(map)):
        for j in range(len(map[i])):
            if(map[i][j] == Constant.PLAYER):
                player = Player.Player(i, j, Constant.BLOCK_SIZE, Image["Player"])
            if(map[i][j] == Constant.CHECKPOINT):
                totalCheckPoint += 1
            if(map[i][j] == Constant.PLAYER + Constant.CHECKPOINT):
                player = Player.Player(i, j, Constant.BLOCK_SIZE, Image["Player"])
                totalCheckPoint += 1
            if(map[i][j] == Constant.FLOOR):
                if(i == 0 or i == len(map) - 1 or j == 0 or j == len(map[0]) - 1):
                    map[i][j] = -10
                    findFloor((i,j),map)

    # offset = (contain.SCREEN_WIDTH/2 - player.pos[0]*contain.BLOCK_SIZE - contain.BLOCK_SIZE/2, contain.SCREEN_HEIGHT/2 - player.pos[1]*contain.BLOCK_SIZE - contain.BLOCK_SIZE/2)
    offset = (Constant.SCREEN_WIDTH - len(map)*Constant.BLOCK_SIZE)//2, (Constant.SCREEN_HEIGHT - len(map[0])*Constant.BLOCK_SIZE)//2
        
def findFloor(pos,map):
    up = (pos[0] - 1, pos[1])
    if(up[0] >= 0 and map[up[0]][up[1]] == Constant.FLOOR):
        map[up[0]][up[1]] = -10
        return findFloor(up,map)
    down = (pos[0] + 1, pos[1])
    if(down[0] < len(map) and map[down[0]][down[1]] == Constant.FLOOR):
        map[down[0]][down[1]] = -10
        return findFloor(down,map)
    left = (pos[0], pos[1] - 1)
    if(left[1] >= 0 and map[left[0]][left[1]] == Constant.FLOOR):
        map[left[0]][left[1]] = -10
        return findFloor(left,map)
    right = (pos[0], pos[1] + 1)
    if(right[1] < len(map[0]) and map[right[0]][right[1]] == Constant.FLOOR):
        map[right[0]][right[1]] = -10
        return findFloor(right,map)

def initChooseMap(isEdit = False):
    global listChooseMap, scrollXRange, indexMap
    listChooseMap = []

    indexMap = None
    buttonWidth = 100
    buttonHeight = 50
    gap = 50
    limitRow = (Constant.SCREEN_HEIGHT - 100)//(buttonHeight + gap)
   
    mapList = readFile("map.json")
  
    scrollXRange = (0, max(0, (len(mapList) - 1)//limitRow)*(buttonWidth + gap) - Constant.SCREEN_WIDTH + buttonWidth + 2 * gap)

    if(isEdit):
        listChooseMap.append(Interact.Button("Create New Map", (Constant.SCREEN_WIDTH - 200)/2, 10, 200, buttonHeight, 2, (255, 250, 221), (255, 204, 112), (0, 0, 0), lambda: setRunStep("createMap"), True))

    for i in range(len(mapList)):
        x = gap + (i//limitRow)*(buttonWidth + gap) 
        y = 30 + (Constant.SCREEN_HEIGHT- (buttonHeight + gap)*limitRow + gap)/2 + (i%limitRow)*(buttonHeight + gap)
        listChooseMap.append(Interact.Button("Map " + str(i + 1), x, y, buttonWidth, buttonHeight, 2, (255, 250, 221), (255, 204, 112), (0, 0, 0), lambda i=i: setIndexMap(i, isEdit)))
        if(isEdit):
            listChooseMap.append(Interact.Button2("",x + buttonWidth - 20, y - 20, 40, 40, 2,  (104, 120, 176), "Delete-map.png", lambda i=i: Interact.createComfirm(500,200,"Delete","Do you want to delete this map",(142, 205, 221),(34, 102, 141),Interact.closeNotification, lambda i=i: deleteMap(i))))

def createMap():
    surfaceAlpha.fill((255,255,255,0))
    global running, runStep
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exitGame()
        if(Interact.notification == None):
            if event.type == pygame.KEYDOWN:
                toolBar.checkPressKey(event.key)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                toolBar.handleClick(event.pos)
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                toolBar.isMouseDown = False
            if event.type == pygame.MOUSEMOTION:
                toolBar.moveAction(event.pos)
        else:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                Interact.notification.checkClick(event.pos)
     
    mousePos = pygame.mouse.get_pos()

    toolBar.drawRuler(screen)
    toolBar.drawData(screen)
    toolBar.blurImageBlock(screen, mousePos)
    toolBar.draw(screen)

def chooseMap():
    global finishGame, offsetScroll
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exitGame()

        if(Interact.notification == None):
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                Button["Menu"].checkClick(event.pos)
                for button in listChooseMap:
                    button.checkClick(event.pos, offsetScroll)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:
                if(offsetScroll[0] < -scrollXRange[0]):
                    if(offsetScroll[0] + 50 > -scrollXRange[0]):
                        offsetScroll = (-scrollXRange[0], offsetScroll[1])
                    else:
                        offsetScroll = (offsetScroll[0] + 50, offsetScroll[1])

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:
                if(offsetScroll[0] > - scrollXRange[1]):
                    if(offsetScroll[0] - 50 < -scrollXRange[1]):
                        offsetScroll = (-scrollXRange[1], offsetScroll[1])
                    else:
                        offsetScroll = (offsetScroll[0] - 50, offsetScroll[1])

        elif(Interact.notification != None):
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                Interact.notification.checkClick(event.pos)


    for button in listChooseMap:
        button.draw(screen, offsetScroll)

    Button["Menu"].draw(screen)

def checkInMap(pos, map):
    if(pos[0] >= 0 and pos[0] < len(map) and pos[1] >= 0 and pos[1] < len(map[pos[0]])):
        return True
    return False

def checkBlock(pos, map):
    if(map[pos[0]][pos[1]] == Constant.WALL or map[pos[0]][pos[1]] == Constant.BOX or map[pos[0]][pos[1]] == Constant.BOXSOLVE):
        return False
    return True

def checkWin(map):
    for i in range(len(map)):
        for j in range(len(map[i])):
            if(map[i][j] == Constant.BOX or map[i][j] == Constant.CHECKPOINT):
                return False
    return True

def saveHistory(indexMap, timeTook, memo_info):
    data = readFile("history.json")
    for i in data:
        if i["indexMap"] == indexMap:
            i["timeTook"] = timeTook
            i["memo_info"] = memo_info
            saveFile("history.json",data)
            return
    data.append({"indexMap": indexMap, "timeTook": timeTook, "memo_info": memo_info})
    saveFile("history.json",data)

def autoPlay():
    global solution, timeTook, memo_info
    solution, timeTook, memo_info = Solve.findSolution(map)
    timeTook = round(timeTook, 6)
    saveHistory(indexMap, timeTook, memo_info)
    player.isAutoMove = True

solution = None
def mainGame():
    global finishGame, offset, solution
    for event in pygame.event.get():
        # bắt sự kiện thoát game
        if event.type == pygame.QUIT:
            exitGame()

        # bắt sự kiện click chuột trái
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            Button["Back"].checkClick(event.pos)
            Button["PlayAgain"].checkClick(event.pos)
            Button["Auto"].checkClick(event.pos)
            if(Interact.notification != None):
                Interact.notification.checkClick(event.pos)

        # bắt sự kiện bàn phím
        if event.type == pygame.KEYDOWN and Interact.notification == None and not finishGame and not player.isAutoMove:
            # xử lí di chuyển theo sự kiện bàn phím của player
            player.handleMoveKey(event.key, map) 
            
            if(event.key == pygame.K_n):
                setIndexMap(indexMap+1)
            if(event.key == pygame.K_p):
                setIndexMap(indexMap-1)
            if(event.key == pygame.K_f):
                autoPlay()

    # nếu player đang di chuyển tự động thì xử lí di chuyển tự động
    if(player.isAutoMove):
        player.handleAutoMove(solution, map)
   
    # vẽ map    
    for i in range(len(map)):
        for j in range(len(map[i])):
            pos = (i*Constant.BLOCK_SIZE + offset[0], j*Constant.BLOCK_SIZE + offset[1])
            if(map[i][j] == Constant.CHECKPOINT) or (map[i][j] == Constant.CHECKPOINT+Constant.PLAYER):
                screen.blit(Image["Floor"], pos)
                screen.blit(Image["CheckPoint"], pos)
            if(map[i][j] == Constant.FLOOR) or (map[i][j] == Constant.FLOOR+Constant.PLAYER):
                screen.blit(Image["Floor"], pos)
            if(map[i][j] == Constant.WALL):
                screen.blit(Image["Wall"], pos)
            if(map[i][j] == Constant.BOX):
                screen.blit(Image["Box"], pos)
            if(map[i][j] == Constant.BOXSOLVE):
                screen.blit(Image["BoxSolve"], pos)

    # cập nhật trạng thái của player và vẽ player
    player.update()   
    player.draw(screen, offset)
    
    # vẽ button và hiển thị thông báo
    Button["Back"].draw(screen)
    Button["PlayAgain"].draw(screen)
    Button["Auto"].draw(screen)

    # hiển thị số bước di chuyển
    moveCount = pygame.font.SysFont(Constant.FONT_FAMILY, 20).render("Move step: " + str(player.moveCount),True,(255, 255, 255))
    screen.blit(moveCount, ((Constant.SCREEN_WIDTH - moveCount.get_width())/2, 10))

    if(indexMap != None):
        iMap = pygame.font.SysFont(Constant.FONT_FAMILY, 20).render("Map: " + str(indexMap + 1),True,(255, 255, 255))
        screen.blit(iMap, (Constant.SCREEN_WIDTH - iMap.get_width() - 10, Constant.SCREEN_HEIGHT - 30))
    if(timeTook != None):
        time = pygame.font.SysFont("Arial", 20, bold = True).render("Time: " + str(timeTook) + " s",True,(255, 255, 255))
        screen.blit(time, (10, Constant.SCREEN_HEIGHT - 30))
    if(memo_info != None):
        memo = pygame.font.SysFont("Arial", 20, bold = True).render("Memo: " + str(memo_info) + " MB",True,(255, 255, 255))
        screen.blit(memo, (10, Constant.SCREEN_HEIGHT - 60))
    # kiểm tra xem game đã kết thúc chưa
    if(not finishGame and checkWin(map)):
        finishGame = True
        Interact.createComfirm(500,200,"Congratulation","You win",(142, 205, 221),(34, 102, 141),lambda: setRunStep("game"),lambda: setIndexMap(indexMap+1) ,lambda: Interact.closeNotification(), "Play Again", "Next Map")

def mainMenu():
    global running, runStep
    for event in pygame.event.get():
        # bắt sự kiện thoát game
        if event.type == pygame.QUIT:
            exitGame()
        
        # bắt sự kiện click chuột trái
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            Button["Play"].checkClick(event.pos)
            Button["Exit"].checkClick(event.pos)
            Button["CreateMap"].checkClick(event.pos)
            if(Interact.notification != None):
                Interact.notification.checkClick(event.pos)
    
    # vẽ tiêu đề game
    for x in [(3,0), (0,3), (-3,0), (0,-3)]: 
        screen.blit(titleGameBorder, ((Constant.SCREEN_WIDTH - titleGameBorder.get_width())/2 + x[0], 60 + x[1]))
    screen.blit(titleGame, ((Constant.SCREEN_WIDTH - titleGame.get_width())/2, 60))

    # vẽ các nút bấm
    Button["Play"].draw(screen)
    Button["CreateMap"].draw(screen)
    Button["Exit"].draw(screen)

# khởi tạo các nút bấm
initButton()

running = True
while running:
    # xóa màn hình
    screen.blit(Image["Background"], (0,0))
    # giới hạn FPS
    pygame.time.Clock().tick(Constant.FPS)

    # kiểm tra xem đang ở bước nào và hiển thị giao diện tương ứng
    if runStep == "menu":
        mainMenu()
    elif runStep == "createMap":
        createMap()
    elif runStep == "chooseMap" or runStep == "chooseMapEdit":
        chooseMap()
    elif runStep == "game":
        mainGame()

    # hiển thị thông báo nếu có
    if(Interact.notification != None):
        Interact.notification.draw(screen)

    # cập nhật màn hình
    pygame.display.update()

# kết thúc game
pygame.quit()
