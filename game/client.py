"""
Created on 2020-02-20

Project: OnlineGame
@author: ollejernstrom
"""

import socket
import pygame
import sys
import pickle

# serveraddress = socket.gethostbyname('localhost')
serveraddress = '192.168.43.7'  # IP för säpo bevakningsbil
print(serveraddress)
port = 6969

"""
p = 0
while True:
    s.send(str.encode(str(p)+'hello'))

    data = s.recv(2048)
    data = data.decode("utf-8")
    print(data)
    p += 1"""

pygame.init()
screen = pygame.display.set_mode((400, 400))
pygame.display.set_caption('SPELET')
clock = pygame.time.Clock()

FPS = 60
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)


class Player(pygame.sprite.Sprite):
    def __init__(self, identification):
        pygame.sprite.Sprite.__init__(self)
        self.width = 40

        self.id = identification

        self.image = pygame.Surface((self.width, self.width))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        if playerid == 0:
            self.pos = [50, 50]
        else:
            self.pos = [200, 200]

        self.speed = 5

    def update(self):

        key = pygame.key.get_pressed()
        # if keystate[pygame.K_LEFT]:

        if key[pygame.K_d]:
            self.pos[0] += self.speed

        if key[pygame.K_a]:
            self.pos[0] -= self.speed

        if key[pygame.K_w]:
            self.pos[1] -= self.speed

        if key[pygame.K_s]:
            self.pos[1] += self.speed

        self.rect = self.pos
        data_to_send = [self.id, self.pos[0], self.pos[1]]
        data_to_send = pickle.dumps(data_to_send)
        s.send(data_to_send)


        # SKicka Player + pos

def get_server_data():
    raw_data = s.recv(2048)
    data = pickle.loads(raw_data)
    return data

def setup(playerid):
    players = pygame.sprite.Group()
    player = Player(playerid)
    players.add(player)
    return players


def main(playerid, players):
    running = True
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Update
        players.update()


        # Draw

        screen.fill(WHITE)
        players.draw(screen)

        pygame.display.flip()


if __name__ == '__main__':
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((serveraddress, port))
        data = s.recv(512)
        playerid = data.decode("utf-8")
        print(playerid)

        players = setup(playerid)
        main(playerid, players)
    except Exception as e:
        print(e)

