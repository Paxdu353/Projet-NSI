import pygame

pygame.init()
pygame.font.init()

h1 = 84
h2 = 108
h3 = 20

class HUD  :
    def __init__(self):
        self.font = pygame.font.SysFont(None, 30)

    def write(self,screen, text,size,x,y):
        text = self.font.render(text, False, (0, 0, 255))
        screen.blit(text, (x, y))

    def draw(self,screen):
        WINDOW_X = screen.get_width()
        WINDOW_Y = screen.get_height()
        pygame.draw.polygon(screen, (0,0,0),[(0,WINDOW_Y - h1),(250 ,WINDOW_Y - h1 ),(300,WINDOW_Y - h3),(WINDOW_X-250,WINDOW_Y - h3),(WINDOW_X-200,WINDOW_Y-h2),(WINDOW_X,WINDOW_Y-h2),(WINDOW_X,WINDOW_Y),(0,WINDOW_Y)])
