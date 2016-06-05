#! /usr/bin/env python3

# Client side

import sys
import socket


def start_client(MAX_BUFFER_SIZE=4096):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # = addr
    host, port = socket.gethostname(), 4242

    try:
        client_socket.connect((host, port))
    except:
        print('No server found for {0}, {1}.'.format(host, port), 
              file=sys.stderr)
        exit(1)

    # Prez
    username = input('Who are you ? ').strip()
    client_socket.send('USER {0}'.format(username).encode('utf-8'))
    out_msg = client_socket.recv(MAX_BUFFER_SIZE).decode('utf-8').rstrip()
    print(out_msg)

    while True:
        in_msg = input('> ')
        client_socket.send(in_msg.encode('utf-8'))

        out_msg = client_socket.recv(MAX_BUFFER_SIZE).decode('utf-8').rstrip()
        print(out_msg)

start_client()
