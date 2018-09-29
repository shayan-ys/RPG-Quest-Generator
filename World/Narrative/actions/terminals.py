from World.properties import Location

from World.Types.Person import Player, NPC
from World.Types.Place import Place
from World.Types.Item import Item
from World.Types.Intel import Intel
from World.Types.BridgeModels import NPCKnowledgeBook, PlayerKnowledgeBook, FavoursBook


def null():
    """
    Nothing to do
    :return:
    """
    print('==> There is nothing to do ("null" action)')
    return []


def exchange(item_holder: NPC, item_to_give: Item, item_to_take: Item):

    player = Player.get()

    # update Player's belongings
    item_to_take.belongs_to = None
    item_to_take.belongs_to_player = player
    item_to_take.save()

    item_to_give.belongs_to_player = None
    item_to_give.belongs_to = item_holder
    item_to_give.save()

    npc_owing = item_to_give.worth_() - item_to_take.worth_()
    FavoursBook.construct(item_holder, npc_owing, player)

    print("==> Exchange '%s' for '%s', with '%s'." % (item_to_give, item_to_take, item_holder))
    return []


def explore(area_location: Location):

    # update Player's location
    player = Player.get()
    player.place = area_location
    player.save()

    print("==> Explore around '", area_location, "'.")


def gather(item_to_gather: Item):

    # update Player's belongings
    item_to_gather.belongs_to_player = Player.get()
    item_to_gather.save()

    print("==> Gather '", item_to_gather, "'.")
    return []


def give(item: Item, receiver: NPC):

    item.belongs_to_player = None
    item.belongs_to = receiver
    item.save()

    FavoursBook.construct(receiver, item.worth_())

    print("==> Give '%s' to '%s'." % (item, receiver))
    return []


def spy(spy_on: NPC, intel_target: Intel):

    # update Player's intel
    player = Player.get()
    PlayerKnowledgeBook.get_or_create(player=player, intel=intel_target)

    print("==> Spy on '%s' to get intel '%s'." % (spy_on, intel_target))
    return []


def stealth(target: NPC):
    print("==> Stealth on '", target, "'.")
    return []


def take(item_to_take: Item, item_holder: NPC):

    # remove item from holder's belongings and add to player's
    player = Player.get()
    item_to_take.belongs_to = None
    item_to_take.belongs_to_player = player
    item_to_take.save()

    FavoursBook.construct(item_holder, -item_to_take.worth_(), player)

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
    player.save()

    print("==> Goto '%s'." % destination)
    return []


def kill(target: NPC):
    print("==> Kill '%s'." % target)
    return []


def listen(intel: Intel, informer: NPC):

    # update Player's intel
    player = Player.get()
    PlayerKnowledgeBook.get_or_create(player=player, intel=intel)

    FavoursBook.construct(informer, -intel.worth_(), player)

    print("==> Listen to '%s' to get the intel '%s'." % (informer, intel))
    print("==> + New intel added: '%s'" % intel)
    return []


def report(intel: Intel, target: NPC):

    # update target's intel list
    NPCKnowledgeBook.get_or_create(npc=target, intel=intel)

    # update Player's favours book
    FavoursBook.construct(target, intel.worth_())

    print("==> Report '%s' to '%s'." % (intel, target))
    return []


def use(item_to_use: Item, target: NPC):
    # depending on positive or negative impact_factor of the item usage, target record in player's favour gets updated
    FavoursBook.construct(target, float(item_to_use.impact_factor or 0.0))

    print("==> Use '%s' on '%s'." % (item_to_use, target))
    return []
