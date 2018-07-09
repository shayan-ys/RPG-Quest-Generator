from World.properties import Location

from Grammar.actions import Terminals as T


class Type:
    applied_actions = []    # Grammar.actions Terminals you can do to this type

    def __str__(self):
        return str(self.__class__)


class Intel(Type):
    pass


class IntelSpell(Intel):
    value = ""


class IntelLocation(Intel):
    value = None    # type: Location


class Person(Type):
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
    allies = []     # list of ally characters
    enemies = []    # list of enemy characters
    intel = []
    belongings = []
    place = None    # type: Place


class NPC(Person):
    """
    Non Player Character
    """
    motivations = {
        # NT.knowledge: 0.7,
        # NT.conquest: 0.2
    }


class Player(Person):
    pass


class Place(Type):
    applied_actions = [
        T.explore,
        T.goto
    ]
    location = None     # type: Location


class Object(Type):
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
    applied_actions = Object.applied_actions + [
        T.read
    ]
    intel = []
