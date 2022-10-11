import pygame
import random
import socket
import time
from datetime import datetime
import threading

players = []
colors = ['red','blue','green','magenta','yellow','white','purple']

host = '172.104.159.86' #for testing on server
#host = '127.0.0.1' #for testing localy

port = 5001
running = True

PlayerID = random.randint(1,9999999)
PlayerColor = random.choice(colors)

pos_X = 500
pos_Y = 500


(width, height) = (1920, 1080)
screen = pygame.display.set_mode((width, height))
pygame.display.flip()




def put(data):
    client_socket.send(f"{data}\n".encode())

def get():
    data = client_socket.recv(1024).decode()
    return data

def draw_players():
    put('get_players')

    string = ""
    while True:
        players = get()
        string = string + players
        if string.find("end") > 0:
            break
    string = string.split("\n")
    for x in string:
        x = x.split(" ")
        if x[0] != 'end':
            pygame.draw.circle(screen, x[3], [int(x[1]),int(x[2])], 50)

def ping():
    while True:
        put('ping')
        v1 = datetime.now()
        x = get()
        v2 = datetime.now()
        delta = v2 - v1
        #print(f"Ping: {int(delta.total_seconds() * 1000)}")

def update_own_position(event):
    global pos_X, pos_Y
    if event.key == pygame.K_a:
        pos_X -= 20
    if event.key == pygame.K_d:
        pos_X += 20

    if event.key == pygame.K_w:
        pos_Y -= 20
    if event.key == pygame.K_s:
        pos_Y += 20

try:
    client_socket = socket.socket()
    client_socket.connect((host, port))

except:
    quit()

#threading._start_new_thread(ping,())

put(f"add_player {PlayerID} {pos_X} {pos_Y} {PlayerColor}")

while running:
    screen.fill((0,0,0))
    draw_players()
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            update_own_position(event)
    put(f"update_player {PlayerID} {pos_X} {pos_Y}")
