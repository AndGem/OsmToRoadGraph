from __future__ import print_function
from optparse import OptionParser

import configuration as config
import graph.contract_graph as contract
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

    if options.contract:
        contracted_graph = contract.contract(graph)
        output.write_to_file(contracted_graph, out_file, "{}c".format(configuration.get_file_extension()))


if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-f", "--file", dest="filename", action="store", type="string")
    parser.add_option("-n", "--networkType", dest="network_type", action="store", default="pedestrian", help="(p)edestrian, (b)icycle, (c)ar, [default: pedestrian]")
    parser.add_option("-l", "--nolcc", dest="lcc", action="store_true", default=False)
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

    convert_osm_to_roadgraph(filename, network_type, options)
