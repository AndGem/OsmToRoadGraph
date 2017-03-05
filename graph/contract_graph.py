from __future__ import absolute_import
from copy import deepcopy

import graph.graphfactory as graphfactory
import graph.graph_types as graph_types
import utils.timer as timer


@timer.timer
def contract(graph):
    all_new_edges = find_new_edges(graph)
    filtered_edges = remove_duplicates(all_new_edges)
    node_ids = gather_node_ids(filtered_edges)
    nodes = get_nodes(graph, node_ids)

    return graphfactory.build_graph_from_vertices_edges(nodes, filtered_edges)


def get_nodes(graph, node_ids):
    return list(map(lambda node_id: graph.get_node(node_id), node_ids))


def gather_node_ids(edges):
    print("\t gathering nodes...")
    node_ids = set()
    for e in edges:
        node_ids.add(e.s)
        node_ids.add(e.t)
    return node_ids


def remove_duplicates(edges):
    print("\t removing duplicate edges...")
    added_edges = set()
    filtered_edges = []
    for edge in edges:
        if (edge.s, edge.t) not in added_edges and (edge.t, edge.s) not in added_edges:
            added_edges.add((edge.s, edge.t))
            filtered_edges.append(edge)

    return filtered_edges


def find_new_edges(graph):
    edge_by_s_t = edge_mapping(graph)
    all_new_edges = []
    for node_id in range(len(graph.vertices)):
        if is_important_node(graph, node_id):
            neighbors = graph.all_neighbors(node_id)
            for neighbor in neighbors:
                node_list = nodes_to_next_important_node(graph, node_id, neighbor)
                edges = get_edges(node_list, edge_by_s_t)
                new_edge = merge_edges(edges)
                if new_edge:
                    all_new_edges.append(new_edge)

    return all_new_edges


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
            return graph_types.SimpleEdge(s, t, sum([e.length for e in edges]))

    return None


def nodes_to_next_important_node(graph, start_node, next_node):
    if start_node == next_node:
        print("\t something is wrong here...")
        return []

    nodes = [start_node, next_node]

    while len(graph.all_neighbors(next_node)) == 2:
        neighbors = graph.all_neighbors(next_node)
        tmp = neighbors[0] if start_node == neighbors[1] else neighbors[1]
        start_node, next_node = next_node, tmp

        nodes.append(next_node)

    return nodes
