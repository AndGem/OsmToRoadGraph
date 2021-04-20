from graph.graph_types import Edge, Vertex
from typing import List, Set


class Graph:
    def __init__(self) -> None:
        self.edges: List[Edge] = []
        self.vertices: List[Vertex] = []
        self.outneighbors: List[Set[int]] = []
        self.inneighbors: List[Set[int]] = []

    def add_edge(self, edge: Edge) -> None:
        self.edges.append(edge)

        if edge.forward:
            self.outneighbors[edge.s].add(edge.t)
            self.inneighbors[edge.t].add(edge.s)

        if edge.backward:
            self.outneighbors[edge.t].add(edge.s)
            self.inneighbors[edge.s].add(edge.t)

    def add_node(self, vertex: Vertex) -> None:
        self.vertices.append(vertex)
        self.outneighbors.append(set())
        self.inneighbors.append(set())

    def get_node(self, node_id: int) -> Vertex:
        return self.vertices[node_id]

    def edge_description(self, edge_id):
        return "{}".format(self.edges[edge_id].description)

    def edge_name(self, edge_id):
        return "{}".format(self.edges[edge_id].name)

    def all_neighbors(self, node_id: int) -> List[int]:
        return list(self.outneighbors[node_id].union(self.inneighbors[node_id]))
