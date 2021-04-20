from osm.osm_types import OSMWay


class WayParserHelper:

    ONEWAY_STR = "oneway"
    MPH_STRINGS = ["mph", "mp/h"]
    KMH_STRINGS = ["kph", "kp/h", "kmh", "km/h"]
    WALK_STR = "walk"
    NONE_STR = "none"
    SIGNALS_STR = "signals"

    def __init__(self, config):
        self.config = config

    def is_way_acceptable(self, way: OSMWay):
        # reject: if the way marks the border of an area
        if way.area == "yes":
            return False

        if way.highway not in self.config.accepted_highways[self.config.network_type]:
            return False

        return True

    def parse_direction(self, way):
        if way.direction == self.ONEWAY_STR:
            return True, False

        return True, True

    def convert_str_to_number(self, s):
        # remove all non-digts except ',' and '.'
        cleaned_up = "".join(filter(lambda x: x.isdigit() or x == "," or x == ".", s))
        # remove everything after first '.' or ','
        if "." in cleaned_up:
            cleaned_up = cleaned_up.split(".")[0]
        if "," in cleaned_up:
            cleaned_up = cleaned_up.split(",")[0]
        return cleaned_up

    def parse_max_speed(self, osm_way: OSMWay) -> int:
        maximum_speed = osm_way.max_speed_str
        highway = osm_way.highway

        if maximum_speed is None:
            return self.config.speed_limits[highway]

        try:
            max_speed = int(maximum_speed)
            return max_speed

        except ValueError:
            max_speed_str = maximum_speed.lower()

            if self.WALK_STR in max_speed_str:
                max_speed = self.config.walking_speed
            elif self.NONE_STR in max_speed_str:
                max_speed = self.config.max_highway_speed
            elif any([s in max_speed_str for s in self.MPH_STRINGS]):
                max_speed_kmh_str = self.convert_str_to_number(max_speed_str)
                max_speed = int(float(max_speed_kmh_str) * 1.609344)
            elif any([s in max_speed_str for s in self.KMH_STRINGS]):
                max_speed = int(self.convert_str_to_number(max_speed_str))
            else:
                if self.SIGNALS_STR in max_speed_str:
                    #  according to https://wiki.openstreetmap.org/wiki/Key:maxspeed 'signals' indicates
                    #  that the max speed is shown by some sort of signalling. Here, we fallback to the default of the highway type.
                    pass
                else:
                    print(
                        "error while parsing max speed of osm way {}! Did not recognize: {}".format(
                            osm_way.osm_id, max_speed_str
                        )
                    )
                    print("fallback by setting it to default value")

                if highway in self.config.speed_limits:
                    max_speed = self.config.speed_limits[highway]
                else:
                    max_speed = 30
                    print(
                        "couldn't find a speed limit for highway type {}! Setting it to {}".format(
                            highway, max_speed
                        )
                    )

            return max_speed
