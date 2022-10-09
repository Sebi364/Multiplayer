import socket
import threading
import time

Players = {

}

def add_player(ID,pos_X,pos_Y,Color):
    print(f"Player {ID} joined the Game")
    Players[ID] = [pos_X, pos_Y, str(int(time.time())), Color]

def get_players(conn,address):
    for (player, pos) in Players.items():
        server_socket.sendto(f"{player} {pos[0]} {pos[1]} {pos[3]}\n".encode(), address)
    server_socket.sendto('end'.encode(), address)

def update_player(player, pos_X, pos_Y):
    Players[player] = [pos_X, pos_Y, str(int(time.time())), Players[player][-1]]

def remove_player(player):
    del Players[player]
    print(f"Player {player} left the Game")

def talk_to_client(conn):
    while True:
        data = conn.recv(1024).decode()
        data = data.split("\n")
        for d in data:
            d = d.split(" ")
            if d[0] == 'add_player':
                add_player(d[1],d[2],d[3],d[4])

            if d[0] == 'get_players':
                get_players(conn)

            if d[0] == 'update_player':
                update_player(d[1] ,d[2], d[3])

            if d[0] == 'remove_player':
                remove_player(d[1])

def talk_to_client2(conn,address):
    data = conn.split("\n")
    for d in data:
        d = d.split(" ")
        if d[0] == 'add_player':
            add_player(d[1],d[2],d[3],d[4])

        if d[0] == 'get_players':
            get_players(conn,address)

        if d[0] == 'update_player':
            update_player(d[1] ,d[2], d[3])

        if d[0] == 'remove_player':
            remove_player(d[1])

def claner():
    global Players
    while True:
        for (player, pos) in Players.items():
            if int(int(time.time()) - int(pos[2])) > 10:
                print(f"Player {player} was removed due to inactivity")
                del Players[player]
                break
        time.sleep(5)


def server_program():
    while True:
        Message, address = server_socket.recvfrom(1024)

        talk_to_client2(Message.decode(),address)

threading._start_new_thread( claner, ( ) )
host = '127.0.0.1'
port = 5001

server_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
server_socket.bind((host, port))
server_program()
