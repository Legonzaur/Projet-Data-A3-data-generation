import random
import pprint as pp


# generate a random number of nodes between min and max
#  and pregen the edges matrix
def generate_nodes(min_node_amount, max_node_amount):
    node_amount = random.randint(min_node_amount, max_node_amount)
    graph = []
    for i in range(node_amount):
        graph.append([])
        for _ in range(node_amount):
            graph[i].append(None)

    return graph


# count the neighbors of a node
def count_neighbors(graph, node):
    neighbor_amount = 0

    # for each existing connection, add one neighbor
    for i in graph[node]:
        if i is not None:
            neighbor_amount += 1

    return neighbor_amount


# get each a list of target nodes eligible for a connection with the given node
def get_eligible_nodes(graph, node):
    eli = []

    # search for missing connections and add the targets to the eligible nodes for a real connection
    for target in range(len(graph)):
        if graph[node][target] is None:
            eli.append(target)
    # remove the source node
    eli.remove(node)

    return eli


# generate the edges within a graph
def generate_edges(graph, min_neighbors, max_neighbors, uni_direct_ratio):
    # iterate through each node in the graph
    for source_node in range(len(graph)):
        # get the current and target neighbor amount
        current_neighbors_amount = count_neighbors(graph, source_node)
        target_neighbors_amount = random.randint(min_neighbors, max_neighbors)

        # get the list of eligible nodes
        eligible_nodes = get_eligible_nodes(graph, source_node)

        for k in range(target_neighbors_amount - current_neighbors_amount):
            # get a random node from the eligible nodes and remove it from the pool
            target_node = random.choice(eligible_nodes)
            eligible_nodes.remove(target_node)

            # generate the link
            generate_link(graph, source_node, target_node, random.random() > uni_direct_ratio)

    return graph


# generate individual edge
def generate_link(graph, source_node, target_node, bi_direct):
    # add the source -> target link
    graph[source_node][target_node] = 1

    # if bidirectional, add the target -> source link
    if bi_direct:
        graph[target_node][source_node] = 1

    return graph


# generate a complete graph
def generate_graph(min_node_amount, max_node_amount, min_neighbor_amount, max_neighbor_amount, uni_direct_ratio):
    return generate_edges(generate_nodes(min_node_amount, max_node_amount), min_neighbor_amount, max_neighbor_amount,
                          uni_direct_ratio)

## EXAMPLES ##
# graph = generate_graph(10, 20, 2, 6, 0.25)
# pp.pprint(graph)

# for node in range(len(graph)):
#     print("Node " + str(node) + " has " + str(count_neighbors(graph, node)) + " neighbors")
