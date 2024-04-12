import pygame
import Sprite, Block, Item

pygame.init()

LARGEUR_ECRAN, HAUTEUR_ECRAN = 500, 400
TAILLE_ECRAN = (LARGEUR_ECRAN, HAUTEUR_ECRAN)

screen = pygame.display.set_mode(TAILLE_ECRAN)

obj= Item.Item()
obj.add(0,0,9)
obj.add(16,0,9)

screen.fill((30,30,30))

obj.draw_debug(screen, 5)
pygame.display.flip()

continuer = True

while continuer:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            continuer = False