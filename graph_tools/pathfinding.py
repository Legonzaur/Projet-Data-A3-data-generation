import numpy as np
import copy


def weightFinding(graph, start, end, horaire=0):
    if graph[start][end] != None and graph[start][end][horaire] != None:
        return graph[start][end][horaire]

    weights = []
    for target, link_weight in enumerate(graph[start]):
        if link_weight != None and link_weight[horaire] != None:
            tmp_graph = copy.deepcopy(graph)

            tmp_graph[start][target] = None
            tmp_graph[target][start] = None
            weights.append(link_weight[horaire] +
                           weightFinding(tmp_graph, target, end))

#    w = np.nanmin(np.array(graph[start], dtype=np.float64))
#    i = graph[start].index(w)
    weight = np.nanmin(np.array(weights, dtype=np.float64))

    return weight
