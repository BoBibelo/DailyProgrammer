#! /usr/bin/env python3

import sys

class Node():
    def __init__(self):
        self.parent = None
        self.adjs = []

    def add_adj(self, *args):
        for adj in args:
            self.adjs.append(adj)


def load_graph(name):
    graph = {}
    flag = False

    with open(name, 'r') as f:
        for line in f:
            if not flag: # Graph size
                graph = { x : set() for x in range(1, int(line.strip()) + 1) }
                flag = True
            else:
                line = line.strip().split(' ')
                a, b = int(line[0]), int(line[1])
                graph[a].add(b)
                graph[b].add(a)

    return graph


def bron_kerbosch(r, p, x, cliques, graph):
    if not p and not x:
        cliques.append(r)
    else:
        u = max(p | x, key=lambda z: len(graph[z]))
        for v in p - graph[u]:
            bron_kerbosch(r | {v}, p & graph[v], x & graph[v], cliques, graph)
            p = p - {v}
            x = x | {v}

def get_largest_cliques(graph):
    cliques = []
    bron_kerbosch(set(), set(graph), set(), cliques, graph)
    max_size = len(max(cliques, key=len))
    return [ clique for clique in cliques if len(clique) == max_size ]

graph = load_graph(sys.argv[1])
cliques = get_largest_cliques(graph)

print(cliques)
