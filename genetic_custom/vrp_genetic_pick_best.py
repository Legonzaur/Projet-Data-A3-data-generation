from functools import cmp_to_key


def get_gene_cost(matrix, gene, initial=0):
    current = initial
    cost = 0
    for i in gene:
        cost += matrix[current][i]
        current = i
    return cost + matrix[current][initial]


def get_best_chromosoms(population, amount, matrix):
    return sorted(population, key=cmp_to_key(lambda item1, item2: get_gene_cost(matrix, item1) - get_gene_cost(matrix, item2)))[0:amount]
