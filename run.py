from __future__ import print_function
from builtins import range
import sys
import time
import xml.sax
from optparse import OptionParser


import configuration as config
from osm.xml_handler import NodeHandler, WayHandler, PercentageFile
from graph.contract_graph import contract
import graph.algorithms as algorithms
import graph.graphfactory as graphfactory
import output.write_graph as output


def remove_adjacent_duplicates(nodes):
    for i in range(len(nodes) - 1, 0, -1):
        if nodes[i] == nodes[i - 1]:
            del nodes[i]


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
    nodes_to_remove = [osm_id for osm_id in nodes.keys() if osm_id not in found_node_ids]
    # remove these nodes
    for index in reversed(nodes_to_remove):
        del nodes[index]

    print("removed {} nodes".format(nmb_nodes - len(nodes)))
    print("removed {} ways".format(nmb_ways - len(ways)))


def read_file(osm_filename, configuration, verbose=True):

    def print_verbose():
        if options.verbose:
            print("done!")
            print("{}s".format(time.time() - start_time))

    parser = xml.sax.make_parser()

    start_time = time.time()
    print("identifying all ways ...")
    w_handler = WayHandler(configuration)

    parser.setContentHandler(w_handler)
    parser.parse(PercentageFile(osm_filename))
    print_verbose()

    ways = w_handler.found_ways
    found_nodes = w_handler.found_nodes

    start_time = time.time()
    print("\nidentifying all nodes ...")
    n_handler = NodeHandler(found_nodes)

    parser.setContentHandler(n_handler)
    parser.parse(PercentageFile(osm_filename))
    print_verbose()

    nodes = n_handler.nodes

    return nodes, ways


def generateGraph(filename, network_type, options):

    def print_verbose():
        if options.verbose:
            print("done!")
            print("{}s".format(time.time() - start_time))

    configuration = config.Configuration(network_type)

    r_index = filename.rfind(".")
    out_file = filename[:r_index]

    print("selected mode: {}".format(configuration.mode))
    print("accepted highway tags: {}".format(configuration.accepted_highways))
    print("opening file: {}".format(filename))

    nodes, ways = read_file(filename, configuration)

    print("\n sanitizing input...")
    start_time = time.time()
    sanitize_input(ways, nodes)

    print_verbose()
    print("\n constructing graph...", end="")
    sys.stdout.flush()

    start_time = time.time()
    graph = graphfactory.build_graph_from_osm(nodes, ways)

    if not options.lcc:
        print("\n computing (L)argest (C)onnected (C)omponent...", end="")
        sys.stdout.flush()
        graph = algorithms.computeLCCGraph(graph)
        print(" done!")

    print("writing data...",)
    output.write_to_file(graph, out_file, configuration.get_file_extension())

    print_verbose()

    if options.contract:
        start_time = time.time()
        print("contracting graph...")
        contracted_graph = contract(graph)
        print("contracting finished")
        output.write_to_file(contracted_graph, out_file, "{}c".format(configuration.get_file_extension()))
        print_verbose()


if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-f", "--file", dest="filename", action="store", type="string")
    parser.add_option("-n", "--networkType", dest="network_type", action="store", default="pedestrian", help="(p)edestrian, (b)icycle, (c)ar, [default: pedestrian]")
    parser.add_option("-v", "--verbose", dest="verbose", action="store_true")
    parser.add_option("-l", "--nolcc", dest="lcc", action="store_false")
    parser.add_option("-c", "--contract", dest="contract", action="store_true")
    (options, args) = parser.parse_args()

    filename = options.filename

    if filename is None:
        parser.print_help()
        exit()

    long_network_type = {"p": "pedestrian", "c": "car", "b": "bicycle"}
    if options.network_type in long_network_type.keys():
        network_type = long_network_type[options.network_type]
    elif options.network_type == long_network_type.values():
        network_type = options.network_type
    else:
        print("network type improperly set")
        exit()

    generateGraph(filename, network_type, options)
