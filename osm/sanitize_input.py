from osm.osm_types import OSMNode, OSMWay
from utils import timer

from typing import Dict, List, Tuple


@timer.timer
def sanitize_input(ways: List[OSMWay], nodes: Dict[int, OSMNode]):
    """
    This function removes all
        - nodes not used in any of the OSMWays, and
        - ways that contain one or more OSMNodes not in nodes

    :rtype : list of Ways, list of Vertices
    :param ways: list of input OSMWays
    :param nodes: list of input OSMNodes
    """

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

    print(f"removed {nmb_nodes - len(nodes)} nodes")
    print(f"removed {nmb_ways - len(ways)} ways")
