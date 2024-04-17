import pygame
import Constant

class Player:
    def __init__(self, posX, posY, block_size, sprites):
        self.sprites = sprites
        self.pos = (posX, posY)
        self.block_size = block_size
        self.status = "Character"
        self.direction = "right"
        self.animation_delay = 3
        self.animation_index = 0

        self.isAutoMove = False
        self.autoMoveDelay = 10
        self.autoMoveIndex = 0
        self.moveCount = 0

    def update(self):
        # cập nhật hoạt ảnh nhân vật
        if(self.animation_index/self.animation_delay < len(self.sprites[self.status+"_"+self.direction]) - 1):
            self.animation_index += 1
        else:
            self.animation_index = 0

    def handleAutoMove(self, action, map):  
        # tăng index dể xác định đã đến lượt di chuyển nào
        self.autoMoveIndex += 1
        # index được chia cho delay để làm chậm tốc độ di chuyển
        if(self.autoMoveIndex%self.autoMoveDelay!=1): return

        # kiểm tra đã hết hành động chưa nếu chưa thì tiếp tục di chuyển
        if(self.autoMoveIndex//self.autoMoveDelay < len(action)):
            # lấy ra hướng di chuyển trong action
            d = action[self.autoMoveIndex//self.autoMoveDelay]
            # xác định vị trí mới sau khi di chuyển
            newPos = (self.pos[0] + d[0], self.pos[1] + d[1])

            # kiểm tra vị trí mới có trùng với Box không nếu có thì di chuyển Box
            if(map[newPos[0]][newPos[1]] == Constant.BOX or map[newPos[0]][newPos[1]] == Constant.BOXSOLVE):
                nextNewPos = (newPos[0] + d[0], newPos[1] + d[1])
                # cập nhât vị trí Box
                map[nextNewPos[0]][nextNewPos[1]] += Constant.BOX
                map[newPos[0]][newPos[1]] -= Constant.BOX

            # cập nhật vị trí của Player
            map[self.pos[0]][self.pos[1]] -= Constant.PLAYER
            map[newPos[0]][newPos[1]] += Constant.PLAYER
            self.pos = newPos 

            # tăng biến đếm số lần di chuyển
            self.moveCount += 1
        else:
            self.isAutoMove = False
    
    def handleMoveKey(self, key, map):
        d = (0, 0)
        if key == pygame.K_LEFT or key == pygame.K_a:
            self.direction = "left"
            d = (-1, 0)
        elif key == pygame.K_RIGHT or key == pygame.K_d:
            self.direction = "right"
            d = (1, 0)
        elif key == pygame.K_UP or key == pygame.K_w:
            d = (0, -1)
        elif key == pygame.K_DOWN or key == pygame.K_s:
            d = (0, 1)
        else:
            return

        # xác định vị trí mới sau khi di chuyển
        newPos = (self.pos[0] + d[0], self.pos[1] + d[1])

        # kiểm tra vị trí mới có trùng với tường không nếu có thì không di chuyển
        if(map[newPos[0]][newPos[1]] == Constant.WALL): return

        # kiểm tra vị trí mới có trùng với Box không nếu có thì di chuyển Box
        if(map[newPos[0]][newPos[1]] == Constant.BOX or map[newPos[0]][newPos[1]] == Constant.BOXSOLVE):
            # xác định vị trí mới của Box 
            nextNewPos = (newPos[0] + d[0], newPos[1] + d[1])
            # kiểm tra vị trí mới của Box có trùng với tường không nếu có thì không di chuyển
            if(map[nextNewPos[0]][nextNewPos[1]] == Constant.WALL or map[nextNewPos[0]][nextNewPos[1]] == Constant.BOX or map[nextNewPos[0]][nextNewPos[1]] == Constant.BOXSOLVE): return
            # cập nhật vị trí Box
            map[nextNewPos[0]][nextNewPos[1]] += Constant.BOX
            map[newPos[0]][newPos[1]] -= Constant.BOX
        
        # cập nhật vị trí của Player
        map[self.pos[0]][self.pos[1]] -= Constant.PLAYER
        map[newPos[0]][newPos[1]] += Constant.PLAYER
        self.pos = newPos 

        # tăng biến đếm số lần di chuyển
        self.moveCount += 1

    def draw(self, screen, offset):
        # vẽ nhân vật
        screen.blit(self.sprites[self.status+"_"+self.direction][int(self.animation_index/self.animation_delay)], (self.pos[0]*self.block_size + offset[0], self.pos[1]*self.block_size + offset[1]))  
