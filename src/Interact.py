from pygame import draw, font, Rect
from HandleImage import getImage
import Constant

notification = None

class Alert:
    def __init__(self,width,height,title,message,backgroundColor = (142, 205, 221),borderColor = (34, 102, 141), closeAction = None):
        x = (Constant.SCREEN_WIDTH - width)//2
        y = (Constant.SCREEN_HEIGHT - height)//2
        self.rect = Rect(x,y,width,height)
        self.title = font.SysFont(Constant.FONT_FAMILY, 30).render(title,True,(0,0,0))
        self.titleRect = self.title.get_rect()
        self.message = font.SysFont(Constant.FONT_FAMILY, 25).render(message,True,(0,0,0))
        self.messageRect = self.message.get_rect()  
        self.border = 4
        self.closeButton = Button("Close",x + (width - 100)//2,y + height - 50,100,40,2,(255, 250, 221),(255, 204, 112),(0, 0, 0), closeAction)
        self.backgroundColor = backgroundColor
        self.borderColor = borderColor

    def checkClick(self,mousePos):  
        self.closeButton.checkClick(mousePos)

    def resize(self,width,height):
        x = (width - self.rect.width)//2
        y = (height - self.rect.height)//2
        self.rect.x = x
        self.rect.y = y
        self.closeButton.resize(x + (self.rect.width - 100)//2,y + self.rect.height - 50,100,40)

    def draw(self,screen):
        draw.rect(screen,self.backgroundColor,self.rect,int(self.rect.height//2),int(self.rect.width//20))
        draw.rect(screen,self.borderColor,self.rect,self.border,int(self.rect.width//20))
        screen.blit(self.title,(self.rect.x + (self.rect.width - self.titleRect.width)//2,self.rect.y + 10))
        screen.blit(self.message,(self.rect.x + (self.rect.width - self.messageRect.width)//2,self.rect.y + (self.rect.height - self.messageRect.height - 45 - 10)//2))
        self.closeButton.draw(screen)
        
class Comfirm:
    def __init__(self,width, height, title, message, backgroundColor, borderColor, leftAction, rightAction, closeAction = None, leftTitle = "No", rightTitle = "Yes", ):
        x = (Constant.SCREEN_WIDTH - width)//2
        y = (Constant.SCREEN_HEIGHT - height)//2
        self.rect = Rect(x,y,width,height)
        self.title = font.SysFont(Constant.FONT_FAMILY, 25).render(title,True,(0,0,0))
        self.titleRect = self.title.get_rect()
        self.message = font.SysFont(Constant.FONT_FAMILY, 20).render(message,True,(0,0,0))
        self.messageRect = self.message.get_rect()  
        self.border = 4
        self.backgroundColor = backgroundColor
        self.borderColor = borderColor
        self.closeButton = None
        self.interactInit(x,y,width,height, rightAction, leftAction, closeAction, rightTitle, leftTitle)

    def interactInit(self,x,y,width,height, rightAction, leftAction, closeAction, rightTitle, leftTitle):
        gap = (width - 300)//3
        self.leftButton = Button(leftTitle,x + gap,y + height - 50, 150,40,2,(255, 250, 221),(255, 204, 112),(0, 0, 0), leftAction)
        self.rightButton = Button(rightTitle,x + gap*2 + 150,y + height - 50, 150,40,2,(255, 250, 221),(255, 204, 112),(0, 0, 0), rightAction)
        if(closeAction != None):  
            self.closeButton = Button2("", x,y,50,50,2,(0,0,0),"Close.png",closeAction)
    def resize(self,width,height):
        x = (width - self.rect.width)//2
        y = (height - self.rect.height)//2
        self.rect.x = x
        self.rect.y = y
        self.interactInit(x,y,width,height)

    def checkClick(self,mousePos):
        self.leftButton.checkClick(mousePos)
        self.rightButton.checkClick(mousePos)
        if(self.closeButton != None):
            self.closeButton.checkClick(mousePos)
    
    def draw(self,screen):
        draw.rect(screen,self.backgroundColor,self.rect,int(self.rect.height//2),int(self.rect.width//20))
        draw.rect(screen,self.borderColor,self.rect,self.border,int(self.rect.width//20))
        screen.blit(self.title,(self.rect.x + (self.rect.width - self.titleRect.width)//2,self.rect.y + 10))
        screen.blit(self.message,(self.rect.x + (self.rect.width - self.messageRect.width)//2,self.rect.y + (self.rect.height - self.messageRect.height - 45 - 10)//2))
        self.leftButton.draw(screen)
        self.rightButton.draw(screen)
        if(self.closeButton != None):
            self.closeButton.draw(screen)

class Button:
    def __init__(self,text,x,y,width,height,border,colorBackground,colorBorder,colorText,action, fixed = False):
        self.rect = Rect(x,y,width,height)
        self.border = border
        self.colorBackground = colorBackground
        self.colorBorder = colorBorder
        self.colorText = colorText
        self.action = action
        self.fixed = fixed
        self.updateText(text)

    def updateText(self,text):
        self.text = text
        self.txt_surface = font.SysFont(Constant.FONT_FAMILY, 20).render(self.text,True,self.colorText)
        self.textRect =  self.txt_surface.get_rect()

    def resize(self,x,y,width,height):
        self.rect = Rect(x,y,width,height)
    
    def draw(self,screen, offset = (0,0)):
        if(self.fixed): offset = (0,0)
        draw.rect(screen,self.colorBackground,(self.rect.x + offset[0], self.rect.y + offset[1], self.rect.width, self.rect.height) ,int(min(self.rect.height,self.rect.width)/2),min(self.rect.height,self.rect.width)//8)
        draw.rect(screen,self.colorBorder,(self.rect.x + offset[0], self.rect.y + offset[1], self.rect.width, self.rect.height),self.border,min(self.rect.height,self.rect.width)//8)
        screen.blit(self.txt_surface,(self.rect.x + (self.rect.width - self.textRect.width)//2 + offset[0], self.rect.y + (self.rect.height - self.textRect.height)//2 + offset[1]))
    
    def checkClick(self,mousePos, offset = (0,0)):
        if(self.fixed): offset = (0,0)
        newRect = Rect(self.rect.x + offset[0], self.rect.y + offset[1], self.rect.width, self.rect.height)
        if(newRect.collidepoint(mousePos)):
            self.action()

class Button2:
    def __init__(self,text, x, y, width, height, border, colorText, imagePath, action, fixed = False):
        self.rect = Rect(x,y,width,height)
        self.colorText = colorText
        self.action = action
        self.image = getImage(imagePath, width, height)
        self.border = border
        self.fixed = fixed
        if(text != None):
            self.updateText(text)
        else:
            self.text = None

    def updateText(self,text):
        self.text = text
        self.txt_surface = font.SysFont(Constant.FONT_FAMILY,int(self.rect.height*0.5)).render(self.text,True,self.colorText)
        self.txt_surface_border = font.SysFont(Constant.FONT_FAMILY,int(self.rect.height*0.5)).render(self.text,True,(255,255,255))

    def resize(self,x,y,width,height):
        self.rect = Rect(x,y,width,height)
    
    def draw(self,screen, offset = (0,0)):
        if(self.fixed): offset = (0,0)
        screen.blit(self.image,(self.rect.x + offset[0],self.rect.y + offset[1]))
        if(self.text!=None):
            if(self.border > 0):
                screen.blit(self.txt_surface_border,(self.rect.x + (self.rect.width - self.txt_surface_border.get_width())//2 + offset[0] - self.border, self.rect.y + (self.rect.height - self.txt_surface_border.get_height())//2 + offset[1]))
                screen.blit(self.txt_surface_border,(self.rect.x + (self.rect.width - self.txt_surface_border.get_width())//2 + offset[0] + self.border, self.rect.y + (self.rect.height - self.txt_surface_border.get_height())//2 + offset[1]))
                screen.blit(self.txt_surface_border,(self.rect.x + (self.rect.width - self.txt_surface_border.get_width())//2 + offset[0], self.rect.y + (self.rect.height - self.txt_surface_border.get_height())//2 + offset[1] - self.border))
                screen.blit(self.txt_surface_border,(self.rect.x + (self.rect.width - self.txt_surface_border.get_width())//2 + offset[0], self.rect.y + (self.rect.height - self.txt_surface_border.get_height())//2 + offset[1] + self.border))
            screen.blit(self.txt_surface,(self.rect.x + (self.rect.width - self.txt_surface.get_width())//2 + offset[0], self.rect.y + (self.rect.height - self.txt_surface.get_height())//2 + offset[1]))

    def checkClick(self,mousePos, offset = (0,0)):
        if(self.fixed): offset = (0,0)
        newRect = Rect(self.rect.x + offset[0], self.rect.y + offset[1], self.rect.width, self.rect.height)
        if(newRect.collidepoint(mousePos)):
            self.action()

def createComfirm(width, height, title, message, backgroundColor, borderColor, leftAction, rightAction, closeAction = None, titleLeft = "No", titleRight = "Yes"):
    global notification
    notification = Comfirm(width, height, title, message, backgroundColor, borderColor, leftAction, rightAction, closeAction, titleLeft, titleRight)

def createAlert(width,height,title,message,backgroundColor = (142, 205, 221),borderColor = (34, 102, 141), closeAction = None):
    global notification
    notification = Alert(width,height,title,message,backgroundColor,borderColor,closeAction)

def closeNotification():
    global notification
    notification = None