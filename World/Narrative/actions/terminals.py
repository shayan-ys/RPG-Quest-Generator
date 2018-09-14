from World.properties import Location
from World import elements as element_types

from World.Types.Person import Player, NPC
from World.Types.Place import Place
from World.Types.Item import Item
from World.Types.Intel import Intel, NPCKnowledgeBook, PlayerKnowledgeBook


def null():
    """
    Nothing to do
    :return:
    """
    print('==> There is nothing to do ("null" action)')
    return []


# def neutral(target: Type):
#     print("==> Do it, target: '%s'" % target)
#     return target, []


def exchange(item_holder: NPC, item_to_give: Item,
             item_to_take: Item):

    # update Player's location
    for player in elements:
        if isinstance(player, Player):
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
    return []


def explore(area_location: Location):

    # update Player's location
    player = Player.get()
    player.place = area_location

    print("==> Explore around '", area_location, "'.")


def gather(item_to_gather: Item):

    # update Player's belongings
    for elem in elements:
        if isinstance(elem, Player):
            elem.belongings.append(item_to_gather)

    print("==> Gather '%s'." % item_to_gather)
    return []


def give(item: Item, receiver: NPC):

    # update Player's belongings
    for player in elements:
        if isinstance(player, Player):
            if item in player.belongings:
                player.belongings.remove(item)
            if receiver not in player.favours_book:
                player.favours_book[receiver] = 0.0
            player.favours_book[receiver] += item.worth

    receiver.belongings.append(item)

    print("==> Give '%s' to '%s'." % (item, receiver))
    return []


def spy(spy_on: NPC, intel_target: Intel):

    # update Player's intel
    for elem in elements:
        if isinstance(elem, Player):
            if intel_target not in elem.intel:
                elem.intel.append(intel_target)

    print("==> Spy on '%s' to get intel '%s'." % (spy_on, intel_target))
    return []


def stealth(target: NPC):
    print("==> Stealth on '", target, "'.")
    return []


def take(item_to_take: Item, item_holder: NPC):

    # remove item from holder's belongings and add to player's
    if item_to_take in item_holder.belongings:
        # item_holder.belongings.where(Item.id == item_to_take.id).get().delete_instance()
        player = Player.get()
        item_to_take.belongs_to = None
        item_to_take.belongs_to_player = player
        item_to_take.save()

    print("==> Take '%s'." % item_to_take)
    return []


def read(intel: Intel, readable: Item):

    # update Player's intel
    player = Player.get()
    PlayerKnowledgeBook.get_or_create(player=player, intel=intel)

    print("==> Read '%s' from '%s'." % (intel, readable))
    print("==> + New intel added: '%s'" % intel)
    return []


def goto(destination: Place):

    # update Player's location
    player = Player.get()
    player.place = destination

    print("==> Goto '%s'." % destination)
    return []


def kill(target: NPC):
    print("==> Kill '%s'." % target)
    return []


def listen(intel: Intel, informer: NPC):

    # update Player's intel
    player = Player.get()
    PlayerKnowledgeBook.get_or_create(player=player, intel=intel)

    print("==> Listen to '%s' to get the intel '%s'." %(informer, intel))
    print("==> + New intel added: '%s'" % intel)
    return []


def report(intel: Intel, target: NPC):

    # update target's intel list
    NPCKnowledgeBook.get_or_create(npc=target, intel=intel)

    # update Player's favours book

    print("==> Report '%s' to '%s'." % (intel, target))
    return []


def use(item_to_use: Item, target: NPC):
    # TODO: depending on positive or negative impact of the item usage, target record in player's favour book should
    # be updated

    print("==> Use '%s' on '%s'." % (item_to_use, target))
    return []
