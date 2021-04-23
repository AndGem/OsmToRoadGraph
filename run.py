import argparse
import importlib.util
import os
import sys

import configuration as config
import graph.contract_graph as contract_graph
import graph.convert_graph as convert_graph
import graph.algorithms as algorithms
import graph.graphfactory as graphfactory
import osm.read_osm
import osm.sanitize_input
import output.write_graph as output
import utils.timer as timer


@timer.timer
def convert_osm_to_roadgraph(filename, network_type, options):

    configuration = config.Configuration(network_type)

    r_index = filename.rfind(".")
    out_file = filename[:r_index]

    print("selected network type: {}".format(configuration.network_type))
    print("accepted highway tags: {}".format(configuration.accepted_highways))
    print("opening file: {}".format(filename))

    nodes, ways = osm.read_osm.read_file(filename, configuration)

    osm.sanitize_input.sanitize_input(ways, nodes)

    graph = graphfactory.build_graph_from_osm(nodes, ways)

    if not options.lcc:
        graph = algorithms.computeLCCGraph(graph)

    output.write_to_file(graph, out_file, configuration.get_file_extension())

    if options.networkx_output:
        nx_graph = convert_graph.convert_to_networkx(graph)
        output.write_nx_to_file(nx_graph, f"{out_file}.json")

    if options.contract:
        contracted_graph = contract_graph.ContractGraph(graph).contract()
        output.write_to_file(
            contracted_graph, out_file, "{}c".format(configuration.get_file_extension())
        )
        if options.networkx_output:
            nx_graph = convert_graph.convert_to_networkx(contracted_graph)
            output.write_nx_to_file(nx_graph, f"{out_file}_contracted.json")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="OSMtoRoadGraph")
    parser.add_argument("-f", "--file", action="store", type=str, dest="filename")
    parser.add_argument(
        "-n",
        "--networkType",
        dest="network_type",
        action="store",
        default="p",
        choices=["p", "b", "c"],
        help="(p)edestrian, (b)icycle, (c)ar, [default: p]",
    )
    parser.add_argument("-l", "--nolcc", dest="lcc", action="store_true", default=False)
    parser.add_argument("-c", "--contract", dest="contract", action="store_true")
    parser.add_argument(
        "--networkx",
        dest="networkx_output",
        action="store_true",
        help="enable additional output of JSON format of networkx [note networkx needs to be installed for this to work].",
        default=False,
    )

    options = parser.parse_args()

    filename = options.filename

    if filename is None:
        parser.print_help()
        sys.exit()

    if not os.path.isfile(filename):
        print("ERROR: provided filename {} does not point to a file!".format(filename))
        sys.exit()

    long_network_type = {"p": "pedestrian", "c": "car", "b": "bicycle"}
    if options.network_type in long_network_type.keys():
        network_type = long_network_type[options.network_type]
    elif options.network_type == long_network_type.values():
        network_type = options.network_type
    else:
        print("network type improperly set")
        sys.exit()

    if options.networkx_output:
        networkx_spec = importlib.util.find_spec("networkx")
        if networkx_spec is None:
            print(
                "Error: networkx Library not found. Please install networkx if you want to use the --networkx option."
            )
            sys.exit(-1)

    convert_osm_to_roadgraph(filename, network_type, options)
