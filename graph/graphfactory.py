from __future__ import absolute_import

from builtins import range
import copy

from graph.graph import Graph
from utils.geo_tools import distance


class Vertex(object):
    __slots__ = ["id", "lat", "lon"]

    def __init__(self, id, lat, lon):
        self.id = id
        self.lat, self.lon = lat, lon

    @property
    def description(self):
        return "{} {} {}".format(self.id, self.lat, self.lon)


class Edge(object):
    __slots__ = ["s", "t", "length", "highway", "max_v", "forward", "backward", "name"]

    def __init__(self, s, t, length, highway, max_v, f, b, name):
        self.s, self.t = s, t
        self.length = length
        self.highway = highway
        self.max_v = max_v
        self.forward, self.backward = f, b
        self.name = name

    @property
    def description(self):
        return "{} {} {} {} {} {} {}".format(self.s, self.t, self.length, self.highway, self.max_v, self.forward, self.backward)


class SimpleEdge(object):
    __slots__ = ["s", "t", "length", "forward", "backward", "name"]

    def __init__(self, s, t, length):
        self.s, self.t = s, t
        self.length = length
        self.name = ""
        self.forward = True
        self.backward = True

    @property
    def description(self):
        return "{} {} {}".format(self.s, self.t, self.length)


def build_graph_from_osm(nodes, ways):

    assert isinstance(nodes, dict)
    assert isinstance(ways, list)

    graph = Graph()

    # 1. add all nodes and create mapping to 0 based index nodes
    node_ids = nodes.keys()
    id_mapper = dict(zip(node_ids, range(len(node_ids))))
    for n in nodes.values():
        graph.add_node(Vertex(id_mapper[n.osm_id], n.lat, n.lon))

    # 2. go through all ways and add edges accordingly
    for w in ways:
        for i in range(len(w.nodes) - 1):
            s_id, t_id = id_mapper[w.nodes[i]], id_mapper[w.nodes[i + 1]]
            s, t = graph.vertices[s_id], graph.vertices[t_id]
            length = distance(s.lat, s.lon, t.lat, t.lon)
            edge = Edge(s_id, t_id, length, w.highway, w.max_speed, w.forward, w.backward, w.name)
            graph.add_edge(edge)

    return graph


def build_graph_from_vertices_edges(vertices, edges):
    print("constructing new graph...")

    graph = Graph()

    # 1. add all nodes and create mapping to 0 based index nodes
    vertex_ids = set([v.id for v in vertices])
    id_mapper = dict(zip(vertex_ids, range(len(vertex_ids))))
    for v in vertices:
        graph.add_node(Vertex(id_mapper[v.id], v.lat, v.lon))

    # 2. add all edges that are valid
    new_edges = [copy.deepcopy(e) for e in edges if e.s in vertex_ids and e.t in vertex_ids]
    for e in new_edges:
        e.s = id_mapper[e.s]
        e.t = id_mapper[e.t]
        graph.add_edge(e)

    print("finished constructing new graph!")
    return graph
