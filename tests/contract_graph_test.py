import unittest

from graph.graph import Graph
from graph.graph_types import Edge, Vertex, EdgeData, VertexData
from graph.contract_graph import ContractGraph


class ContractGraphTest(unittest.TestCase):
    def test_contract_a_path_to_two_nodes_and_one_edge(self):
        g = self.create_graph(number_nodes=3)

        g.add_edge(Edge(s=0, t=1, forward=True, backward=True, data=self.edge_data()))
        g.add_edge(Edge(s=1, t=2, forward=True, backward=True, data=self.edge_data()))

        contracted_graph = ContractGraph(g).contract()

        self.assertEqual(len(contracted_graph.vertices), 2)
        self.assertEqual(len(contracted_graph.edges), 1)

    def test_contract_loop_to_nothing(self):
        g = self.create_graph(number_nodes=4)

        # loop
        g.add_edge(Edge(s=0, t=1, forward=True, backward=True, data=self.edge_data()))
        g.add_edge(Edge(s=1, t=2, forward=True, backward=True, data=self.edge_data()))
        g.add_edge(Edge(s=2, t=0, forward=True, backward=True, data=self.edge_data()))

        # connection (otherwise no intersections will be found)
        g.add_edge(Edge(s=0, t=3, forward=True, backward=True, data=self.edge_data()))

        contracted_graph = ContractGraph(g).contract()

        self.assertEqual(len(contracted_graph.vertices), 2)
        self.assertEqual(len(contracted_graph.edges), 1)

    def test_contracting_stops_if_edge_is_different(self):
        g = self.create_graph(number_nodes=10)

        g.add_edge(
            Edge(
                s=0,
                t=1,
                forward=True,
                backward=True,
                data=self.edge_data(length=2, name="abc"),
            )
        )
        g.add_edge(
            Edge(
                s=1,
                t=2,
                forward=True,
                backward=True,
                data=self.edge_data(length=3, name="abc"),
            )
        )
        g.add_edge(
            Edge(
                s=2,
                t=3,
                forward=True,
                backward=True,
                data=self.edge_data(length=5, name="def"),
            )
        )
        g.add_edge(
            Edge(
                s=3,
                t=4,
                forward=True,
                backward=True,
                data=self.edge_data(length=7, name="def"),
            )
        )
        g.add_edge(
            Edge(
                s=4,
                t=5,
                forward=True,
                backward=True,
                data=self.edge_data(length=11, name="ghi"),
            )
        )
        g.add_edge(
            Edge(
                s=5,
                t=6,
                forward=True,
                backward=True,
                data=self.edge_data(length=13, name="ghi"),
            )
        )
        g.add_edge(
            Edge(
                s=6,
                t=7,
                forward=True,
                backward=True,
                data=self.edge_data(length=17, name="jkl"),
            )
        )
        g.add_edge(
            Edge(
                s=7,
                t=8,
                forward=True,
                backward=True,
                data=self.edge_data(length=23, name="mno"),
            )
        )
        g.add_edge(
            Edge(
                s=8,
                t=9,
                forward=True,
                backward=True,
                data=self.edge_data(length=29, name="mno"),
            )
        )
        # input: 0-1-2-3-4-5-6-7-8-9
        # expected outcome: 0-2-4-6-7-9

        contracted_graph = ContractGraph(g).contract()

        self.assertEqual(len(contracted_graph.vertices), 6)
        self.assertEqual(len(contracted_graph.edges), 5)

        result_edge_data = [e.data for e in contracted_graph.edges]
        expected_edge_data = [
            self.edge_data(length=5, name="abc"),
            self.edge_data(length=12, name="def"),
            self.edge_data(length=24, name="ghi"),
            self.edge_data(length=17, name="jkl"),
            self.edge_data(length=52, name="mno"),
        ]
        self.assertCountEqual(result_edge_data, expected_edge_data)

    def test_contracting_stops_at_intersections(self):
        g = self.create_graph(number_nodes=7)

        # path of 5 nodes
        g.add_edge(Edge(s=0, t=1, forward=True, backward=True, data=self.edge_data()))
        g.add_edge(Edge(s=1, t=2, forward=True, backward=True, data=self.edge_data()))
        g.add_edge(Edge(s=2, t=3, forward=True, backward=True, data=self.edge_data()))
        g.add_edge(Edge(s=3, t=4, forward=True, backward=True, data=self.edge_data()))

        # path of two nodes attached in the middle of the path above
        g.add_edge(Edge(s=2, t=5, forward=True, backward=True, data=self.edge_data()))
        g.add_edge(Edge(s=5, t=6, forward=True, backward=True, data=self.edge_data()))

        # expected outcome: 4 nodes remain, and 3 edges, one deg 3 node, all others are deg 1 nodes

        contracted_graph = ContractGraph(g).contract()

        self.assertEqual(len(contracted_graph.vertices), 4)
        self.assertEqual(len(contracted_graph.edges), 3)

        nmb_neigbors = [len(contracted_graph.all_neighbors(n_id)) for n_id in range(4)]
        self.assertCountEqual(nmb_neigbors, [3, 1, 1, 1])

    def test_no_contraction_if_each_edge_is_different(self):
        g = self.create_graph(number_nodes=6)

        g.add_edge(
            Edge(s=0, t=1, forward=True, backward=True, data=self.edge_data(name="a"))
        )
        g.add_edge(
            Edge(
                s=1,
                t=2,
                forward=True,
                backward=True,
                data=self.edge_data(name="a", highway="b"),
            )
        )
        g.add_edge(
            Edge(
                s=2,
                t=3,
                forward=True,
                backward=False,
                data=self.edge_data(name="a", highway="b"),
            )
        )
        g.add_edge(
            Edge(
                s=3,
                t=4,
                forward=True,
                backward=True,
                data=self.edge_data(name="a", highway="b"),
            )
        )
        g.add_edge(
            Edge(
                s=4,
                t=5,
                forward=True,
                backward=True,
                data=self.edge_data(name="a", highway="b", max_v=123),
            )
        )

        contracted_graph = ContractGraph(g).contract()

        self.assertEqual(len(contracted_graph.vertices), 6)
        self.assertEqual(len(contracted_graph.edges), 5)

        result_edge_data = [e.data for e in contracted_graph.edges]
        expected_edge_data = [
            self.edge_data(name="a"),
            self.edge_data(name="a", highway="b"),
            self.edge_data(name="a", highway="b"),
            self.edge_data(name="a", highway="b"),
            self.edge_data(name="a", highway="b", max_v=123),
        ]
        self.assertCountEqual(result_edge_data, expected_edge_data)

    def create_graph(self, number_nodes):
        g = Graph()
        for i in range(number_nodes):
            g.add_node(self.vertex(i))
        return g

    def edge_data(self, length=1, highway="", max_v=50, name=""):
        return EdgeData(length=length, highway=highway, max_v=max_v, name=name)

    def vertex(self, index):
        return Vertex(index, VertexData(0, 0))
