# On a une grapue à 5 nodes et 8 arêtes
import pprint
import math
from genetic_custom.vrp_genetic_remi import generate_gene
from genetic_custom.vrp_genetic_crossover import crossover
from genetic_custom.vrp_genetic_mutation import mutation
from genetic_custom.vrp_genetic_pick_best import get_best_chromosoms
from genetic_custom.vrp_genetic_pick_best import get_gene_cost


matrix = [
    [None, 3, 9, 7, 6],
    [3, None, 1, 2, 8],
    [9, 1, None, 1, 4],
    [7, 2, 1, None, 5],
    [6, 8, 4, 5, None]
]

population = []
initial_population_count = 4
crossover_chance = 0.5
mutation_chance = 0.25
random_chance = 0.25
iterations = 10

# Création de la population intiale
for i in range(4):
    population.append(generate_gene(matrix))

# Création des enfants
children = []

for iterate in range(iterations):
    # Création des crossover
    crossover_amount = math.floor(crossover_chance*initial_population_count)
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

    pprint.pprint(population)
    pprint.pprint(
        list(map(lambda item: get_gene_cost(matrix, item), population)))
    pprint.pprint(children)
    pprint.pprint(
        list(map(lambda item: get_gene_cost(matrix, item), children)))
    pprint.pprint(next_gen)
    pprint.pprint(
        list(map(lambda item: get_gene_cost(matrix, item), next_gen)))

    population = next_gen
