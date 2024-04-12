import Sprite

ANIMATION_TIME_MS = 200

class AnimatedSpite():
    
    def __init__(self, liste):
        self.sprite_list = []
        self.index = 0 # Index du sprite courant
        for id in liste:
            # Chargement du sprite et ajout à la liste des sprites
            self.sprite_list.append(Sprite.Sprite(id))
            
    def draw_debug(self, x, y):
        # Affiche le sprite aux coordonnées x,y
        self.sprite_list[self.index].draw_debug(x,y)
    
    def scale(self, factor):
        # Scale de tous les sprites de la liste
        for sprite in self.sprite_list:
            sprite.scale(factor)
            
            

    def update(self):
        # Mise à jour de l'index
        pass
