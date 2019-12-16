from dataclasses import dataclass, field
from typing import Optional, List


@dataclass
class OSMWay:
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
    osm_id: int
    lat: float
    lon: float
