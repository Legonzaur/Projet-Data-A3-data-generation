from db.db_connector import DbConnector
from graph_tools.generate_graph import Graph
from graph_tools.generate_traffic import Traffic

db = DbConnector()
graph = Graph()
traffic = Traffic(graph)

graph.generate_graph()
matrix = traffic.browse_matrix()
db.save_graph_with_traffic(matrix)
