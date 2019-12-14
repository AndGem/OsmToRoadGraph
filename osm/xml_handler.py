import os
import sys
import xml.sax

from osm.osm_types import OSMWay, OSMNode

from osm.way_parser_helper import WayParserHelper
from typing import Set
from xml.sax.xmlreader import AttributesImpl
try:
    intern = sys.intern
except AttributeError:
    pass


class PercentageFile(object):

    def __init__(self, filename: str) -> None:
        self.size = os.stat(filename)[6]
        self.delivered = 0
        self.f = open(filename)
        self.percentages = [1000] + [100 - 10 * x for x in range(0, 11)]

    def read(self, size: Optional[int] = None) -> str:
        if size is None:
            self.delivered = self.size
            return self.f.read()
        data = self.f.read(size)
        self.delivered += len(data)

        if self.percentage >= self.percentages[-1]:
            if self.percentages[-1] < 100:
                print("{}%..".format(self.percentages[-1]), end="")
                sys.stdout.flush()
            else:
                print("100%")
            self.percentages = self.percentages[:-1]
        return data

    def close(self) -> None:
        self.f.close()

    @property
    def percentage(self) -> float:
        return float(self.delivered) / self.size * 100.0


class NodeHandler(xml.sax.ContentHandler):

    def __init__(self, found_nodes: Set[int]) -> None:
        self.found_nodes = found_nodes
        self.nodes = {}

    def startElement(self, tag: str, attributes: AttributesImpl) -> None:
        if tag == "node":
            osm_id = int(attributes["id"])
            if osm_id not in self.found_nodes:
                return

            self.nodes[osm_id] = OSMNode(osm_id, float(attributes["lat"]), float(attributes["lon"]))


class WayHandler(xml.sax.ContentHandler):

    def __init__(self, parser_helper: WayParserHelper) -> None:
        # stores all found ways
        self.found_ways = []
        self.found_nodes = set()

        self.start_tag_found = False
        self.current_way = None

        self.parser_helper = parser_helper

    def startElement(self, tag: str, attributes: AttributesImpl) -> None:
        if tag == "way":
            self.start_tag_found = True
            self.current_way = OSMWay(int(attributes["id"]))
            return

        if self.start_tag_found:
            try:
                if tag == "nd":
                    # gather nodes
                    node_id = int(attributes["ref"])
                    self.current_way.add_node(node_id)

                elif tag == "tag":
                    if attributes["k"] == "highway":
                        self.current_way.highway = attributes["v"]
                    elif attributes["k"] == "area":
                        self.current_way.area = attributes["v"]
                    elif attributes["k"] == "maxspeed":
                        self.current_way.max_speed = str(attributes["v"])
                    elif attributes["k"] == "oneway":
                        if attributes["v"] == "yes":
                            self.current_way.direction = "oneway"
                    elif attributes["k"] == "name":
                        try:
                            self.current_way.name = intern(attributes["v"])
                        except TypeError:
                            self.current_way.name = attributes["v"]
                    elif attributes["k"] == "junction":
                        if attributes["v"] == "roundabout":
                            self.current_way.direction = "oneway"
                    elif attributes["k"] == "indoor":
                        # this is not an ideal solution since it sets the pedestrian flag irrespective of the real value in osm data
                        # but aims to cover the simple indoor tagging approach: https://wiki.openstreetmap.org/wiki/Simple_Indoor_Tagging
                        # more info: https://help.openstreetmap.org/questions/61025/pragmatic-single-level-indoor-paths
                        if attributes["v"] == "corridor":
                            self.current_way.highway = "pedestrian_indoor"
            except:
                e = sys.exc_info()[0]
                print("Error while parsing: {}".format(e))

    def endElement(self, tag: str) -> None:
        if tag == "way":
            self.start_tag_found = False

            # check if way is acceptable
            if not self.parser_helper.is_way_acceptable(self.current_way):
                self.current_way = None
                return

            self.found_nodes.update(self.current_way.nodes)

            self.current_way.max_speed = self.parser_helper.parse_max_speed(self.current_way.max_speed, self.current_way.highway)
            self.current_way.forward, self.current_way.backward = self.parser_helper.parse_direction(self.current_way)

            self.found_ways.append(self.current_way)

            self.current_way = None
