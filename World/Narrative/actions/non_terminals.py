from World.Types import fn, JOIN
from World.Types.Person import Player, NPC
from World.Types.Place import Place
from World.Types.Intel import Intel, IntelTypes
from World.Types.Item import Item, ItemTypes, GenericItem
from World.Types.BridgeModels import Need, Exchange, ReadableKnowledgeBook, NPCKnowledgeBook, PlayerKnowledgeBook

from helper import sort_by_list


def sub_quest_1():
    # just go somewhere - pick a place unknown to player to go to
    # the reason for unknown place is, if "learn" comes up in next level, we'll be lucky,
    # if it doesn't, intel can be added to Players knowledge right away.
    results = Place.select()\
        .join(Intel)\
        .join(PlayerKnowledgeBook, JOIN.LEFT_OUTER)\
        .group_by(Intel).having(fn.COUNT(PlayerKnowledgeBook.id) == 0)

    locations = list(results)
    results = sort_by_list(results, locations)

    place_to_go = results[0]
    player = Player.get()
    player.next_location = place_to_go
    player.save()

    # steps:
    # goto
    steps = [
        [place_to_go]
    ]

    print("==> Goto '%s'." % place_to_go)

    return steps


def goto_1(destination: Place):
    """
    You are already there.
    :return:
    """
    print('==> Already at your destination, %s.' % destination)

    # update player's location
    player = Player.get()
    player.place = destination
    player.save()

    return destination, [[]]


def goto_2(destination: Place):
    """
    Just wander around and look.
    :return:
    """
    # place[1] is destination
    # area around location[1] is given to player to explore and find location[1]

    # steps:
    # T.explore
    steps = [
        [destination]
    ]
    print("==> Explore around '", destination, "'.")

    return steps


def goto_3(destination: Place):
    """
    Find out where to go and go there.
    :return:
    """
    # place[1] is destination
    # location[1] is place[1] exact location
    results = Intel.select(Intel)\
        .where(Intel.type == IntelTypes.place.name, Intel.place == destination).limit(1)

    if not results:
        return []

    intel_location = results[0]

    # update player's next location
    player = Player.select().limit(1)[0]
    player.next_location = destination
    player.save()

    # steps:
    #   learn: location[1]
    #   T.goto: location[1]
    steps = [
        [intel_location],
        [destination]
    ]
    print("==> Find out how to get to '", destination, "', then goto it.")

    return steps


def learn_1(required_intel: Intel):
    # update player intel
    PlayerKnowledgeBook.get_or_create(player=Player.get(), intel=required_intel)

    print("==> Intel '%s' added." % required_intel)
    return [[]]


def learn_2(required_intel: Intel):
    # find NPC who has the intel, goto the NPC and listen to get the intel
    player = Player.get()
    results = NPC.select()\
        .join(NPCKnowledgeBook)\
        .where(NPCKnowledgeBook.intel == required_intel)

    results_ally = results.where(NPC.clan == player.clan)
    if results_ally:
        # if there is any ally, just pick them, if not then only enemies has the intel, no need to filter
        results = results_ally

    # sort by triangle distance
    result_distances = [player.distance(row.place) for row in results]
    results = sort_by_list(results, result_distances)

    knowledgeable_npc = results[0]

    player.next_location = knowledgeable_npc.place
    player.save()
    # steps:
    # do sub-quest
    # goto knowledgeable_npc place
    # listen knowledgeable_npc to get required_intel
    steps = [
        [],
        [knowledgeable_npc.place],
        [required_intel, knowledgeable_npc]
    ]

    print("==> Do a sub-quest, goto '%s', listen intel '%s' from '%s'." %
          (knowledgeable_npc.place, required_intel, knowledgeable_npc))

    return steps


def learn_3(required_intel: Intel):
    """
    Go someplace, get something, and read what is written on it.
    :param required_intel:
    :return:
    """

    # intel[1] is to be learned

    # find a book[1] (readable, it could be a sign) that has intel[1] on it
    results = ReadableKnowledgeBook.select().where(ReadableKnowledgeBook.intel == required_intel)

    # sort by readable place_ triangle
    locations = [knowledge_book.readable.place_() for knowledge_book in results]
    results = sort_by_list(results, locations)

    book_containing_intel = results[0].readable

    book_holder_place = book_containing_intel.belongs_to.place
    player = Player.get()
    player.next_location = book_holder_place
    player.save()

    # steps:
    # goto: place[1]
    # get: book[1]
    # T.read: intel[1] from book[1]
    steps = [
        [book_holder_place],
        [book_containing_intel],
        [required_intel, book_containing_intel]
    ]
    print("==> Goto '", book_holder_place, "', get '", book_containing_intel, "', and read the intel '", required_intel,
          "' from it.")

    return steps


def learn_4(required_intel: Intel):
    # find an NPC who has the required intel in exchange, get the NPC's needed item to give

    results = NPC.select(NPC, Need.item_id.alias('needed_item_id')) \
        .join(Need) \
        .join(Exchange) \
        .where(Exchange.intel == required_intel, Need.item_id.is_null(False)).objects()

    # triangle distance sort
    locations = [npc.place for npc in results]
    results = sort_by_list(results, locations)

    informer = results[0]
    item_to_exchange = Item.get_by_id(informer.needed_item_id)
    del informer.needed_item_id

    player = Player.get()
    player.next_location = informer.place
    player.save()

    # steps:
    # get
    # sub-quest
    # give
    # listen
    steps = [
        [item_to_exchange],
        [],
        [item_to_exchange, informer],
        [required_intel, informer]
    ]

    print("==> Get '", item_to_exchange, "', perform sub-quest, give the acquired item to '", informer,
          "' in return get an intel on '", required_intel, "'")

    return steps


def get_1(item_to_fetch: Item):
    print("==> You already have the item.")

    # if not, add it to player's belongings
    item_to_fetch.belongs_to_player = Player.get()
    item_to_fetch.save()

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
        results_enemy = results.where(NPC.clan != Player.get().clan)
        if results_enemy:
            results = results_enemy
        # sort by triangle distance
        locations = [npc.place for npc in results]
        results = sort_by_list(results, locations)

        item_holder = results[0]

    # steps:
    #   steal: steal item[1] from NPC[1]
    steps = [
        [item_to_fetch, item_holder]
    ]
    print("==> Steal '", item_to_fetch, "' from '", item_holder, "'.")

    return steps


def get_3(item_to_fetch: Item):
    # steps:
    # goto
    # gather
    steps = [
        [item_to_fetch.place_()],
        [item_to_fetch]
    ]
    print("==> Goto '%s' and gather '%s'." % (item_to_fetch.place_(), item_to_fetch))

    return steps


def get_4(item_to_fetch: Item):
    """
    an NPC have the item, but you need to give the NPC something for an exchange
    :param item_to_fetch:
    :return:
    """

    # find an NPC who has the needed item, and has it in exchange list
    exchanges = Exchange.select().join(Item)
    if item_to_fetch.is_singleton():
        exchanges = exchanges.where(Exchange.item == item_to_fetch)
    else:
        exchanges = exchanges.where(Exchange.item.generic == item_to_fetch.generic)

    # todo: This is useless now, since being sorted again later, but when sort by triangle distance added to database,
    # this ordering will be changed again.
    exchanges = exchanges.order_by(Exchange.need.item.worth.asc())

    locations = [exc.need.npc for exc in exchanges]
    exchanges = sort_by_list(exchanges, locations)

    exchange = exchanges[0]
    item_to_give = exchange.need.item
    item_holder = exchange.need.npc

    player = Player.get()
    player.next_location = item_holder.place
    player.save()

    # check for player belonging for the exchange item
    if item_to_fetch.is_singleton():
        player_owns = item_to_fetch.belongs_to_player == player
    else:
        player_owns = Item.select().where(Item.generic == item_to_fetch.generic, Item.belongs_to_player == player) \
                      is not None

    if player_owns:
        # player has the item
        steps = [
            [],
            [],
            [],
            [item_holder.place],
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
        [item_to_give.place_()],
        [item_to_give],
        [],
        [item_holder.place],
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

    # place[1] is where NPC[1] lives
    item_holder_place = item_holder.place

    player = Player.get()
    player.next_location = item_holder_place
    player.save()

    # steps:
    #   goto: place[1]
    #   T.stealth: stealth NPC[1]
    #   T.take: take item[1] from NPC[1]
    steps = [
        [item_holder_place],
        [item_holder],
        [item_to_steal, item_holder]
    ]
    print("==> Goto '", item_holder_place, "', sneak up on '", item_holder, "', and take '", item_to_steal, "'.")

    return steps


def steal_2(item_to_steal: Item, item_holder: NPC):

    player = Player.get()
    player.next_location = item_holder.place
    player.save()

    # steps:
    # goto holder
    # kill holder
    # T.take item from holder
    steps = [
        [item_holder.place],
        [item_holder],
        [item_to_steal, item_holder]
    ]

    print("==> Goto and kill '%s', then take '%s'." % (item_holder, item_to_steal))

    return steps


def spy_1(spy_on: NPC, intel_needed: Intel, receiver: NPC):

    player = Player.get()
    player.next_location = spy_on.place
    player.save()

    # steps:
    # goto spy_on place
    # spy on 'spy_on' get the intel_needed
    # goto receiver place
    # report intel_needed to receiver
    steps = [
        [spy_on.place],
        [spy_on, intel_needed],
        [receiver.place],
        [intel_needed, receiver]
    ]

    print("==> Goto '%s', spy on '%s' to get intel '%s', goto '%s', report the intel to '%s'." %
          (spy_on.place, spy_on, intel_needed, receiver.place, receiver))

    return steps


def kill_1(target: NPC):

    player = Player.get()
    player.next_location = target.place
    player.save()

    # steps:
    # goto target
    # kill target
    steps = [
        [target.place],
        [target]
    ]

    print("==> Goto '%s' and kill '%s'." % (target.place, target))

    return steps
