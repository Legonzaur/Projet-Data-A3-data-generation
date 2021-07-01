import numpy as np
import copy
from graph_tools.count_not_none import count_not_none


def weightFinding(graph, start, end, horaire=0):
    if graph[start][end] != None and graph[start][end][horaire] != None:
        return graph[start][end][horaire]

    weights = []
    for target, link_weight in enumerate(graph[start]):
        if link_weight != None and link_weight[horaire] != None:
            tmp_graph = copy.deepcopy(graph)

            tmp_graph[start] = [None]*len(tmp_graph[start])

            for link in range(len(tmp_graph)):
                tmp_graph[link][start] = None

            if count_not_none(tmp_graph[target]) > 0:
                data = weightFinding(tmp_graph, target, end)
                if data != None:
                    weights.append(link_weight[horaire] + data)

#    w = np.nanmin(np.array(graph[start], dtype=np.float64))
#    i = graph[start].index(w)
    if len(weights) != 0:
        weight = np.nanmin(np.array(weights, dtype=np.float64))
        return weight
