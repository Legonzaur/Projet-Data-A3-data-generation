import copy
import pprint
import random
import generate_graph as gg


initial_matrix = [
    [None, 1, None, None],
    [1, None, 1, None],
    [None, 1, None, 1],
    [None, None, None, None]
]

congestion_table = [0.05, 0.1, 0.1, 0.05, 0.05, 0.2, 0.6, 0.9, 1, 0.7,
                    0.5, 0.7, 0.9, 0.9, 0.7, 0.5, 0.7, 0.9, 1, 0.7, 0.5, 0.4, 0.3, 0.1]

temp_matrix = copy.deepcopy(initial_matrix)


def generate_traffic(graph, source, target):
    traffic_table = [round(congestion * random.randint(10, 100) * ((gg.count_neighbors(
        graph, source) + gg.count_neighbors(graph, target)) / 2), 2) for congestion in congestion_table]
    return traffic_table


def browse_matrix(matrix):
    output = copy.deepcopy(matrix)
    # Iterate through matrix
    for ligneIndex, ligne in enumerate(matrix):
        for colonneIndex, case in enumerate(ligne):
            # If connection is present
            if case == 1:
                output[ligneIndex][colonneIndex] = generate_traffic(
                    matrix, ligneIndex, colonneIndex)
                # If connection is bidirectional
                if matrix[colonneIndex][ligneIndex] == 1:
                    matrix[colonneIndex][ligneIndex] = None
                    output[colonneIndex][ligneIndex] = output[ligneIndex][colonneIndex]
    return output


pprint.pprint(browse_matrix(temp_matrix))
