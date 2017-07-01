class Vertex(object):
    __slots__ = ["id", "lat", "lon"]

    def __init__(self, id, lat, lon):
        self.id = id
        self.lat, self.lon = lat, lon

    @property
    def description(self):
        return "{} {} {}".format(self.id, self.lat, self.lon)


class Edge(object):
    __slots__ = ["s", "t", "length", "highway", "max_v", "forward", "backward", "name"]

    def __init__(self, s, t, length, highway, max_v, f, b, name):
        self.s, self.t = s, t
        self.length = length
        self.highway = highway
        self.max_v = max_v
        self.forward, self.backward = f, b
        self.name = name

    @property
    def description(self):
        both_directions = "1" if self.forward and self.backward else "0"
        return "{} {} {} {} {} {}".format(self.s, self.t, self.length, self.highway, self.max_v, both_directions)


class SimpleEdge(object):
    __slots__ = ["s", "t", "length", "name"]

    def __init__(self, s, t, length):
        self.s, self.t = s, t
        self.length = length
        self.name = ""

    @property
    def forward(self):
        return True

    @property
    def backward(self):
        return True

    @property
    def description(self):
        return "{} {} {}".format(self.s, self.t, self.length)