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


def exchange(elements: list, item_holder: element_types.NPC, item_to_give: element_types.Object,
             item_to_take: element_types.Object):

    # update Player's location
    for elem in elements:
        if isinstance(elem, element_types.Player):
            if item_to_give in elem.belongings:
                elem.belongings.remove(item_to_give)
            elem.belongings.append(item_to_take)

    item_holder.belongings.append(item_to_give)
    if item_to_take in item_holder.belongings:
        item_holder.belongings.remove(item_to_take)

    print("==> Exchange '%s' for '%s', with '%s'." % (item_to_give, item_to_take, item_holder))
    return item_to_give, []


def explore(elements: list, area_location: Location):

    # update Player's location
    for elem in elements:
        if isinstance(elem, element_types.Player):
            elem.current_location = area_location

    print("==> Explore around '%s'." % area_location)
    return area_location, []


def gather(elements: list, item_to_gather: element_types.Object):

    # update Player's belongings
    for elem in elements:
        if isinstance(elem, element_types.Player):
            elem.belongings.append(item_to_gather)

    print("==> Gather '%s'." % item_to_gather)
    return item_to_gather, []


def give(elements: list, item: element_types.Object, receiver: element_types.NPC):

    # update Player's belongings
    for elem in elements:
        if isinstance(elem, element_types.Player):
            if item in elem.belongings:
                elem.belongings.remove(item)

    receiver.belongings.append(item)

    print("==> Give '%s' to '%s'." % (item, receiver))
    return item, []


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


def kill(elements: list, target: element_types.NPC):
    print("==> Kill '%s'." % target)
    return target, []


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


def use(elements: list, item_to_use: element_types.Object, target: element_types.NPC):
    print("==> Use '%s' on '%s'." % (item_to_use, target))
    return item_to_use, []
