from World.properties import Location
from World import elements as element_types


def null(elements: list):
    """
    Nothing to do
    :param elements:
    :return:
    """
    print('==> There is nothing to do ("null" action)')
    return None, []


# def neutral(elements: list, target: element_types.Type):
#     print("==> Do it, target: '%s'" % target)
#     return target, []


def explore(elements: list, area_location: Location):

    # update Player's location
    for elem in elements:
        if isinstance(elem, element_types.Player):
            elem.current_location = area_location

    print("==> Explore around '%s'." % area_location)
    return area_location, []


def stealth(elements: list, target: element_types.NPC):
    print("==> Stealth on '%s'." % target)
    return target, []


def take(elements: list, item_to_take: element_types.Object):

    # TODO: remove item from holder's belongings

    # add the item to Player's belongings
    for elem in elements:
        if isinstance(elem, element_types.Player):
            elem.belongings.append(item_to_take)

    print("==> Take '%s'." % item_to_take)
    return item_to_take, []


def read(elements: list, intel: element_types.Intel, readable: element_types.Readable):

    # update Player's intel
    for elem in elements:
        if isinstance(elem, element_types.Player):
            elem.intel.append(intel)

    print("==> Read '%s' from '%s'." % (intel, readable))
    print("==> + New intel added: '%s'" % intel.value)
    return readable, []


def goto(elements: list, destination: element_types.Location):

    # update Player's location
    for elem in elements:
        if isinstance(elem, element_types.Player):
            elem.current_location = destination

    print("==> Goto '%s'." % destination)
    return destination, []


def listen(elements: list, intel: element_types.Intel, informer: element_types.NPC):

    # update Player's intel
    for elem in elements:
        if isinstance(elem, element_types.Player):
            elem.intel.append(intel)

    print("==> Listen to '%s' to get the intel '%s'." %(informer, intel))
    print("==> + New intel added: '%s'" % intel.value)
    return informer, []


def report(elements: list, intel: element_types.Intel, target: element_types.NPC):

    # update target's intel list
    target.intel.append(intel)

    print("==> Report '%s' (%s) to '%s'." % (intel, intel.value, target))
    return target, []
