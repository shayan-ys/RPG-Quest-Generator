from World.Types import fn, JOIN
from World.Types.Person import Player, NPC
from World.Types.Place import Place
from World.Types.Intel import Intel, IntelTypes
from World.Types.Item import Item, ItemTypes, GenericItem
from World.Types.BridgeModels import Need, Exchange, ReadableKnowledgeBook, NPCKnowledgeBook, PlayerKnowledgeBook
from World.Narrative import helper as NarrativeHelper

from Data.statics import World as WorldParams
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

    print("==> Goto '%s'." % place_to_go)

    return steps


def goto_1(destination: Place, npc: NPC=None, item: Item=None):
    """
    You are already there.
    :return:
    """
    if npc or item:
        destination_str = str(npc if npc else item) + ' (' + str(destination) + ')'
    else:
        destination_str = str(destination)
    print('==> Already at your destination,', destination_str)

    # todo: if npc then move npc to player's current location
    # todo: if item then move item to player's current location (or if its not unique, create another one at place)

    # update player's location
    player = Player.current()
    player.place = destination
    player.save()

    # todo: game event add: player moved to location 'name'

    return [[]]


def goto_2(destination: Place, npc: NPC=None, item: Item=None):
    """
    Just wander around and look.
    :return:
    """
    # place_location[1] is destination
    # area around location[1] is given to player to explore and find location[1]

    # steps:
    # T.explore
    steps = [
        [destination, npc, item]
    ]

    if npc or item:
        destination_str = str(npc if npc else item) + ' (' + str(destination) + ')'
    else:
        destination_str = str(destination)
    print("==> Explore around", destination_str)

    return steps


def goto_3(destination: Place, npc: NPC=None, item: Item=None):
    """
    Find out where to go and go there.
    :return:
    """
    # place_location[1] is destination
    # location[1] is place_location[1] exact location

    # results = Intel.select(Intel) \
    #     .where(Intel.type == IntelTypes.location.name, Intel.place_location == destination).limit(1)
    results = Intel.select(Intel)
    if npc:
        results = results.where(Intel.type == IntelTypes.npc_place.name, Intel.npc_place == npc)
    elif item:
        if item.belongs_to:
            results = results.where(Intel.type == IntelTypes.npc_place.name, Intel.npc_place == item.belongs_to)
        else:
            results = results.where(Intel.type == IntelTypes.item_place.name, Intel.item_place == item)
    else:
        results = results.where(Intel.type == IntelTypes.location.name, Intel.place_location == destination)

    if not results:
        if npc:
            intel_location = Intel.construct(npc_place=npc)
        elif item and item.belongs_to:
            intel_location = Intel.construct(npc_place=item.belongs_to)
        elif item:
            intel_location = Intel.construct(item_place=item)
        else:
            intel_location = Intel.construct(place_location=destination)
    else:
        # results query is not None
        results = results.limit(1)
        intel_location = results[0]

    # update player's next location
    player = Player.current()
    player.next_location = destination
    player.save()

    # steps:
    #   learn: location[1]
    #   T.goto: location[1]
    steps = [
        [intel_location],
        [destination]
    ]

    if npc or item:
        destination_str = str(npc if npc else item) + ' (' + str(destination) + ')'
    else:
        destination_str = str(destination)
    print("==> Find out how to get to '", destination_str, "', then goto it.")

    return steps


def learn_1(required_intel: Intel):
    # update player intel
    PlayerKnowledgeBook.get_or_create(player=Player.current(), intel=required_intel)
    if (required_intel.npc_place or required_intel.item_place) and not required_intel.place_location:
        if required_intel.npc_place:
            place = required_intel.npc_place.place
        else:
            place = required_intel.item_place.place
        if not place:
            # todo: error log
            # todo: game event add: intel required not found
            pass
        PlayerKnowledgeBook.get_or_create(player=Player.current(), intel=Intel.construct(place_location=place))

    # todo: game event add: intel(s) added to player's knowledge book

    print("==> Intel '%s' added." % required_intel)
    return [[]]


def learn_2(required_intel: Intel):

    player = Player.current()

    # find NPC who has the intel, goto the NPC and listen to get the intel
    results = NPC.select()\
        .join(NPCKnowledgeBook)\
        .where(NPCKnowledgeBook.intel == required_intel, NPC.health_meter > 0, NPC.clan == player.clan)

    # sort by triangle distance
    locations_scores = [player.distance(row.place) for row in results]
    results = sort_by_list(results, locations_scores)

    if results:
        knowledgeable_npc = results[0]
    else:
        # NPC pool to add required intel to one of them
        results = NPC.select().where(NPC.health_meter > 0, NPC.clan == player.clan)
        if not results:
            # No NPC in clan found search among all NPCs
            results = NPC.select().where(NPC.health_meter > 0)

        if required_intel.npc_place:
            # exclude the same NPC looking for
            results = results.where(NPC.id != required_intel.npc_place)

        if not results:
            # No NPC left in the world
            return []

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

    print("==> Do a sub-quest, goto '%s (%s)', listen intel '%s' from '%s'." %
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
        known_places = Place.select()\
            .join(Intel, on=(Intel.place_location == Place.id))\
            .join(PlayerKnowledgeBook, on=(PlayerKnowledgeBook.intel == Intel.id))\
            .where(PlayerKnowledgeBook.player == player)
        if known_places:
            known_place = known_places.order_by(fn.Random()).get()
        else:
            known_place = NarrativeHelper.create_place(known_to_player=True)

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
    print("==> Goto", book_containing_intel, "(", book_containing_intel.place_(), "), get '", book_containing_intel, "', and read the intel '",
          required_intel, "' from it.")

    return steps


def learn_4(required_intel: Intel):
    # find an NPC who has the required intel in exchange, get the NPC's needed item to give

    results = NPC.select(NPC, Need.item_id.alias('needed_item_id')) \
        .join(Need) \
        .join(Exchange) \
        .where(Exchange.intel == required_intel, Need.item_id.is_null(False)).objects()

    player = Player.current()

    # triangle distance sort
    locations_scores = [player.distance(npc.place) for npc in results]
    results = sort_by_list(results, locations_scores)

    informer = results[0]
    item_to_exchange = Item.get_by_id(informer.needed_item_id)
    del informer.needed_item_id

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

    print("==> Get '", item_to_exchange, "', perform sub-quest, give the acquired item to '", informer,
          "' in return get an intel on '", required_intel, "'")

    return steps


def get_1(item_to_fetch: Item):
    print("==> You already have the item.")

    # if not, add it to player's belongings
    item_to_fetch.belongs_to_player = Player.current()
    item_to_fetch.save()

    # todo: game event add: player acquired the item

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

    # check for singleton and common items, if it's common, select query should be executed, sort by distance
    if item_to_fetch.is_singleton():
        item_holder = item_to_fetch.belongs_to
    else:
        results = NPC.select().join(Item, on=(Item.belongs_to.id == NPC.id))\
            .where(Item.generic == item_to_fetch.generic)
        # enemies are preferred
        results_enemy = results.where(NPC.clan != Player.current().clan)
        if results_enemy:
            results = results_enemy
        # sort by triangle distance
        player = Player.current()
        locations_scores = [player.distance(npc.place) for npc in results]
        results = sort_by_list(results, locations_scores)

        item_holder = results[0]

    # steps:
    #   steal: steal item[1] from NPC[1]
    steps = [
        [item_to_fetch, item_holder]
    ]
    print("==> Steal '", item_to_fetch, "' from '", item_holder, "'.")

    return steps


def get_3(item_to_fetch: Item):

    player = Player.current()

    holder = None
    if item_to_fetch.place:
        dest = item_to_fetch.place
    elif item_to_fetch.belongs_to:
        holder = item_to_fetch.belongs_to  # type: NPC
        dest = holder.place
    elif item_to_fetch.belongs_to_player == player:
        # player already has the item, take it away
        # todo: game event add: someone has stolen the item from the player
        # todo: give item to an NPC
        holder = item_to_fetch.belongs_to  # type: NPC
        dest = holder.place

    else:
        # no one has the item
        # todo: put item in a place
        dest = item_to_fetch.place
    # steps:
    # goto
    # gather
    steps = [
        [dest, holder],
        [item_to_fetch]
    ]
    print("==> Goto '%s' and gather '%s'." % (dest, item_to_fetch))

    return steps


def get_4(item_to_fetch: Item):
    """
    an NPC have the item, but you need to give the NPC something for an exchange
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
        # todo: This is useless now, since being sorted again later,
        #  but when sort by triangle distance added to database, this ordering will be changed again.
        exchanges = exchanges.order_by(Exchange.need.item.worth.asc())

        locations_scores = [player.distance(exc.need.npc.place) for exc in exchanges]
        exchanges = sort_by_list(exchanges, locations_scores)

        exchange = exchanges[0]
        item_to_give = exchange.need.item
        item_holder = exchange.need.npc
    else:
        # no one wants to offer the "item_to_fetch" in exchange for something else
        # you can even trade with your enemies so alliance doesn't really matters here
        # first try find someone who needs this item
        needs = Need.select().where(Need.item == item_to_fetch).group_by(Need.npc)
        if needs.count():
            need = needs.get()
            item_holder = need.npc
        else:
            # no one need anything create a need for coin for an NPC
            results = NPC.select()
            locations_scores = [player.distance(npc.place) for npc in results]
            results = sort_by_list(results, locations_scores)
            item_holder = results[0]
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
        print("==> Do a sub-quest, goto '%s' to meet '%s' and exchange '%s' with '%s'" %
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
    print("==> Goto '%s', get '%s', do a sub-quest, goto '%s' to meet '%s' and exchange '%s' with '%s'" %
          (item_to_give.place_(), item_to_give, item_holder.place, item_holder, item_to_give, item_to_fetch))

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
    print("==> Goto '", item_holder_place, "', sneak up on '", item_holder, "', and take '", item_to_steal, "'.")

    return steps


def steal_2(item_to_steal: Item, item_holder: NPC):

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
        [item_to_steal, item_holder]
    ]

    print("==> Goto and kill '%s', then take '%s'." % (item_holder, item_to_steal))

    return steps


def spy_1(spy_on: NPC, intel_needed: Intel, receiver: NPC):

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

    print("==> Goto '%s' (%s), spy on '%s' to get intel '%s', goto '%s' (%s), report the intel to '%s'." %
          (spy_on, spy_on.place, spy_on, intel_needed, receiver, receiver.place, receiver))

    return steps


def kill_1(target: NPC):

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

    print("==> Goto '%s' and kill '%s'." % (target.place, target))

    return steps
