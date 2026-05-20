from math import asin, cos, radians, sin, sqrt

# radius kept identical to the previous implementation so edge lengths
# stay comparable across versions (~6373 km, see johndcook.com reference)
EARTH_RADIUS_M = 6373000


def distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Great-circle distance between two points, in meters.

    Uses the haversine formula. Unlike the spherical law of cosines, it
    stays numerically stable for the very short distances between adjacent
    OSM nodes, which is the dominant case for this tool.
    """
    phi1, phi2 = radians(lat1), radians(lat2)
    d_phi = radians(lat2 - lat1)
    d_lambda = radians(lon2 - lon1)

    a = sin(d_phi / 2.0) ** 2 + cos(phi1) * cos(phi2) * sin(d_lambda / 2.0) ** 2

    return 2.0 * EARTH_RADIUS_M * asin(sqrt(a))
