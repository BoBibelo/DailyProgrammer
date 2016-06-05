#! /usr/bin/env python3

# server side

import socket
import threading
import sys

class GameData():
    def __init__(self):
        self.users = {}

    def add_user(self, username, user_socket):
        self.users[username] = User(user_socket)

    def get_users_list(self, fancy=False):
        if fancy:
            ans = 'Users connected:\n'
            ans += ', '.join([ username for username, _ in self.users.items() ])
            return ans
        else:
            return self.users

    def send_msg_all(self, msg):
        msg = msg.encode('utf-8')
        for user in self.users:
            user.send_msg(msg)

    def get_user(self, username):
        return self.users[username]

    def remove_user(self, username):
        del self.users[username]

    def set_ready(self, username):
        self.users[username].ready = True
        for _, v in self.users.items():
            if not v.ready:
                break
        else:
            return len(self.users) > 1
        return False

class User():
    def __init__(self, skt):
        self.skt = skt
        self.ready = False

    def send_msg(self, msg):
        self.skt.sendall(msg)


def launch_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #  = addr
    host, port = socket.gethostname(), 4242

    server_socket.bind((host, port))
    server_socket.listen(5)

    gameData = GameData()

    print("Server launched...")
    print('Host: {0}\tPort: {1}'.format(host, port))
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
    username = ''
    lock = threading.Lock()

    while True:
        in_msg = client.recv(MAX_BUFFER_SIZE).decode('utf-8').strip()

        lock.acquire()
        if in_msg.startswith('WHO'):
            out_msg = gameData.get_users_list(fancy=True)
        elif in_msg.startswith('START'):
            if gameData.set_ready(username):
                out_msg = 'All players are ready, the game start !'
            else:
                out_msg = 'You are ready but we are waiting others players.'
        elif in_msg.startswith('USER'):
            username = in_msg.split(' ')[1]
            gameData.add_user(username, client)
            out_msg = 'Hello ' + username
        elif in_msg.startswith('QUIT'):
            gameData.remove_user(username)
            client.close()
            break
        else:
            out_msg = "Sorry, but I did not understand your request"\
                        + ", type HELP for more informations."
        lock.release()

        client.sendall(out_msg.encode('utf-8'))



launch_server()
