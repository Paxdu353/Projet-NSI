import pygame
from queue import Empty
from Class.Multiple_Screen import Ecran

class MainScreen(Ecran):
    def run(self, queue):
        pygame.init()
        screen = pygame.display.set_mode(self.dimensions, pygame.RESIZABLE)
        pygame.display.set_caption("Main Screen")
        clock = pygame.time.Clock()
        list_of_images = []

        while True:
            for evenement in pygame.event.get():
                if evenement.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                elif evenement.type == pygame.MOUSEBUTTONDOWN:
                    if evenement.button == 1:
                        try:
                            choice = queue.get_nowait()
                            print(choice)
                            if choice:
                                choice = choice.replace('\\', '/')
                                list_of_images.append(choice)
                        except Empty:
                            pass

            screen.fill((0, 120, 230))

            for img in list_of_images:
                image = pygame.image.load(img)
                new = pygame.transform.scale(image, (64, 64))
                screen.blit(new, (pygame.mouse.get_pos()))

            pygame.display.flip()
            clock.tick(60)
