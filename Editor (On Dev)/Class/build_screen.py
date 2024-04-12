import os
import pygame

pygame.init()







class BuildScreen:
    def __init__(self, dimensions):
        self.dimensions = dimensions
        self.build_screen = pygame.Surface(self.dimensions)
        self.clock = pygame.time.Clock()

        self.dossier_icon = pygame.image.load("../icon/dossier.png")
        self.back_icon = pygame.image.load("../icon/retour.png")

        self. folder_positions = []
        self.image_positions = []
        self.current_folder = None
        self.choice = None
        self.img_choice = []


    def build_main(self):
        start_x, start_y = 50, 50
        step_x = self.dossier_icon.get_height() + 20
        for folder_name in os.listdir("../assets/sprites"):
            full_path = os.path.join("../assets/sprites", folder_name)
            if os.path.isdir(full_path):
                self.folder_positions.append((full_path, (start_x, start_y)))
                start_x += step_x


            for evenement in pygame.event.get():
                if evenement.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif evenement.type == pygame.MOUSEBUTTONDOWN:
                    if self.current_folder:
                        if self.back_icon.get_rect(topleft=(10, 10)).collidepoint(evenement.pos):
                            self.current_folder = None
                            self.image_positions.clear()
                        else:
                            for img_path, pos in self.image_positions:
                                img_rect = pygame.Rect(pos, (32, 32))
                                img_rect.width= 40
                                img_rect.height = 40
                                img_rect.x -= 3
                                img_rect.y -= 3
                                if img_rect.collidepoint(evenement.pos):
                                    self.img_choice = img_rect
                                    self.choice = img_path


                    else:
                        for path, pos in self.folder_positions:
                            icon_rect = pygame.Rect(pos, self.dossier_icon.get_size())
                            if icon_rect.collidepoint(evenement.pos):
                                self.current_folder = path
                                break




    def build_update(self):
        pass


    def build_draw(self):
        self.build_screen.fill((77, 77, 77))

        if self.current_folder:
            if self.img_choice:
                pygame.draw.rect(self.build_screen, (0, 255, 255), self.img_choice)
            x, y = 75, 25
            max_img = (self.build_screen.get_width() - 75) // 42
            n = 0
            self.image_positions.clear()
            for image in os.listdir(self.current_folder):
                if image.lower().endswith(('.png', '.jpg', '.jpeg')):
                    img_path = os.path.join(self.current_folder, image)
                    img = pygame.image.load(img_path).convert_alpha()
                    img = pygame.transform.scale(img, (32, 32))
                    if n == max_img:
                        y += 50
                        x = 75
                        n = 0
                    self.build_screen.blit(img, (x, y))
                    self.image_positions.append((img_path, (x, y)))
                    x += img.get_width() + 10
                    n += 1
            self.build_screen.blit(self.back_icon, (10, 10))
        else:
            for path, pos in self.folder_positions:
                self.build_screen.blit(self.dossier_icon, pos)
                label = pygame.font.Font(None, 24).render(os.path.basename(path), True, (255, 255, 255))
                self.build_screen.blit(label, (pos[0], pos[1] + self.dossier_icon.get_height()))

        pygame.display.flip()


    def build_run(self):
        while True:
            self.build_main()
            self.build_update()
            self.build_draw()

            self.clock.tick(60)




