import xml.sax

from osm.osm_types import OSMNode, OSMWay
from osm.way_parser_helper import WayParserHelper
from osm.xml_handler import NodeHandler, WayHandler, PercentageFile
import utils.timer as timer

from typing import Dict, List, Set, Tuple
from zipfile import ZipFile


@timer.timer
def read_file(osm_filename, configuration, verbose=True) -> Tuple[Dict[int, OSMNode], List[OSMWay]]:

    parserHelper = WayParserHelper(configuration)
    zip_content = read_zipfile(osm_filename)
    if zip_content:
        ways, found_node_ids = _read_ways(zip_content, parserHelper)
        nodes = _read_nodes(zip_content, found_node_ids)
    else:
        ways, found_node_ids = _read_ways(PercentageFile(osm_filename), parserHelper)
        nodes = _read_nodes(PercentageFile(osm_filename), found_node_ids)

    return nodes, ways


def read_zipfile(osm_filename):
    try:
        zipfile = ZipFile(osm_filename)
        osm_file_in_zip = None
        for f in zipfile.infolist():
            if f.filename.endswith(".osm"):
                osm_file_in_zip = f.filename
                break
        return zipfile.read(name=osm_file_in_zip)

    except zipfile.BadZipFile
        return None


@timer.timer
def _read_ways(osm_file, configuration) -> Tuple[List[OSMWay], Set[int]]:
    parser = xml.sax.make_parser()
    w_handler = WayHandler(configuration)

    parser.setContentHandler(w_handler)
    if type(osm_file) == PercentageFile:
        parser.parse(osm_file)
    else:
        parser.parseString(osm_file)

    return w_handler.found_ways, w_handler.found_nodes


@timer.timer
def _read_nodes(osm_file, found_nodes) -> Dict[int, OSMNode]:
    parser = xml.sax.make_parser()
    n_handler = NodeHandler(found_nodes)

    parser.setContentHandler(n_handler)
    if type(osm_file) == PercentageFile:
        parser.parse(osm_file)
    else:
        parser.parseString(osm_file)

    return n_handler.nodes
