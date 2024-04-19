# Description du fonctionnement du jeu (pour le programmeur)

L'écran de jeu doit afficher la carte (map) et les différents objets qui la composent, ainsi que le joueur, toujours situé au centre de l'écran (sauf aux extrémités de la map).

Seule une petite partie de la map est affichée, correspondant à ce que voit le joueur.

Lorsque le joueur se déplace, ses coordonnées sont modifiées, et la variable `scroll` est mise à jour ; `scroll` est un couple de valeurs `(scroll_x, scroll_y)` correspondant au décalage de l'écran de jeu par rapport au point d'origine de la map.

![schemas_projet_nsi](https://github.com/Paxdu353/Projet-NSI/assets/130542548/58988092-4a00-4406-b59b-75a88b7be87a)

Chaque objet composant la map , appelé _bloc_ (que ce soit le sol, une barrière, un autre personnage...) possède des **coordonnées absolues** (relativement à l'origine de la map, en haut à gauche) et des **coordonnées relatives** (relativement à l'origine de l'écran du joueur). Le passage des unes aux autres se fait grâce à la connaissance du scroll.

>[!IMPORTANT]
>Les blocs situés hors de l'écran ne sont pas représentés.

Par défaut, les sprites ont une taille de 16x16 pixels (ou des dimensions similaires si les sprites ne sont pas carrés). Si l'écran de jeu fait 800x600, la zone visible du jeu est très importante, les personnages et les objets sont très petits. Il est donc nécessaire de **simuler un zoom de la map** et des différents objets qui la composent.

Pour *zoomer*, il faut ruser un peu. Par exemple, pour un zoom égal à 2, les sprites doivent doubler de taille. Il faut donc les redimensionner proportionnellement (`pygame` fait ça très bien) mais également les afficher de façon décalée à l'écran.

![schemas_projet_nsi_2](https://github.com/Paxdu353/Projet-NSI/assets/130542548/80be8c23-a287-43b6-bef4-c82daf2d9601)


Si on se contente de les redimensionner, les sprites vont se chevaucher et la map ne ressemblera plus à rien...

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
  - `draw(screen, scroll, zoom)` : dessine le rectangle sur l'écran `screen`, en prenant en compte le scroll actuel (tuple) et le zoom utilisé, et à condition que ce dernier soit visible à l'écran
  - `collide(other_block)` : retourne `True` si collision avec `other_block`
 
Item
-
Une liste de blocs représentant un objet, comme une maison.

Création : un `filename` facultatif pour charger un item déjà existant.
- Attributs :
  - `x`, `y` : coordonnées absolues de l'objet
  - `block_list` : une liste d'objets de type `Block`. Chaque bloc composant l'item possède des **coordonnées relatives** à l'item.
- Méthodes :
  - `draw(screen, scroll, zoom)` : dessine chaque bloc de la liste sur l'écran `screen` en fonction du scroll et du zoom. Attention, il faut tenir compte des coordonnées absolues de l'item et des coordonnées relatives de chaque bloc composant l'item !
  - `save(filename)` : enregistre l'item courant dans un fichier (utile lors de la création d'item)

Pour l'enregistrement d'un item dans un fichier, on peut imaginer une solution de ce type :

```
30, 100          # Coordonnées de l'item
0, 0, 85         # Coordonnées et id_sprite du premier bloc, relativement à l'item
0, 16, 86        # Coordonnées du 2nd bloc
...
```

Player
-
Une classe représentant un joueur. Cette classe hérite de la classe `Block`, c'est à dire qu'on considère qu'un joueur est un bloc, disposant d'attributs et de méthodes supplémentaires. On définira la classe comme ceci :

```
import Block

class Player(Block):
  ...
```

Création : une liste de sprites animés (de type `AnimatedSprite`), un sprite animé par direction de déplacement
- Attributs non hérités de `Block` :
  - `sprite_dic` : un dictionnaire dont les clés sont les différentes directions (haut, bas, gauche, droite) et les valeurs des sprites animés correspondant à chaque direction
  - `vx`, `vy` : coordonnées du vecteur vitesse de déplacement (utile pour la mise à jour des sprites et le déplacement du personnage)
- Méthodes non héritées de `Block`:
  - `check_moves()` : méthode à appeler à chaque tour dans la boucle de jeu, vérifiant si un événement est survenu (clic souris, appui sur une touche...) et mettant à jour le sprite du joueur ainsi que sa vitesse.
  - `move(blocks)` : déplace le personnage, en fonction de `vx` et `vy` et des éventuelles collisions avec `blocks` qui pourraient survenir. **Cette fonction retourne le scroll associé au joueur.**

Map
-
Une map est constituée de deux couches : une couche `background` représentée par une liste d'objets de type `Block` **traversants** (terre, route, herbe...) et une couche `items` représentées par une liste d'objets de type `Block` ou `Item` **non traversants** (barrière, voiture, maison...) pour lesquels il faudra gérer les collisions avec les différents joueurs.

Création : un `filename` facultatif pour charger une map déjà existante.
- Attributs :
  - `background`
  - `items`
  - `players` : une liste de joueurs à afficher
  - `zoom` : niveau de zoom utilisé pour l'affichage
- Méthodes :
  - `draw(screen, scroll)` : dessine la map *locale*, c'est à dire l'ensemble des éléments la composant visibles par le joueur, en fonction du scroll et du zoom.
  - `save(filename)` : enregistre la map dans un fichier (utile lors de la création de map)
  - `zoom_to(new_zoom)` : change le zoom actuellement utilisé sur la map : il faut rescaler tous les sprites.
