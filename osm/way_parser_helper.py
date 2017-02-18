class WayParserHelper:

    def __init__(self, config):
        self.config = config

    def accept_way(self, way):
        # reject: if the way marks the border of an area
        if way.area == 'yes':
            return False

        if way.highway not in self.config.accepted_highways[self.config.nextwork_type]:
            return False

        return True

    def parse_direction(self, way):
        way.forward = True
        way.backward = True

        if way.direction == 'oneway':
            way.forward = True
            way.backward = False

        if self.config.network_type == 'pedestrian':
            way.forward = True
            way.backward = True

    def parse_max_speed(self, way):

        if way.max_speed is None:
            way.max_speed = self.config.speed_limits[way.highway]
            return

        try:
            way.max_speed = int(way.max_speed)

        except ValueError:

            max_speed = way.max_speed
            max_speed.lower()

            if 'walk' in max_speed:
                way.max_speed = self.config.walking_speed
            elif 'none' in max_speed:
                way.max_speed = self.config.max_highway_speed
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