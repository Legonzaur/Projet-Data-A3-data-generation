import copy
from pprint import pprint
import random
from generate_graph import Graph


class Traffic:
    congestion_table = [0.05, 0.1, 0.1, 0.05, 0.05, 0.2, 0.6, 0.9, 1, 0.7,
                        0.5, 0.7, 0.9, 0.9, 0.7, 0.5, 0.7, 0.9, 1, 0.7, 0.5, 0.4, 0.3, 0.1]

    graph = None

    def __init__(self, graph):
        self.graph = graph

    def generate_traffic(self, source, target):
        traffic_table = [
            round(
                congestion * random.randint(100, 1000) * (
                        (self.graph.count_neighbors(source) + self.graph.count_neighbors(target))
                        / 2),
                2
            ) for congestion in self.congestion_table
        ]

        return traffic_table

    def browse_matrix(self):
        matrix = self.graph.matrix
        output = copy.deepcopy(matrix)
        # Iterate through matrix
        for source_node, target_links in enumerate(matrix):
            for target_index, link in enumerate(target_links):
                # If connection is present
                if link == 1:
                    output[source_node][target_index] = self.generate_traffic(source_node, target_index)
                    # If connection is bidirectional
                    if matrix[target_index][source_node] == 1:
                        matrix[target_index][source_node] = None
                        output[target_index][source_node] = output[source_node][target_index]

        return output
