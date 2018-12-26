from World.Types.Person import Player, NPC, NPCDead
from World.Types.Place import Place
from World.Types.Item import Item, ItemTypes
from World.Types.Intel import Intel
from World.Types.BridgeModels import NPCKnowledgeBook, PlayerKnowledgeBook, FavoursBook, ReadableKnowledgeBook
from World.Types.Log import Message

from World.Narrative import helper as NarrativeHelper

""" return True if action is do-able """


def null(*args):
    """
    Nothing to do
    :return:
    """
    # print('==> There is nothing to do ("null" action)')
    Message.debug("null terminal called")
    return True


def talk(npc: NPC):
    player = Player.current()
    if player.place != npc.place:
        # print("Player is not at the npc's place_location,", npc.place)
        Message.instruction("Player is not at the NPC '%s' place, can't talk to him" % npc)
        return False

    if not PlayerKnowledgeBook.get_or_none(player=player, intel=Intel.construct(npc_place=npc)):
        # print("Player doesn't know where the NPC (%s) is" % npc)
        Message.instruction("Player doesn't know where the NPC (%s) is" % npc)
        return False

    # print("==> Talking to", npc)
    Message.achievement("Talking to '%s'" % npc)
    return True


def exchange(item_holder: NPC, item_to_give: Item, item_to_take: Item):

    player = Player.current()

    # check if player has the item_to_give and holder has the item_to_take
    if item_to_give.belongs_to_player != player:
        # print("DEBUG:")
        # print("item_to_give:", item_to_give, ",belongs_to_player:", item_to_give.belongs_to_player, ",player:", player)
        Message.debug("item_to_give: '%s', belongs_to_player: '%s'" % (item_to_give, item_to_give.belongs_to_player))
        return False
    if item_to_take.belongs_to != item_holder:
        # print("DEBUG:")
        # print("item_to_take:", item_to_take, ",belongs_to:", item_to_take.belongs_to, ",item_holder:", item_holder)
        Message.debug("item_to_take: '%s', belongs_to: '%s', item_holder: '%s'" %
                      (item_to_take, item_to_give.belongs_to, item_holder))
        return False

    # check if player is at item_holder's place_location
    if item_holder.place != player.place:
        # print("Player is not at the item_holder's place_location,", item_holder.place)
        Message.debug("Player is not at the item_holder (%s) place_location (%s)" % (item_holder, item_holder.place))
        Message.instruction("Player is not at the item_holder (%s) location" % item_holder)
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

    # print("==> Exchange '%s' for '%s', with '%s'." % (item_to_give, item_to_take, item_holder))
    Message.achievement("Item '%s' exchanged for '%s', with NPC '%s'" % (item_to_give, item_to_take, item_holder))
    return True


def explore(area_location: Place, npc: NPC=None, item: Item=None):

    player = Player.current()

    # check if player knows the location
    results = PlayerKnowledgeBook.select().join(Intel)\
        .where(PlayerKnowledgeBook.player == player, Intel.place_location == area_location).limit(1)
    if not results:
        # print("Location", area_location, "unknown (Intel not found in player's knowledge book)")
        Message.debug("Location %s unknown (Intel not found in player's knowledge book)" % area_location)
        Message.instruction("Location %s unknown to the player" % area_location)
        return False

    # update Player's location
    player.place = area_location
    player.save()

    if npc:
        target = npc
    elif item:
        target = item
    else:
        target = ''

    # print("==> Explore around '", area_location, "'.")
    Message.achievement("Player found '%s' by exploring '%s'" % (target, area_location))

    if npc:
        # find npc for player (give npc place intel to player)
        intel = Intel.construct(npc_place=npc)
    elif item:
        intel = Intel.construct(item_place=item)
    else:
        intel = None
    if intel:
        PlayerKnowledgeBook.get_or_create(player=player, intel=intel)
        # print("Intel gathered", intel)
        Message.achievement("Intel '%s' learned" % intel)

    return True


def gather(item_to_gather: Item):

    player = Player.current()

    # check if player is at item location
    if item_to_gather.place != player.place:
        # print("Player is not at the item's location to gather it")
        Message.debug("Player is not at the item '%s's location (%s) to gather it" %
                            (item_to_gather, item_to_gather.place))
        Message.instruction("Player is not at the item '%s's location to gather it" % item_to_gather)
        return False

    # update Player's belongings
    item_to_gather.belongs_to_player = player
    item_to_gather.save()

    # print("==> Gather '", item_to_gather, "'.")
    Message.achievement("Item '%s' gathered" % item_to_gather)
    return True


def give(item: Item, receiver: NPC):

    # check if player has the item
    player = Player.current()
    if item.belongs_to_player != player:
        # print("Player doesn't have the item")
        Message.instruction("Player doesn't have the item (%s) to give" % item)
        return False

    # check if player is at receiver's location
    if player.place != receiver.place:
        # print("Player is not at the receiver NPC's location,", receiver.place)
        Message.debug("Player is not at the receiver NPC (%s) location (%s)" % (receiver, receiver.place))
        Message.instruction("Player is not at the receiver NPC (%s) location" % receiver)
        return False

    item.belongs_to_player = None
    item.belongs_to = receiver
    item.save()

    # update favours book
    FavoursBook.construct(npc=receiver, owe_factor=item.worth_(), player=player)

    # print("==> Give '%s' to '%s'." % (item, receiver))
    Message.achievement("Item '%s' has been given to the NPC '%s'" % (item, receiver))
    return True


def spy(spy_on: NPC, intel_target: Intel):

    player = Player.current()

    # check if player is at target's location
    if player.place != spy_on.place:
        # print("Player is not at the target NPC's location")
        Message.debug("Player is not at the NPC (%s) location (%s) for spy" % (spy_on, spy_on.place))
        Message.instruction("Player is not at the NPC '%s's location for spy" % spy_on)
        return False

    # check if the target has the piece of intel
    if not NPCKnowledgeBook.get_or_none(npc=spy_on, intel=intel_target):
        # print("Target hasn't the intel")
        Message.debug("Target (%s) does not have the intel (%s) player wanted" % (spy_on, intel_target))
        Message.event("Target (%s) does not have the intel (%s) player wanted" % (spy_on, intel_target))
        return False

    # update Player's intel
    NarrativeHelper.add_intel(intel_target)

    # print("==> Spy on '%s' to get intel '%s'." % (spy_on, intel_target))
    Message.achievement("Intel '%s' gathered by spying on '%s'" % (intel_target, spy_on))
    return True


def stealth(target: NPC):

    player = Player.current()

    # check if player at target's place_location
    if player.place != target.place:
        # print("Player is not at the target's place_location", target.place)
        Message.debug("Player is not at the target (%s) place_location (%s)" % (target, target.place))
        Message.instruction("Player is not at the target NPC '%s's location" % target)
        return False

    # print("==> Stealth on '", target, "'.")
    Message.achievement("Successfully snuck on '%s'" % target)
    return True


def take(item_to_take: Item, item_holder: NPC=None):

    if item_holder is None:
        return take_loot(item_to_take)

    player = Player.current()

    # check if NPC has the item
    if item_to_take.belongs_to != item_holder:
        # print("NPC", item_holder, "doesn't have the item", item_to_take, "to take")
        Message.debug("NPC '%s' doesn't have the item '%s' to give. It belongs to '%s'" %
                      (item_holder, item_to_take, item_to_take.belongs_to))
        Message.event("NPC '%s' doesn't have the item '%s' to give" % (item_holder, item_to_take))
        return False

    # check if player is at item_holder's place_location
    if item_holder.place != player.place:
        # print("Player is not at the item_holder's place_location", item_holder.place)
        Message.debug("Player is not at the item_holder (%s) place_location (%s)" % (item_holder, item_holder.place))
        Message.instruction("Player is not at the NPC '%s' location" % item_holder)
        return False

    # remove item from holder's belongings and add to player's
    item_to_take.belongs_to = None
    item_to_take.belongs_to_player = player
    item_to_take.save()

    FavoursBook.construct(item_holder, -item_to_take.worth_(), player)

    # print("==> Take '%s'." % item_to_take)
    Message.achievement("Item '%s' taken" % item_to_take)
    return True


def take_loot(item_to_take: Item, loot_npc: NPCDead=None):

    player = Player.current()

    # check if the item belongs to dead
    if not loot_npc:
        # NPC confirmed dead already, object among dead is given
        try:
            holder = item_to_take.belongs_to
        except:
            # holder not found = dead
            Message.debug("Item '%s' holder is dead")
            holder = None

        if holder:
            # holder is alive
            return take(item_to_take, item_holder=holder)

    # remove item from holder's belongings and add to player's
    item_to_take.belongs_to = None
    item_to_take.belongs_to_player = player
    item_to_take.save()

    # FavoursBook.construct(item_holder, -item_to_take.worth_(), player)

    # print("==> Take '%s' by looting" % item_to_take)
    Message.achievement("Item '%s' taken by looting" % item_to_take)
    return True


def read(intel: Intel, readable: Item):

    # check if the readable has the intel
    if not ReadableKnowledgeBook.get_or_none(
            ReadableKnowledgeBook.intel == intel,
            ReadableKnowledgeBook.readable == readable):
        # print("ReadableKnowledgeBook not found")
        Message.debug("Readable '%s' does not contain the intel '%s', ReadableKnowledgeBook not found" %
                      (readable, intel))
        Message.event("Readable '%s' does not contain the intel player looking for" % readable)
        return False

    player = Player.current()
    # check if player owns the readable
    if readable.belongs_to_player != player:
        # print("Player neither own the item, nor at the readable item's place_location,", readable.place_())
        Message.debug("Player doesn't have the readable '%s'" % readable)
        if readable.place_() == player.place:
            readable.belongs_to = None
            readable.belongs_to_player = player
            readable.save()
            # print("Player didn't own the readable (%s) but at its place so he take it" % readable)
            Message.debug("Player didn't own the readable (%s) but at its place so he take it" % readable)
        else:
            # print("Player neither own the readable (%s), nor at the item's place_location" % readable.place_())
            Message.debug("Player neither own the readable (%s), nor at the item's place_location (%s)" %
                          (readable, readable.place_()))
            Message.instruction("Player neither own the readable (%s), nor at the item's location" % readable)
            return False

    # update Player's intel
    NarrativeHelper.add_intel(intel)

    # print("==> Read '%s' from '%s'." % (intel, readable))
    Message.achievement("By reading '%s' intel '%s' learned" % (readable, intel))
    return True


def goto(destination: Place):

    player = Player.current()

    # check if player knows the location
    results = PlayerKnowledgeBook.select().join(Intel)\
        .where(PlayerKnowledgeBook.player == player, Intel.place_location == destination).limit(1)
    if not results:
        # print("Location '", destination, "' unknown (Intel not found in player's knowledge book)")
        Message.instruction("Location '%s' is unknown to the player" % destination)
        return False

    # update Player's location
    player.place = destination
    player.save()

    # print("==> Goto '%s'." % destination)
    Message.achievement("Player went to '%s'" % destination)
    return True


def kill(target: NPC):

    player = Player.current()

    # check if player is at target place_location
    if player.place != target.place:
        # print("Player is not at target's location,", target.place)
        Message.instruction("Player is not at the target '%s's location" % target)
        return False

    # print("==> Kill '%s'." % target)
    Message.achievement("NPC '%s' has been killed" % target)

    NPCDead.create(name=target.name, place=target.place, clan=target.clan)
    target.delete_instance()

    return True


def listen(intel: Intel, informer: NPC):

    # check if informer has the intel
    if not NPCKnowledgeBook.get_or_none(intel=intel, npc=informer):
        # print("Informer hasn't the intel player wants")
        Message.event("Informer hasn't the intel (%s) player wants" % intel)
        return False

    player = Player.current()

    # check if player is in the informer place_location
    if informer.place != player.place:
        # print("Player is not at the informer's place_location,", informer.place)
        Message.instruction("Player is not at the informer (%s)'s location" % informer)
        return False

    # update Player's intel
    NarrativeHelper.add_intel(intel)
    FavoursBook.construct(informer, -intel.worth_(), player)

    # print("==> Listen to '%s' to get the intel '%s'." % (informer, intel))
    Message.achievement("Intel '%s' acquired by listening to '%s'" % (intel, informer))
    return True


def report(intel: Intel, target: NPC):

    player = Player.current()

    # check if player has the intel
    if not PlayerKnowledgeBook.get_or_none(player=player, intel=intel):
        # print("Player doesn't have the intel")
        Message.instruction("Player doesn't have the intel '%s'" % intel)
        return False

    # check if player is in the target place_location
    if target.place != player.place:
        # print("Player is not at the target's place_location,", target.place)
        Message.debug("Player is not at the target (%s) location (%s)" % (target, target.place))
        Message.instruction("Player is not at the target (%s) location" % target)
        return False

    # update Player's favours book if target hasn't have it already
    if not NPCKnowledgeBook.get_or_none(npc=target, intel=intel):
        FavoursBook.construct(target, intel.worth_())
        # update target's intel list
        NPCKnowledgeBook.create(npc=target, intel=intel)

    # print("==> Report '%s' to '%s'." % (intel, target))
    Message.achievement("Intel '%s' reported to the NPC '%s'" % (intel, target))
    return True


def use(item_to_use: Item, target: NPC):

    player = Player.current()
    # check if player has the item
    if item_to_use.belongs_to_player != player:
        # print("Player doesn't have the item,", item_to_use)
        Message.instruction("Player doesn't have the item (%s)" % item_to_use)
        return False

    # check if player at target's place_location
    if target.place != player.place:
        # print("Player is not at the target's place_location,", target.place)
        Message.debug("Player is not at the target '%s's location (%s)" % (target, target.place))
        Message.instruction("Player is not at the target '%s's location" % target)
        return False

    # check if item is a tool
    if item_to_use.type != ItemTypes.tool.name:
        # print("Item is not usable, it's not a tool, it is a,", item_to_use.type)
        Message.debug("Item '%s' is not a tool, not usable, it's a '%s'" % (item_to_use, item_to_use.type))
        Message.event("Item '%s' is not a tool, not usable" % item_to_use)
        return False

    item_to_use.use(npc=target)

    # depending on positive or negative impact_factor of the item usage, target record in player's favour gets updated
    FavoursBook.construct(target, float(item_to_use.impact_factor or 0.0))

    # print("==> Use '%s' on '%s'." % (item_to_use, target))
    Message.achievement("Item '%s' used on the '%s'" % (item_to_use, target))
    return True
