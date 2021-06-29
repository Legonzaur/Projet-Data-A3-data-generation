import sys
import random
import copy
import pprint
# On a une grapue à 5 nodes et 8 arêtes

vrp = [
    [None, 3, 9, 7, 6],
    [3, None, 1, 2, 8],
    [9, 1, None, 1, 4],
    [7, 2, 1, None, 5],
    [6, 8, 4, 5, None]
]


def get_random_chromosom(population):
    return population[random.randint(0, len(population)-1)]


def mutation(population, amount):
    if(amount > len(population)):
        raise Exception("mutation amount cannot exceed population amount")

    chromosoms_length = len(population[0])

    for x in range(amount):
        # Copie d'un chromosome aléatoire dans la population
        target = copy.deepcopy(get_random_chromosom(population))
        # Création d'une liste comprenant deux indexes aléatoires
        random_list = random.sample(range(0, chromosoms_length), 2)
        # obtention de deux indexes différents
        swap1 = random_list[0]
        swap2 = random_list[1]
        # échange les allèles des chromosomes
        temp = target[swap1]
        target[swap1] = target[swap2]
        target[swap2] = temp
        yield target


print(list(mutation([[1, 2, 3, 4, 5, 6]], 1)))
