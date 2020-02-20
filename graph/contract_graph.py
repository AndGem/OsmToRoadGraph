from copy import deepcopy
from collections import deque, defaultdict

import graph.graphfactory as graphfactory
import utils.timer as timer

from graph.graph import Graph
from graph.graph_types import Vertex, Edge
from typing import List, Set


@timer.timer
def contract(graph: Graph):
    all_new_edges = _find_new_edges(graph)
    node_ids = _gather_node_ids(all_new_edges)
    nodes = _get_nodes(graph, node_ids)

    print(f"finished contracting: {len(all_new_edges)}/{len(graph.edges)} edges and {len(nodes)}/{len(graph.vertices)} vertices.")

    return graphfactory.build_graph_from_vertices_edges(nodes, all_new_edges)


def _find_new_edges(graph: Graph):
    #  TODO: simplify and test this method
    #  maintain a list L of nodes from which we want to start searches to find new contracted edges
    #  initialize L with all intersection nodes (i.e., all nodes with degree != 2)
    #   for each node n in L
    #     for each of n's neighbor
    #       search until:
    #           - an intersection node is found or edge is found
    #           - the next edge is different in it's structure (e.g., different highway type, different max speed, ...)
    start_nodes = _find_all_intersections(graph)
    seen_start_nodes = set(start_nodes)
    new_edges = set()
    bidirectional_edges = set()

    out_edges_per_node = _get_out_edges(graph)
    while len(start_nodes) > 0:
        node_id = start_nodes.popleft()

        out_edges = out_edges_per_node[node_id]
        for first_out_edge in out_edges:
            used_edges = []
            start_node_id = node_id

            out_edge = first_out_edge
            current_node_id = start_node_id
            while True:
                used_edges.append(out_edge)
                next_node_id = out_edge.t if out_edge.s == current_node_id else out_edge.s
                if _is_intersection(next_node_id, graph):
                    break
                if next_node_id == start_node_id:
                    # detected a loop => remove it
                    used_edges = []
                    break

                next_out_edges = list(filter(lambda e: (e.s != current_node_id) and (e.t != current_node_id), out_edges_per_node[next_node_id]))

                if len(next_out_edges) == 0:
                    # detected a dead end => stop
                    break
                elif len(next_out_edges) > 1:
                    # something is wrong.. this should have been filtered out by the intersection check
                    assert False
                else:
                    next_out_edge = next_out_edges[0]
                    if _is_not_same_edge(out_edge, next_out_edge):
                        if next_node_id not in seen_start_nodes:
                            #  found a new possible start node
                            seen_start_nodes.add(next_node_id)
                            start_nodes.append(next_node_id)
                        #  break out since we need to stop here
                        break
                    else:
                        out_edge = next_out_edge
                        current_node_id = next_node_id
            final_node_id = next_node_id

            if len(used_edges) == 0:
                continue

            data = deepcopy(used_edges[0].data)
            data.length = sum([e.data.length for e in used_edges])
            if used_edges[0].backward:
                #  deduplication measure; if not for this for bidirectional edges, that are
                #  removed between intersections, 2 new edges would be created
                smaller_node_id = start_node_id if start_node_id < final_node_id else final_node_id
                bigger_node_id = start_node_id if start_node_id > final_node_id else final_node_id
                if (smaller_node_id, bigger_node_id) in bidirectional_edges:
                    # already added this edge skip it
                    continue
                bidirectional_edges.add((smaller_node_id, bigger_node_id))
                merged_edge = Edge(smaller_node_id, bigger_node_id, True, used_edges[0].backward, data)
            else:
                merged_edge = Edge(start_node_id, final_node_id, True, used_edges[0].backward, data)
            new_edges.add(merged_edge)
    return new_edges


def _is_not_same_edge(e1: Edge, e2: Edge):
    return e1.data.highway != e2.data.highway or e1.data.max_v != e2.data.max_v or e1.data.name != e2.data.name or e1.backward != e2.backward


def _get_out_edges(graph: Graph):
    result = defaultdict(list)
    for e in graph.edges:
        if e.forward:
            result[e.s].append(e)
        if e.backward:
            result[e.t].append(e)
    return result


def _find_all_intersections(graph: Graph):
    node_ids = range(0, len(graph.vertices))
    return deque(filter(lambda node_id: _is_intersection(node_id, graph), node_ids))


def _get_nodes(graph: Graph, node_ids: Set[int]) -> List[Vertex]:
    return list(map(lambda node_id: graph.get_node(node_id), node_ids))


def _gather_node_ids(edges: List[Edge]) -> Set[int]:
    print("\t gathering nodes...")
    node_ids = set()
    for e in edges:
        node_ids.add(e.s)
        node_ids.add(e.t)
    return node_ids


def _is_intersection(node_id: int, graph: Graph) -> bool:
    return len(graph.all_neighbors(node_id)) != 2
