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


def exchange(elements: list, item_holder: element_types.NPC, item_to_give: element_types.Item,
             item_to_take: element_types.Item):

    # update Player's location
    for player in elements:
        if isinstance(player, element_types.Player):
            if item_to_give in player.belongings:
                player.belongings.remove(item_to_give)
            player.belongings.append(item_to_take)
            if item_holder not in player.favours_book:
                player.favours_book[item_holder] = 0
            player.favours_book[item_holder] += item_to_give.worth - item_to_take.worth

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


def gather(elements: list, item_to_gather: element_types.Item):

    # update Player's belongings
    for elem in elements:
        if isinstance(elem, element_types.Player):
            elem.belongings.append(item_to_gather)

    print("==> Gather '%s'." % item_to_gather)
    return item_to_gather, []


def give(elements: list, item: element_types.Item, receiver: element_types.NPC):

    # update Player's belongings
    for player in elements:
        if isinstance(player, element_types.Player):
            if item in player.belongings:
                player.belongings.remove(item)
            if receiver not in player.favours_book:
                player.favours_book[receiver] = 0.0
            player.favours_book[receiver] += item.worth

    receiver.belongings.append(item)

    print("==> Give '%s' to '%s'." % (item, receiver))
    return item, []


def spy(elements: list, spy_on: element_types.NPC, intel_target: element_types.Intel):

    # update Player's intel
    for elem in elements:
        if isinstance(elem, element_types.Player):
            if intel_target not in elem.intel:
                elem.intel.append(intel_target)

    print("==> Spy on '%s' to get intel '%s'." % (spy_on, intel_target))
    return intel_target, []


def stealth(elements: list, target: element_types.NPC):
    print("==> Stealth on '%s'." % target)
    return target, []


def take(elements: list, item_to_take: element_types.Item, item_holder: element_types.NPC):

    # remove item from holder's belongings
    if item_to_take in item_holder.belongings:
        item_holder.belongings.remove(item_to_take)

    # add the item to Player's belongings
    for player in elements:
        if isinstance(player, element_types.Player):
            player.belongings.append(item_to_take)
            if item_holder not in player.favours_book:
                player.favours_book[item_holder] = 0
            player.favours_book[item_holder] -= item_to_take.worth

    print("==> Take '%s'." % item_to_take)
    return item_to_take, []


def read(elements: list, intel: element_types.Intel, readable: element_types.Readable):

    # update Player's intel
    for elem in elements:
        if isinstance(elem, element_types.Player):
            elem.intel.append(intel)

    print("==> Read '%s' from '%s'." % (intel, readable))
    print("==> + New intel added: '%s'" % intel.data)
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
    for player in elements:
        if isinstance(player, element_types.Player):
            player.intel.append(intel)
            if informer not in player.favours_book:
                player.favours_book[informer] = 0
            player.favours_book[informer] -= intel.worth

    print("==> Listen to '%s' to get the intel '%s'." %(informer, intel))
    print("==> + New intel added: '%s'" % intel.data)
    return informer, []


def report(elements: list, intel: element_types.Intel, target: element_types.NPC):

    # update target's intel list
    target.intel.append(intel)

    # update Player's favours book
    for player in elements:
        if isinstance(player, element_types.Player):
            if target not in player.favours_book:
                player.favours_book[target] = 0
            player.favours_book[target] += intel.worth

    print("==> Report '%s' (%s) to '%s'." % (intel, intel.data, target))
    return target, []


def use(elements: list, item_to_use: element_types.Item, target: element_types.NPC):
    # TODO: depending on positive or negative impact of the item usage, target record in player's favour book should
    # be updated

    print("==> Use '%s' on '%s'." % (item_to_use, target))
    return item_to_use, []
