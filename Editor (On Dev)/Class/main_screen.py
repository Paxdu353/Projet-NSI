import pygame
import os
import SPRITES
from Block import Block
from AnimatedSpite import AnimatedSpite
from Sprite import Sprite
import glob
pygame.init()


class MainScreen:

    def __init__(self, dimensions, titre):
        self.dimensions = dimensions
        self.titre = titre
        self.choice = None
        self.screen = pygame.display.set_mode(self.dimensions, pygame.RESIZABLE, pygame.APPACTIVE)



        pygame.display.set_caption(self.titre)



        self.dossier_icon = pygame.image.load("../icon/dossier.png")
        self.back_icon = pygame.image.load("../icon/retour.png")
        self.settings_icon = pygame.image.load("../icon/settings.png")
        self.menu_icon = pygame.transform.rotate(pygame.transform.scale(pygame.image.load("../icon/menu.png").convert_alpha(), (64,64)), -90)
        self.menu_rect = pygame.Rect(self.menu_icon.get_rect())
        self.settings_rect = self.settings_icon.get_rect()
        self.folder_positions = []
        self.image_positions = []
        self.maps = []
        self.current_folder = None
        self.scroll = 5
        self.is_dragging = False
        self.is_draging_settings = False
        self.color_outline_settings = (255, 255, 255)
        self.settings = None
        self.is_close = False
        self.size = 500
        self.current_scroll = 1
        self.clock = pygame.time.Clock()
        self.offset_x = 0
        self.offset_y = 0
        self.last_pos = pygame.mouse.get_pos()
        self.settings_surf = None




    def main(self):
        self.build_screen = pygame.Surface((self.scroll, self.screen.get_height()))
        self.resizable_menu = pygame.Rect(((self.build_screen.get_width() - 10), 0), (10, self.screen.get_height()))
        self.settings_surf = pygame.Surface((self.screen.get_width() // 6, self.screen.get_height()//2))
        self.settings_mask = pygame.mask.from_surface(self.settings_surf)
        self.settings_outline = [(p[0], p[1]) for p in self.settings_mask.outline(every=1)]
        self.settings_surf.fill((77, 77, 77))
        maximum_resize = self.screen.get_width() // 2
        minimum_resize = self.screen.get_height() // 4
        self.menu_rect.x = -5
        self.menu_rect.y = (self.screen.get_height() // 2) - self.menu_icon.get_height()//2






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



        if pygame.mouse.get_pressed()[0]:
            if not self.is_dragging and not self.build_screen.get_rect().collidepoint(pygame.mouse.get_pos()) and self.choice:
                self.add_block()

        elif pygame.mouse.get_pressed()[1]:
            x, y = self.get_mouse_movement()
            self.offset_x += x
            self.offset_y += y

        elif pygame.mouse.get_pressed()[2]:
            if not self.is_dragging:
                self.remove_block()


        for folder_name in SPRITES.SPRITES:
            try:
                self.folder_positions.index(folder_name)
            except ValueError:
                self.folder_positions.append(folder_name)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.resizable_menu.collidepoint(pygame.mouse.get_pos()) and not self.is_close and not self.settings_icon.get_rect().collidepoint(pygame.mouse.get_pos()):
                        if self.is_dragging:
                            self.is_dragging = False
                        else:
                            self.is_dragging = True

                    elif self.settings_rect.collidepoint(event.pos):
                        if self.settings:
                            self.settings = False
                        else:
                            self.settings = True

                    elif self.is_close and self.menu_rect.collidepoint(pygame.mouse.get_pos()):
                        self.is_close = False
                        self.scroll = minimum_resize

                    elif self.build_screen.get_rect().collidepoint(pygame.mouse.get_pos()):
                        if self.current_folder:
                            if self.back_icon.get_rect(topleft=(10, 10)).collidepoint(event.pos):
                                self.current_folder = None
                                self.image_positions.clear()

                            else:
                                for img in self.image_positions:
                                    if img.hitbox.collidepoint(event.pos):
                                        self.choice = img

                        else:
                            start_x, start_y = 25, 25
                            step_x = self.dossier_icon.get_width() + 50
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
                                start_x += step_x
                                n += 1
                                if rect_dossier.collidepoint(event.pos):
                                    self.current_folder = path
                                    break

                elif event.button == 2:
                    self.last_pos = pygame.mouse.get_pos()



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
            x, y = 75, 25
            max_img = (self.build_screen.get_width() - 75) // 42
            n = 0
            self.image_positions.clear()
            for name, id in SPRITES.SPRITES[self.current_folder].items():
                if max_img == 0:
                    break
                if n == max_img:
                    y += 50
                    x = 75
                    n = 0
                if isinstance(id, int):
                    img = Block(x, y, Sprite(id), 32)
                else:
                    img = Block(x, y, Sprite(id[0]))
                img.debug_draw(self.build_screen, x, y, (0, 0))
                img.hitbox.x = img.x
                img.hitbox.y = img.y
                self.image_positions.append(img)
                x += img.sprite.image.get_width() + 10
                n += 1
            self.build_screen.blit(self.back_icon, (10, 10))
        else:
            start_x, start_y = 25, 25
            step_x = self.dossier_icon.get_width() + 50
            max_img = self.build_screen.get_width() // (step_x + 5)
            n = 0

            for file in SPRITES.SPRITES:
                if max_img == 0:
                    break
                if n == max_img:
                    start_y += 80
                    start_x = 25
                    n = 0

                self.build_screen.blit(self.dossier_icon, (start_x, start_y))
                label = pygame.font.Font(None, 13).render(file, True, (255, 255, 255))
                self.build_screen.blit(label, (start_x, start_y + self.dossier_icon.get_height()))


                start_x += step_x
                n += 1

        if self.is_dragging:
            pygame.draw.rect(self.build_screen, (0, 255, 0), self.resizable_menu)
        else:
            pygame.draw.rect(self.build_screen, (255, 255, 255), self.resizable_menu)



        for img in self.maps:
            img.draw(self.screen, (self.offset_x, self.offset_y))



        for line in range(self.size + 1):
            pygame.draw.line(self.screen, (255, 255, 255),
                             (line * tile_size - self.offset_x, 0),
                             (line * tile_size - self.offset_x, self.screen.get_height()))

            pygame.draw.line(self.screen, (255, 255, 255),
                             (0, line * tile_size - self.offset_y),
                             (self.screen.get_width(), line * tile_size - self.offset_y))



        self.screen.blit(self.build_screen, (0, 0))
        if self.is_close:
            pygame.draw.circle(self.screen, (255, 255, 255), (0, self.screen.get_height() // 2), 65)
            self.screen.blit(self.menu_icon, (-5, (self.screen.get_height() // 2) - self.menu_icon.get_height()//2))

        if self.settings:
            lines = pygame.draw.lines(self.settings_surf, self.color_outline_settings, False, self.settings_outline, 10)

            if lines.collidepoint(pygame.mouse.get_pos()):
                print('treue')

            self.screen.blit(self.settings_surf, (self.screen.get_width() - self.settings_surf.get_width(),  self.screen.get_height() - self.settings_surf.get_height()))


        self.screen.blit(self.settings_icon, (self.screen.get_width() - self.settings_icon.get_width(), self.screen.get_height() - self.settings_icon.get_height()))

        self.settings_rect.x, self.settings_rect.y = (self.screen.get_width() - self.settings_icon.get_width(), self.screen.get_height() - self.settings_icon.get_height())



        pygame.display.flip()

    def scroll_tile(self, next_index):
        tile_size = self.scale(self.current_scroll, 64)
        x, y = pygame.mouse.get_pos()
        x = x //tile_size
        y = y //tile_size

        if next_index == -0.1 and round(self.current_scroll, 1) == 0.2:
            self.current_scroll = 0.2

        elif round(self.current_scroll, 1) == 1 and next_index == 0.1:
            self.current_scroll = 1

        else:
            self.current_scroll = self.current_scroll + next_index
            self.current_scroll = round(self.current_scroll, 1)


        for img in self.maps:
            img.resize(tile_size)

    def add_block(self):
        try:
            tile_size = self.scale(self.current_scroll, 64)
            x, y = pygame.mouse.get_pos()
            x += self.offset_x
            y += self.offset_y
            self.choice.x = x // tile_size
            self.choice.y = y // tile_size
            for img in self.maps:
                if [img.x, img.y] == [self.choice.x, self.choice.y]:
                    return

            block = Block(self.choice.x, self.choice.y, self.choice.sprite, tile_size)
            self.maps.append(block)
        except TypeError:
            return


    def remove_block(self):
        for _, img in enumerate(self.maps):
            if img.hitbox.collidepoint(pygame.mouse.get_pos()):
                self.maps.pop(_)

    def scale(self, factor, dimension):
        return int(dimension * factor)

    def scale_sprite(self, factor, image):
        new_height = int(image.get_height() * factor)
        new_width = int(image.get_width() * factor)
        return pygame.transform.scale(image, (new_width, new_height))

    def get_mouse_movement(self):
        current_pos = pygame.mouse.get_pos()
        dx = current_pos[0] - self.last_pos[0]
        dy = current_pos[1] - self.last_pos[1]

        self.last_pos = current_pos

        return (-dx, -dy)

    def run(self):
        while True:
            self.main()
            self.update()
            self.draw()

            self.clock.tick(60)


s = MainScreen((500, 500), 'Map Editor')
s.run()
