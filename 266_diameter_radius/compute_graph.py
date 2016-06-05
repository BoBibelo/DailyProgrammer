#! /usr/bin/env python3

import sys
from collections import deque

class Node():
    def __init__(self, distance):
        self.distance = distance
        self.parent = None
        self.adjs = []

    def add_adj(self, *args):
        for adj in args:
            self.adjs.append(adj)


def prepare_graph(graph, size):
    for i in range(size):
        graph[str(i + 1)] = Node(-1)


def load_graph(name):
    graph = {} # Key is name, value a Node.
    flag = False

    with open(name, 'r') as f:
        for line in f:
            if not flag: # Graph size
                prepare_graph(graph, int(line.strip()))
                flag = True
            else:
                line = line.strip().split(' ')
                graph[line[0]].add_adj(line[1])

    return graph

def breadth_first_search(graph, node_label):
    for _, v in graph.items():
        v.distance = -1
        v.parent = None

    queue = deque()
    graph[node_label].distance = 0
    queue.append(node_label)

    while len(queue) != 0:
        current = queue.popleft()

        for label in graph[current].adjs:
            if graph[label].distance == -1:
                graph[label].distance = graph[current].distance + 1
                graph[label].parent = current
                queue.append(label)

    return graph


def get_eccentricity(graph, node_label):
    graph = breadth_first_search(graph, node_label)
    ecc = -1
    for k, v in graph.items():
        if k != node_label:
            ecc = max(ecc, v.distance)
    return ecc


def get_radius_diameter(graph):
    radius = float('Inf')
    diameter = -1
    for k, v in graph.items():
        ecc = get_eccentricity(graph, k)
        if ecc != -1:
            radius = min(radius, ecc)
        diameter = max(diameter, ecc)

    return radius, diameter


graph = load_graph(sys.argv[1])
radius, diameter = get_radius_diameter(graph)

print('Radius: {0}.'.format(radius))
print('Diameter: {0}.'.format(diameter))
