
class VertexData:
    __slots__ = ["lat", "lon"]

    def __init__(self, lat: float, lon: float) -> None:
        self.lat, self.lon = lat, lon

    def __repr__(self) -> str:
        return "{} {}".format(self.lat, self.lon)


class Vertex:
    __slots__ = ["id", "data"]

    def __init__(self, id: int, data: VertexData) -> None:
        self.id = id
        self.data = data

    @property
    def description(self) -> str:
        return "{} {}".format(self.id, self.data)


class EdgeData:
    __slots__ = ["length", "highway", "max_v", "name"]

    def __init__(self, length: float, highway: str, max_v: int, name: str) -> None:
        self.length: float = length
        self.highway: str = highway
        self.max_v: int = max_v
        self.name: str = name

    def __eq__(self, other):
        if isinstance(other, EdgeData):
            return self.length == other.length and self.highway == other.highway and self.max_v == other.max_v and self.name == other.name
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self) -> str:
        return "{} {} {}".format(self.length, self.highway, self.max_v)


class Edge:
    __slots__ = ["s", "t", "forward", "backward", "data"]

    def __init__(self, s: int, t: int, f: bool, b: bool, data: EdgeData) -> None:
        self.s: int = s
        self.t: int = t
        self.forward: bool = f
        self.backward: bool = b
        self.data = data

    @property
    def description(self) -> str:
        both_directions = "1" if self.forward and self.backward else "0"
        return "{} {} {} {}".format(self.s, self.t, self.data, both_directions)
