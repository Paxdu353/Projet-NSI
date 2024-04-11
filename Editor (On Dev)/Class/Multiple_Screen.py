from multiprocessing import Process, Queue

def lancer_ecran(ecran, queue):
    ecran.run(queue)

class Ecran:
    def __init__(self, titre, dimensions):
        self.titre = titre
        self.dimensions = dimensions

    def run(self, queue):
        raise NotImplementedError("Cette méthode doit être implémentée par les enfants.")




if __name__ == "__main__":
    # Importations des sous-classes ici -->
    from Class.Screen.main_screen import *
    from Class.Screen.build_screen import *

    # Fin des importations des sous classes ici <--

    queue = Queue()
    ecrans = [classe(f'Ecran numéro {index+1}', (640, 480)) for index, classe in enumerate(Ecran.__subclasses__())]
    processus = [Process(target=lancer_ecran, args=(ecran, queue)) for ecran in ecrans]

    for p in processus:
        p.start()

    while not queue.empty():
        current_choice = queue.get()
        print(current_choice)

    for p in processus:
        p.join()
