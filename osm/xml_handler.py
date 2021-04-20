import os
import sys
from typing import Optional, Set, List, Dict
from xml.sax.xmlreader import AttributesImpl
from xml.sax.handler import ContentHandler

from osm.osm_types import OSMWay, OSMNode
from osm.way_parser_helper import WayParserHelper

intern = sys.intern


class PercentageFile:
    def __init__(self, filename: str) -> None:
        self.size = os.stat(filename)[6]
        self.delivered = 0
        self.f = open(filename, encoding="utf-8")
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


class NodeHandler(ContentHandler):
    def __init__(self, found_nodes: Set[int]) -> None:
        self.found_nodes: Set[int] = found_nodes
        self.nodes: Dict[int, OSMNode] = {}

    def startElement(self, name: str, attrs: AttributesImpl) -> None:
        if name == "node":
            osm_id = int(attrs["id"])
            if osm_id not in self.found_nodes:
                return

            self.nodes[osm_id] = OSMNode(
                osm_id, float(attrs["lat"]), float(attrs["lon"])
            )


class WayHandler(ContentHandler):
    def __init__(self, parser_helper: WayParserHelper) -> None:
        self.found_ways: List[OSMWay] = []
        self.found_nodes: Set[int] = set()

        self.current_way: Optional[OSMWay] = None

        self.parser_helper = parser_helper

    def startElement(self, name: str, attrs: AttributesImpl) -> None:
        if name == "way":
            self.current_way = OSMWay(osm_id=int(attrs["id"]))
            return

        if self.current_way is not None:
            try:
                if name == "nd":
                    node_id = int(attrs["ref"])
                    self.current_way.add_node(node_id)

                elif name == "tag":
                    if attrs["k"] == "highway":
                        self.current_way.highway = attrs["v"]
                    elif attrs["k"] == "area":
                        self.current_way.area = attrs["v"]
                    elif attrs["k"] == "maxspeed":
                        self.current_way.max_speed_str = str(attrs["v"])
                    elif attrs["k"] == "oneway":
                        if attrs["v"] == "yes":
                            self.current_way.direction = "oneway"
                    elif attrs["k"] == "name":
                        try:
                            self.current_way.name = intern(attrs["v"])
                        except TypeError:
                            self.current_way.name = attrs["v"]
                    elif attrs["k"] == "junction":
                        if attrs["v"] == "roundabout":
                            self.current_way.direction = "oneway"
                    elif attrs["k"] == "indoor":
                        # this is not an ideal solution since it sets the pedestrian flag irrespective of the real value in osm data
                        # but aims to cover the simple indoor tagging approach: https://wiki.openstreetmap.org/wiki/Simple_Indoor_Tagging
                        # more info: https://help.openstreetmap.org/questions/61025/pragmatic-single-level-indoor-paths
                        if attrs["v"] == "corridor":
                            self.current_way.highway = "pedestrian_indoor"
            except:
                e = sys.exc_info()[0]
                print("Error while parsing: {}".format(e))

    def endElement(self, name: str) -> None:
        if name == "way":
            assert self.current_way is not None

            if not self.parser_helper.is_way_acceptable(self.current_way):
                self.current_way = None
                return

            self.found_nodes.update(self.current_way.nodes)

            self.current_way.max_speed_int = self.parser_helper.parse_max_speed(
                self.current_way
            )
            (
                self.current_way.forward,
                self.current_way.backward,
            ) = self.parser_helper.parse_direction(self.current_way)

            self.found_ways.append(self.current_way)

            self.current_way = None
