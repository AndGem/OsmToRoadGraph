from dataclasses import dataclass
from typing import Optional, Union


@dataclass
class Vertex:
    id: int
    lat: float
    lon: float

    @property
    def description(self) -> str:
        return "{} {} {}".format(self.id, self.lat, self.lon)


@dataclass
class Edge:
    s: int
    t: int
    length: float
    highway: str
    max_v: int
    forward: bool
    backward: bool
    name: str

    @property
    def description(self) -> str:
        both_directions = "1" if self.forward and self.backward else "0"
        return "{} {} {} {} {} {}".format(self.s, self.t, self.length, self.highway, self.max_v, both_directions)


@dataclass
class SimpleEdge:
    s: int
    t: int
    length: float
    name: Optional[str] = ""

    @property
    def forward(self) -> bool:
        return True

    @property
    def backward(self) -> bool:
        return True

    @property
    def description(self) -> str:
        return "{} {} {}".format(self.s, self.t, self.length)


EdgeType = Union[Edge, SimpleEdge]
VertexType = Union[Vertex]
