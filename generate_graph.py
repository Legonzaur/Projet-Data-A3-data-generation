import random
import pprint as pp


class Graph:
    matrix = [[]]
    connected_graphs = []

    # generate a random number of nodes between min and max
    #  and pregen the edges matrix
    def generate_nodes(self, min_node_amount, max_node_amount):
        node_amount = random.randint(min_node_amount, max_node_amount)
        graph = []
        for i in range(node_amount):
            graph.append([])
            self.connected_graphs.append([i])
            for _ in range(node_amount):
                graph[i].append(None)

        self.matrix = graph
        return graph

    # count the neighbors of a node
    def count_neighbors(self, node):
        neighbor_amount = 0

        # for each existing connection, add one neighbor
        for i in self.matrix[node]:
            if i is not None:
                neighbor_amount += 1

        return neighbor_amount

    # get each a list of target nodes eligible for a connection with the given node
    def get_eligible_nodes(self, node):
        eli = []

        # search for missing connections and add the targets to the eligible nodes for a real connection
        for target in range(len(self.matrix)):
            if self.matrix[node][target] is None:
                eli.append(target)
        # remove the source node
        eli.remove(node)

        return eli

    # generate the edges within a graph
    def generate_edges(self, min_neighbors, max_neighbors, uni_direct_ratio):
        # iterate through each node in the graph
        for source_node in range(len(self.matrix)):
            # get the current and target neighbor amount
            current_neighbors_amount = self.count_neighbors(source_node)
            target_neighbors_amount = random.randint(min_neighbors, max_neighbors)

            # get the list of eligible nodes
            eligible_nodes = self.get_eligible_nodes(source_node)

            for k in range(target_neighbors_amount - current_neighbors_amount):
                # get a random node from the eligible nodes and remove it from the pool
                target_node = random.choice(eligible_nodes)
                eligible_nodes.remove(target_node)

                # generate the link
                self.generate_link(source_node, target_node, random.random() > uni_direct_ratio)

    # generate individual edge
    def generate_link(self, source_node, target_node, bi_direct):
        # add the source -> target link
        self.matrix[source_node][target_node] = 1

        src_idx = self.find_in_array_array(self.connected_graphs, source_node)
        trg_idx = self.find_in_array_array(self.connected_graphs, target_node)

        if src_idx[0] is not trg_idx[0]:
            self.connected_graphs[src_idx[0]] += self.connected_graphs[trg_idx[0]]
            self.connected_graphs[src_idx[0]].sort()
            self.connected_graphs.pop(trg_idx[0])

        # if bidirectional, add the target -> source link
        if bi_direct:
            self.matrix[target_node][source_node] = 1

    def find_in_array_array(self, array, value):
        for i in range(len(array)):
            if isinstance(array[i], list):
                idx = [i, self.find_in_array_array(array[i], value)]
                if idx[- 1] is not None:
                    return idx
            if array[i] == value:
                return i

    # generate a complete graph
    def generate_graph(self, min_node_amount, max_node_amount, min_neighbor_amount, max_neighbor_amount,
                       uni_direct_ratio):
        self.generate_nodes(min_node_amount, max_node_amount)
        self.generate_edges(min_neighbor_amount, max_neighbor_amount, uni_direct_ratio)

        if len(self.connected_graphs) > 1:
            self.connect_graph()

    def connect_graph(self):
        while len(self.connected_graphs) > 1:
            source = random.choice(self.connected_graphs[0])
            target = random.choice(self.connected_graphs[1])
            self.generate_link(source, target, True)


# EXAMPLES #
# graph = Graph()
# graph.generate_graph(1000, 1000, 1, 2, 0.1)
# print(graph.connected_graphs)
# print(len(graph.connected_graphs) == 1)
