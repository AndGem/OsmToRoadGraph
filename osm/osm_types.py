from dataclasses import dataclass, field
from typing import Optional, List


@dataclass
class OSMWay:
    __slots__ = ["osm_id", "nodes", "highway", "area", "max_speed", "direction", "forward", "backward", "name"]
    
    osm_id: int
    name: str = ""
    highway: Optional[str] = None
    area: Optional[str] = None
    max_speed: Optional[str] = None
    direction: Optional[str] = None
    nodes: List[int] = field(default_factory=list)
    forward: bool = True
    backward: bool = True

    def add_node(self, osm_id: int) -> None:
        self.nodes.append(osm_id)


@dataclass
class OSMNode(object):
    __slots__ = ["lat", "lon", "osm_id"]
    
    osm_id: int
    lat: float
    lon: float
