import sys
import random
import math

# On a une graphe à 5 nodes et 8 arêtes

vrp = [
    [None, 3, 9, 7, 6],
    [3, None, 1, 2, 8]
    [9, 1, None, 1, 4],
    [7, 2, 1, None, 5],
    [6, 8, 4, 5, None]
]


def crossover(population, amount):
    if(amount > len(population)):
        raise Exception("crossover amount cannot exceed population amount")
    output = []

    for x in range(amount):
        first = population[random.randint(0, len(population)-1)]
    return
