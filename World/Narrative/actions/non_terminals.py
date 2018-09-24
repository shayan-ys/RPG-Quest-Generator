from World.Types import fn, JOIN
from World.Types.Person import Player, NPC
from World.Types.Place import Place
from World.Types.Intel import Intel, IntelTypes
from World.Types.Item import Item, ItemTypes, GenericItem
from World.Types.BridgeModels import BelongItem, BelongItemPlayer, Need, Exchange, ReadableKnowledgeBook, NPCKnowledgeBook, PlayerKnowledgeBook

from World import elements as element_types


def sub_quest_1():
    # just go somewhere - pick a place unknown to player to go to
    # the reason for unknown place is, if "learn" comes up in next level, we'll be lucky,
    # if it doesn't, intel can be added to Players knowledge right away.
    places_to_go = Place.select()\
        .join(Intel)\
        .join(PlayerKnowledgeBook, JOIN.LEFT_OUTER)\
        .group_by(Intel).having(fn.COUNT(PlayerKnowledgeBook.id) == 0)

    if not places_to_go:
        return None, []

    # todo: loop through places to find closest next place to go
    # for row in places_to_go:
    #     print(row)

    place_to_go = places_to_go[0]
    # steps:
    # goto
    steps = [
        [place_to_go]
    ]

    print("==> Goto '%s'." % place_to_go)

    return steps


def goto_1(elements: list, destination: element_types.Place):
    """
    You are already there.
    :return:
    """
    print('==> Already at your destination, %s.' % destination)

    # update player's location
    for player in elements:
        if isinstance(player, element_types.Player):
            player.current_location = destination.location

    return destination, [[]]


def goto_2(destination: element_types.Place):
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
        print("NONE")
        return []

    intel_location = results[0]

    # update player's next location
    player = Player.select().limit(1)[0]
    player.next_location = destination

    # steps:
    #   learn: location[1]
    #   T.goto: location[1]
    steps = [
        [intel_location],
        [destination]
    ]
    print("==> Find out how to get to '", destination, "', then goto it.")

    return steps


def learn_1(elements: list, required_intel: element_types.Intel):
    for elem in elements:
        if isinstance(elem, element_types.Player):
            if required_intel not in elem.intel:
                elem.intel.append(required_intel)

    print("==> Intel '%s' added." % required_intel)

    return required_intel, [[]]


def learn_2(required_intel: Intel):
    # find NPC who has the intel, goto the NPC and listen to get the intel
    results = NPC.select()\
        .join(NPCKnowledgeBook)\
        .where(NPCKnowledgeBook.intel == required_intel)
    # todo: put ally NPC first, then enemies

    if not results:
        return []

    knowledgeable_npc = results[0]

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
    :param list[element_types.Intel] elements:
    :param required_intel:
    :return:
    """

    # intel[1] is to be learned

    # find a book[1] (readable, it could be a sign) that has intel[1] on it
    book_containing_intel = ReadableKnowledgeBook.get(intel=required_intel).readable
    book_holder_place = book_containing_intel.belongs_to.place

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

    informers = NPC.select(NPC, Need.item_id.alias('needed_item_id')) \
        .join(Need) \
        .join(Exchange) \
        .where(Exchange.intel == required_intel, Need.item_id.is_null(False)).objects()

    # Todo: loop through for distance sort
    # for row in informers:
    #     pass
    if informers:
        informer = informers[0]
        print(informer)
        item_to_exchange = Item.get_by_id(informer.needed_item_id)
        del informer.needed_item_id
    else:
        return []

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


def get_1(elements: list, item_to_fetch: element_types.Item):
    print("==> You already have the item.")

    # if not, add it to player's belongings
    for player in elements:
        if isinstance(player, element_types.Player):
            if item_to_fetch not in player.belongings:
                player.belongings.append(item_to_fetch)

    return None, []


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
    item_holder = item_to_fetch.belongs_to

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
    if item_to_fetch.generic.name == ItemTypes.singleton.name:
        exchanges = exchanges.where(Exchange.item == item_to_fetch)
    else:
        exchanges = exchanges.where(Exchange.item.generic == item_to_fetch.generic)

    exchanges = exchanges.order_by(Exchange.need.item.worth.asc())

    if not exchanges:
        return []

    # Todo: distance check with NPCs i exchange list
    exchange = exchanges[0]
    item_to_give = exchange.need.item
    item_holder = exchange.need.npc

    player = Player.get()
    results = BelongItemPlayer.select().where(BelongItemPlayer.player == player, BelongItemPlayer.item == item_to_give)
    if results:
        # todo: add check for number of needed item
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

    # check if player has the needed item
    # (BelongItemPlayer.player == player)
    # & (BelongItemPlayer.item.generic == Exchange.need.item.generic)
    # & (BelongItemPlayer.count >= Exchange.need.item_count)
    #
    # | Exchange.need.item.in_(player.belongings)

    # if alter_steps:
    #     steps = alter_steps
    #     print("==> Do a sub-quest, goto '%s' to meet '%s' and exchange '%d' of '%s' with '%s'" %
    #           (item_holder.place, item_holder, count_item_to_exchange, item_to_exchange, item_to_fetch))
    # else:
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
    # steps:
    # goto target
    # kill target
    steps = [
        [target.place],
        [target]
    ]

    print("==> Goto '%s' and kill '%s'." % (target.place, target))

    return steps
