from fileinput import filename
from tarfile import BLOCKSIZE
import Block, Sprite, pygame

class Item :

    def __init__(self, filename = None) :
        """ Création d'un item
        
        `filename` : si renseigné, charge l'item depuis un fichier """

        self.x = 0
        self.y = 0
        self.blocks = []

        if filename != None:
            with open(filename, "r") as fichier:
                contenu = fichier.readlines()
                print(contenu)
                for block in contenu:
                    block = block.split(",")
                    block[2] = block[2][:-1]
                    self.add(int(block[0]), int(block[1]), int(block[2]))
                    print(block)

                

    def add(self, x, y, id_sprite, size = Block.DEFAULT_SIZE):
        """ Ajoute un bloc à la liste

        x,y : coordonnées relatives du bloc
        id_sprite : id du sprite choisi pour le bloc
         """
        sprite = Sprite.Sprite(id_sprite)
        block = Block.Block(x / size, y / size, sprite, size)
        self.blocks.append(block)

    def draw(self, screen, scroll):
        for block in self.blocks:
            block.draw(screen , scroll)
    
    def draw_debug(self, screen : pygame.Surface, size):
        for block in self.blocks:
            block.resize(size)
            block.draw(screen , (0,0))
        
        # Dessin des lignes verticales
        for x in range(size, screen.get_width(), size):
            pygame.draw.line(screen, (255,0,0), (x, 0), (x, screen.get_height()))
        # Dessin des lignes horizontale
        for y in range(size, screen.get_height(), size):
            pygame.draw.line(screen, (255,0,0), (0, y), (screen.get_width(), y))
    
    def save(self, filename):
        pass
