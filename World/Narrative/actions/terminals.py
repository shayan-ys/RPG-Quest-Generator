from World.properties import Location
from World import types


# def neutral(elements: list, target: types.Type):
#     print("==> Do it, target: '%s'" % target)
#     return target, []


def explore(elements: list, area_location: Location):
    print("==> Explore around '%s'." % area_location)
    return area_location, []


def stealth(elements: list, target: types.NPC):
    print("==> Stealth on '%s'." % target)
    return target, []


def take(elements: list, item_to_take: types.Object):
    print("==> Take '%s'." % item_to_take)
    return item_to_take, []


def read(elements: list, intel: types.Intel, readable: types.Readable):
    print("==> Read '%s' from '%s'." % (intel, readable))
    print("==> + New intel added: '%s'" % intel.type.value)
    return readable, []


def goto(elements: list, destination: types.Place):
    print("==> Goto '%s'." % destination)
    return destination, []


def listen(elements: list, intel: types.Intel, informer: types.NPC):
    print("==> Listen to '%s' to get the intel '%s'." %(informer, intel))
    print("==> + New intel added: '%s'" % intel.type.value)
    return informer, []


def report(elements: list, intel: types.Intel, target: types.NPC):
    print("==> Report '%s' (%s) to '%s'." % (intel, intel.type.value, target))
    return target, []
