from collections import deque

from graph import graphfactory
from utils import timer

from graph.graph import Graph
from typing import Deque, Set


def BFS(graph: Graph, s: int) -> Set[int]:
    seen_nodes: Set[int] = {s}
    unvisited_nodes: Deque[int] = deque([s])

    while unvisited_nodes:
        current_node = unvisited_nodes.popleft()
        unseen_nodes = [
            neighbor
            for neighbor in graph.all_neighbors(current_node)
            if neighbor not in seen_nodes
        ]
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

    if len(found_nodes) == 0:
        return []

    # determine largest connected components
    lcc = max(found_nodes, key=len)

    print(
        f"\t LCC contains {len(lcc)} nodes (removed { len(graph.vertices) - len(lcc)} nodes)"
    )

    return lcc


def computeLCCGraph(graph: Graph) -> Graph:
    lcc = computeLCC(graph)
    new_nodes = [graph.vertices[id] for id in lcc]
    return graphfactory.build_graph_from_vertices_edges(new_nodes, graph.edges)
