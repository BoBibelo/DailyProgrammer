#! /usr/bin/env python3

import sys

def fill_adj_matrix(mat, name):
    with open(name, 'r') as f:
        for line in f:
            line = line.strip().split(' ')
            if len(line) == 1:
                continue # first line for nodes amount

            a, b = int(line[0]) - 1, int(line[1]) - 1
            mat[b][a] = 1
            mat[a][b] = 1


def print_adj(mat):
    for x in mat:
        for y in x:
            print(y, end=' ')
        print()


def print_degree(mat):
    for x, _ in enumerate(mat):
        degree = 0
        for y in mat[x]:
            degree += y
        print('Node {0} has a degree of {1}.'.format(x + 1, degree))

name = sys.argv[1]
with open(name, 'r') as f:
    size = int(f.readline().strip())
adj_matrix = [ [ 0 for _ in range(size) ] for _ in range(size) ]

fill_adj_matrix(adj_matrix, name)
print_degree(adj_matrix)
print()
print_adj(adj_matrix)
