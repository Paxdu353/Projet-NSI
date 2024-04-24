import pygame
import Sprite, Block, Item, Player, AnimatedSprite, HUD

pygame.init()
clock = pygame.time.Clock()

LARGEUR_ECRAN, HAUTEUR_ECRAN = 800, 600
TAILLE_ECRAN = (LARGEUR_ECRAN, HAUTEUR_ECRAN)
SIZE = 32
L2, H2 = LARGEUR_ECRAN/(2*SIZE)-0.5, HAUTEUR_ECRAN/(2*SIZE)-0.5

screen = pygame.display.set_mode(TAILLE_ECRAN, vsync=1)
hud = HUD.HUD()

player = Player.Player(400, 300, {
    "UP" : AnimatedSprite.AnimatedSprite([483,484,485]),
    "DOWN" : AnimatedSprite.AnimatedSprite([477,478,479]),
    "LEFT" : Sprite.Sprite(11),
    "RIGHT" : AnimatedSprite.AnimatedSprite([480,481,482])
}, SIZE)

continuer = True

while continuer:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            continuer = False
    
    player.check_moves()
    player.move([])
    player.update()
    scroll = player.scroll
    sx, sy = scroll[0], scroll[1]

    screen.fill((30,30,30))

    # Dessin des lignes verticales
    for x in range(0, 1201, SIZE):
        pygame.draw.line(screen, (255,0,0), (x-sx, -sy), (x-sx, 1200-sy))
    # Dessin des lignes horizontale
    for y in range(0, 1201, SIZE):
        pygame.draw.line(screen, (255,0,0), (-sx, y-sy), (1200-sx, y-sy))

    player.draw(screen, player.scroll)
    hud.write(screen, f"Player : {player.x}, {player.y}", 20, 10, 10)
    hud.write(screen, f"Player scroll : {player.scroll}", 20, 10, 40)
    hud.write(screen, f"Player hitbox : {player.hitbox.x}, {player.hitbox.y}", 20, 10, 70)

    pygame.display.flip()
    clock.tick(60)
