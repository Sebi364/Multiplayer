import socket
import threading
import time

Players = {

}

def add_player(ID,pos_X,pos_Y,Color):
    print(f"Player {ID} joined the Game")
    Players[ID] = [pos_X, pos_Y, str(int(time.time())), Color]

def get_players(conn):
    for (player, pos) in Players.items():
        conn.send(f"{player} {pos[0]} {pos[1]} {pos[3]}\n".encode())
    conn.send('end'.encode())

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
    host = ''
    port = 5001

    server_socket = socket.socket()
    server_socket.bind((host, port))
    while True:
        server_socket.listen(2)
        conn, address = server_socket.accept()

        threading._start_new_thread( talk_to_client, (conn, ) )

    conn.close()

threading._start_new_thread( claner, ( ) )
server_program()
