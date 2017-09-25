class WayParserHelper:

    def __init__(self, config):
        self.config = config

    def is_way_acceptable(self, way):
        # reject: if the way marks the border of an area
        if way.area == 'yes':
            return False

        if way.highway not in self.config.accepted_highways[self.config.network_type]:
            return False

        return True

    def parse_direction(self, way):
        if way.direction == 'oneway':
            return True, False

        return True, True

    def parse_max_speed(self, maximum_speed, highway):

        if maximum_speed is None:
            return self.config.speed_limits[highway]

        try:
            max_speed = int(maximum_speed)
            return max_speed

        except ValueError:
            max_speed = maximum_speed.lower()

            if 'walk' in max_speed:
                max_speed = self.config.walking_speed
            elif 'none' in max_speed:
                max_speed = self.config.max_highway_speed
            elif 'mph' in max_speed or 'mp/h' in max_speed:
                max_speed = ''.join(c for c in max_speed if c.isdigit())
                max_speed = int(float(max_speed) * 1.609344)
            elif 'kmh' in max_speed or 'km/h' in max_speed or 'kph' in max_speed or 'kp/h' in max_speed:
                max_speed = ''.join(c for c in max_speed if c.isdigit())
                max_speed = int(max_speed)
            else:
                print("error while parsing max speed! Did not recognize: {}".format(max_speed))
                print("fallback by setting it to default value")
                if highway in self.config.speed_limits:
                    max_speed = self.config.speed_limits[highway]
                else:
                    max_speed = 30
                    print("coulnd't find a speed limit for highway type {}! Setting it to {}".format(highway, max_speed))

            return max_speed
