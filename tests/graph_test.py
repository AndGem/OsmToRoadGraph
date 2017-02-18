from __future__ import absolute_import

import unittest

from graph.graph import Graph
from graph.graph_types import Edge, Vertex


class GraphTest(unittest.TestCase):

    def add_edge_adds_one_edge_test(self):
        g = Graph()

        v1, v2 = self.get_vertex(0), self.get_vertex(1)
        e = Edge(v1.id, v2.id, 1, " ", 100, True, True, "Test")

        g.add_node(v1)
        g.add_node(v2)
        g.add_edge(e)

        self.assertEqual(len(g.edges), 1)
        self.assertEqual(g.edges[0], e)

    def add_edges_correct_in_out_neighbors_test(self):
        g = Graph()

        v1, v2, v3, v4 = self.get_vertex(0), self.get_vertex(1), self.get_vertex(2), self.get_vertex(3)
        e_forward = Edge(v1.id, v2.id, 1, " ", 100, True, False, "Test")
        e_backward = Edge(v2.id, v3.id, 1, " ", 100, False, True, "Test")
        e_nothing = Edge(v3.id, v4.id, 1, " ", 100, False, False, "Test")
        e_both = Edge(v4.id, v1.id, 1, " ", 100, True, True, "Test")

        g.add_node(v1)
        g.add_node(v2)
        g.add_node(v3)
        g.add_node(v4)

        g.add_edge(e_forward)
        g.add_edge(e_backward)
        g.add_edge(e_nothing)
        g.add_edge(e_both)

        self.assertEqual(len(g.edges), 4)
        self.assertEqual(g.edges[0], e_forward)
        self.assertEqual(g.edges[1], e_backward)
        self.assertEqual(g.edges[2], e_nothing)
        self.assertEqual(g.edges[3], e_both)

        self.assertTrue(e_forward.s in g.inneighbors[e_forward.t])
        self.assertTrue(e_forward.t in g.outneighbors[e_forward.s])
        self.assertTrue(e_forward.s not in g.outneighbors[e_forward.t])
        self.assertTrue(e_forward.t not in g.inneighbors[e_forward.s])

        self.assertTrue(e_backward.s not in g.inneighbors[e_backward.t])
        self.assertTrue(e_backward.t not in g.outneighbors[e_backward.s])
        self.assertTrue(e_backward.s in g.outneighbors[e_backward.t])
        self.assertTrue(e_backward.t in g.inneighbors[e_backward.s])

        self.assertTrue(e_nothing.s not in g.inneighbors[e_nothing.t])
        self.assertTrue(e_nothing.t not in g.outneighbors[e_nothing.s])
        self.assertTrue(e_nothing.s not in g.outneighbors[e_nothing.t])
        self.assertTrue(e_nothing.t not in g.inneighbors[e_nothing.s])

        self.assertTrue(e_both.s in g.inneighbors[e_both.t])
        self.assertTrue(e_both.t in g.outneighbors[e_both.s])
        self.assertTrue(e_both.s in g.outneighbors[e_both.t])
        self.assertTrue(e_both.t in g.inneighbors[e_both.s])

    def add_edges_correct_set_of_neighbors_test(self):
        g = Graph()
        v1, v2, v3 = self.get_vertex(0), self.get_vertex(1), self.get_vertex(2)
        e_forward = Edge(v1.id, v2.id, 1, " ", 100, True, False, "Test")
        e_backward = Edge(v2.id, v3.id, 1, " ", 100, False, True, "Test")
        e_both = Edge(v3.id, v1.id, 1, " ", 100, True, True, "Test")

        g.add_node(v1)
        g.add_node(v2)
        g.add_node(v3)

        g.add_edge(e_forward)
        g.add_edge(e_backward)
        g.add_edge(e_both)

        self.assertTrue(self.checkEqual([v2.id, v3.id], g.all_neighbors(v1.id)))
        self.assertTrue(self.checkEqual([v1.id, v3.id], g.all_neighbors(v2.id)))
        self.assertTrue(self.checkEqual([v1.id, v2.id], g.all_neighbors(v3.id)))

    def checkEqual(self, L1, L2):
        return len(L1) == len(L2) and sorted(L1) == sorted(L2)

    def get_vertex(self, index=0):
        return Vertex(index, 1.2, 2.3)
