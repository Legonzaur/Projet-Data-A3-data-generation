from functools import cmp_to_key
import math
from graph_tools.pathfinding import weightFinding


def get_gene_cost(matrix, gene, initial=0):
    current = initial
    cost = 0.0
    for i in gene:
        if(matrix[current][i] == None):
            matrix[current][i] = [None]*24
            matrix[current][i][math.floor(cost/3600) % 24] = weightFinding(
                matrix, current, i, math.floor(cost/3600) % 24)

        if matrix[current][i][math.floor(cost/3600) % 24] == None:
            test = weightFinding(
                matrix, current, i, math.floor(cost/3600) % 24)
            if test == None:
                raise Exception("Graph is not connected")
        cost += matrix[current][i][math.floor(cost/3600) % 24]
        current = i

    if(matrix[current][initial] == None):
        matrix[current][initial] = [None]*24
        matrix[current][initial][math.floor(cost/3600) % 24] = weightFinding(
            matrix, current, initial, math.floor(cost/3600) % 24)
    return cost + matrix[current][initial][math.floor(cost/3600) % 24]


def get_best_chromosoms(population, amount, matrix):
    return sorted(population, key=cmp_to_key(lambda item1, item2: get_gene_cost(matrix, item1) - get_gene_cost(matrix, item2)))[0:amount]
