from collections import deque

import graphfactory


def BFS(graph, s):
    found_nodes = set([s])
    current_nodes = deque([s])

    while len(current_nodes) > 0:
        node_id = current_nodes.popleft()

        # add all unvisited nodes to current_nodes
        for neighbor in graph.all_neighbors(node_id):
            if neighbor not in found_nodes:
                current_nodes.append(neighbor)
                found_nodes.add(neighbor)

    return found_nodes


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

    print("LCC contains {} nodes (removed {} nodes)".format(len(lcc), len(graph.vertices) - len(lcc)))
    return lcc


def computeLCCGraph(graph):
    lcc = computeLCC(graph)
    new_nodes = [graph.vertices[id] for id in lcc]
    return graphfactory.build_graph_from_vertices_edges(new_nodes, graph.edges)
