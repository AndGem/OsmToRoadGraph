import random
import string
import unittest

from graph.graph import Graph
from graph.graph_types import Edge, Vertex, EdgeData, VertexData
from graph.convert_graph import convert_to_networkx


def random_string(length=8):
    return "".join(random.choice(string.ascii_lowercase) for i in range(length))


def random_uint(max=1000):
    return random.randint(1, max)


class TestConvertGraphTest(unittest.TestCase):
    def test_converting_K4_graph(self):
        g = self.create_graph(number_nodes=4)

        g.add_edge(Edge(s=0, t=1, forward=True, backward=True, data=self.edge_data()))
        g.add_edge(Edge(s=1, t=2, forward=True, backward=True, data=self.edge_data()))
        g.add_edge(Edge(s=2, t=3, forward=True, backward=True, data=self.edge_data()))
        g.add_edge(Edge(s=3, t=0, forward=True, backward=True, data=self.edge_data()))

        g.add_edge(Edge(s=1, t=3, forward=True, backward=True, data=self.edge_data()))
        g.add_edge(Edge(s=0, t=2, forward=True, backward=True, data=self.edge_data()))

        nx_graph = convert_to_networkx(g)

        self.assertEqual(len(nx_graph.nodes), 4)
        self.assertEqual(len(nx_graph.edges), 12)

    def test_if_data_is_converted(self):
        g = self.create_graph(number_nodes=2)

        edge_data = self.edge_data()
        g.add_edge(Edge(s=0, t=1, forward=True, backward=True, data=edge_data))

        nx_graph = convert_to_networkx(g)

        self.assertEqual(len(nx_graph.nodes), 2)
        self.assertEqual(len(nx_graph.edges), 2)

        nx_edges = nx_graph.edges(data=True)
        e0, e1 = nx_edges
        self.assertCountEqual([(e0[0], e0[1]), (e1[0], e1[1])], [(0, 1), (1, 0)])
        self.assertDictEqual(
            e0[2],
            {
                "highway": edge_data.highway,
                "length": edge_data.length,
                "max_v": edge_data.max_v,
                "name": edge_data.name,
            },
        )
        self.assertDictEqual(
            e1[2],
            {
                "highway": edge_data.highway,
                "length": edge_data.length,
                "max_v": edge_data.max_v,
                "name": edge_data.name,
            },
        )

    def create_graph(self, number_nodes):
        g = Graph()
        for i in range(number_nodes):
            g.add_node(self.vertex(i))
        return g

    def edge_data(self):
        length = random_uint()
        highway = random_string()
        max_v = random_uint()
        name = random_string()

        return EdgeData(length=length, highway=highway, max_v=max_v, name=name)

    def vertex(self, index):
        return Vertex(index, VertexData(0, 0))
