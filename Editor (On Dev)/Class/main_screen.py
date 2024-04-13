import pygame
import os
pygame.init()


class MainScreen:

    def __init__(self, dimensions, titre):
        self.dimensions = dimensions
        self.titre = titre
        self.choice = None
        self.list_of_images = []
        self.screen = pygame.display.set_mode(self.dimensions, pygame.RESIZABLE, pygame.APPACTIVE)



        pygame.display.set_caption(self.titre)



        self.dossier_icon = pygame.image.load("../icon/dossier.png")
        self.back_icon = pygame.image.load("../icon/retour.png")
        self.settings_icon = pygame.image.load("../icon/settings.png")
        self.menu_icon = pygame.transform.rotate(pygame.transform.scale(pygame.image.load("../icon/menu.png").convert_alpha(), (64,64)), -90)
        self.menu_rect = pygame.Rect(self.menu_icon.get_rect())
        self.settings_rect = pygame.Rect(self.settings_icon.get_rect())
        self.folder_positions = []
        self.image_positions = []
        self.maps = []
        self.current_folder = None
        self.img_choice = []
        self.scroll = 5
        self.is_dragging = False
        self.is_close = False
        self.size = 500
        self.current_scroll = 1
        self.clock = pygame.time.Clock()



    def main(self):
        self.build_screen = pygame.Surface((self.scroll, self.screen.get_height()))
        self.resizable_menu = pygame.Rect(((self.build_screen.get_width() - 10), 0), (10, self.screen.get_height()))
        maximum_resize = self.screen.get_width() // 2
        minimum_resize = self.screen.get_height() // 4
        self.menu_rect.x = -5
        self.menu_rect.y = (self.screen.get_height() // 2) - self.menu_icon.get_height()//2

        self.settings_rect.x = self.screen.get_width() - self.settings_icon.get_width() - 10
        self.settings_rect.y = 10




        if self.is_dragging:
            self.is_close = False
            current_mouse_x, _ = pygame.mouse.get_pos()
            if current_mouse_x > maximum_resize:
                current_mouse_x = maximum_resize
            self.scroll = current_mouse_x + 5

            if self.resizable_menu.x < 0:
                self.resizable_menu.x = 0
            if self.resizable_menu.x > self.screen.get_width() - self.resizable_menu.width:
                self.resizable_menu.x = self.screen.get_width() - self.resizable_menu.width

        if -5 <= self.resizable_menu.x <= 5 and not self.is_dragging:
            self.is_close = True

        print(pygame.mouse.get_pressed())

        if pygame.mouse.get_pressed()[0]:
            if not self.is_dragging and not self.build_screen.get_rect().collidepoint(pygame.mouse.get_pos()):
                self.add_block(self.choice)
        elif pygame.mouse.get_pressed()[2]:
            if not self.is_dragging:
                self.remove_block()


        #print(max_img)
        for folder_name in os.listdir("../assets/sprites"):
            full_path = os.path.join("../assets/sprites", folder_name)

            if os.path.isdir(full_path):
                try:
                    self.folder_positions.index(full_path)
                except ValueError:
                    self.folder_positions.append(full_path)


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.resizable_menu.collidepoint(pygame.mouse.get_pos()) and not self.is_close:
                            if self.is_dragging == True:
                                self.is_dragging = False
                            else:
                                self.is_dragging = True

                        elif self.is_close and self.menu_rect.collidepoint(pygame.mouse.get_pos()):
                            self.is_close = False
                            self.scroll = minimum_resize

                        elif self.build_screen.get_rect().collidepoint(pygame.mouse.get_pos()):
                            if self.current_folder:
                                if self.back_icon.get_rect(topleft=(10, 10)).collidepoint(event.pos):
                                    self.current_folder = None
                                    self.img_choice = None
                                    self.image_positions.clear()
                                else:
                                    for img_path, pos in self.image_positions:
                                        img_rect = pygame.Rect(pos, (32, 32))
                                        img_rect.width = 40
                                        img_rect.height = 40
                                        img_rect.x -= 3
                                        img_rect.y -= 3
                                        if img_rect.collidepoint(event.pos):
                                            self.img_choice = img_rect
                                            self.choice = img_path

                            else:
                                start_x, start_y = 25, 25
                                step_x = self.dossier_icon.get_width() + 25
                                max_img = self.build_screen.get_width() // (step_x + 5)
                                n = 0
                                for path in self.folder_positions:
                                    if max_img == 0:
                                        break
                                    if n == max_img:
                                        start_y += 80
                                        start_x = 25
                                        n = 0
                                    rect_dossier = pygame.Rect((start_x, start_y), self.dossier_icon.get_size())
                                    print(rect_dossier.x, rect_dossier.y)
                                    start_x += step_x
                                    n += 1
                                    if rect_dossier.collidepoint(event.pos):
                                        self.current_folder = path
                                        break

                    elif event.button == 4:
                        if not self.build_screen.get_rect().collidepoint(event.pos):
                            self.scroll_tile(0.1)

                    elif event.button == 5:
                        if not self.build_screen.get_rect().collidepoint(event.pos):
                            self.scroll_tile(-0.1)


    def update(self):
        pass

    def draw(self):
        self.screen.fill((144, 144, 144))
        self.build_screen.fill((77, 77, 77))
        tile_size = self.scale(self.current_scroll, 64)



        if self.current_folder:
            if self.choice:
                pygame.draw.circle(self.screen, (0, 0, 0), (self.screen.get_width(), 0),
                                   (self.screen.get_width() // 10) + 5)

                pygame.draw.circle(self.screen, (255, 255, 255), (self.screen.get_width(), 0),
                                   self.screen.get_width()//10)

            x, y = 75, 25
            max_img = (self.build_screen.get_width() - 75) // 42
            n = 0
            self.image_positions.clear()
            for image in os.listdir(self.current_folder):
                if max_img == 0:
                    break
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
            start_x, start_y = 25, 25
            step_x = self.dossier_icon.get_width() + 25
            max_img = self.build_screen.get_width() // (step_x + 5)
            n = 0
            for path in self.folder_positions:
                if max_img == 0:
                    break
                if n == max_img:
                    start_y += 80
                    start_x = 25
                    n = 0
                self.build_screen.blit(self.dossier_icon, (start_x, start_y))
                label = pygame.font.Font(None, 24).render(os.path.basename(path), True, (255, 255, 255))
                self.build_screen.blit(label, (start_x+4, start_y + self.dossier_icon.get_height()))
                start_x += step_x
                n += 1

        for img in self.list_of_images:
            new = pygame.transform.scale(img, (64, 64))
            self.screen.blit(new, (pygame.mouse.get_pos()))

        if self.is_dragging:
            pygame.draw.rect(self.build_screen, (0, 255, 0), self.resizable_menu)
        else:
            pygame.draw.rect(self.build_screen, (255, 255, 255), self.resizable_menu)

        for _, (sprite, pos) in enumerate(self.maps):
            img_scaled = self.scale_sprite(self.current_scroll * 4, sprite)
            x, y = pos[0], pos[1]
            self.screen.blit(img_scaled, (x*tile_size, y*tile_size))


        for line in range(self.size):
            pygame.draw.line(self.screen, (255, 255, 255), (line * tile_size, 0),
                             (line * tile_size, 1080))
            pygame.draw.line(self.screen, (255, 255, 255), (0, line * tile_size), (self.size * tile_size, line * tile_size))



        self.screen.blit(self.build_screen, (0, 0))

        if self.is_close:
            pygame.draw.circle(self.screen, (255, 255, 255), (0, self.screen.get_height() // 2), 65)
            self.screen.blit(self.menu_icon, (-5, (self.screen.get_height() // 2) - self.menu_icon.get_height()//2))



        pygame.display.flip()

    def scroll_tile(self, next_index):
        if next_index == -0.1 and round(self.current_scroll, 1) == 0.2:
            self.current_scroll = 0.2

        elif round(self.current_scroll, 1) == 1 and next_index == 0.1:
            self.current_scroll = 1

        else:
            self.current_scroll = self.current_scroll + next_index
            self.current_scroll = round(self.current_scroll, 1)


    def add_block(self, path):
        try:
            tile_size = self.scale(self.current_scroll, 64)
            x, y = pygame.mouse.get_pos()
            x = x // tile_size
            y = y // tile_size
            img = pygame.image.load(path)
            for img, pos in self.maps:
                if pos == [x, y]:
                    print('deja')
                    return

            self.maps.append((img, [x, y]))
        except TypeError:
            pass


    def remove_block(self):

        for _, (image, pos) in enumerate(self.maps):
            print(image, pos)
            tile_size = self.scale(self.current_scroll, 64)
            rect = image.get_rect()
            rect.x = pos[0] * tile_size
            rect.y = pos[1] * tile_size
            rect.width = tile_size
            rect.height = tile_size
            if rect.collidepoint(pygame.mouse.get_pos()):
                self.maps.pop(_)

    def scale(self, factor, dimension):
        return int(dimension * factor)

    def scale_sprite(self, factor, image):
        new_height = int(image.get_height() * factor)
        new_width = int(image.get_width() * factor)
        return pygame.transform.scale(image, (new_width, new_height))


    def run(self):
        while True:
            self.main()
            self.update()
            self.draw()

            self.clock.tick(60)


s = MainScreen((500, 500), 'Map Editor')
s.run()
