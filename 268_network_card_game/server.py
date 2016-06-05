#! /usr/bin/env python3

# server side

import socket
import threading
import sys

class GameData():
    def __init__(self):
        self.users = []

    def add_user(self, *args):
        for user in args:
            self.users.append(user)

    def get_users_list(self, fancy=False):
        if fancy:
            ans = 'Users connected:\n'
            ans += ','.join(self.users)
            return ans
        else:
            return self.users

def launch_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #  = addr
    host, port = socket.gethostname(), 4242

    server_socket.bind((host, port))
    server_socket.listen(5)

    gameData = GameData()

    while True:
        # Create connection with a client
        try:
            client, addr = server_socket.accept()
        except:
            print('Server ending...', file=sys.stderr)
            exit(1)

        print('New connection:\tip: {0}\tPort: {1}'.format(addr[0], addr[1]))

        try:
            threading.Thread(target=process_input,
                             args=(client, addr, gameData)).start()
        except:
            print("Something when wrong...", file=sys.stderr)
            exit(1)
    server_socket.close()


def process_input(client, addr, gameData, MAX_BUFFER_SIZE=4096):
    while True:
        in_msg = client.recv(MAX_BUFFER_SIZE).decode('utf-8').strip()

        print('Got ' + in_msg)
        if in_msg.startswith('WHO'):
            out_msg = gameData.get_users_list(fancy=True)
        elif in_msg.startswith('USER'):
            new_user = in_msg.split(' ')[1]
            gameData.add_user(new_user)
            out_msg = 'Hello ' + new_user
        elif in_msg.startswith('QUIT'):
            client.sendall('Bye bye'.encode('utf-8'))
            client.close()
            break
        else:
            out_msg = "GIMME REAL DATA"
        client.sendall(out_msg.encode('utf-8'))



launch_server()
