from pymongo import MongoClient
from pprint import pprint
import copy


class DbConnector:
    client = None
    database_name = None
    db_data = None

    # Initialize connection. arguments can be given to override defaults
    def __init__(self, host="localhost", port=27017, db_name="data_project"):
        self.client = MongoClient(host, port)
        self.database_name = db_name
        self.db_data = self.client[db_name]

    def get_graph(self, _id, collection="graphs"):
        return self.db_data[collection].find_one({"_id": _id})

    def save_graph(self, graph_data, collection="graphs"):
        graph = {
            "size": len(graph_data),
            "matrix": graph_data
        }
        return self.db_data[collection].insert_one(graph).inserted_id

    def get_traffic(self, graph_id, source_node, target_node, collection="traffic"):
        search_filter = {
            "graph_id": graph_id,
            "source_node": source_node,
            "target_node": target_node,
        }
        return self.db_data[collection].find(search_filter)

    def save_traffic(self, graph_id, source_node, target_node, traffic_data, collection="traffic"):
        traffic = {
            "graph_id": graph_id,
            "source_node": source_node,
            "target_node": target_node,
            "data": traffic_data
        }
        return self.db_data[collection].insert_one(traffic).inserted_id

    def get_graph_with_traffic(self, graph_id, graph_collection="graphs", traffic_collection="traffic"):
        graph = self.get_graph(graph_id, graph_collection)["matrix"]
        for source_node, targets in enumerate(graph):
            for target_node, link_weight in enumerate(targets):
                if link_weight is not None:
                    graph[source_node][target_node] = self.get_traffic(graph_id, source_node, target_node, traffic_collection)["data"]

        return graph

    def save_graph_with_traffic(self, graph_data, graph_collection="graphs", traffic_collection="traffic"):
        matrix = copy.deepcopy(graph_data)
        for source_node, targets in enumerate(matrix):
            for target_node, link in enumerate(targets):
                if isinstance(link, list):
                    matrix[source_node][target_node] = 1

        graph_id = self.save_graph(matrix, graph_collection)
        for source_node, targets in enumerate(graph_data):
            for target_node, link in enumerate(targets):
                if isinstance(link, list):
                    self.save_traffic(graph_id, source_node, target_node, link, traffic_collection)

        return graph_id
