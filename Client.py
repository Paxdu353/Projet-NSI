import socket
from threading import Thread
import os, sys
import pygame
import random
import json

class Client:

    def __init__(self, server_host, server_port) -> None:
        self.__server_host = server_host
        self.__server_port = server_port
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__server_data = {}

        print(f"Connecting to {self.__server_host}:{self.__server_port}...")
        self.__socket.connect((self.__server_host, self.__server_port))
        print("Connected !")

        # Lancement du thread d'écoute du serveur
        t = Thread(target=self.listen_for_messages)
        t.daemon = True
        t.start()
    
    def close(self):
        print(f"Close client socket")
        self.__socket.close()

    def get_server_data(self):
        return dict(self.__server_data)

    def listen_for_messages(self):
        while True:
            try:
                data = self.__socket.recv(1024)

                if not data:
                    print("\nDisconnected from server")
                    self.close()
                    os._exit(1) # On termine le programme

                for name, pos, color in json.loads(data.decode()):
                    try:
                        if name not in self.__server_data:
                            self.__server_data[name] = {"pos": pos, "color": color}
                        else:
                            self.__server_data[name]["pos"] = pos
                    except Exception:
                        print("Error json decode from server")

            except json.JSONDecodeError:
                print("JSON decode error")
            except Exception as e:
                print(f"Error : {e}")
                break
    
    def send(self, message):
        self.__socket.send(str(message).encode())

HOST = "192.168.1.16"
PORT = 2324

player_name = input("Entrez votre pseudo : ")

pygame.init()
pygame.font.init()

screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

rect = pygame.rect.Rect(0,0,10,10)
RECT_COLOR = (random.randint(0,255), random.randint(0,255), random.randint(0,255))

FONT = pygame.font.SysFont("arial", 12)

try:
    C = Client(HOST, PORT)
except ConnectionRefusedError:
    print(f"Connection refused")
else:
    try:
        while True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            if pygame.key.get_pressed()[pygame.K_z]:
                rect.y -= 5
            if pygame.key.get_pressed()[pygame.K_s]:
                rect.y += 5
            if pygame.key.get_pressed()[pygame.K_q]:
                rect.x -= 5
            if pygame.key.get_pressed()[pygame.K_d]:
                rect.x += 5

            screen.fill((255,255,255))
            pygame.draw.rect(screen, RECT_COLOR, rect)

            other_players = C.get_server_data()
            for name in other_players:
                if name != player_name:
                    color = tuple(other_players[name]["color"])
                    pos = other_players[name]["pos"]
                    pygame.draw.rect(screen, color, pygame.rect.Rect(pos[0], pos[1], 10, 10))

                    name_text = FONT.render(name, True, (0,0,0))
                    screen.blit(name_text, (pos[0], pos[1]-15))

            pygame.display.flip()

            clock.tick(60)

            dataToServer = [player_name, (rect.x, rect.y), RECT_COLOR]
            C.send(json.dumps(dataToServer))

    except Exception as e:
        print(f"Error : {e.with_traceback()}")
    except KeyboardInterrupt:
        C.close()
    finally:
        C.close()