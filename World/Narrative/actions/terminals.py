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
    return True


def exchange(item_holder: NPC, item_to_give: Item, item_to_take: Item):

    player = Player.get()

    # check if player has the item_to_give and holder has the item_to_take
    if item_to_give.belongs_to_player != player or item_to_take.belongs_to != item_holder:
        print("DEBUG:")
        print("item_to_give:", item_to_give, ",belongs_to_player:", item_to_give.belongs_to_player, ",player:", player)
        print("item_to_take:", item_to_take, ",belongs_to:", item_to_take.belongs_to, ",item_holder:", item_holder)
        return False

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
    return True


def explore(area_location: Place):

    # Todo: implement exploration around the location

    player = Player.get()

    # check if player knows the location
    results = PlayerKnowledgeBook.select().join(Intel)\
        .where(PlayerKnowledgeBook.player == player, Intel.place == area_location).limit(1)
    if not results:
        print("Location unknown (Intel not found in player's knowledge book)")
        return False

    # update Player's location
    player.place = area_location
    player.save()

    print("==> Explore around '", area_location, "'.")
    return True


def gather(item_to_gather: Item):

    player = Player.get()

    # check if player is at item location
    if item_to_gather.place != player.place:
        print("Player is not at the item's location to gather it")
        return False

    # update Player's belongings
    item_to_gather.belongs_to_player = player
    item_to_gather.save()

    print("==> Gather '", item_to_gather, "'.")
    return True


def give(item: Item, receiver: NPC):

    # check if player has the item
    player = Player.get()
    if item.belongs_to_player != player:
        print("Player doesn't have the item")
        return False

    # check if player is at receiver's location
    if player.place != receiver.place:
        print("Player is not at the receiver NPC's location")
        return False

    item.belongs_to_player = None
    item.belongs_to = receiver
    item.save()

    FavoursBook.construct(receiver, item.worth_())

    print("==> Give '%s' to '%s'." % (item, receiver))
    return True


def spy(spy_on: NPC, intel_target: Intel):

    player = Player.get()

    # check if player is at target's location
    if player.place != spy_on.place:
        print("Player is not at the target NPC's location")
        return False

    # update Player's intel
    PlayerKnowledgeBook.get_or_create(player=player, intel=intel_target)

    print("==> Spy on '%s' to get intel '%s'." % (spy_on, intel_target))
    return True


def stealth(target: NPC):
    print("==> Stealth on '", target, "'.")
    return True


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

    player = Player.get()

    # check if player knows the location
    results = PlayerKnowledgeBook.select().join(Intel)\
        .where(PlayerKnowledgeBook.player == player, Intel.place == destination).limit(1)
    if not results:
        print("Location unknown (Intel not found in player's knowledge book)")
        return False

    # update Player's location
    player.place = destination
    player.save()

    print("==> Goto '%s'." % destination)
    return True


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
