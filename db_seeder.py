import pprint

from bson.objectid import ObjectId
from DbConnector import DbConnector
from generate_graph import Graph
from generate_traffic import Traffic

db = DbConnector()
graph = Graph()
traffic = Traffic(graph)
nb = 10

# for i in range(nb):
#     print("seeding " + str(i + 1) + "/" + str(nb))
#     graph.generate_graph()
#     matrix = traffic.browse_matrix()
#     db.save_graph_with_traffic(matrix)

# pprint.pprint(db.get_graph_with_traffic(ObjectId("60dca30d29285cf539498a78")))
