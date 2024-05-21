import argparse
import importlib.util
import os
import sys

import configuration as config
from osm import read_osm, sanitize_input
from output import write_graph as output
from graph import contract_graph, convert_graph, algorithms, graphfactory
from utils import timer

@timer.timer
def convert_osm_to_roadgraph(filename, network_type, options):
    configuration = config.Configuration(network_type)

    out_file, _ = os.path.splitext(filename)

    print(f"selected network type: {configuration.network_type}")
    print(f"accepted highway tags: {configuration.accepted_highways}")
    print(f"opening file: {filename}")

    try:
        nodes, ways = read_osm.read_file(filename, configuration)
    except Exception as e:
        print(f"Error occurred while reading file {filename}: {e}")
        return

    sanitize_input.sanitize_input(ways, nodes)

    graph = graphfactory.build_graph_from_osm(nodes, ways)

    if not options.lcc:
        graph = algorithms.computeLCCGraph(graph)

    output.write_to_file(graph, out_file, configuration.get_file_extension())

    if options.networkx_output:
        validate_networkx()
        nx_graph = convert_graph.convert_to_networkx(graph)
        output.write_nx_to_file(nx_graph, f"{out_file}.json")

    if options.contract:
        contracted_graph = contract_graph.ContractGraph(graph).contract()
        output.write_to_file(
            contracted_graph, out_file, f"{configuration.get_file_extension()}c"
        )
        if options.networkx_output:
            nx_graph = convert_graph.convert_to_networkx(contracted_graph)
            output.write_nx_to_file(nx_graph, f"{out_file}_contracted.json")

def validate_networkx():
    networkx_spec = importlib.util.find_spec("networkx")
    if networkx_spec is None:
        raise ImportError("Networkx library not found. Please install networkx if you want to use the --networkx option.")

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

    try:
        if not os.path.isfile(filename):
            raise FileNotFoundError(f"Provided filename {filename} does not point to a file!")
        network_type = config.Configuration.validate_network_type(options.network_type)
    except FileNotFoundError as e:
        print(f"ERROR: {e}")
        sys.exit(1)
    except ValueError as e:
        print(f"ERROR: {e}")
        sys.exit(1)

    try:
        convert_osm_to_roadgraph(filename, network_type, options)
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)
