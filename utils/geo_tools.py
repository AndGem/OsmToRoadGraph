from math import acos, cos, pi, sin


# from http://www.johndcook.com/blog/python_longitude_latitude/
def distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:

    # Convert latitude and longitude to
    # spherical coordinates in radians.
    degrees_to_radians = pi / 180.0

    # phi = 90 - latitude
    phi1 = (90.0 - lat1) * degrees_to_radians
    phi2 = (90.0 - lat2) * degrees_to_radians

    # theta = longitude
    theta1 = lon1 * degrees_to_radians
    theta2 = lon2 * degrees_to_radians

    cos_val = sin(phi1) * sin(phi2) * cos(theta1 - theta2) + cos(phi1) * cos(phi2)
    cos_val = min(1, cos_val)
    arc_val = acos(cos_val)

    return arc_val * 6373000  # distance in meters
