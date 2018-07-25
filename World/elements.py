from World.properties import Location

from Grammar.actions import Terminals as T

from enum import Enum
from typing import List, Dict


class BaseElement:
    applied_actions = []    # Grammar.actions Terminals you can do to this type

    def __str__(self):
        if hasattr(self, 'name'):
            return self.name
        return str(self.__class__.__name__)

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
    worth = 0.0     # general worth (price)

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

    def __eq__(self, other: 'Intel'):
        return self.value == other.value

    def __hash__(self):
        return hash(self.value)


class IntelSpell(Intel):
    value = ""  # type: str
    worth = 1.0


class IntelLocation(Intel):
    value = None    # type: Place
    worth = 0.1


class IntelHolding(Intel):
    value = None    # type: Item
    holder = None   # type: Person
    worth = 0.3

    def __init__(self, value: 'Item', holder: 'Person'):
        super(IntelHolding, self).__init__(value)
        self.holder = holder

    def __eq__(self, other: 'IntelHolding'):
        return self.value == other.value and self.holder == other.holder

    def __hash__(self):
        return hash((self.value, self.holder))


class Place(BaseElement):
    name = ""
    applied_actions = [
        T.explore,
        T.goto
    ]
    location = None     # type: Location
    items = []          # type: List[Item]
    # list of items can be found at the place

    def __init__(self, name: str, location: Location, items: List['Item']=None):
        self.name = name
        self.location = location
        if items:
            self.items = items
            for item in self.items:
                item.place = self

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
    place: Place = None                               # the place where Person is
    allies: List['Person'] = []                       # list of ally characters
    enemies: List['Person'] = []                      # list of enemy characters
    intel: List[Intel] = []                           # list of intel pieces
    belongings: List['Item'] = []                   # list of holding items
    needs: List['Item'] = []                        # list of items needed
    exchange_motives: Dict['Item', 'Item'] = {}   # dictionary of exchange motivations,
    #   key is what Person has, value is list of items they need


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
        for item in self.belongings:
            item.place = place


class Player(Person):
    current_location: Location = None
    coins = 0

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


class Item(BaseElement):
    name = ""
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
    place = None   # Person's place or the Place where the object is

    def __init__(self, name: str=""):
        self.name = name


class UnknownItem(Item):
    applied_actions = Item.applied_actions + [
        T.experiment,
        T.spy,
    ]


class Tool(Item):
    usage: T = None
    applied_actions = Item.applied_actions + [
        T.use
    ]

    def __init__(self, name: str, usage: T):
        super(Tool, self).__init__(name=name)
        self.usage = usage


class Readable(Item):
    applied_actions = Item.applied_actions + [
        T.read
    ]
    intel: List[Intel] = []

    def __init__(self, name: str, intel: list):
        super(Readable, self).__init__(name=name)
        """
        :param list[Intel] intel:
        """
        self.intel = intel


class Coin(BaseElement):
    pass


coin = Coin()
