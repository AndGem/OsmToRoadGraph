import xml.sax

from osm.osm_types import OSMNode, OSMWay
from osm.way_parser_helper import WayParserHelper
from osm.xml_handler import NodeHandler, WayHandler, PercentageFile
import utils.timer as timer

from typing import Dict, List, Set, Tuple


@timer.timer
def read_file(osm_filename, configuration, verbose=True) -> Tuple[Dict[int, OSMNode], List[OSMWay]]:
    parserHelper = WayParserHelper(configuration)
    ways, found_node_ids = _read_ways(PercentageFile(osm_filename), parserHelper)
    nodes = _read_nodes(PercentageFile(osm_filename), found_node_ids)

    return nodes, ways


@timer.timer
def _read_ways(osm_file, configuration) -> Tuple[List[OSMWay], Set[int]]:
    parser = xml.sax.make_parser()
    w_handler = WayHandler(configuration)

    parser.setContentHandler(w_handler)
    parser.parse(osm_file)

    return w_handler.found_ways, w_handler.found_nodes


@timer.timer
def _read_nodes(osm_file, found_nodes) -> Dict[int, OSMNode]:
    parser = xml.sax.make_parser()
    n_handler = NodeHandler(found_nodes)

    parser.setContentHandler(n_handler)
    parser.parse(osm_file)

    return n_handler.nodes
