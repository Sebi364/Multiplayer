import pygame
import random
import socket
import time

players = []
colors = ['red','blue','green','magenta','yellow','white','purple']

host = '170.187.189.225'
port = 5001
running = True

PlayerID = random.randint(1,9999999)

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
            print(x)
            pygame.draw.circle(screen, 'white', [int(x[1]),int(x[2])], 50)

def update_own_position(event):
    global pos_X, pos_Y
    if event.key == pygame.K_LEFT:
        pos_X -= 20
    if event.key == pygame.K_RIGHT:
        pos_X += 20

    if event.key == pygame.K_UP:
        pos_Y += 20
    if event.key == pygame.K_DOWN:
        pos_Y -= 20
    put(f"update_player {PlayerID} {pos_X} {pos_Y}")

try:
    client_socket = socket.socket()
    client_socket.connect((host, port))

except:
    quit()


put(f"add_player {PlayerID} {pos_X} {pos_Y}")

while running:
    screen.fill((0,0,0))
    draw_players()
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            update_own_position(event)