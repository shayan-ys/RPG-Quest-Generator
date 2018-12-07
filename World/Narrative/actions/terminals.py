from World.Types.Person import Player, NPC
from World.Types.Place import Place
from World.Types.Item import Item, ItemTypes
from World.Types.Intel import Intel
from World.Types.BridgeModels import NPCKnowledgeBook, PlayerKnowledgeBook, FavoursBook, ReadableKnowledgeBook

from World.Narrative import helper as NarrativeHelper

""" return True if action is do-able """


def null(*args):
    """
    Nothing to do
    :return:
    """
    print('==> There is nothing to do ("null" action)')
    return True


def exchange(item_holder: NPC, item_to_give: Item, item_to_take: Item):

    player = Player.current()

    # check if player has the item_to_give and holder has the item_to_take
    if item_to_give.belongs_to_player != player:
        print("DEBUG:")
        print("item_to_give:", item_to_give, ",belongs_to_player:", item_to_give.belongs_to_player, ",player:", player)
        return False
    if item_to_take.belongs_to != item_holder:
        print("DEBUG:")
        print("item_to_take:", item_to_take, ",belongs_to:", item_to_take.belongs_to, ",item_holder:", item_holder)
        return False

    # check if player is at item_holder's place_location
    if item_holder.place != player.place:
        print("Player is not at the item_holder's place_location,", item_holder.place)
        return False

    # todo: check if owing factor of NPC is more than different of items worth
    # todo: one item might worth more for an NPC than to other

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

    player = Player.current()

    # check if player knows the location
    results = PlayerKnowledgeBook.select().join(Intel)\
        .where(PlayerKnowledgeBook.player == player, Intel.place_location == area_location).limit(1)
    if not results:
        print("Location unknown (Intel not found in player's knowledge book)")
        return False

    # update Player's location
    player.place = area_location
    player.save()

    print("==> Explore around '", area_location, "'.")
    return True


def gather(item_to_gather: Item):

    player = Player.current()

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
    player = Player.current()
    if item.belongs_to_player != player:
        print("Player doesn't have the item")
        return False

    # check if player is at receiver's location
    if player.place != receiver.place:
        print("Player is not at the receiver NPC's location,", receiver.place)
        return False

    item.belongs_to_player = None
    item.belongs_to = receiver
    item.save()

    # update favours book
    FavoursBook.construct(npc=receiver, owe_factor=item.worth_(), player=player)

    print("==> Give '%s' to '%s'." % (item, receiver))
    return True


def spy(spy_on: NPC, intel_target: Intel):

    player = Player.current()

    # check if player is at target's location
    if player.place != spy_on.place:
        print("Player is not at the target NPC's location")
        return False

    # check if the target has the piece of intel
    if not NPCKnowledgeBook.get_or_none(npc=spy_on, intel=intel_target):
        print("Target hasn't the intel")
        return False

    # update Player's intel
    NarrativeHelper.add_intel(intel_target)

    print("==> Spy on '%s' to get intel '%s'." % (spy_on, intel_target))
    return True


def stealth(target: NPC):

    player = Player.current()

    # check if player at target's place_location
    if player.place != target.place:
        print("Player is not at the target's place_location", target.place)
        return False

    print("==> Stealth on '", target, "'.")
    return True


def take(item_to_take: Item, item_holder: NPC):

    player = Player.current()

    # check if NPC has the item
    if item_to_take.belongs_to != item_holder:
        print("NPC", item_holder, "doesn't have the item", item_to_take, "to take")
        return False

    # check if player is at item_holder's place_location
    if item_holder.place != player.place:
        print("Player is not at the item_holder's place_location,", item_holder.place)
        return False

    # todo: check if NPC has an owing favour or is less powerful, or killed
    if item_holder.health_meter == 0:
        pass

    # remove item from holder's belongings and add to player's
    item_to_take.belongs_to = None
    item_to_take.belongs_to_player = player
    item_to_take.save()

    FavoursBook.construct(item_holder, -item_to_take.worth_(), player)

    print("==> Take '%s'." % item_to_take)
    return True


def read(intel: Intel, readable: Item):

    # check if the readable has the intel
    if not ReadableKnowledgeBook.get_or_none(
            ReadableKnowledgeBook.intel == intel,
            ReadableKnowledgeBook.readable == readable):
        print("ReadableKnowledgeBook not found")
        return False

    player = Player.current()
    # check if player is at the readable item's place_location
    if readable.place_() != player.place and readable.belongs_to_player != player:
        print("Player neither own the item, nor at the readable item's place_location,", readable.place_())
        return False

    # todo: an NPC might have it that doesn't want you to read it! So you have to deal with the NPC first!

    # update Player's intel
    NarrativeHelper.add_intel(intel)

    print("==> Read '%s' from '%s'." % (intel, readable))
    # print("==> + New intel added: '%s'" % intel)
    return True


def goto(destination: Place):

    player = Player.current()

    # check if player knows the location
    results = PlayerKnowledgeBook.select().join(Intel)\
        .where(PlayerKnowledgeBook.player == player, Intel.place_location == destination).limit(1)
    if not results:
        print("Location '", destination, "' unknown (Intel not found in player's knowledge book)")
        return False

    # update Player's location
    player.place = destination
    player.save()

    print("==> Goto '%s'." % destination)
    return True


def kill(target: NPC):

    player = Player.current()

    # check if player is at target place_location
    if player.place != target.place:
        print("Player is not at target's location,", target.place)
        return False

    # todo: check if player has more power than the NPC, take not of their health. (Attack and defense power
    # + current health)

    target.health_meter = 0
    target.save()

    print("==> Kill '%s'." % target)
    return True


def listen(intel: Intel, informer: NPC):

    # check if informer has the intel
    if not NPCKnowledgeBook.get_or_none(intel=intel, npc=informer):
        print("Informer hasn't the intel player wants")
        return False

    player = Player.current()

    # check if player is in the informer place_location
    if informer.place != player.place:
        print("Player is not at the informer's place_location,", informer.place)
        return False

    # check if informer is an ally to player
    # todo: temporary
    # if informer.clan != player.clan:
    #     print("Player and the informer are from different clans")
    #     return False

    # todo: maybe even an enemy with huge amount of owing factor could work too

    # check if player has enough favours book's score for this
    # todo: temporary
    # fb, created = FavoursBook.get_or_create(npc=informer, player=player)
    # if fb.owe_factor <= 0:
    #     print("Player doesn't have enough favour factor,", fb.owe_factor)
    #     return False

    # update Player's intel
    NarrativeHelper.add_intel(intel)
    FavoursBook.construct(informer, -intel.worth_(), player)

    print("==> Listen to '%s' to get the intel '%s'." % (informer, intel))
    # print("==> + New intel added: '%s'" % intel)
    return True


def report(intel: Intel, target: NPC):

    player = Player.current()

    # check if player has the intel
    if not PlayerKnowledgeBook.get_or_none(player=player, intel=intel):
        print("Player doesn't have the intel")
        return False

    # check if player is in the target place_location
    if target.place != player.place:
        print("Player is not at the target's place_location,", target.place)
        return False

    # update Player's favours book if target hasn't have it already
    if not NPCKnowledgeBook.get_or_none(npc=target, intel=intel):
        # todo: check if NPC wanted this piece of intel (?)
        FavoursBook.construct(target, intel.worth_())
        # update target's intel list
        NPCKnowledgeBook.create(npc=target, intel=intel)

    print("==> Report '%s' to '%s'." % (intel, target))
    return True


def use(item_to_use: Item, target: NPC):

    player = Player.current()
    # check if player has the item
    if item_to_use.belongs_to_player != player:
        print("Player doesn't have the item,", item_to_use)
        return False

    # check if player at target's place_location
    if target.place != player.place:
        print("Player is not at the target's place_location,", target.place)
        return False

    # check if item is a tool
    if item_to_use.type != ItemTypes.tool.name:
        print("Item is not usable, it's not a tool, it is a,", item_to_use.type)
        return False

    # todo: if item has an negative impact, check if player has more power than the target and alliance

    item_to_use.use(npc=target)

    # depending on positive or negative impact_factor of the item usage, target record in player's favour gets updated
    FavoursBook.construct(target, float(item_to_use.impact_factor or 0.0))

    print("==> Use '%s' on '%s'." % (item_to_use, target))
    return True
