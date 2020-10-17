import copy

from graph.graph import Graph
from graph.graph_types import Vertex, Edge, VertexData, EdgeData
from osm.osm_types import OSMNode, OSMWay
import utils.geo_tools as geo_tools
import utils.timer as timer

from typing import Dict, List, Tuple


@timer.timer
def build_graph_from_osm(nodes: Dict[int, OSMNode], ways: List[OSMWay]) -> Graph:

    assert isinstance(nodes, dict)
    assert isinstance(ways, list)

    g = Graph()

    # 1. add all nodes and create mapping to 0 based index nodes
    node_ids = nodes.keys()
    id_mapper = dict(zip(node_ids, range(len(node_ids))))
    for n in nodes.values():
        g.add_node(Vertex(id_mapper[n.osm_id], data=VertexData(n.lat, n.lon)))

    # 2. go through all ways and add edges accordingly
    bidirectional_edges: Dict[Tuple[int, int], int] = dict()
    for w in ways:
        for i in range(len(w.nodes) - 1):
            s_id, t_id = id_mapper[w.nodes[i]], id_mapper[w.nodes[i + 1]]
            s, t = g.vertices[s_id], g.vertices[t_id]
            length = round(geo_tools.distance(s.data.lat, s.data.lon, t.data.lat, t.data.lon), 2)
            data = EdgeData(length=length, highway=w.highway, max_v=w.max_speed_int, name=w.name)
            edge = Edge(s_id, t_id, w.forward, w.backward, data=data)
            if w.forward and w.backward:
                smaller = s_id if s_id < t_id else t_id
                bigger = s_id if s_id > t_id else t_id
                if (smaller, bigger) in bidirectional_edges:
                    print(f"found duplicated bidirectional edge {(smaller, bigger)}.. (osm ids {w.osm_id} and {bidirectional_edges[(smaller, bigger)]})... skipping one")
                    continue
                bidirectional_edges[(smaller, bigger)] = w.osm_id

            g.add_edge(edge)

    return g


@timer.timer
def build_graph_from_vertices_edges(vertices: List[Vertex], edges: List[Edge]) -> Graph:
    g = Graph()

    # 1. add all nodes and create mapping to 0 based index nodes
    vertex_ids = set(v.id for v in vertices)
    id_mapper = dict(zip(vertex_ids, range(len(vertex_ids))))
    for v in vertices:
        g.add_node(Vertex(id_mapper[v.id], v.data))

    # 2. add all edges that are valid
    new_edges = [copy.deepcopy(e) for e in edges if e.s in vertex_ids and e.t in vertex_ids]
    for e in new_edges:
        e.s = id_mapper[e.s]
        e.t = id_mapper[e.t]
        g.add_edge(e)

    return g
