import pygame
import os
import SPRITES
import glob



class Sprite(pygame.sprite.Sprite):
    """
    :param id: correspond au sprite dans le dictionnaire 'SPRITES'
    """

    def __init__(self, id):
        super().__init__()
        try:
            self.filename = glob.glob(f'{os.path.dirname(SPRITES.__file__)}/sprites/Zombie-Tileset---_*_Capa-{id}.png')[0]
            self.image = pygame.image.load(self.filename).convert_alpha()

        except IndexError:
            self.filename = glob.glob(f'{os.path.dirname(SPRITES.__file__)}/sprites/bug_sprite.png')[0]
            self.image = pygame.image.load(self.filename).convert_alpha()

        '''except IndexError:
            raise IndexError(f'Le sprite {id} n\'existe pas')'''

        self.id = id
        self.rect = self.image.get_rect()

        # CONSTANTE
        self.screen = pygame.display.get_surface()

    def draw_debug(self, x, y):
        """
            :param x: x position de type int
            :param y: y position de type int

            Affiche le sprite sur la surface self.screen
            :return: Nothing
        """
        self.screen.blit(self.image, (x, y))

    def scale(self, factor):
        """

        :param factor: Facteur d'agrandissement de type int
        Permet de redimmensionner le sprite
        :return: Nothing
        """
        self.image = pygame.image.load(self.filename).convert_alpha()
        new_height = self.image.get_height() * factor
        new_width = self.image.get_width() * factor

        self.image = pygame.transform.scale(self.image, (new_width, new_height))

    def __repr__(self):
        return f"ID: {self.id}, FileName: {self.filename}"

