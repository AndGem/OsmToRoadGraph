from typing import Set, Dict
from lxml import etree

from osm.osm_types import OSMNode


class NodeHandlerLXML:
    def __init__(self, found_nodes: Set[int]) -> None:
        self.found_nodes: Set[int] = found_nodes
        self.nodes: Dict[int, OSMNode] = {}

    def parse(self, osm_file) -> None:
        context = etree.iterparse(osm_file)
        for event, elem in context:
            if event == "end" and elem.tag == "node":
                osm_id = int(elem.attrib["id"])
                if osm_id not in self.found_nodes:
                    # elem.clear()
                    continue
                self.nodes[osm_id] = OSMNode(
                    osm_id, float(elem.attrib["lat"]), float(elem.attrib["lon"])
                )
            # elem.clear()
