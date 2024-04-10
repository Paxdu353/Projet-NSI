# Description des différentes classes

Sprite
-
Permet la manipulation des sprites. Un sprite peut-être vu comme un "autocollant".

- Création : à partir d'un identifiant (int)
- Attributs : id (identifiant, de type int), image (pygame.Surface), rect (pygame.Rect)
- Méthodes : scale (mise à l'échelle)

Un sprite n'a pas de coordonnées, c'est simplement une image

AnimatedSprite
-
Permet la manipulation de sprites animés, par exemple pour animer le déplacement d'un personnage dans une certaine direction

- Création : à partir d'une liste d'identifiants (list(int))
- Attributs : sprite_list (liste de sprites, ordonnée)
- Méthodes : update (mise à jour du sprite)

La méthode .update() est à appeler autant que possible (à chaque boucle de jeu), et met à jour le sprite en fonction du temps

Block
-
