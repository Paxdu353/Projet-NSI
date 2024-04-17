import pygame
import Sprite

DEFAULT_SIZE = 16

class Block :

    def __init__(self, x, y, sprite : Sprite.Sprite, size = DEFAULT_SIZE, crossable = False):
        self.x = x
        self.y = y
        self.sprite = sprite
        self.hitbox = self.sprite.rect
        self.size = size
        self.crossable = crossable

        self.resize(size)

    
    def __repr__(self):
        return str([self.x, self.y, self.sprite])

    def collide(self, other_block):
        return self.hitbox.x < other_block.hitbox.x and self.hitbox.y < other_block.hitbox.y
    
    def draw(self, screen : pygame.Surface, scroll):
        self.hitbox.x = self.x*self.size - scroll[0]
        self.hitbox.y = self.y*self.size - scroll[1]
        if 0 <= self.hitbox.right and self.hitbox.left < screen.get_width() and 0 <= self.hitbox.bottom and self.hitbox.top < screen.get_height() :
            screen.blit(self.sprite.image, self.hitbox)
    
    def resize(self, size):
        self.size = size
        self.sprite.scale(size / DEFAULT_SIZE)
        self.hitbox = self.sprite.image.get_rect()


    def debug_draw(self, screen : pygame.Surface, x, y, scroll):
    self.hitbox.x = self.x * self.size + scroll[0]
    self.hitbox.y = self.y * self.size + scroll[1]
    screen.blit(self.sprite.image, (x + scroll[0], y + scroll[1]))

    
