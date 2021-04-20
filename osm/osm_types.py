from typing import List, Optional


class OSMWay:
    __slots__ = [
        "osm_id",
        "nodes",
        "highway",
        "area",
        "max_speed_str",
        "max_speed_int",
        "direction",
        "forward",
        "backward",
        "name",
    ]

    def __init__(self, osm_id: int) -> None:
        self.osm_id = osm_id
        self.nodes: List[int] = []
        self.highway: str = ""
        self.area: Optional[str] = None
        self.max_speed_str: Optional[str] = None
        self.max_speed_int: int
        self.direction: str = ""
        self.forward = True
        self.backward = True
        self.name = ""

    def add_node(self, osm_id: int) -> None:
        self.nodes.append(osm_id)


class OSMNode:
    __slots__ = ["lat", "lon", "osm_id"]

    def __init__(self, osm_id: int, lat: float, lon: float) -> None:
        self.osm_id: int = osm_id
        self.lat: float = lat
        self.lon: float = lon
