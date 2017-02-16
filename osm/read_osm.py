import time
import xml.sax
from osm.xml_handler import NodeHandler, WayHandler, PercentageFile


def read_file(osm_filename, configuration, verbose=True):

    def print_verbose():
        if verbose:
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
