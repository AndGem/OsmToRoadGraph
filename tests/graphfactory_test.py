import unittest

import graph.graphfactory as gf
from graph.graph_types import Vertex, SimpleEdge


class GraphfactorTest(unittest.TestCase):

    def empty_input_test(self):
        g = gf.build_graph_from_vertices_edges([], [])
        self.assertTrue(len(g.vertices) == 0)
        self.assertTrue(len(g.edges) == 0)

    def one_vertex_should_be_no_edge_test(self):
        v = Vertex(23, 1, 2)
        g = gf.build_graph_from_vertices_edges([v], [])
        self.assertTrue(len(g.vertices) == 1)
        self.assertEqual(g.vertices[0].lat, v.lat)
        self.assertEqual(g.vertices[0].lon, v.lon)
        self.assertTrue(len(g.edges) == 0)

    def two_vertex_should_be_one_edge_test(self):
        v1 = Vertex(23, 1, 1)
        v2 = Vertex(24, 2, 1)
        e = SimpleEdge(23, 24, 123)
        g = gf.build_graph_from_vertices_edges([v1, v2], [e])
        self.assertTrue(len(g.vertices) == 2)
        self.assertTrue(len(g.edges) == 1)
        self.assertEquals(g.edges[0].length, 123)

    def two_vertex_should_fail_test(self):
        v1 = Vertex(23, 1, 1)
        v2 = Vertex(24, 2, 1)
        e = SimpleEdge(21, 24, 123)
        g = gf.build_graph_from_vertices_edges([v1, v2], [e])
        self.assertTrue(len(g.vertices) == 2)
        self.assertTrue(len(g.edges) == 0)

    def three_vertex_should_three_edges_test(self):
        v1 = Vertex(23, 1, 2)
        v2 = Vertex(24, 3, 4)
        v3 = Vertex(1, 5, 6)
        e1 = SimpleEdge(v1.id, v2.id, 123)
        e2 = SimpleEdge(v2.id, v3.id, 1234)
        e3 = SimpleEdge(v1.id, v3.id, 12345)
        g = gf.build_graph_from_vertices_edges([v1, v2, v3], [e1, e2, e3])
        self.assertTrue(len(g.vertices) == 3)
        self.assertTrue(len(g.edges) == 3)
