import pygame

from Block import *
class Map:
    """
    :param blocks: Liste de blocks de la classe 'Block' -> Hérite de la classe 'Sprite'
    :param objects: Liste d'objet de la classe 'Block' -> Hérite de la classe 'Sprite'

    """

    def __init__(self, blocks: [Block], objects: [Block]):
        self.Blocks = blocks
        self.Objects = objects


    def draw(self, screen: pygame.Surface, scroll: tuple):
        '''
        :param scroll: Scroll de la map en fonction de chaque joueur présent sur la map de type tuple (int, int)
        :return: Nothing
        '''
        for block in self.Blocks + self.Objects:
            block.draw(screen, scroll)


    def load_map(self):
        """
        Permet de charger une map présente sur un fichier
        :return: Nothing
        """
        pass


    def save_map(self):
        """
        Permet de sauvegarder une map sur un fichier

        :return:
        """
        pass

    def __repr__(self):
        return f'Blocks list: {self.Blocks}\n Objects list: {self.Objects}'
