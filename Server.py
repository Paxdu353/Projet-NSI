import socket
import threading
from datetime import datetime
import pygame
import json

class Server:

    def __init__(self, host, port):
        self.__host = host
        self.__port = port
        self.__clients = {} # Données clients
        self.__clock = pygame.time.Clock()

        # Création du socket
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Rend le socket réutilisable
        self.__socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Démarrage du serveur
        self.__socket.bind((self.__host, self.__port))

        # Écoute des clients
        self.__socket.listen()

        print(f">> Listening on {self.__host}:{self.__port}")

        # Transmission des données aux clients
        t = threading.Thread(target=self.send_clients)
        t.daemon = True
        t.start()
    
    def check_new_clients(self):
        """ Vérifie les nouveaux clients (en continu) """

        client_socket, client_address = self.__socket.accept() # Bloquant
        print(f">> {client_address} connected")

        if not client_address in self.__clients:
            self.__clients[client_address] = {"socket": client_socket, "data": None}

        # Démarrage d'un thread spécifique pour le client

        try:
            t = threading.Thread(target=self.listen_client, args=(client_socket, client_address))
            t.daemon = True
            t.start()
        except Exception:
            print("Impossible de lancer le thread client")
            print(f"Nombre de threads : {threading.active_count()}")

    def close(self):
        """ Ferme le socket associé au serveur et tous les sockets clients associés """

        for address in self.__clients:
            self.__clients[address]["socket"].close()
        
        self.__socket.close()
    
    def listen_client(self, socket, address):
        """ Écoute du socket client """

        socket.setblocking(True)

        while True:
            try:
                data = socket.recv(1024) # Bloquant

                if not data: # Pas de données : client déconnecté
                    del self.__clients[address]
                    print(f"Client {address} disconnected from server")
                    break
            
                self.__clients[address]["data"] = data.decode()
            except Exception as e:
                print(f"[{self.now()}] Error : {e}")
                
    def now(self):
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
    
    def send_clients(self):
        while True:
            try:
                self.__clock.tick(60) # Nombre de transmissions par seconde

                data = []

                for address in self.__clients:
                    try:
                        decodedData = json.loads(self.__clients[address]["data"])
                        data.append(decodedData)
                    except Exception:
                        pass

                data = json.dumps(data)

                for address in self.__clients:
                    try:
                        client_socket = self.__clients[address]["socket"]
                        client_socket.send(data.encode())
                    except Exception as e:
                        print(f"Error : {e.with_traceback()}")
            except Exception as e:
                print(e.with_traceback())

HOST = "0.0.0.0"
PORT = 2324

S = Server(HOST, PORT)

try:
    while True:
        S.check_new_clients()
except KeyboardInterrupt:
    print("Exiting server")
finally:
    S.close()