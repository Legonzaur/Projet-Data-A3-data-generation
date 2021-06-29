def get_gene_cost(matrix, gene, initial=0):
    current = initial
    cost = 0
    for i in gene:
        cost += matrix[current][i]
        current = i
    return cost + matrix[current][initial]
