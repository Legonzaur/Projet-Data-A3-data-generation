import sys
import random
import math
import pprint
# On a une graphe à 5 nodes et 8 arêtes

vrp = [
    [None, 3, 9, 7, 6],
    [3, None, 1, 2, 8],
    [9, 1, None, 1, 4],
    [7, 2, 1, None, 5],
    [6, 8, 4, 5, None]
]


def get_random_chromosom_pair(population):
    random_list = random.sample(range(0, len(population)), 2)
    return population[random_list[0]], population[random_list[1]]


def crossover(population, amount):
    if(amount > len(population)):
        raise Exception("crossover amount cannot exceed population amount")
    if(amount % 1 != 0):
        raise Exception(
            "crossover amount must be even (pair of children and parents)")

    chomosoms_length = len(population[0])
    # Création de paires d'enfants à partir des parents
    for x in range(math.floor(amount/2)):
        # Obtention des deux parents de manière aléatoire
        first_parent, second_parent = get_random_chromosom_pair(population)
        # Génération du point de séparation pour la génération des enfants
        split_point = random.randint(1, chomosoms_length-1)
        # Génération des deux enfants
        first_child = first_parent[0:split_point] + \
            second_parent[split_point:chomosoms_length]
        second_child = second_parent[0:split_point] + \
            first_parent[split_point:chomosoms_length]

        yield first_child, second_child
    return


pprint.pprint(crossover([[1, 2, 3, 4, 5, 6], [0, 0, 0, 0, 0, 0]], 2))
