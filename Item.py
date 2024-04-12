import Block, Sprite, pygame

class Item :

    def __init__(self) :
        
        self.x = 0
        self.y = 0
        self.blocks = []

    def add (self, x, y, id_sprite):
        sprite = Sprite.Sprite(id_sprite)
        block = Block.Block(x, y, sprite)
        self.blocks.append(block)

    def draw(self, screen, scroll):
        for block in self.blocks:
            block.draw(screen , scroll)
    
    def draw_debug(self, screen : pygame.Surface, zoom_factor):
        self.zoom(zoom_factor)
        for block in self.blocks:
            block.draw(screen , (0,0))
        
        # Dessin des lignes verticales
        for x in range(16*zoom_factor, screen.get_width(), 16*zoom_factor):
            pygame.draw.line(screen, (255,0,0), (x, 0), (x, screen.get_height()))
        # Dessin des lignes horizontale
        for y in range(16*zoom_factor, screen.get_height(), 16*zoom_factor):
            pygame.draw.line(screen, (255,0,0), (0, y), (screen.get_width(), y))

    def move(self, x, y):
        self.x = x
        self.y = y
        
        for block in self.blocks:
            block.x += x
            block.y += y
    
    def zoom(self, factor):
        for block in self.blocks:
            block.sprite.scale(factor)
            block.x *= factor
            block.y *= factor

"""
    
    def load(self, filename):
    
    def save(self, filename):
        
"""
