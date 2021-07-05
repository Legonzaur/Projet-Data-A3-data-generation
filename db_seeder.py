#!/bin/python

import sys
from db.db_connector import DbConnector
from graph_tools.generate_graph import Graph
from graph_tools.generate_traffic import Traffic

db = DbConnector()
graph = Graph()
traffic = Traffic(graph)

graph.generate_graph(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
matrix = traffic.browse_matrix()
db.save_graph_with_traffic(matrix)
