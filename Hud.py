import pygame

pygame.init()
pygame.font.init()

WINDOW_X, WINDOW_Y = 1200,800
h1 = 84
h2 = 108
h3 = 20

ecran = pygame.display.set_mode((WINDOW_X, WINDOW_Y), pygame.RESIZABLE)
clock = pygame.time.Clock()
run = True

font = pygame.font.SysFont(None, 30)
i = 0

class HUD  :
    def __init__(self):
        self.texts = []


    def write(self,screen, text,size,x,y):
        text = font.render(text, False, (0, 0, 255))
        screen.blit(text, (x, y))

    def draw(self,screen):
        WINDOW_X = screen.get_width()
        WINDOW_Y = screen.get_height()
        pygame.draw.polygon(ecran, (0,0,0),[(0,WINDOW_Y - h1),(250 ,WINDOW_Y - h1 ),(300,WINDOW_Y - h3),(WINDOW_X-250,WINDOW_Y - h3),(WINDOW_X-200,WINDOW_Y-h2),(WINDOW_X,WINDOW_Y-h2),(WINDOW_X,WINDOW_Y),(0,WINDOW_Y)])


hud = HUD()

while run:
    pygame.display.update()
    clock.tick(40)
    event_list = pygame.event.get()



    ecran.fill((255,255,255)) # Fill window
    hud.draw(ecran)
    hud.write(ecran, "test", 10, 50, 50)






    for event in event_list:
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()
        elif event.type == pygame.VIDEORESIZE: # Redimensionnement écran
            WINDOW_X = event.w
            WINDOW_Y = event.h
            ecran = pygame.display.set_mode((WINDOW_X, WINDOW_Y), pygame.RESIZABLE)
    pygame.display.flip()