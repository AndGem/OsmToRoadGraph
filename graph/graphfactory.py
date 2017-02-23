from __future__ import absolute_import

import copy

import graph.graph as graph
import graph.graph_types as graph_types
import utils.geo_tools as geo_tools
import utils.timer as timer


@timer.timer
def build_graph_from_osm(nodes, ways):

    assert isinstance(nodes, dict)
    assert isinstance(ways, list)

    g = graph.Graph()

    # 1. add all nodes and create mapping to 0 based index nodes
    node_ids = nodes.keys()
    id_mapper = dict(zip(node_ids, range(len(node_ids))))
    for n in nodes.values():
        g.add_node(graph_types.Vertex(id_mapper[n.osm_id], n.lat, n.lon))

    # 2. go through all ways and add edges accordingly
    for w in ways:
        for i in range(len(w.nodes) - 1):
            s_id, t_id = id_mapper[w.nodes[i]], id_mapper[w.nodes[i + 1]]
            s, t = g.vertices[s_id], g.vertices[t_id]
            length = geo_tools.distance(s.lat, s.lon, t.lat, t.lon)
            edge = graph_types.Edge(s_id, t_id, length, w.highway, w.max_speed, w.forward, w.backward, w.name)
            g.add_edge(edge)

    return g


@timer.timer
def build_graph_from_vertices_edges(vertices, edges):
    g = graph.Graph()

    # 1. add all nodes and create mapping to 0 based index nodes
    vertex_ids = set([v.id for v in vertices])
    id_mapper = dict(zip(vertex_ids, range(len(vertex_ids))))
    for v in vertices:
        g.add_node(graph_types.Vertex(id_mapper[v.id], v.lat, v.lon))

    # 2. add all edges that are valid
    new_edges = [copy.deepcopy(e) for e in edges if e.s in vertex_ids and e.t in vertex_ids]
    for e in new_edges:
        e.s = id_mapper[e.s]
        e.t = id_mapper[e.t]
        g.add_edge(e)

    return g
