from World.Types import fn, JOIN
from World.Types.Person import Player, NPC, Clan
from World.Types.Place import Place
from World.Types.Intel import Intel, IntelTypes
from World.Types.Item import Item, ItemTypes, GenericItem
from World.Types.BridgeModels import Need, Exchange, ReadableKnowledgeBook, NPCKnowledgeBook, PlayerKnowledgeBook
from World.Types.Log import Message
from World.Narrative import helper as narrative_helper

from Data.statics import World as WorldParams
from Grammar.actions import Terminals as T
from helper import sort_by_list
from random import randint


def sub_quest_1(suggested_destination: Place=None):
    # just go somewhere - pick a place_location unknown to player to go to
    # the reason for unknown place_location is, if "learn" comes up in next level, we'll be lucky,
    # if it doesn't, intel can be added to Players knowledge right away.
    player = Player.current()

    if suggested_destination:
        place_to_go = suggested_destination
    else:
        results = Place.select()\
            .join(Intel)\
            .join(PlayerKnowledgeBook, JOIN.LEFT_OUTER)\
            .group_by(Intel).having(fn.COUNT(PlayerKnowledgeBook.id) == 0)

        locations_scores = [player.distance(place) for place in results]
        results = sort_by_list(results, locations_scores)

        if results:
            place_to_go = results[0]
        else:
            # not enough places to go, then create a new place unknown to player
            new_x = randint(WorldParams.minimum_distance, WorldParams.reachable_distance)
            new_y = randint(WorldParams.minimum_distance, WorldParams.reachable_distance)
            place_to_go = Place.create(name='arbitrary_' + str(randint(100, 999)), x=new_x, y=new_y)

    player.next_location = place_to_go
    player.save()

    # steps:
    # goto
    steps = [
        [place_to_go]
    ]

    # print("==> Goto '%s'." % place_to_go)
    Message.instruction("Goto '%s'." % place_to_go)

    return steps


def goto_1(destination: Place, npc: NPC=None, item: Item=None):
    """
    You are already there.
    :return:
    """
    if npc or item:
        event_dest_str = str(npc if npc else item) + ' (' + str(destination) + ')'
    else:
        event_dest_str = str(destination)
    # print('==> Already at your destination,', event_dest_str)
    Message.instruction("Already at your destination %s" % event_dest_str)

    player = Player.current()

    if npc:
        # move the npc
        npc.place = player.place
        npc.save()
        intel = Intel.construct(npc_place=npc)
        PlayerKnowledgeBook.get_or_create(player=player, intel=intel)
        Message.debug("NPC (%s) moved to the player location (%s)" % (npc, player.place))
    elif item:
        # move item or the holder
        if item.belongs_to:
            holder = item.belongs_to  # type: NPC
            holder.place = player.place
            holder.save()
            intel = Intel.construct(npc_place=holder)
            PlayerKnowledgeBook.get_or_create(player=player, intel=intel)
            Message.debug("Item (%s) holder (%s) moved to the player location (%s)" % (item, item.belongs_to,
                                                                                       player.place))
        elif item.belongs_to_player:
            Message.debug("Player already has the item" % item)
        else:
            item.place = player.place
            item.save()
            intel = Intel.construct(item_place=item)
            PlayerKnowledgeBook.get_or_create(player=player, intel=intel)
            Message.debug("Item (%s) moved to the player location (%s)" % (item, player.place))
    else:
        # update player's location
        player.place = destination
        player.save()
        Message.debug("Player moved to %s location" % event_dest_str)

    return [[]]


def goto_2(destination: Place, npc: NPC=None, item: Item=None):
    """
    Explore destination to find npc or item
    :return:
    """
    # place_location[1] is destination
    # area around location[1] is given to player to explore and find location[1]
    player = Player.current()

    # ensure player doesn't already know where the NPC or item is
    if npc:
        intel = Intel.construct(npc_place=npc)
        if PlayerKnowledgeBook.get_or_none(player=player, intel=intel):
            npc.place = Place.select().where(Place.id != destination).order_by(fn.Random()).get()
            npc.save()
            destination = npc.place
        event_target_str = npc
    elif item:
        intel = Intel.construct(item_place=item)
        if PlayerKnowledgeBook.get_or_none(player=player, intel=intel):
            if item.belongs_to:
                holder = item.belongs_to
                holder.place = Place.select().where(Place.id != destination).order_by(fn.Random()).get()
                holder.save()
                destination = holder.place
            else:
                item.place = Place.select().where(Place.id != destination).order_by(fn.Random()).get()
                item.save()
                destination = item.place
        event_target_str = item
    else:
        event_target_str = ''

    # steps:
    # T.explore
    steps = [
        [destination, npc, item]
    ]

    # if event_target_str:
        # print("==> Explore around", destination, "to find", event_target_str)
    # else:
        # print("==> Explore around", str(event_target_str) + ' (' + str(destination) + ')', "to find", event_target_str)

    Message.instruction("Explore around '%s' to find '%s'" % (destination, event_target_str))

    return steps


def goto_3(destination: Place, npc: NPC=None, item: Item=None):
    """
    Find out where to go and go there.
    :return:
    """
    # place_location[1] is destination
    # location[1] is place_location[1] exact location
    player = Player.current()

    # find correct type of Intel from npc_place, item_place and place_location
    if npc:
        intel = Intel.get_or_none(type=IntelTypes.npc_place.name, npc_place=npc)
        if PlayerKnowledgeBook.get_or_none(player=player, intel=intel):
            # player already knows, move the npc
            destination = Place.select().where(Place.id != npc.place).order_by(fn.Random())
            if destination:
                destination = destination.get()
            else:
                destination = narrative_helper.create_place()
            npc.place = destination
            npc.save()
            # by moving NPC place, npc_place intel removes from player knowledge book automatically
            Message.event("NPC %s has moved to somewhere else" % npc)
    elif item:
        if item.belongs_to:
            intel = Intel.get_or_none(type=IntelTypes.npc_place.name, npc_place=item.belongs_to)
            if PlayerKnowledgeBook.get_or_none(player=player, intel=intel):
                # player already knows where the item holder is, move the npc
                holder = item.belongs_to
                destination = Place.select().where(Place.id != holder.place).order_by(fn.Random())
                if destination:
                    destination = destination.get()
                else:
                    destination = narrative_helper.create_place()
                holder.place = destination
                holder.save()
                Message.event("Item holder (%s) is moved somewhere else (item: %s)" % (item.belongs_to, item))
        else:
            intel = Intel.get_or_none(type=IntelTypes.item_place.name, item_place=item)
            if PlayerKnowledgeBook.get_or_none(player=player, intel=intel):
                # player already knows where the item is located at, move the item
                destination = Place.select().where(Place.id != item.place).order_by(fn.Random())
                if destination:
                    destination = destination.get()
                else:
                    destination = narrative_helper.create_place()
                item.place = destination
                item.save()
                Message.event("Item (%s) has been misplaced" % item)
    else:
        intel = Intel.get_or_none(type=IntelTypes.location.name, place_location=destination)
        if PlayerKnowledgeBook.get_or_none(player=player, intel=intel):
            # player already knows where the place is exactly,
            # so create a new place at the same location with a different name, now player doesn't know!
            destination = Place.create(name='arbitrary_' + str(randint(100, 999)), x=destination.x, y=destination.y)
            intel = Intel.construct(place_location=destination)

    if not intel:
        # create the correct type of intel based on what is being asked
        if npc:
            intel = Intel.construct(npc_place=npc)
        elif item and item.belongs_to:
            intel = Intel.construct(npc_place=item.belongs_to)
        elif item:
            intel = Intel.construct(item_place=item)
        else:
            intel = Intel.construct(place_location=destination)

    # update player's next location
    player.next_location = destination
    player.save()

    # steps:
    #   learn: location[1]
    #   T.goto: location[1]
    steps = [
        [intel],
        [destination]
    ]

    if npc or item:
        destination_str = str(npc if npc else item) + ' (' + str(destination) + ')'
    else:
        destination_str = str(destination)
    # print("==> Find out how to get to '", destination_str, "', then goto it.")
    Message.instruction("Find out how to get to '%s', then go to it" % destination_str)

    return steps


def learn_1(required_intel: Intel):
    """
    You already know it.
    :param required_intel:
    :return:
    """
    player = Player.current()
    # update player intel
    PlayerKnowledgeBook.get_or_create(player=player, intel=required_intel)

    if (required_intel.npc_place or required_intel.item_place) and not required_intel.place_location:
        # if player knows an NPC's place but doesn't know the location of that place, add the location too
        if required_intel.npc_place:
            place = required_intel.npc_place.place
        else:
            place = required_intel.item_place.place
        if not place:
            Message.debug("Error! npc_place or item_place are empty")

        PlayerKnowledgeBook.get_or_create(player=player, intel=Intel.construct(place_location=place))

    # print("==> Intel '%s' added." % required_intel)
    Message.event("Intel '%s' discovered" % required_intel)
    return [[]]


def learn_2(required_intel: Intel):
    """
    Go someplace, perform subquest, get info from NPC.
    :param required_intel:
    :return:
    """

    player = Player.current()

    # find NPC who has the intel, goto the NPC and listen to get the intel
    results = NPC.select()\
        .join(NPCKnowledgeBook)\
        .where(NPCKnowledgeBook.intel == required_intel, NPC.clan == player.clan)

    # sort by triangle distance
    locations_scores = [player.distance(row.place) for row in results]
    results = sort_by_list(results, locations_scores)

    if results:
        knowledgeable_npc = results[0]
    else:
        # NPC pool to add required intel to one of them
        results = NPC.select().where(NPC.clan == player.clan)
        if not results:
            # No NPC in clan found search among all NPCs
            Message.debug("No NPC in clan %s found, search among all NPCs" % NPC.clan)
            results = NPC.select().order_by(fn.Random()).get()
            if required_intel.npc_place:
                # exclude the same NPC looking for
                results = results.where(NPC.id != required_intel.npc_place)
        elif required_intel.item_place and required_intel.item_place.belongs_to:
            # exclude the owner of the item to ask where is the item!
            results = results.where(NPC.id != required_intel.item_place.belongs_to)

        if not results:
            # No NPC left in the world
            knowledgeable_npc = NPC.create(place=Place.select().order_by(fn.Random()).get(),
                                           clan=Clan.select().order_by(fn.Random()).get(),
                                           name='arbitrary_npc_' + str(randint(100, 999)))
            Message.debug("No NPC left in the world, new one %s created for learn_2" % knowledgeable_npc)
        else:
            locations_scores = [player.distance(row.place) for row in results]
            results = sort_by_list(results, locations_scores)
            knowledgeable_npc = results[0]

        NPCKnowledgeBook.create(npc=knowledgeable_npc, intel=required_intel)

    player.next_location = knowledgeable_npc.place
    player.save()

    # steps:
    # do sub-quest
    # goto knowledgeable_npc place_location
    # listen knowledgeable_npc to get required_intel
    steps = [
        [],
        [knowledgeable_npc.place, knowledgeable_npc],
        [required_intel, knowledgeable_npc]
    ]

    # print("==> Do a sub-quest, goto '%s (%s)', listen intel '%s' from '%s'." %
    #       (knowledgeable_npc, knowledgeable_npc.place, required_intel, knowledgeable_npc))
    Message.instruction("==> Do a sub-quest, goto '%s (%s)', listen intel '%s' from '%s'." %
                        (knowledgeable_npc, knowledgeable_npc.place, required_intel, knowledgeable_npc))

    return steps


def learn_3(required_intel: Intel):
    """
    Go someplace, get something, and read what is written on it.
    :param required_intel:
    :return:
    """

    player = Player.current()
    # intel[1] is to be learned

    # find a book[1] (readable, it could be a sign) that has intel[1] on it
    results = ReadableKnowledgeBook.select()\
        .join(Item, on=(ReadableKnowledgeBook.readable == Item.id))\
        .where(ReadableKnowledgeBook.intel == required_intel,
               Item.belongs_to_player != player)

    # sort by readable place_ triangle
    locations_scores = [player.distance(knowledge_book.readable.place_()) for knowledge_book in results]
    results = sort_by_list(results, locations_scores)

    if results:
        book_containing_intel = results[0].readable  # type: Item
    else:
        # create an address book containing the intel player is looking for
        known_places = Place.select()\
            .join(Intel, on=(Intel.place_location == Place.id))\
            .join(PlayerKnowledgeBook, on=(PlayerKnowledgeBook.intel == Intel.id))\
            .where(PlayerKnowledgeBook.player == player)
        if known_places:
            known_place = known_places.order_by(fn.Random()).get()
        else:
            known_place = narrative_helper.create_place(known_to_player=True)

        book_containing_intel = Item.create(type=ItemTypes.readable.name,
                                            generic=GenericItem.get_or_create(name=ItemTypes.singleton.name)[0],
                                            name='address_book_' + str(randint(100, 999)), place=known_place)
        ReadableKnowledgeBook.create(readable=book_containing_intel, intel=required_intel)
        PlayerKnowledgeBook.create(player=player, intel=Intel.construct(item_place=book_containing_intel))

    player.next_location = book_containing_intel.place_()
    player.save()

    # steps:
    # goto: place_location[1]
    # get: book[1]
    # T.read: intel[1] from book[1]
    steps = [
        [book_containing_intel.place_(), None, book_containing_intel],
        [book_containing_intel],
        [required_intel, book_containing_intel]
    ]
    # print("==> Goto", book_containing_intel, "(", book_containing_intel.place_(), "), get '",
    #       book_containing_intel, "', and read the intel '", required_intel, "' from it.")
    Message.instruction("Goto %s (%s), get '%s', and read the intel '%s' from it" %
                        (book_containing_intel, book_containing_intel.place_(), book_containing_intel, required_intel))

    return steps


def learn_4(required_intel: Intel):
    # find an NPC who has the required intel in exchange, get the NPC's needed item to give

    results = NPC.select(NPC, Need.item_id.alias('needed_item_id')) \
        .join(Need) \
        .join(Exchange) \
        .where(Exchange.intel == required_intel, Need.item_id.is_null(False)).objects()

    player = Player.current()

    if results:
        # triangle distance sort
        locations_scores = [player.distance(npc.place) for npc in results]
        results = sort_by_list(results, locations_scores)

        informer = results[0]
        item_to_exchange = Item.get_by_id(informer.needed_item_id)
        del informer.needed_item_id
    else:
        # find NPC with a need
        results = NPC.select(NPC, Need.id.alias('need_id')) \
            .join(Need) \
            .where(Need.item_id.is_null(False)).objects()

        if results:
            # NPC found with a need
            # triangle distance sort
            locations_scores = [player.distance(npc.place) for npc in results]
            results = sort_by_list(results, locations_scores)
            informer = results[0]

            need = Need.get_by_id(informer.need_id)
            item_to_exchange = need.item

        else:
            # No NPC need anything so create a need
            results = NPC.select().order_by(fn.Random()).get()
            # triangle distance sort
            locations_scores = [player.distance(npc.place) for npc in results]
            results = sort_by_list(results, locations_scores)
            informer = results[0]

            item_to_exchange = Item.select().order_by(fn.Random()).get()
            need = Need.create(item=item_to_exchange, npc=informer)
            Message.debug("No NPC, need anything. So a need is created (%s)" % need)

        Exchange.create(intel=required_intel, need=need)

    player.next_location = informer.place
    player.save()

    # steps:
    # get
    # sub-quest
    # give
    # listen
    steps = [
        [item_to_exchange],
        [informer.place],
        [item_to_exchange, informer],
        [required_intel, informer]
    ]

    # print("==> Get '", item_to_exchange, "', perform sub-quest, give the acquired item to '", informer,
    #       "' in return get an intel on '", required_intel, "'")
    Message.instruction("Get '%s', perform sub-quest, give the acquired item to '%s' in return get an intel on '%s'" %
                        (item_to_exchange, informer, required_intel))
    return steps


def get_1(item_to_fetch: Item):
    # print("==> You already have the item.")

    # if not, add it to player's belongings
    item_to_fetch.belongs_to_player = Player.current()
    item_to_fetch.save()

    Message.event("Player got the item '%s'" % item_to_fetch)

    return []


def get_2(item_to_fetch: Item):
    """
    Steal it from somebody.
    :return:
    """
    # item[1] is to be fetched

    # find an NPC[1] who
    #   has the item,
    #   preferably is an enemy
    #   not too far from Player's current location
    player = Player.current()

    # check for singleton and common items, if it's common, select query should be executed, sort by distance
    if item_to_fetch.is_singleton():
        item_holder = item_to_fetch.belongs_to
    else:
        results = NPC.select(NPC, Item.id.alias('item_to_fetch_id')).join(Item, on=(Item.belongs_to.id == NPC.id))\
            .where(Item.generic == item_to_fetch.generic)
        # enemies are preferred
        results_enemy = results.where(NPC.clan != player.clan)
        if results_enemy:
            results = results_enemy

        if results:
            results = results.group_by(NPC).objects()

            # sort by triangle distance
            player = Player.current()
            locations_scores = [player.distance(npc.place) for npc in results]
            results = sort_by_list(results, locations_scores)

            item_holder = results[0]
            item_to_fetch = Item.get_by_id(item_holder.item_to_fetch_id)
        else:
            # No NPC found that have the item
            # Select a close NPC and assign one instance of the item to him
            results = NPC.select().where(NPC.clan != player)
            if not results:
                results = NPC.select().order_by(fn.Random()).get()
                # sort by triangle distance
            player = Player.current()
            locations_scores = [player.distance(npc.place) for npc in results]
            results = sort_by_list(results, locations_scores)

            item_holder = results[0]
            item_to_fetch = Item.create(name=item_to_fetch + '_' + str(randint(100, 999)),
                                        generic=item_to_fetch.generic, belongs_to=item_holder,
                                        type=item_to_fetch.type, usage=item_to_fetch.usage,
                                        impact_factor=item_to_fetch.impact_factor, worth=item_to_fetch.worth)
            Message.debug("No NPC found that have the item, "
                          "select a close NPC '%s' and assign a new instance of the item '%s' to it" %
                          (item_holder, item_to_fetch))

    # steps:
    #   steal: steal item[1] from NPC[1]
    steps = [
        [item_to_fetch, item_holder]
    ]
    # print("==> Steal '", item_to_fetch, "' from '", item_holder, "'.")
    Message.instruction("Steal '%s' from '%s'" % (item_to_fetch, item_holder))

    return steps


def get_3(item_to_fetch: Item):
    """
    Go someplace and pick something up that’s lying around there
    :param item_to_fetch:
    :return:
    """

    if item_to_fetch.place:
        dest = item_to_fetch.place
    elif item_to_fetch.belongs_to:
        # someone took it and put it in a specific place, put it where the NPC is
        Message.event("Someone has stolen the item '%s' and put it somewhere else!" % item_to_fetch)
        dest = item_to_fetch.belongs_to.place
        item_to_fetch.belongs_to = None
        item_to_fetch.place = dest
        item_to_fetch.save()
    else:
        # player already has the item or no one has it, put it in a random place
        Message.event("Someone has stolen the item '%s' and put it in a random place!" % item_to_fetch)
        dest = Place.select().order_by(fn.Random()).get()
        item_to_fetch.place = dest
        item_to_fetch.save()
    # steps:
    # goto
    # gather
    steps = [
        [dest, None, item_to_fetch],
        [item_to_fetch]
    ]
    # print("==> Goto '%s' and gather '%s'." % (dest, item_to_fetch))
    Message.instruction("Goto '%s' and gather '%s'." % (dest, item_to_fetch))

    return steps


def get_4(item_to_fetch: Item):
    """
    an NPC have the item, but you need to give the NPC something in an exchange
    :param item_to_fetch:
    :return:
    """
    player = Player.current()

    # find an NPC who has the needed item, and has it in exchange list
    exchanges = Exchange.select().join(Item)
    if item_to_fetch.is_singleton():
        exchanges = exchanges.where(Exchange.item == item_to_fetch)
    else:
        exchanges = exchanges.where(Exchange.item.generic == item_to_fetch.generic)

    if exchanges:

        locations_scores = [player.distance(exc.need.npc.place) for exc in exchanges]
        exchanges = sort_by_list(exchanges, locations_scores)

        exchange = exchanges[0]
        item_to_give = exchange.need.item
        item_holder = exchange.need.npc
    else:
        # no one wants to offer the "item_to_fetch" in exchange for something else
        # you can even trade with your enemies so alliance doesn't really matters here
        # first try find someone who needs this item
        Message.debug("No one wants to offer the '%s' in exchange for something else" % item_to_fetch)
        needs = Need.select().where(Need.item == item_to_fetch).group_by(Need.npc)
        if needs.count():
            need = needs.order_by(fn.Random()).get()
            item_holder = need.npc
            Message.debug("NPC '%s' needs something, ideal to create an exchange motive with the item '%s' for him" %
                          (item_holder, item_to_fetch))
        else:
            # no one need anything create a need for coin for an NPC
            results = NPC.select()
            locations_scores = [player.distance(npc.place) for npc in results]
            results = sort_by_list(results, locations_scores)
            item_holder = results[0]
            Message.debug("No one need anything create a need for 'coin' for a close-by NPC '%s'" % item_holder)

            need = Need.create(npc=item_holder, item=Item.get(generic=GenericItem.get(name='coin')))

        Exchange.create(need=need, item=item_to_fetch)

        if item_to_fetch.belongs_to != item_holder:
            # ensure NPC has the item
            item_to_fetch.belongs_to = item_holder
            item_to_fetch.save()

        item_to_give = need.item

    player.next_location = item_holder.place
    player.save()

    # check for player belonging for the exchange item
    if item_to_give.is_singleton():
        player_owns = (item_to_give.belongs_to_player == player)
    else:
        player_owns = Item.select().where(Item.generic == item_to_give.generic,
                                          Item.belongs_to_player == player) is True

    if player_owns:
        # player has the item
        # goto
        # exchange
        steps = [
            [],
            [],
            [],
            [item_holder.place, item_holder],
            [item_holder, item_to_give, item_to_fetch]
        ]
        # print("==> Do a sub-quest, goto '%s' to meet '%s' and exchange '%s' with '%s'" %
        #       (item_holder.place, item_holder, item_to_give, item_to_fetch))
        Message.instruction("Do a sub-quest, goto '%s' to meet '%s' and exchange '%s' with '%s'" %
                            (item_holder.place, item_holder, item_to_give, item_to_fetch))
        return steps

    # steps:
    # goto
    # get
    # sub-quest
    # goto
    # exchange
    steps = [
        [item_to_give.place_(), None, item_to_give],
        [item_to_give],
        [],
        [item_holder.place, item_holder],
        [item_holder, item_to_give, item_to_fetch]
    ]
    # print("==> Goto '%s', get '%s', do a sub-quest, goto '%s' to meet '%s' and exchange '%s' with '%s'" %
    #       (item_to_give.place_(), item_to_give, item_holder.place, item_holder, item_to_give, item_to_fetch))
    Message.instruction("==> Goto '%s', get '%s', do a sub-quest, goto '%s' to meet '%s' and exchange '%s' with '%s'" %
                        (item_to_give.place_(), item_to_give, item_holder.place, item_holder, item_to_give,
                         item_to_fetch))
    return steps


def steal_1(item_to_steal: Item, item_holder: NPC):
    """
    Go someplace, sneak up on somebody, and take something.
    :return:
    """
    # item[1] is to be stolen from NPC[1] who has it

    # place_location[1] is where NPC[1] lives
    item_holder_place = item_holder.place

    player = Player.current()
    player.next_location = item_holder_place
    player.save()

    # steps:
    #   goto: place_location[1]
    #   T.stealth: stealth NPC[1]
    #   T.take: take item[1] from NPC[1]
    steps = [
        [item_holder_place, item_holder],
        [item_holder],
        [item_to_steal, item_holder]
    ]
    # print("==> Goto '", item_holder_place, "', sneak up on '", item_holder, "', and take '", item_to_steal, "'.")
    Message.instruction("Goto '%s', sneak up on '%s', and take '%s'" % (item_holder_place, item_holder, item_to_steal))

    return steps


def steal_2(item_to_steal: Item, item_holder: NPC):
    """
    Go someplace, kill somebody and take something
    :param item_to_steal:
    :param item_holder:
    :return:
    """
    player = Player.current()
    player.next_location = item_holder.place
    player.save()

    # steps:
    # goto holder
    # kill holder
    # T.take item from holder
    steps = [
        [item_holder.place, item_holder],
        [item_holder],
        [item_to_steal]
    ]

    # print("==> Goto and kill '%s', then take '%s'." % (item_holder, item_to_steal))
    Message.instruction("Goto and kill '%s', then take '%s'." % (item_holder, item_to_steal))

    return steps


def spy_1(spy_on: NPC, intel_needed: Intel, receiver: NPC):
    """
    Go someplace, spy on somebody, return and report
    :param spy_on:
    :param intel_needed:
    :param receiver:
    :return:
    """
    player = Player.current()
    player.next_location = spy_on.place
    player.save()

    # steps:
    # goto spy_on place_location
    # spy on 'spy_on' get the intel_needed
    # goto receiver place_location
    # report intel_needed to receiver
    steps = [
        [spy_on.place, spy_on],
        [spy_on, intel_needed],
        [receiver.place, receiver],
        [intel_needed, receiver]
    ]

    # print("==> Goto '%s' (%s), spy on '%s' to get intel '%s', goto '%s' (%s), report the intel to '%s'." %
    #       (spy_on, spy_on.place, spy_on, intel_needed, receiver, receiver.place, receiver))
    Message.instruction("==> Goto '%s' (%s), spy on '%s' to get intel '%s', goto '%s' (%s), report the intel to '%s'." %
                        (spy_on, spy_on.place, spy_on, intel_needed, receiver, receiver.place, receiver))

    return steps


def capture_1(target: NPC):
    """
    Get something, go someplace and use it to capture somebody
    :param target:
    :return:
    """
    item_to_fetch = Item.get_or_none(type=ItemTypes.tool.name, usage=T.capture.value)
    if not item_to_fetch:
        # No item usable for capture, left in the world
        item_to_fetch = Item.create(
            name='arbitrary_capture_tool_' + str(randint(100, 999)),
            type=ItemTypes.tool.name,
            usage=T.capture.value,
            generic=GenericItem.get_or_create(name=ItemTypes.singleton.name)[0],
            place=Place.select().order_by(fn.Random()).get(),
            impact_factor=1.0,
            worth=0.75
        )
        Message.debug("No item usable for 'capture' left in the world, create a new one '%s'" % item_to_fetch)

    # steps:
    # get
    # goto
    # T.capture
    steps = [
        [item_to_fetch],
        [target.place, target],
        [target]
    ]
    # print("==> Get '%s', then goto '%s' (%s) and capture '%s'" % (item_to_fetch, target, target.place, target))
    Message.instruction("==> Get '%s', then goto '%s' (%s) and capture '%s'" %
                        (item_to_fetch, target, target.place, target))
    return steps


def kill_1(target: NPC):
    """
    Go someplace and kill somebody.
    :param target:
    :return:
    """
    player = Player.current()
    player.next_location = target.place
    player.save()

    # steps:
    # goto target
    # kill target
    steps = [
        [target.place, target],
        [target]
    ]

    # print("==> Goto '%s' and kill '%s'." % (target.place, target))
    Message.instruction("Goto '%s' and kill '%s'." % (target.place, target))

    return steps
