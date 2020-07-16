import bz2
import xml.sax

from osm.osm_types import OSMNode, OSMWay
from osm.way_parser_helper import WayParserHelper
from osm.xml_handler import NodeHandler, WayHandler, PercentageFile
import utils.timer as timer

from typing import Dict, List, Set, Tuple
from zipfile import ZipFile, BadZipFile


@timer.timer
def read_file(osm_filename, configuration, verbose=True) -> Tuple[Dict[int, OSMNode], List[OSMWay]]:

    parserHelper = WayParserHelper(configuration)
    compressed_content = uncompress_content(osm_filename)
    if compressed_content:
        ways, found_node_ids = _read_ways(compressed_content, parserHelper)
        nodes = _read_nodes(compressed_content, found_node_ids)
    else:
        ways, found_node_ids = _read_ways(PercentageFile(osm_filename), parserHelper)
        nodes = _read_nodes(PercentageFile(osm_filename), found_node_ids)

    return nodes, ways


def uncompress_content(osm_filename):
    magic_bz2 = "\x42\x5a\x68"
    magic_zip = "\x50\x4b\x03\x04"

    with open(osm_filename) as f:
        content_begin = f.read(max(len(x) for x in [magic_bz2, magic_zip]))
        if content_begin.startswith(magic_bz2):
            print("identified bz2 compressed file.. decompressing")
            content = bz2.read()
            print("done!")
            return content
        elif content_begin.startswith(magic_zip):
            print("identified bz2 compressed file.. decompressing")
            zipfile = ZipFile(osm_filename)
            osm_file_in_zip = None
            for f in zipfile.infolist():
                if f.filename.endswith(".osm"):
                    osm_file_in_zip = f.filename
                    break
            content = zipfile.read(name=osm_file_in_zip)
            print("done!")
            return content

        print("no compression recognized!")
        return None


@timer.timer
def _read_ways(osm_file, configuration) -> Tuple[List[OSMWay], Set[int]]:
    parser = xml.sax.make_parser()
    w_handler = WayHandler(configuration)

    parser.setContentHandler(w_handler)
    if type(osm_file) == PercentageFile:
        parser.parse(osm_file)
    else:
        xml.sax.parseString(osm_file, w_handler)

    return w_handler.found_ways, w_handler.found_nodes


@timer.timer
def _read_nodes(osm_file, found_nodes) -> Dict[int, OSMNode]:
    parser = xml.sax.make_parser()
    n_handler = NodeHandler(found_nodes)

    parser.setContentHandler(n_handler)
    if type(osm_file) == PercentageFile:
        parser.parse(osm_file)
    else:
        xml.sax.parseString(osm_file, n_handler)

    return n_handler.nodes
