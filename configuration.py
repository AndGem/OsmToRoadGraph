
class Configuration(object):

    def __init__(self, mode="pedestrian"):
        self.accepted_highways = set()
        self.max_highway_speed = 120
        self.mode = mode
        self.speed_limits = {}
        self.walking_speed = 5

        self.set_mode(mode)
        self.set_default_speed_limit()

    def set_walking_speed(self, speed):
        assert isinstance(speed, int)
        self.walking_speed = speed

    def set_max_highway_speed(self, value):
        assert isinstance(value, int)
        self.max_highway_speed = value

    def set_mode(self, value):
        assert isinstance(value, str)
        self.mode = value
        self.set_accepted_highways(value)

    def set_accepted_highways(self, mode):
        if mode == 'pedestrian':
            self.accepted_highways = set(["primary", "secondary", "tertiary", "unclassified", "residential", "service", "primary_link", "secondary_link", "tertiary_link", "living_street", "pedestrian", "track", "road", "footway", "steps", "path"])
        elif mode == 'bicycle':
            self.accepted_highways = set(["primary", "secondary", "tertiary", "unclassified", "residential", "service", "primary_link", "secondary_link", "tertiary_link", "living_street", "track", "road", "path", "cycleway"])
        elif mode == 'car':
            self.accepted_highways = set(["motorway", "trunk", "primary", "secondary", "tertiary", "unclassified", "residential", "service", "motorway_link", "trunk_link", "primary_link", "secondary_link", "tertiary_link", "living_street"])
        else:
            self.accepted_highways = set()

    def set_default_speed_limit(self):
            self.speed_limits = {"motorway"     :120, "trunk"        :120, "primary"       :100,
                                 "secondary"    :100, "tertiary"     : 70, "unclassified"  : 50,
                                 "residential"  : 30, "service"      : 10, "motorway_link" : 60,
                                 "trunk_link"   : 60, "primary_link" : 60, "secondary_link": 60,
                                 "tertiary_link": 35, "living_street":  5, "pedestrian"    :  5,
                                 "track"        :  5, "road"         :  5, "footway"       :  5,
                                 "steps"        :  5, "path"         :  5, "cycleway"      :  5}

    def accept_way(self, way):
        # reject: if the way marks the border of an area
        if way.area == 'yes':
            return False

        if way.highway not in self.accepted_highways:
            return False

        return True

    def get_file_extension(self):
        extension = {"pedestrian":"pypgr", "car":"pycgr", "bicycle":"pybgr"}
        return extension[self.mode]

    def get_network_type(self):
        return self.mode


    def parse_direction(self, way):
        way.forward = True
        way.backward = True

        if way.direction == 'oneway':
            way.forward = True
            way.backward = False

        if self.mode == 'pedestrian':
            way.forward = True
            way.backward = True

    def parse_max_speed(self, way):

        if way.max_speed is None:
            way.max_speed = self.speed_limits[way.highway]
            return

        try:
            way.max_speed = int(way.max_speed)

        except ValueError:

            max_speed = way.max_speed
            max_speed.lower()

            if 'walk' in max_speed:
                way.max_speed = self.walking_speed
            elif 'none' in max_speed:
                way.max_speed = self.max_highway_speed
            elif 'mph' in way.max_speed or 'mp/h' in way.max_speed:
                max_speed = ''.join(c for c in max_speed if c.isdigit())
                way.max_speed = int(float(max_speed) * 1.609344)
            elif 'kmh' in way.max_speed or 'km/h' in way.max_speed or 'kph' in way.max_speed or 'kp/h' in way.max_speed:
                max_speed = ''.join(c for c in max_speed if c.isdigit())
                way.max_speed = int(max_speed)
            else:
                print("error while parsing max speed! Did not recognize: {}".format(way.max_speed))
                print("fallback by setting it to default value")

                way.max_speed = self.speed_limits[way.highway]
