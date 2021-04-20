class Configuration:

    accepted_highways = dict()
    accepted_highways["pedestrian"] = set(
        [
            "primary",
            "secondary",
            "tertiary",
            "unclassified",
            "residential",
            "service",
            "primary_link",
            "secondary_link",
            "tertiary_link",
            "living_street",
            "pedestrian",
            "track",
            "road",
            "footway",
            "steps",
            "path",
        ]
    )
    accepted_highways["bicycle"] = set(
        [
            "primary",
            "secondary",
            "tertiary",
            "unclassified",
            "residential",
            "service",
            "primary_link",
            "secondary_link",
            "tertiary_link",
            "living_street",
            "track",
            "road",
            "path",
            "cycleway",
        ]
    )
    accepted_highways["car"] = set(
        [
            "motorway",
            "trunk",
            "primary",
            "secondary",
            "tertiary",
            "unclassified",
            "residential",
            "service",
            "motorway_link",
            "trunk_link",
            "primary_link",
            "secondary_link",
            "tertiary_link",
            "living_street",
        ]
    )

    speed_limits = {
        "motorway": 120,
        "trunk": 120,
        "primary": 100,
        "secondary": 100,
        "tertiary": 70,
        "motorway_link": 60,
        "trunk_link": 60,
        "primary_link": 60,
        "secondary_link": 60,
        "unclassified": 50,
        "tertiary_link": 35,
        "residential": 30,
        "service": 10,
        "living_street": 5,
        "pedestrian": 5,
        "track": 5,
        "road": 5,
        "footway": 5,
        "steps": 5,
        "path": 5,
        "cycleway": 5,
        "pedestrian_indoor": 5,
    }

    walking_speed = 5
    max_highway_speed = 120

    extension = {"pedestrian": "pypgr", "car": "pycgr", "bicycle": "pybgr"}
    network_type = None

    def __init__(self, network_type="pedestrian"):
        self.network_type = network_type

    def get_file_extension(self):
        return self.extension[self.network_type]
