#!/usr/bin/python

import pprint
import math
import time
import sys
from bson.objectid import ObjectId

from genetic_custom.vrp_genetic import genetic

from db.db_connector import DbConnector

# print("Obtaining graph from database. Please wait.")

iterations = int(sys.argv[1])
initial_population_count = int(sys.argv[2])
# Complete
graph_id = "60ded3ff2ee5a75b536b9bf6"
# Connected
#graph_id = "60dedca6c8735c99673b9bdb"
db = DbConnector()
matrix = db.get_graph_with_traffic(ObjectId(graph_id))


# print("Graph obtained")
startTime = time.time()
population = []

random_chance = 1/initial_population_count
mutation_chance = 4/initial_population_count
crossover_chance = 1-(random_chance+mutation_chance)


genetic(matrix, iterations, initial_population_count,
        random_chance, mutation_chance, crossover_chance)
