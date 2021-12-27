from typing import List
import sys
import json
import DiGraph
from src import GraphAlgoInterface
from src import GraphInterface
from itertools import permutations
import copy

class GraphAlgo(GraphAlgoInterface.GraphAlgoInterface):

    def __init__(self, g: GraphInterface.GraphInterface = DiGraph.DiGraph()):
        self.g = g

    def get_graph(self) -> GraphInterface:
        return self.g

    def load_from_json(self, file_name: str) -> bool:
        try:
            f = open(file_name)
            data = json.load(f)
            Edges = data.get("Edges")
            Nodes = data.get("Nodes")
            for n in Nodes:
                pos = n.get("pos")
                new_pos = pos.split(",")
                self.g.add_node(n.get("id"), (new_pos[0], new_pos[1]))
            for e in Edges:
                self.g.add_edge(e.get("src"), e.get("dest"), e.get("w"))
            return True
        except FileNotFoundError:
            return False

    def save_to_json(self, file_name: str) -> bool:

        Nodes = self.g.get_all_v()
        new_Nodes = []
        for n in Nodes:
            new_n = Nodes.get(n)
            st = new_n.getPos()
            st1 = st[0] + "," + st[1] + ",0.0"
            list_n = {}
            list_n["pos"] = st1
            list_n["id"] = n
            new_Nodes.append(list_n)

        Edges = self.g.get_all_edges()
        new_Edges = []
        for e in Edges:
            list_e = {}
            list_e["src"] = e.get_src()
            list_e["w"] = e.get_weight()
            list_e["dest"] = e.get_dest()
            new_Edges.append(list_e)
        new_graph = {}
        new_graph["Edges"] = new_Edges
        new_graph["Nodes"] = new_Nodes

        try:
            with open(file_name, 'w') as outfile:
                json.dump(new_graph, outfile)
                return True
        except:
            return False

    def shortest_path(self, id1: int, id2: int) -> (float, list):
        id_weight = {}
        id_previous = {}
        unvisited = list(self.g.get_all_v().keys())
        visited = []
        for n in self.g.get_all_v():
            if n == id1:
                id_weight[n] = 0
            else:
                id_weight[n] = sys.float_info.max

        while unvisited:
            current_vertex = min(unvisited, key=id_weight.get)
            neighbours = self.g.all_out_edges_of_node(current_vertex)
            for n in neighbours:
                path_weight = neighbours[n] + id_weight[current_vertex]
                if path_weight < id_weight[n]:
                    id_weight[n] = path_weight
                    id_previous[n] = current_vertex
            unvisited.remove(current_vertex)
            visited.append(current_vertex)

        if not id_previous:
            return -1, []

        w = id_weight[id2]
        path = [id2]
        current_node = id2
        while current_node != id1:
            if current_node in id_previous:
                current_node = id_previous[current_node]
                path.append(current_node)
            else:
                return -1, []

        path = path[::-1]
        return w, path


    def longest_path(self, id1: int) -> float:
        id_weight = {}
        id_previous = {}
        unvisited = list(self.g.get_all_v().keys())
        visited = []
        for n in self.g.get_all_v():
            if n == id1:
                id_weight[n] = 0
            else:
                id_weight[n] = sys.float_info.max

        while unvisited:
            current_vertex = min(unvisited, key=id_weight.get)
            neighbours = self.g.all_out_edges_of_node(current_vertex)
            for n in neighbours:
                path_weight = neighbours[n] + id_weight[current_vertex]
                if path_weight < id_weight[n]:
                    id_weight[n] = path_weight
                    id_previous[n] = current_vertex
            unvisited.remove(current_vertex)
            visited.append(current_vertex)

        return max(id_weight.values())

    def TSP(self, node_lst: List[int]) -> (List[int], float):
        start_end = list(permutations(node_lst, 2))
        best_path = None
        best_path_weight = sys.float_info.max
        for pair in start_end:
            w, p = GraphAlgo.shortest_path(self, pair[0], pair[1])
            check = all(item in p for item in node_lst)
            if w < best_path_weight and check:
                best_path = p
                best_path_weight = w
        return best_path, best_path_weight


    def centerPoint(self) -> (int, float):
        center = None
        weight = sys.float_info.max
        for n in self.g.get_all_v():
            longest_path = GraphAlgo.longest_path(self, n)
            if longest_path < weight:
                center = n
                weight = longest_path

        return center, weight

    def plot_graph(self) -> None:

        raise NotImplementedError
