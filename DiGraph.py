import EdgeData
import NodeData
from collections import defaultdict
from src import GraphInterface


class DiGraph(GraphInterface.GraphInterface):

    def __init__(self):
        self.Nodes = {}
        self.Edges = []
        self.from_node = defaultdict(list)
        self.to_node = defaultdict(list)
        self.mc = 0

    def v_size(self) -> int:
        return len(self.Nodes)

    def e_size(self) -> int:
        return len(self.Edges)

    def get_all_v(self) -> dict:
        return self.Nodes

    def get_all_edges(self) -> list:
        return self.Edges

    def all_in_edges_of_node(self, id1: int) -> dict:
        edges = {}
        for e in self.to_node[id1]:
            edges[e.get_src()] = e.get_weight()

        return edges

    def all_out_edges_of_node(self, id1: int) -> dict:
        edges = {}
        for e in self.from_node[id1]:
            edges[e.get_dest()] = e.get_weight()

        return edges

    def get_mc(self) -> int:
        return self.mc

    def add_edge(self, id1: int, id2: int, weight: float) -> bool:
        if id1 not in self.Nodes.keys() or id2 not in self.Nodes.keys():
            return False

        for e in self.Edges:
            if e.get_src() == id1 and e.get_dest() == id2:
                return False

        e = EdgeData.EdgeData(id1, id2, weight)
        self.Edges.append(e)
        self.from_node[id1].append(e)
        self.to_node[id2].append(e)
        self.mc += 1
        return True

    def add_node(self, node_id: int, pos: tuple = None) -> bool:
        n = NodeData.NodeData(node_id, pos)
        if node_id not in self.Nodes.keys():
            self.Nodes[node_id] = n
            self.mc += 1
            return True
        return False

    def remove_node(self, node_id: int) -> bool:
        if node_id in self.Nodes.keys():
            del self.Nodes[node_id]
            del self.from_node[node_id]
            del self.to_node[node_id]
            for e in self.Edges:
                if e.get_src() == node_id or e.get_dest() == node_id:
                    self.Edges.remove(e)
            self.mc += 1
            return True
        return False

    def remove_edge(self, node_id1: int, node_id2: int) -> bool:
        if node_id1 in self.Nodes.keys() and node_id2 in self.Nodes.keys():
            for e in self.from_node.get(node_id1):
                if e.get_dest() == node_id2:
                    self.from_node.get(node_id1).remove(e)

            for e in self.to_node.get(node_id2):
                if e.get_src() == node_id1:
                    self.to_node.get(node_id2).remove(e)

            for e in self.Edges:
                if e.get_src() == node_id1 and e.get_dest() == node_id2:
                    self.Edges.remove(e)
            self.mc += 1
            return True
        return False
