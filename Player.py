import Block, pygame, math

import Sprite

DEFAULT_SPEED = 10

class Player(Block.Block):
    def __init__(self, x, y, sprite_dic, size):
        self.vx = 0
        self.vy = 0
        self.scroll = [0,0]
        self.sprite_dic = sprite_dic

        super().__init__(x,y,self.sprite_dic["DOWN"])
        self.resize(size)
    
    def check_moves(self):
        self.vx, self.vy = 0, 0

        if pygame.key.get_pressed()[pygame.K_DOWN]:
            self.vy += 1
            self.sprite = self.sprite_dic["DOWN"]
            
        if pygame.key.get_pressed()[pygame.K_LEFT]:
            self.vx += -1
            self.sprite = self.sprite_dic["LEFT"]

        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            self.vx += 1
            self.sprite = self.sprite_dic["RIGHT"]

        if pygame.key.get_pressed()[pygame.K_UP]:
            self.vy += -1
            self.sprite = self.sprite_dic["UP"]
        
        norme = math.sqrt(self.vx**2 + self.vy**2)
        if norme != 0:
            self.vx = self.vx / norme * DEFAULT_SPEED
            self.vy = self.vy / norme * DEFAULT_SPEED

    def move(self, blocks):
        collision = False
        for block in blocks:
            if self.collide(block):
                collision = True
                break
               
        if not collision:
            self.x += self.vx
            self.y += self.vy
            self.scroll[0] += self.vx
            self.scroll[1] += self.vy

        self.scroll[0] = min(400, self.x-400)
        self.scroll[0] = max(0, self.x-400)

    def resize(self, size):
        self.size = size
        for sprite in self.sprite_dic.values():
            sprite.scale(size / Block.DEFAULT_SIZE)
        
        self.hitbox = self.sprite.image.get_rect()

    def update(self):
        """ Si le personnage est immobile, on ne fait rien
        Sinon, si le sprite est un animatedSprite, on appelle la méthode update
        du sprite """

        if self.vx != 0 or self.vy != 0:
            self.sprite.update()
