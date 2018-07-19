from World.properties import Location

from Grammar.actions import Terminals as T

from enum import Enum
from typing import List


class BaseElement:
    applied_actions = []    # Grammar.actions Terminals you can do to this type

    def __str__(self):
        if hasattr(self, 'name'):
            return self.name
        return str(self.__class__)

    def __repr__(self):
        return self.__str__()


list_of_elements = List[BaseElement]


class DistanceMeasures(Enum):
    near = 20
    close = 75
    far = 150
    unreachable = 300


def distance_meter(src: Location, dest: Location) -> DistanceMeasures:
    distance = ((src.x - dest.x)**2 + (src.y - dest.y)**2)**(1/2)

    if distance <= DistanceMeasures.near.value:
        return DistanceMeasures.near
    elif distance <= DistanceMeasures.close.value:
        return DistanceMeasures.close
    elif distance <= DistanceMeasures.far.value:
        return DistanceMeasures.far
    else:
        return DistanceMeasures.unreachable


class Intel(BaseElement):
    value = None

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

    def __eq__(self, other: 'Intel'):
        return self.value == other.value


class IntelSpell(Intel):
    value = ""  # type: str


class IntelLocation(Intel):
    value = None    # type: Location


class Place(BaseElement):
    name = ""
    applied_actions = [
        T.explore,
        T.goto
    ]
    location = None     # type: Location

    def __init__(self, name: str, location: Location):
        self.name = name
        self.location = location

    def distance_from(self, player: 'Player') -> DistanceMeasures:
        return distance_meter(self.location, player.current_location)


class Person(BaseElement):
    name = ""
    applied_actions = [
        T.capture,
        T.damage,
        T.defend,
        T.escort,
        T.kill,
        T.listen,
        T.spy,
        T.stealth
    ]
    place = None    # type: Place
    allies = []     # list of ally characters
    enemies = []    # list of enemy characters
    intel = []
    belongings = []


class NPC(Person):
    """
    Non Player Character
    """
    motivations = {
        # NT.knowledge: 0.7,
        # NT.conquest: 0.2
    }

    def __init__(self, name: str, motivations: dict, place: Place, **kwargs):
        self.name = name
        self.motivations = motivations
        self.place = place
        self.__dict__.update(kwargs)


class Player(Person):
    current_location: Location = None

    def __init__(self, name: str, intel: List[Intel]):
        self.name = name
        self.intel = intel


class Clan:
    members: List[NPC] = []

    def __init__(self, members: List[NPC]):
        self.members = []
        for mem in members:
            mem.allies = members
            self.members.append(mem)

    def set_enemy(self, enemy: 'Clan'):
        for mem in self.members:
            mem.enemies = enemy.members


class Object(BaseElement):
    applied_actions = [
        T.damage,
        T.defend,
        T.exchange,
        T.gather,
        T.give,
        T.repair,
        T.take,
        T.use
    ]


class UnknownObject(Object):
    applied_actions = Object.applied_actions + [
        T.experiment,
        T.spy,
    ]


class Tool(Object):
    applied_actions = Object.applied_actions + [
        T.use
    ]


class Readable(Object):
    name: str = ""
    applied_actions = Object.applied_actions + [
        T.read
    ]
    intel: List[Intel] = []

    def __init__(self, name: str, intel: list):
        """
        :param list[Intel] intel:
        """
        self.name = name
        self.intel = intel
