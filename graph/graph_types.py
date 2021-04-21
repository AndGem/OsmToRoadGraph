from dataclasses import dataclass


@dataclass(frozen=True)
class VertexData:
    __slots__ = ["lat", "lon"]
    lat: float
    lon: float

    def __repr__(self) -> str:
        return "{} {}".format(self.lat, self.lon)


@dataclass(frozen=True)
class Vertex:
    __slots__ = ["id", "data"]
    id: int
    data: VertexData

    @property
    def description(self) -> str:
        return "{} {}".format(self.id, self.data)


@dataclass(frozen=True)
class EdgeData:
    __slots__ = ["length", "highway", "max_v", "name"]
    length: float
    highway: str
    max_v: int
    name: str

    def __repr__(self) -> str:
        return "{} {} {}".format(self.length, self.highway, self.max_v)


@dataclass(frozen=True)
class Edge:
    __slots__ = ["s", "t", "forward", "backward", "data"]
    s: int
    t: int
    forward: bool
    backward: bool
    data: EdgeData

    @property
    def description(self) -> str:
        both_directions = "1" if self.forward and self.backward else "0"
        return "{} {} {} {}".format(self.s, self.t, self.data, both_directions)
