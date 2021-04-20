import unittest

import graph.graphfactory as gf
from graph.graph_types import Vertex, Edge, VertexData, EdgeData


class GraphfactorTest(unittest.TestCase):
    def test_empty_input_test(self):
        g = gf.build_graph_from_vertices_edges([], [])
        self.assertTrue(len(g.vertices) == 0)
        self.assertTrue(len(g.edges) == 0)

    def test_one_vertex_should_be_no_edge_test(self):
        v = Vertex(23, VertexData(1, 2))
        g = gf.build_graph_from_vertices_edges([v], [])
        self.assertTrue(len(g.vertices) == 1)
        self.assertEqual(g.vertices[0].data, v.data)
        self.assertTrue(len(g.edges) == 0)

    def test_two_vertex_should_be_one_edge_test(self):
        v1 = Vertex(23, VertexData(1, 1))
        v2 = Vertex(24, VertexData(2, 1))
        e = Edge(23, 24, True, True, EdgeData(123, "", 50, ""))
        g = gf.build_graph_from_vertices_edges([v1, v2], [e])
        self.assertTrue(len(g.vertices) == 2)
        self.assertTrue(len(g.edges) == 1)
        self.assertEqual(g.edges[0].data.length, 123)

    def test_two_vertex_should_fail_test(self):
        v1 = Vertex(23, VertexData(1, 1))
        v2 = Vertex(24, VertexData(2, 1))
        e = Edge(21, 24, True, True, EdgeData(123, "", 50, ""))
        g = gf.build_graph_from_vertices_edges([v1, v2], [e])
        self.assertTrue(len(g.vertices) == 2)
        self.assertTrue(len(g.edges) == 0)

    def test_three_vertex_should_three_edges_test(self):
        v1 = Vertex(23, VertexData(1, 1))
        v2 = Vertex(24, VertexData(2, 1))
        v3 = Vertex(1, VertexData(5, 6))
        e1 = Edge(v1.id, v2.id, True, True, EdgeData(123, "", 50, ""))
        e2 = Edge(v2.id, v3.id, True, True, EdgeData(123, "", 50, ""))
        e3 = Edge(v1.id, v3.id, True, True, EdgeData(123, "", 50, ""))
        g = gf.build_graph_from_vertices_edges([v1, v2, v3], [e1, e2, e3])
        self.assertTrue(len(g.vertices) == 3)
        self.assertTrue(len(g.edges) == 3)
