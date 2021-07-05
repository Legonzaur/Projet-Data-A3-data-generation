
# On a une grapue à 5 nodes et 8 arêtes
import pprint
import math
import time
import sys
from bson.objectid import ObjectId

from genetic_custom.vrp_genetic_generate_gene import generate_gene
from genetic_custom.vrp_genetic_crossover import crossover
from genetic_custom.vrp_genetic_mutation import mutation
from genetic_custom.vrp_genetic_pick_best import get_best_chromosoms
from genetic_custom.vrp_genetic_pick_best import get_gene_cost


def genetic(matrix, iterations, initial_population_count, random_chance, mutation_chance, crossover_chance):
    # Création de la population intiale
    startTime = time.time()
    population = []
    for i in range(initial_population_count):
        population.append(generate_gene(matrix))

    for iterate in range(iterations):
        # Création des enfants
        children = []
        # Création des crossover
        crossover_amount = math.floor(
            crossover_chance*initial_population_count)
        for i in range(crossover_amount):
            children += list(crossover(population, crossover_amount))

        # Création des mutations
        mutation_amount = math.floor(mutation_chance*initial_population_count)
        for i in range(mutation_amount):
            children += list(mutation(population, mutation_amount))

        # Obtention des solutions aléatoires
        random_amount = math.floor(random_chance*initial_population_count)
        for i in range(random_amount):
            children.append(generate_gene(matrix))

        # Election des gènes les plus forts
        next_gen = get_best_chromosoms(
            population + children, initial_population_count, matrix)

        population = next_gen

    print(str(time.time() - startTime))
