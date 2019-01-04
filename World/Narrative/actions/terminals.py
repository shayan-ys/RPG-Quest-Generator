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
    Message.debug("null terminal called")
    return True


def talk(npc: NPC):
    player = Player.current()
    if player.place != npc.place:
        Message.error("You are not at the NPC '%s's place, can't talk to him" % npc)
        return False

    if not PlayerKnowledgeBook.get_or_none(player=player, intel=Intel.construct(npc_place=npc)):
        Message.error("NPC '%s's current location is unknown" % npc)
        return False

    Message.achievement("Talking to '%s'" % npc)
    return True


def exchange(item_holder: NPC, item_to_give: Item, item_to_take: Item):

    player = Player.current()

    # check if player has the item_to_give and holder has the item_to_take
    if item_to_give.belongs_to_player != player:
        Message.debug("item_to_give: '%s', belongs_to_player: '%s'" % (item_to_give, item_to_give.belongs_to_player))
        return False
    if item_to_take.belongs_to != item_holder:
        Message.debug("item_to_take: '%s', belongs_to: '%s', item_holder: '%s'" %
                      (item_to_take, item_to_give.belongs_to, item_holder))
        return False

    # check if player is at item_holder's place_location
    if item_holder.place != player.place:
        Message.debug("Player is not at the item_holder (%s) place_location (%s)" % (item_holder, item_holder.place))
        Message.error("You are not at the item holder (%s) location" % item_holder)
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

    Message.achievement("Item '%s' exchanged for '%s', with NPC '%s'" % (item_to_give, item_to_take, item_holder))
    return True


def explore(area_location: Place, npc: NPC=None, item: Item=None):

    player = Player.current()

    if player.place != area_location:
        Message.error("You are not at the area '%s'" % area_location)
        return False

    if (npc and npc.place != area_location) or (item and item.place != area_location):
        Message.error("What you're looking for, is not here")
        return False

    # check if player knows the location
    results = PlayerKnowledgeBook.select().join(Intel)\
        .where(PlayerKnowledgeBook.player == player, Intel.place_location == area_location).limit(1)
    if not results:
        Message.debug("Location %s unknown (Intel not found in player's knowledge book)" % area_location)
        Message.error("Location %s is unknown" % area_location)
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

    Message.achievement("You have found '%s' by exploring '%s'" % (target, area_location))

    if npc:
        # find npc for player (give npc place intel to player)
        intel = Intel.construct(npc_place=npc)
    elif item:
        intel = Intel.construct(item_place=item)
    else:
        intel = None
    if intel:
        PlayerKnowledgeBook.get_or_create(player=player, intel=intel)
        Message.achievement("Intel '%s' learned" % intel.detail())

    return True


def gather(item_to_gather: Item):

    player = Player.current()

    # check if player is at item location
    if item_to_gather.place != player.place:
        Message.debug("Player is not at the item '%s's location (%s) to gather it" %
                      (item_to_gather, item_to_gather.place))
        Message.error("You are not at the item '%s's location to gather it" % item_to_gather)
        return False

    # update Player's belongings
    item_to_gather.belongs_to_player = player
    item_to_gather.save()

    Message.achievement("Item '%s' gathered" % item_to_gather)
    return True


def give(item: Item, receiver: NPC):

    # check if player has the item
    player = Player.current()
    if item.belongs_to_player != player:
        Message.error("You don't have the item (%s) to give" % item)
        return False

    # check if player is at receiver's location
    if player.place != receiver.place:
        Message.debug("Player is not at the receiver NPC (%s) location (%s)" % (receiver, receiver.place))
        Message.error("You are not at the receiver's (%s) location" % receiver)
        return False

    item.belongs_to_player = None
    item.belongs_to = receiver
    item.save()

    # update favours book
    FavoursBook.construct(npc=receiver, owe_factor=item.worth_(), player=player)

    Message.achievement("Item '%s' has been given to the NPC '%s'" % (item, receiver))
    return True


def spy(spy_on: NPC, intel_target: Intel):

    player = Player.current()

    # check if player is at target's location
    if player.place != spy_on.place:
        Message.debug("Player is not at the NPC (%s) location (%s) to spy" % (spy_on, spy_on.place))
        Message.error("You are not at the NPC '%s's location to spy" % spy_on)
        return False

    # check if the target has the piece of intel
    if not NPCKnowledgeBook.get_or_none(npc=spy_on, intel=intel_target):
        Message.debug("Target (%s) does not have the intel (%s) player wanted" % (spy_on, intel_target))
        Message.error("Target (%s) does not have the intel (%s) player wanted" % (spy_on, intel_target))
        return False

    # update Player's intel
    NarrativeHelper.add_intel(intel_target)

    Message.achievement("Intel '%s' gathered by spying on '%s'" % (intel_target.detail(), spy_on))
    return True


def stealth(target: NPC):

    player = Player.current()

    # check if player at target's place_location
    if player.place != target.place:
        Message.debug("Player is not at the target (%s) place_location (%s)" % (target, target.place))
        Message.error("You are not at the target '%s's location" % target)
        return False

    Message.achievement("Successfully snuck on '%s'" % target)
    return True


def take(item_to_take: Item, item_holder: NPC=None):

    if item_holder is None:
        return take_loot(item_to_take)

    player = Player.current()

    # check if NPC has the item
    if item_to_take.belongs_to != item_holder:
        Message.debug("NPC '%s' doesn't have the item '%s' to give. It belongs to '%s'" %
                      (item_holder, item_to_take, item_to_take.belongs_to))
        Message.error("NPC '%s' doesn't have the item '%s' to give" % (item_holder, item_to_take))
        return False

    # check if player is at item_holder's place_location
    if item_holder.place != player.place:
        Message.debug("Player is not at the item_holder (%s) place_location (%s)" % (item_holder, item_holder.place))
        Message.error("You are not at the NPC '%s's location" % item_holder)
        return False

    # remove item from holder's belongings and add to player's
    item_to_take.belongs_to = None
    item_to_take.belongs_to_player = player
    item_to_take.save()

    FavoursBook.construct(item_holder, -item_to_take.worth_(), player)

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

    Message.achievement("Item '%s' has taken by looting" % item_to_take)
    return True


def read(intel: Intel, readable: Item):

    # check if the readable has the intel
    if not ReadableKnowledgeBook.get_or_none(
            ReadableKnowledgeBook.intel == intel,
            ReadableKnowledgeBook.readable == readable):
        Message.debug("Readable '%s' does not contain the intel '%s', ReadableKnowledgeBook not found" %
                      (readable, intel))
        Message.error("Readable '%s' does not contain the intel player looking for" % readable)
        return False

    player = Player.current()
    # check if player owns the readable
    if readable.belongs_to_player != player:
        Message.debug("Player doesn't have the readable '%s'" % readable)
        if readable.place_() == player.place:
            readable.belongs_to = None
            readable.belongs_to_player = player
            readable.save()
            Message.debug("Player didn't own the readable (%s) but at its place so he take it" % readable)
        else:
            Message.debug("Player neither own the readable (%s), nor at the item's place_location (%s)" %
                          (readable, readable.place_()))
            Message.error("You neither own the readable (%s), nor are at the item's location" % readable)
            return False

    # update Player's intel
    NarrativeHelper.add_intel(intel)

    Message.achievement("By reading '%s', intel '%s' has been learned" % (readable, intel.detail()))
    return True


def goto(destination: Place):

    player = Player.current()

    # check if player knows the location
    results = PlayerKnowledgeBook.select().join(Intel)\
        .where(PlayerKnowledgeBook.player == player, Intel.place_location == destination).limit(1)
    if not results:
        Message.error("Location '%s' is unknown" % destination)
        return False

    # update Player's location
    player.place = destination
    player.save()

    Message.achievement("Player went to '%s'" % destination)
    return True


def kill(target: NPC):

    player = Player.current()

    # check if player is at target place_location
    if player.place != target.place:
        Message.error("You are not at the target '%s's location" % target)
        return False

    NPCDead.create(name=target.name, place=target.place, clan=target.clan)

    Message.achievement("NPC '%s' has been killed" % target)
    target.delete_instance(recursive=True)
    return True


def damage(target: NPC):

    player = Player.current()

    # check if player is at target place_location
    if player.place != target.place:
        Message.error("You are not at the target '%s's location" % target)
        return False

    target.health_meter -= 0.3
    if target.health_meter <= 0:
        return kill(target)
    else:
        Message.debug("NPC '%s' has been damaged, current health meter: %s" % (target, target.health_meter))
        Message.achievement("NPC '%s' has been damaged" % target)
        target.save()

    return True


def listen(intel: Intel, informer: NPC):

    # check if informer has the intel
    if not NPCKnowledgeBook.get_or_none(intel=intel, npc=informer):
        Message.error("Informer doesn't have the intel (%s) player wants" % intel)
        return False

    player = Player.current()

    # check if player is in the informer place_location
    if informer.place != player.place:
        Message.error("You are not at the informer's (%s) location" % informer)
        return False

    # update Player's intel
    NarrativeHelper.add_intel(intel)
    FavoursBook.construct(informer, -intel.worth_(), player)

    Message.achievement("Intel '%s' acquired by listening to '%s'" % (intel.detail(), informer))
    return True


def report(intel: Intel, target: NPC):

    player = Player.current()

    # check if player has the intel
    if not PlayerKnowledgeBook.get_or_none(player=player, intel=intel):
        Message.error("You don't have the intel '%s'" % intel)
        return False

    # check if player is in the target place_location
    if target.place != player.place:
        Message.debug("Player is not at the target (%s) location (%s)" % (target, target.place))
        Message.error("You are not at the target's (%s) location" % target)
        return False

    # update Player's favours book if target hasn't have it already
    if not NPCKnowledgeBook.get_or_none(npc=target, intel=intel):
        FavoursBook.construct(target, intel.worth_())
        # update target's intel list
        NPCKnowledgeBook.create(npc=target, intel=intel)

    Message.achievement("Intel '%s' reported to the NPC '%s'" % (intel.detail(), target))
    return True


def use(item_to_use: Item, target: NPC):

    player = Player.current()
    # check if player has the item
    if item_to_use.belongs_to_player != player:
        Message.error("You don't have the item (%s)" % item_to_use)
        return False

    # check if player at target's place_location
    if target.place != player.place:
        Message.debug("Player is not at the target '%s's location (%s)" % (target, target.place))
        Message.error("You are not at the target '%s's location" % target)
        return False

    # check if item is a tool
    if item_to_use.type != ItemTypes.tool.name:
        Message.debug("Item '%s' is not a tool, not usable, it's a '%s'" % (item_to_use, item_to_use.type))
        Message.error("Item '%s' is not a tool, not usable" % item_to_use)
        return False

    item_to_use.use(npc=target)

    # depending on positive or negative impact_factor of the item usage, target record in player's favour gets updated
    FavoursBook.construct(target, float(item_to_use.impact_factor or 0.0))

    Message.achievement("Item '%s' used on the '%s'" % (item_to_use, target))
    return True
