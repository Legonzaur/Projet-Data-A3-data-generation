import random
import math
import copy
# On a une graphe à 5 nodes et 8 arêtes


def get_random_chromosom_pair(population):
    random_list = random.sample(range(0, len(population)), 2)
    return copy.deepcopy(population[random_list[0]]), copy.deepcopy(population[random_list[1]])


def crossover(population, amount):
    if(amount > len(population)):
        raise Exception("crossover amount cannot exceed population amount")
    if(amount % 1 != 0):
        raise Exception(
            "crossover amount must be even (pair of children and parents)")

    chromosoms_length = len(population[0])
    # Création de paires d'enfants à partir des parents
    for x in range(math.floor(amount/2)):
        # Obtention des deux parents de manière aléatoire
        first_parent, second_parent = get_random_chromosom_pair(population)
        # Génération du point de séparation pour la génération des enfants
        split_point = random.randint(1, chromosoms_length-1)
        # Génération de l'enfant
        cut_part = first_parent[split_point:chromosoms_length]
        for i in cut_part:
            second_parent.pop(second_parent.index(i))

        random.shuffle(cut_part)
        yield second_parent + cut_part
