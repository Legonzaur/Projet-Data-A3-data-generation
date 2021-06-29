import sys
import random
import math
from genetic_custom.vrp_genetic_get_cost import get_gene_cost

# On a une grapue à 5 nodes et 8 arêtes


def get_best_chromosoms(population, amount):
    return sorted(population, key=get_gene_cost)[0:amount]


print(get_best_chromosoms([[1, 2, 3, 4, 5, 6]], [1, 3, 5, 4, 6, 2], 1))
