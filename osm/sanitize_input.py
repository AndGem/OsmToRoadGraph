import utils.timer as timer


@timer.timer
def sanitize_input(ways, nodes):
    """
    This function removes all
        - nodes not used in any of the Ways, and
        - ways that contain one or more vertices not in nodes

    :rtype : list of Ways, list of Vertices
    :param ways: list of input Ways
    :param nodes: list of input Vertices
    :return: Filtered list of Ways and Nodes
    """
    assert isinstance(ways, list)
    assert isinstance(nodes, dict)

    def remove_adjacent_duplicates(nodes):
        for i in range(len(nodes) - 1, 0, -1):
            if nodes[i] == nodes[i - 1]:
                del nodes[i]

    ways_to_remove = []
    nodes_to_remove = []
    found_node_ids = set()

    nmb_ways = len(ways)
    nmb_nodes = len(nodes)

    # determine ways that have missing nodes
    for index, w in enumerate(ways):
        for node in w.nodes:
            if node not in nodes:
                ways_to_remove.append(index)
                break
        else:
            remove_adjacent_duplicates(w.nodes)
            found_node_ids.update(w.nodes)

    # remove ways
    for index in reversed(ways_to_remove):
        del ways[index]

    # determine nodes that do not appear in any of the ways
    nodes_to_remove = [
        osm_id for osm_id in nodes.keys() if osm_id not in found_node_ids
    ]
    # remove these nodes
    for index in reversed(nodes_to_remove):
        del nodes[index]

    print("removed {} nodes".format(nmb_nodes - len(nodes)))
    print("removed {} ways".format(nmb_ways - len(ways)))
