from builtins import range
from copy import deepcopy

import graphfactory


def contract(graph):

    edge_by_s_t = edge_mapping(graph)

    # find stuff
    all_edges = []
    for node_id in range(len(graph.vertices)):

        if is_important_node(graph, node_id):
            neighbors = graph.all_neighbors(node_id)
            for neighbor in neighbors:
                node_list = nodes_to_next_important_node(graph, node_id, neighbor)
                edges = get_edges(node_list, edge_by_s_t)
                new_edge = merge_edges(edges)
                if new_edge:
                    all_edges.append(new_edge)

    # 
    print("removing duplciate edges...")
    added_edges = set()
    filtered_edges = []
    for edge in all_edges:
        if (edge.s, edge.t) not in added_edges and (edge.t, edge.s) not in added_edges:
            added_edges.add((edge.s, edge.t))
            filtered_edges.append(edge)

    print("gathering nodes...")
    vertex_ids = set()
    for e in all_edges:
        vertex_ids.add(e.s)
        vertex_ids.add(e.t)

    nodes = list(map(lambda n: graph.vertices[n], vertex_ids))
    print("done")
    print("creating graph...")

    return graphfactory.build_graph_from_vertices_edges(nodes, filtered_edges)


def edge_mapping(graph):
    edge_by_s_t = {}
    for edge in graph.edges:
        edge_by_s_t[(edge.s, edge.t)] = edge

        if (edge.t, edge.s) not in edge_by_s_t:
            new_edge = deepcopy(edge)
            new_edge.s, new_edge.t = edge.t, edge.s
            edge_by_s_t[(edge.t, edge.s)] = new_edge

    return edge_by_s_t


def is_important_node(graph, node_id):
    return len(graph.all_neighbors(node_id)) != 2


def get_edges(nodes, edges_by_s_t):
    if nodes:
        edges = []
        for i in range(len(nodes) - 1):
            edges.append(edges_by_s_t[(nodes[i], nodes[i+1])])
        return edges

    return []


def merge_edges(edges):
    if edges:
        s, t = edges[0].s, edges[-1].t
        if s != t:
            return graphfactory.SimpleEdge(s, t, sum([e.length for e in edges]))

    return None


def nodes_to_next_important_node(graph, start_node, next_node):
    if start_node == next_node:
        print("something is wrong here...")
        return []

    nodes = [start_node, next_node]

    while len(graph.all_neighbors(next_node)) == 2:
        neighbors = graph.all_neighbors(next_node)
        tmp = neighbors[0] if start_node == neighbors[1] else neighbors[1]
        start_node, next_node = next_node, tmp

        nodes.append(next_node)

    return nodes
