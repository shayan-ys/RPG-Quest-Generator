from World.Types import *
from math import acos, cos, degrees, radians


class Place(BaseElement, Named):
    x = IntegerField(default=0, constraints=[Check('x >= 0')])
    y = IntegerField(default=0, constraints=[Check('y >= 0')])


def angle(adjacent_1: float, adjacent_2: float, far_hand: float) -> float:
    """
    Calculates the angle between adjacent_1 and 2, returning angle between 0 and 180
    :param adjacent_1:
    :param adjacent_2:
    :param far_hand:
    :return:
    """
    if not adjacent_1 or not adjacent_2:
        return 180.0

    a = adjacent_1
    b = adjacent_2
    c = far_hand
    return degrees(acos((a * a + b * b - c * c)/(2.0 * a * b)))


def two_point_distance(src: Place, dest: Place) -> float:
    return ((src.x - dest.x)**2 + (src.y - dest.y)**2)**(1/2)


def triangle_distance(src: Place, dest: Place, later: Place) -> float:
    """
    Custom measuring function measuring distance needs to travel by player to two sequential destinations
    The function adds penalty distances if the player should go an extra way and come back.
    :param src: player's current location
    :param dest: player's next location (the one that is being measured)
    :param later: player's next designated distance, where has to go after reaching the destination
    :return: float of a custom distance, if the three points create a perfect triangle,
    return value is sum of distance from src to dest + from dest to later + possible penalties.
    """
    src_dest = two_point_distance(src, dest)
    src_later = two_point_distance(src, later)
    dest_later = two_point_distance(dest, later)

    aggr_dist = src_dest + dest_later

    src_angle = angle(src_dest, src_later, dest_later)
    later_angle = angle(dest_later, src_later, src_dest)

    src_passed_amount = cos(radians(src_angle)) * src_dest
    later_passed_amount = cos(radians(later_angle)) * dest_later

    if later_passed_amount < 0:
        aggr_dist += 2 * (-later_passed_amount)

    if src_passed_amount < 0:
        aggr_dist += 3 * (-src_passed_amount)

    return aggr_dist


list_of_models = [Place]
