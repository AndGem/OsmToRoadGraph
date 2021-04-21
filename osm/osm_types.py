from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class OSMWay:
    osm_id: int
    nodes: List[int] = field(init=False, default_factory=list)
    highway: str = field(init=False, default="")
    area: Optional[str] = field(init=False, default=None)
    max_speed_str: Optional[str] = field(init=False, default=None)
    max_speed_int: int = field(init=False)
    direction: str = field(init=False, default="")
    forward: bool = field(init=False, default=True)
    backward: bool = field(init=False, default=True)
    name: str = field(init=False, default="")

    def add_node(self, osm_id: int) -> None:
        self.nodes.append(osm_id)


@dataclass(frozen=True)
class OSMNode:
    __slots__ = ["lat", "lon", "osm_id"]

    osm_id: int
    lat: float
    lon: float
