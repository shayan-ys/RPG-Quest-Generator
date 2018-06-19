from World.tags import ActionTags

from Grammar.actions import Terminals as T


class Type:
    tags = []
    
    def __str__(self):
        return self.__class__


class Person(Type):
    tags = [
        ActionTags(action=T.capture),
        ActionTags(action=T.damage),
        ActionTags(action=T.defend),
        ActionTags(action=T.escort),
        ActionTags(action=T.kill),
        ActionTags(action=T.listen),
        ActionTags(action=T.spy),
        ActionTags(action=T.stealth)
    ]


class Place(Type):
    tags = [
        ActionTags(action=T.explore),
        ActionTags(action=T.goto)
    ]


class Territory(Place):
    tags = Place.tags + []


class Object(Type):
    tags = [
        ActionTags(action=T.damage),
        ActionTags(action=T.defend),
        ActionTags(action=T.exchange),
        ActionTags(action=T.gather),
        ActionTags(action=T.give),
        ActionTags(action=T.repair),
        ActionTags(action=T.take),
        ActionTags(action=T.use),
    ]


class UnknownObject(Object):
    tags = Object.tags + [
        ActionTags(action=T.experiment),
        ActionTags(action=T.spy),
    ]


class Tool(Object):
    tags = Object.tags + [
        ActionTags(action=T.use)
    ]


class Book(Object):
    tags = Object.tags + [
        ActionTags(action=T.read)
    ]
