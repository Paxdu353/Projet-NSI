import pygame

class Block:

    def __init__(self, x, y, sprite, crossable = True):
        self.x = x
        self.y = y
        self.sprite = sprite
        self.hitbox = self.sprite.rect
        self.crossable = crossable

    def draw(self, screen, scroll):
        self.hitbox.x = self.x - scroll[0]
        self.hitbox.y = self.y - scroll[1]
        if 0 <= self.hitbox.x < screen.get_width() and 0 <= self.hitbox.y < screen.get_height():
            screen.blit(self.sprite.image, self.hitbox)

    def __repr__(self):
        return f"X: {self.x}, Y: {self.y}, Filename: {self.sprite.filename}"

        
pygame.init()

LARGEUR_ECRAN, HAUTEUR_ECRAN = 500, 400
TAILLE_ECRAN = (LARGEUR_ECRAN, HAUTEUR_ECRAN)

screen = pygame.display.set_mode(TAILLE_ECRAN)
