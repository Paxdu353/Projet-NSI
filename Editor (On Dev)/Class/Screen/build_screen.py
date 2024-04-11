import os
import pygame
from Class.Multiple_Screen import Ecran






class BuildScreen(Ecran):

    def run(self, queue):
        global current_choice
        pygame.init()
        screen = pygame.display.set_mode(self.dimensions, pygame.RESIZABLE)
        pygame.display.set_caption(self.titre)
        clock = pygame.time.Clock()

        dossier_icon = pygame.image.load("../icon/dossier.png")
        back_icon = pygame.image.load("../icon/retour.png")
        folder_positions = []
        image_positions = []
        current_folder = None
        img_choice = None

        start_x, start_y = 50, 50
        step_x = dossier_icon.get_height() + 20
        for folder_name in os.listdir("../assets/sprites"):
            full_path = os.path.join("../assets/sprites", folder_name)
            if os.path.isdir(full_path):
                folder_positions.append((full_path, (start_x, start_y)))
                start_x += step_x

        running = True
        while running:


            for evenement in pygame.event.get():
                if evenement.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif evenement.type == pygame.MOUSEBUTTONDOWN:
                    if current_folder:
                        if back_icon.get_rect(topleft=(10, 10)).collidepoint(evenement.pos):
                            current_folder = None
                            image_positions.clear()
                        else:
                            for img_path, pos in image_positions:
                                img_rect = pygame.Rect(pos, (32, 32))
                                img_rect.width= 40
                                img_rect.height = 40
                                img_rect.x -= 3
                                img_rect.y -= 3
                                if img_rect.collidepoint(evenement.pos):
                                    img_choice = img_rect
                                    queue.put(img_path)


                    else:
                        for path, pos in folder_positions:
                            icon_rect = pygame.Rect(pos, dossier_icon.get_size())
                            if icon_rect.collidepoint(evenement.pos):
                                current_folder = path
                                break

            screen.fill((77, 77, 77))
            if img_choice:
                pygame.draw.rect(screen, (0, 255, 255), img_choice)
            if current_folder:
                x, y = 75, 25
                max_img = (screen.get_width() - 75) // 42
                n = 0
                image_positions.clear()
                for image in os.listdir(current_folder):
                    if image.lower().endswith(('.png', '.jpg', '.jpeg')):
                        img_path = os.path.join(current_folder, image)
                        img = pygame.image.load(img_path).convert_alpha()
                        img = pygame.transform.scale(img, (32, 32))
                        if n == max_img:
                            y += 50
                            x = 75
                            n = 0
                        screen.blit(img, (x, y))
                        image_positions.append((img_path, (x, y)))
                        x += img.get_width() + 10
                        n += 1
                screen.blit(back_icon, (10, 10))
            else:
                for path, pos in folder_positions:
                    screen.blit(dossier_icon, pos)
                    label = pygame.font.Font(None, 24).render(os.path.basename(path), True, (255, 255, 255))
                    screen.blit(label, (pos[0], pos[1] + dossier_icon.get_height()))

            pygame.display.flip()
            clock.tick(60)


