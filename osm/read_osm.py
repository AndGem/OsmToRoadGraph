import bz2
import xml.sax
from xml.sax.xmlreader import InputSource

from osm.osm_types import OSMNode, OSMWay
from osm.way_parser_helper import WayParserHelper
from osm.xml_handler import NodeHandler, WayHandler, PercentageFile
from utils import timer

from typing import Dict, List, Set, Tuple, Union


@timer.timer
def read_file(osm_filename, configuration) -> Tuple[Dict[int, OSMNode], List[OSMWay]]:
    parserHelper = WayParserHelper(configuration)
    decompressed_content = decompress_content(osm_filename)
    if decompressed_content:
        ways, found_node_ids = _read_ways(decompressed_content, parserHelper)
        nodes = _read_nodes(decompressed_content, found_node_ids)
    else:
        ways, found_node_ids = _read_ways(PercentageFile(osm_filename), parserHelper)
        nodes = _read_nodes(PercentageFile(osm_filename), found_node_ids)

    return nodes, ways


def decompress_content(osm_filename):
    magic_bz2 = "\x42\x5a\x68"

    try:
        with open(osm_filename, "r", encoding="utf-8", errors="replace") as f:
            content_begin = f.read(10)
    except Exception as e:
        print(f"Error occurred while opening {osm_filename}: {e}")
        return None

    if content_begin.startswith(magic_bz2):
        print("identified bz2 compressed file.. decompressing")
        try:
            with bz2.open(osm_filename, "rb") as f:
                content = f.read()
            print("done!")
            return content
        except Exception as e:
            print(f"Error occurred while decompressing {osm_filename}: {e}")
            return None

    print("no compression recognized!")
    return None


@timer.timer
def _read_ways(
    osm_file: Union[PercentageFile, InputSource, str], configuration
) -> Tuple[List[OSMWay], Set[int]]:
    parser = xml.sax.make_parser()
    w_handler = WayHandler(configuration)

    parser.setContentHandler(w_handler)
    if isinstance(osm_file, str):
        osm_file = InputSource(osm_file)
    parser.parse(osm_file)

    return w_handler.found_ways, w_handler.found_nodes


@timer.timer
def _read_nodes(
    osm_file: Union[PercentageFile, InputSource, str], found_nodes
) -> Dict[int, OSMNode]:
    parser = xml.sax.make_parser()
    n_handler = NodeHandler(found_nodes)

    parser.setContentHandler(n_handler)
    if isinstance(osm_file, str):
        osm_file = InputSource(osm_file)
    parser.parse(osm_file)

    return n_handler.nodes
