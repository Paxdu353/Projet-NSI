# Description du fonctionnement du jeu (pour le programmeur)

L'écran de jeu doit afficher la carte (map) et les différents objets qui la composent, ainsi que le joueur, toujours situé au centre de l'écran (sauf aux extrémités de la map).

Seule une petite partie de la map est affichée, correspondant à ce que voit le joueur.

Lorsque le joueur se déplace, ses coordonnées sont modifiées, et la variable `scroll` est mise à jour ; `scroll` est un couple de valeurs `(scroll_x, scroll_y)` correspondant au décalage de l'écran de jeu par rapport au point d'origine de la map.

![schemas_projet_nsi](https://github.com/Paxdu353/Projet-NSI/assets/130542548/58988092-4a00-4406-b59b-75a88b7be87a)


Chaque objet composant la map , appelé _bloc_ (que ce soit le sol, une barrière, un autre personnage...) possède des **coordonnées absolues** (relativement à l'origine de la map, en haut à gauche) et des **coordonnées relatives** (relativement à l'origine de l'écran du joueur). Le passage des unes aux autres se fait grâce à la connaissance du scroll.

>[!IMPORTANT]
>Les blocs situés hors de l'écran ne sont pas représentés.

# Description des différentes classes

>[!NOTE]
> _Les informations ci-dessous ne sont pas des contraintes à respecter à la lettre, ce sont de simples indications, qu'il est toutefois conseillé de suivre..._

Sprite
-
Permet la manipulation des sprites. Un sprite peut-être vu comme un "autocollant".

- Création : à partir d'un identifiant (int)
- Attributs :
  - `id` : identifiant, de type int
  - `image` : un objet de type `pygame.Surface`
  - `rect` : un objet de type `pygame.Rect` correspond au rect de `image`
- Méthodes :
  - `scale(factor)` : mise à l'échelle d'un facteur donné

Un sprite n'a pas de coordonnées, c'est simplement une image.

```
sprite = Sprite(18)     # Création d'un sprite à partir de son identifiant
sprite.scale(3.5)       # Agrandissement d'un facteur 3.5
```

AnimatedSprite
-
Permet la manipulation de sprites animés, par exemple pour animer le déplacement d'un personnage dans une certaine direction.

- Création : à partir d'une liste d'identifiants (list(int))
- Attributs :
  - `sprite_list` : liste de sprites
- Méthodes :
  - `update()` : met à jour le sprite si le temps écoulé depuis le dernier appel de `update` est supérieur à une certaine valeur fixée (typiquement 0,1s pour une animation rapide)
  - `scale(factor)` : mise à l'échelle de tous les sprites

La méthode .update() est à appeler autant que possible (à chaque boucle de jeu), dès que l'on désire animer le sprite.

```
player_sprites = AnimatedSprite([18, 19, 20])     # Création du sprite animé
player_sprites.scale(2)                           # Agrandissement d'un facteur 2 de tous les sprites
```

Block
-
Un objet de type `Block` a vocation à être dessiné sur l'écran du joueur. Chaque bloc est associé à un sprite ou à un sprite animé, et possède des coordonnées. Il peut être traversant (barrière, voiture...) ou non (route, herbe, terre...).

- Création : deux coordonnées (`x` et `y`), un objet de type `Sprite` ou `AnimatedSprite` (`sprite`) et un booléen optionnel désignant l'objet comme traversant ou non (`crossable`)
- Attributs :
  - `x`, `y` : coordonnées absolues de l'objet
  - `sprite`
  - `hitbox` : un `pygame.Rect` pour la gestion des collisions
  - `crossable` : si `crossable` vaut `True`, alors le bloc est traversant et la gestion des collisions n'est pas activée
- Méthodes :
  - `draw(screen, scroll)` : dessine le rectangle sur l'écran `screen`, en prenant en compte le scroll actuel (tuple), et à condition que ce dernier soit visible à l'écran
 
Item
-
Une liste de blocs représentant un objet, comme une maison.

Création : un `filename` facultatif pour charger un item déjà existant.
- Attributs :
  - `x`, `y` : coordonnées absolues de l'objet
  - `block_list` : une liste d'objets de type `Block`. Chaque bloc composant l'item possède des **coordonnées relatives** à l'item.
- Méthodes :
  - `draw(screen, scroll)` : dessine chaque bloc de la liste sur l'écran `screen` en fonction du scroll. Attention, il faut tenir compte des coordonnées absolues de l'item et des coordonnées relatives de chaque bloc composant l'item !
  - `save(filename)` : enregistre l'item courant dans un fichier

Pour l'enregistrement d'un item dans un fichier, on peut imaginer une solution de ce type :

```
30, 100          # Coordonnées de l'item
0, 0, 85         # Coordonnées et id_sprite du premier bloc, relativement à l'item
0, 16, 86        # Coordonnées du 2nd bloc
...
```

Map
-
Une map est constituée de deux couches
