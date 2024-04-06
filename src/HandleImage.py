from pygame import image, transform, SRCALPHA, Surface, Rect
from os import getcwd
from os.path import join

def splitSpriteImgPath(path, original_width, original_height, new_width, new_height, direction=False):
    fullPath = join(getcwd(),"assets","Image", path + ".png")
    imgName = path
        
    all_sprites = {}
    sprite_sheet = image.load(fullPath).convert_alpha()
    sprites = []
    for i in range(sprite_sheet.get_width() // original_width):
        surface = Surface((original_width, original_height), SRCALPHA, 32)
        rect = Rect(i * original_width, 0, original_width, original_height)
        surface.blit(sprite_sheet, (0, 0), rect)
        sprites.append(transform.scale(surface,(new_width, new_height)))
    if direction:
        all_sprites[imgName + "_right"] = sprites
        all_sprites[imgName + "_left"] = [transform.flip(sprite, True, False) for sprite in sprites]
    else:
        all_sprites[imgName] = sprites
    return all_sprites

def getImage(path, width, height):
    fullPath = join(getcwd(),"assets","Image", path)
    img = image.load(fullPath).convert_alpha()
    return transform.scale(img, (width, height))
