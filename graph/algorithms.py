from __future__ import absolute_import
from collections import deque

import graph.graphfactory as graphfactory
import utils.timer as timer


def BFS(graph, s):
    seen_nodes = set([s])
    unvisited_nodes = deque([s])

    while len(unvisited_nodes) > 0:
        node_id = unvisited_nodes.popleft()
        unseen_nodes = list(filter(lambda n: n not in seen_nodes, graph.all_neighbors(node_id)))
        seen_nodes.update(unseen_nodes)
        unvisited_nodes.extend(unseen_nodes)

    return seen_nodes


@timer.timer
def computeLCC(graph):

    # repeatedly run BFS searches until all vertices have been reached
    total_nodes = set(range(len(graph.vertices)))
    found_nodes = []
    while len(total_nodes) > 0:
        f_nodes = BFS(graph, total_nodes.pop())
        found_nodes.append(f_nodes)
        total_nodes = total_nodes - f_nodes

    # determine largest connected components
    lcc = max(found_nodes, key=lambda component: len(component))

    print("\t LCC contains {} nodes (removed {} nodes)".format(len(lcc), len(graph.vertices) - len(lcc)))
    return lcc


def computeLCCGraph(graph):
    lcc = computeLCC(graph)
    new_nodes = [graph.vertices[id] for id in lcc]
    return graphfactory.build_graph_from_vertices_edges(new_nodes, graph.edges)
