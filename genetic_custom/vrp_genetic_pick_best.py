from genetic_custom.vrp_genetic_get_cost import get_gene_cost


def get_best_chromosoms(population, amount):
    return sorted(population, key=get_gene_cost)[0:amount]
