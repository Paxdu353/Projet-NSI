import pygame
import Sprite

class Block :

    def __init__(self, x, y, sprite : Sprite.Sprite, crossable = True):
        self.x = x
        self.y = y
        self.sprite = sprite
        self.hitbox = self.sprite.rect
        self.crossable = crossable
    
    def __repr__(self):
        return str([self.x, self.y, self.sprite])

    def draw(self, screen : pygame.Surface, scroll):
        self.hitbox.x = self.x - scroll[0]
        self.hitbox.y = self.y - scroll[1]
        if 0 <= self.hitbox.x < screen.get_width() and 0 <= self.hitbox.y < screen.get_height() :
            screen.blit(self.sprite.image, self.hitbox)  
