#!/usr/bin/python

import time
import sys

from genetic_custom.vrp_genetic import genetic

from db.db_connector import DbConnector

iterations = int(sys.argv[1])
initial_population_count = int(sys.argv[2])

db = DbConnector()
matrix = db.get_graph_by_length(int(sys.argv[3]))


startTime = time.time()
population = []

random_chance = 1/initial_population_count
mutation_chance = 4/initial_population_count
crossover_chance = 1-(random_chance+mutation_chance)


genetic(matrix, iterations, initial_population_count,
        random_chance, mutation_chance, crossover_chance)
