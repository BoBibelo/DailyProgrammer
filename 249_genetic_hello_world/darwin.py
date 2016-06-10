#! /usr/bin/env/python3

import random
import string
import sys
from typing import *

MUTATION_FACTOR = 0.1
LETTERS = string.ascii_letters + ' '
TARGET = sys.argv[1]

def init_population(pop_size : int, elt_size : int) -> Sequence[str]:
    return [random_string(elt_size) for _ in range(pop_size)]


def random_string(elt_size : int) -> str:
    return ''.join([random.choice(LETTERS) for _ in range(elt_size)])


def fitness(word : str) -> int:
    return sum(char1 == char2 for char1, char2 in zip(word, TARGET))


def mix_pop(pop : Sequence[str]) -> Sequence[str]:
    return [make_child(random.choice(pop), random.choice(pop))
            for _ in range(pop_size)]


def make_child(lparent : str, rparent : str) -> str:
    return mutate(''.join([random.choice([c1, c2])
                           for c1, c2 in zip(lparent, rparent)]))


def mutate(word : str) -> str:
    return ''.join([c if random.random() >= MUTATION_FACTOR
                      else random.choice(LETTERS)
                      for c in word])


def generate(pop : Sequence[str], best : int, target : str) -> Sequence[str]:
    pop.sort(key=fitness, reverse=True)
    return mix_pop(pop[:best])


pop_size = 4000
best = int(pop_size * (20 / 100)) # Best 20%
pop = init_population(pop_size, len(TARGET))
gen = 1
current_best = pop[0]

while current_best != TARGET:
    print('gen: {0}\nFitness: {1}\t Best: {2}'
          .format(gen, fitness(current_best), current_best))

    pop = generate(pop, best, TARGET)
    current_best = pop[0]
    gen += 1

print('gen: {0}\nFitness: {1}\t Best: {2}'
        .format(gen, fitness(current_best), current_best))
print("Found !")
