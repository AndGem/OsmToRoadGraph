# -*- coding: utf-8 -*-
class OSMWay:
    __slots__ = ["osm_id", "nodes", "highway", "area", "max_speed", "direction", "forward", "backward", "name"]

    def __init__(self, osm_id):
        self.osm_id = osm_id
        self.nodes = []
        self.highway = None
        self.area = None
        self.max_speed = None
        self.direction = None
        self.forward = True
        self.backward = True
        self.name = ""

    def add_node(self, osm_id):
        self.nodes.append(osm_id)


class OSMNode(object):
    __slots__ = ["lat", "lon", "osm_id"]

    def __init__(self, osm_id, lat=None, lon=None):
        self.osm_id = osm_id
        self.lat, self.lon = lat, lon