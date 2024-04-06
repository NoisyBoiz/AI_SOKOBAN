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
        if(self.animation_index/self.animation_delay < len(self.sprites[self.status+"_"+self.direction]) - 1):
            self.animation_index += 1
        else:
            self.animation_index = 0

    def handleAutoMove(self, action, map):  
        self.autoMoveIndex += 1
        if(self.autoMoveIndex%self.autoMoveDelay!=1): return
        if(self.autoMoveIndex//self.autoMoveDelay < len(action)):
            d = action[self.autoMoveIndex//self.autoMoveDelay]
            newPos = (self.pos[0] + d[0], self.pos[1] + d[1])
            if(map[newPos[0]][newPos[1]] == Constant.WALL): return
            if(map[newPos[0]][newPos[1]] == 2 or map[newPos[0]][newPos[1]] == 5):
                nextNewPos = (newPos[0] + d[0], newPos[1] + d[1])
                if(map[nextNewPos[0]][nextNewPos[1]] == Constant.WALL or map[nextNewPos[0]][nextNewPos[1]] == Constant.BOX or map[nextNewPos[0]][nextNewPos[1]] == Constant.BOXSOLVE): return
                map[nextNewPos[0]][nextNewPos[1]] += 2
                map[newPos[0]][newPos[1]] -= 2
            map[self.pos[0]][self.pos[1]] -= 1
            map[newPos[0]][newPos[1]] += 1
            self.pos = newPos 
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

        newPos = (self.pos[0] + d[0], self.pos[1] + d[1])

        if(map[newPos[0]][newPos[1]] == Constant.WALL): return
        if(map[newPos[0]][newPos[1]] == 2 or map[newPos[0]][newPos[1]] == 5):
            nextNewPos = (newPos[0] + d[0], newPos[1] + d[1])
            if(map[nextNewPos[0]][nextNewPos[1]] == Constant.WALL or map[nextNewPos[0]][nextNewPos[1]] == Constant.BOX or map[nextNewPos[0]][nextNewPos[1]] == Constant.BOXSOLVE): return
            map[nextNewPos[0]][nextNewPos[1]] += 2
            map[newPos[0]][newPos[1]] -= 2
        map[self.pos[0]][self.pos[1]] -= 1
        map[newPos[0]][newPos[1]] += 1
        self.pos = newPos 
        self.moveCount += 1

    def draw(self, screen, offset):
        screen.blit(self.sprites[self.status+"_"+self.direction][int(self.animation_index/self.animation_delay)], (self.pos[0]*self.block_size + offset[0], self.pos[1]*self.block_size + offset[1]))  
