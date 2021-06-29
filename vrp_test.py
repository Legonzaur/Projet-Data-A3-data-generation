# On a une grapue à 5 nodes et 8 arêtes
from genetic_custom.vrp_genetic_get_cost import get_gene_cost


vrp = [
    [None, 3, 9, 7, 6],
    [3, None, 1, 2, 8],
    [9, 1, None, 1, 4],
    [7, 2, 1, None, 5],
    [6, 8, 4, 5, None]
]

print(get_gene_cost(vrp, [1, 2, 3, 4]))
