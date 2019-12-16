from typing import Optional, List


class OSMWay:
    __slots__ = ["osm_id", "nodes", "highway", "area", "max_speed", "direction", "forward", "backward", "name"]

    def __init__(self, osm_id: int) -> None:
        self.osm_id = osm_id
        self.nodes = []
        self.highway = None
        self.area = None
        self.max_speed = None
        self.direction = None
        self.forward = True
        self.backward = True
        self.name = ""

    def add_node(self, osm_id: int) -> None:
        self.nodes.append(osm_id)


class OSMNode(object):
    __slots__ = ["lat", "lon", "osm_id"]

    def __init__(self, osm_id: int, lat: float, lon: float) -> None:
        self.osm_id: int = osm_id
        self.lat: float = lat
        self.lon: float = lon
