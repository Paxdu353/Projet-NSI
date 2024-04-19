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
                    block[3] = block[3][:-1]
                    self.add(int(block[0]), int(block[1]), int(block[2]), int(block[3]))
                    print(block)

                

    def add(self, x, y, id_sprite, crossable = False, size = Block.DEFAULT_SIZE):
        """ Ajoute un bloc à la liste

        x,y : coordonnées relatives du bloc
        id_sprite : id / liste d'id du sprite choisi pour le bloc
         """
        
        sprite = Sprite.Sprite(id_sprite)
        if crossable == 0:
            block = Block.Block(x / size, y / size, sprite, size)
        if crossable == 1:
            block = Block.Block(x / size, y / size, sprite, size, True)
        else:
            block = Block.Block(x / size, y / size, sprite, size, crossable)
        self.blocks.append(block)

    def draw(self, screen, scroll):
        for block in self.blocks:
            block.draw(screen , scroll)
    
    def draw_debug(self, screen : pygame.Surface, size):
        for block in self.blocks:
            block.resize(size)
            block.draw(screen , (0,0))

            if block.crossable:
                surface = pygame.Surface(block.hitbox.size, pygame.SRCALPHA)
                pygame.draw.rect(surface, (255,0,0,127), surface.get_rect())
                screen.blit(surface, block.hitbox)
            else:
                surface = pygame.Surface(block.hitbox.size, pygame.SRCALPHA)
                pygame.draw.rect(surface, (0,255,0,127), surface.get_rect())
                screen.blit(surface, block.hitbox)
        
        # Dessin des lignes verticales
        for x in range(size, screen.get_width(), size):
            pygame.draw.line(screen, (255,0,0), (x, 0), (x, screen.get_height()))
        # Dessin des lignes horizontale
        for y in range(size, screen.get_height(), size):
            pygame.draw.line(screen, (255,0,0), (0, y), (screen.get_width(), y))
    
    def save(self, filename):
        with open(filename, "w") as fichier:
            for block in self.blocks:
                c = 0
                if block.crossable:
                    c = 1
                fichier.write(f"{int(block.x*16)},{int(block.y*16)},{block.sprite.id},{c}\n")
