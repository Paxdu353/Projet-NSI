import Sprite
import pygame

class AnimatedSprite():

    def __init__(self, liste, animation_time = 200):
        self.sprite_list = []
        self.index = 0 # Index du sprite courant
        self.last_update_time = pygame.time.get_ticks()
        for id in liste:
            # Chargement du sprite et ajout à la liste des sprites
            self.sprite_list.append(Sprite.Sprite(id))

        self.animation_time = animation_time

    def draw_debug(self, x, y):
        # Affiche le sprite aux coordonnées x,y
        self.sprite_list[self.index].draw_debug(x,y)

    def scale(self, factor):
        # Scale de tous les sprites de la liste
        for sprite in self.sprite_list:
            sprite.scale(factor)



    def update(self):
        current_time = pygame.time.get_ticks()
        print(current_time)
        if current_time - self.last_update_time > self.animation_time:
            self.index = (self.index + 1) % len(self.sprite_list)
            self.last_update_time = current_time

        print(self.index)

