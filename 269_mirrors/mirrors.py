#! /usr/bin/env python3

import sys
import string

def generate_alphabet():
    dico = {}
    for letter in string.ascii_letters:
        dico[letter] = None
    return dico


def fill_board(board, name):
    x = 0
    y = 0
    with open(name, 'r') as f:
        for line in f:
            line = line.rstrip('\n')
            x = 0
            for char in line:
                if char == '/':
                    board[x][y] = 1
                elif char == '\\':
                    board[x][y] = 2
                x += 1
            y += 1


def fill_dico(board, dico):
    for src, dst in dico.items():
        if not dst: # Still 'None'
            dst = compute_value(board, src)
            dico[src] = dst
            dico[dst] = src

"""
. x --->
y
|
V

d:
    0
  3 . 1
    2
"""
def compute_value(board, letter):
    if ord(letter) >= ord('a') and ord(letter) <= ord('m'):
        x, y, d = ord(letter) - ord('a'), 0, 2
    elif ord(letter) >= ord('n') and ord(letter) <= ord('z'):
        x, y, d = 12, ord(letter) - ord('n'), 3
    elif ord(letter) >= ord('A') and ord(letter) <= ord('M'):
        x, y, d = 0, ord(letter) - ord('A'), 1
    elif ord(letter) >= ord('N') and ord(letter) <= ord('Z'):
        x, y, d = ord(letter) - ord('N'), 12, 0
    else:
        return letter
    print(letter)
    return compute_value_(board, x, y, d)


def compute_value_(board, x, y, d):
    flag = False
    while True:
        print('{0} {1}'.format(x, y))
        if (x > 12 or x < 0 or y > 12 or y < 0) and flag:
            return get_letter(x, y)

        if board[x][y] == 1: # '/'
            if d == 0:      d = 1
            elif d == 1:    d = 0
            elif d == 2:    d = 3
            else:           d = 2
        elif board[x][y] == 2: # '\'
            if d == 0:      d = 3
            elif d == 1:    d = 2
            elif d == 2:    d = 1
            else:           d = 0

        flag = True

        if d == 0:      y -= 1
        elif d == 1:    x += 1
        elif d == 2:    y += 1
        else:           x -= 1



def get_letter(x, y):
    x, y = normalize(x, y)
    if y == 0:          return chr(ord('a') + x)
    elif y == 12:       return chr(ord('N') + x)
    elif x == 0:        return chr(ord('A') + y)
    else:               return chr(ord('n') + y)


def normalize(x, y):
    if x < 0:       x = 0
    elif x > 12:    x = 12

    if y < 0:       y = 0
    elif y > 12:    y = 12

    return x, y

def decode_word(alphabet, word):
    ans = ''
    for c in word:
        try:
            ans += alphabet[c]
        except:
            ans += c
    return ans


alphabet = generate_alphabet()
board = [ [ 0 for _ in range(13) ] for _ in range(13) ]

name = sys.argv[1]
fill_board(board, name)

fill_dico(board, alphabet)

while True:
    print('> ', end='')
    try:
        i = input('')
    except:
        break
    print(decode_word(alphabet, i))
