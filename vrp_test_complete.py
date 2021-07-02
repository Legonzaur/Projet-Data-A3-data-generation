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


matrix = [
    [None, [3]*24, [9]*24, [7]*24, [6]*24],
    [[3]*24, None, [1]*24, [2]*24, [8]*24],
    [[9]*24, [1]*24, None, [1]*24, [4]*24],
    [[7]*24, [2]*24, [1]*24, None, [5]*24],
    [[6]*24, [8]*24, [4]*24, [5]*24, None]
]

startTime = time.time()
population = []
initial_population_count = 4
random_chance = 1/initial_population_count
mutation_chance = 4/initial_population_count
crossover_chance = 1-(random_chance+mutation_chance)


iterations = 1000

# Création de la population intiale
for i in range(initial_population_count):
    population.append(generate_gene(matrix))

for iterate in range(iterations):
    sys.stdout.write("\rIteration %i" % iterate)
    sys.stdout.flush()
    # Création des enfants
    children = []
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

    population = next_gen


# pprint.pprint(population)
# pprint.pprint(
#     list(map(lambda item: get_gene_cost(matrix, item), population)))
# pprint.pprint(children)
# pprint.pprint(
#     list(map(lambda item: get_gene_cost(matrix, item), children)))
# pprint.pprint(next_gen)
# pprint.pprint(
#     list(map(lambda item: get_gene_cost(matrix, item), next_gen)))
print("")
next_gen_costs = list(map(lambda item: get_gene_cost(matrix, item), next_gen))
best_path_cost = sorted(next_gen_costs)[0]
print("Best path found is")
pprint.pprint(next_gen[next_gen_costs.index(best_path_cost)])
print("This path takes " + str(best_path_cost) + " seconds to drive")
print("Solution took " + str(time.time() - startTime) + " seconds to generate")
