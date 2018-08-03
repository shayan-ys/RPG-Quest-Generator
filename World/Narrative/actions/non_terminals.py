from World import elements as element_types


def sub_quest_1(elements: list):
    # just go somewhere - pick a place unknown to player to go to
    # the reason for unknown place is, if "learn" comes up in next level, we'll be lucky,
    # if it doesn't, intel can be added to Players knowledge right away.
    places_to_go = []
    place = None
    for elem in elements:
        if isinstance(elem, element_types.Place):
            place = elem
            for player in elements:
                if isinstance(player, element_types.Player):
                    for intel in player.intel:
                        if isinstance(intel, element_types.IntelLocation):
                            if intel.data != place:
                                places_to_go.append(place)

    if not places_to_go:
        return None, []

    place_to_go = places_to_go[0]
    # steps:
    # goto
    steps = [
        [place_to_go]
    ]

    print("==> Goto '%s'." % place_to_go)

    return place_to_go, steps


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


def goto_2(elements: list, destination: element_types.Place):
    """
    Just wander around and look.
    :return:
    """
    # place[1] is destination
    # area around location[1] is given to player to explore and find location[1]
    area_destination = destination.location

    # steps:
    # T.explore
    steps = [
        [area_destination]
    ]
    print("==> Explore around '%s' to find '%s'." % (area_destination, destination.location))

    return destination, steps


def goto_3(elements: list, destination: element_types.Place):
    """
    Find out where to go and go there.
    :return:
    """
    # place[1] is destination
    # location[1] is place[1] exact location

    # for player in elements:
    #     if isinstance(player, element_types.Player):
    #         if player.current_location == destination.location:
    #             return None, []

    intel_location = None
    for elem in elements:
        if isinstance(elem, element_types.IntelLocation):
            if elem.data == destination:
                intel_location = elem

    if not intel_location:
        return None, [[]]

    # update player's next location
    for player in elements:
        if isinstance(player, element_types.Player):
            player.next_location = destination.location

    # steps:
    #   learn: location[1]
    #   T.goto: location[1]
    steps = [
        [intel_location],
        [destination.location]
    ]
    print("==> Find out how to get to '%s', then goto it" % destination)

    return destination, steps


def learn_1(elements: list, required_intel: element_types.Intel):
    for elem in elements:
        if isinstance(elem, element_types.Player):
            if required_intel not in elem.intel:
                elem.intel.append(required_intel)

    print("==> Intel '%s' added." % required_intel)

    return required_intel, [[]]


def learn_2(elements: list, required_intel: element_types.Intel):
    # find NPC who has the intel, goto the NPC and listen to get the intel
    knowledgeable_npc = None  # type: element_types.NPC
    for elem in elements:
        if isinstance(elem, element_types.NPC):
            if required_intel in elem.intel:
                knowledgeable_npc = elem

    if not knowledgeable_npc:
        return None, []

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

    return required_intel, steps


def learn_3(elements: list, required_intel: element_types.Intel):
    """
    Go someplace, get something, and read what is written on it.
    :param list[element_types.Intel] elements:
    :param required_intel:
    :return:
    """
    
    # intel[1] is to be learned
    intel_elem = None
    for elem in elements:
        if isinstance(elem, element_types.Intel):
            if required_intel == elem:
                intel_elem = elem
                break
    if not intel_elem:
        return None, []

    # find a book[1] (readable, it could be a sign) that has intel[1] on it
    books = []
    for elem in elements:
        if isinstance(elem, element_types.Readable):
            if intel_elem in elem.intel:
                books.append(elem)
    if books:
        book_containing_intel = books[0]
    else:
        return None, []

    book_holder_place = None
    if hasattr(book_containing_intel, 'place'):
        book_holder_place = book_containing_intel.place
    else:
        # NPC[1] has the book[1]
        holders = []
        for elem in elements:
            if hasattr(elem, 'belongings') and book_containing_intel in elem.belongings:
                holders.append(elem)

        if holders:
            book_holder = holders[0]    # type: element_types.NPC
            if hasattr(book_holder, 'place'):
                book_holder_place = book_holder.place

    # place[1] is where the NPC[1] is
    if not book_holder_place:
        return None, []

    # steps:
    # goto: place[1]
    # get: book[1]
    # T.read: intel[1] from book[1]
    steps = [
        [book_holder_place],
        [book_containing_intel],
        [intel_elem, book_containing_intel]
    ]
    print("==> Goto '%s', get '%s', and read the '%s' from it." % (book_holder_place, book_containing_intel, intel_elem))

    return book_containing_intel, steps


def learn_4(elements: list, required_intel: element_types.Intel):
    # find an NPC who has the required intel in exchange, get the NPC's needed item to give
    item_to_exchange = None
    informer = None
    for elem in elements:
        if isinstance(elem, element_types.NPC):
            if required_intel in elem.exchange_motives.keys():
                item_to_exchange = elem.exchange_motives[required_intel]
                informer = elem

    if not item_to_exchange or not informer:
        return None, []

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

    print("==> Get '%s', perform sub-quest, give the acquired item to '%s' in return get an intel on '%s'" %
          (item_to_exchange, informer, required_intel))

    return required_intel, steps


def get_1(elements: list, item_to_fetch: element_types.Item):

    print("==> You already have the item.")

    # if not, add it to player's belongings
    for player in elements:
        if isinstance(player, element_types.Player):
            if item_to_fetch not in player.belongings:
                player.belongings.append(item_to_fetch)

    return None, []


def get_2(elements: list, item_to_fetch: element_types.Item):
    """
    Steal it from somebody.
    :return:
    """
    # item[1] is to be fetched

    # find an NPC[1] who
    #   has the item,
    #   preferably is an enemy
    #   not too far from Player's current location
    holders = []
    for elem in elements:
        if isinstance(elem, element_types.NPC):
            if item_to_fetch in elem.belongings:
                holders.append(elem)

    if len(holders) > 1:
        holders_reachable = []
        player = None
        for elem in elements:
            if isinstance(elem, element_types.Player):
                player = elem
        for holder in holders:
            if not holder.place.distance_from(player).unreachable:
                holders_reachable.append(holder)

    if holders:
        item_holder = holders[0]
    else:
        return None, []

    # steps:
    #   steal: steal item[1] from NPC[1]
    steps = [
        [item_to_fetch, item_holder]
    ]
    print("==> Steal '%s' from '%s'." % (item_to_fetch, item_holder))

    return item_holder, steps


def get_3(elements: list, item_to_fetch: element_types.Item):
    # steps:
    # goto
    # gather
    steps = [
        [item_to_fetch.place],
        [item_to_fetch]
    ]
    print("==> Goto '%s' and gather '%s'." % (item_to_fetch.place, item_to_fetch))

    return item_to_fetch, steps


def get_4(elements: list, item_to_fetch: element_types.Item):
    """
    an NPC have the item, but you need to give the NPC something for an exchange
    :param elements:
    :param item_to_fetch:
    :return:
    """
    # find an NPC who has the needed item, and has it in exchange list
    item_to_exchange = None  # type: element_types.Item
    item_holder = None       # type: element_types.NPC
    count_item_to_exchange = 0
    alter_steps = []
    for elem in elements:
        if isinstance(elem, element_types.NPC):
            if item_to_fetch in elem.belongings:
                if item_to_fetch in elem.exchange_motives.keys():
                    item_holder = elem
                    item_to_exchange = elem.exchange_motives[item_to_fetch]

    if alter_steps:
        steps = alter_steps
        print("==> Do a sub-quest, goto '%s' to meet '%s' and exchange '%d' of '%s' with '%s'" %
              (item_holder.place, item_holder, count_item_to_exchange, item_to_exchange, item_to_fetch))
    else:
        # steps:
        # goto
        # get
        # sub-quest
        # goto
        # exchange
        steps = [
            [item_to_exchange.place],
            [item_to_exchange],
            [],
            [item_holder.place],
            [item_holder, item_to_exchange, item_to_fetch]
        ]
        print("==> Goto '%s', get '%s', do a sub-quest, goto '%s' to meet '%s' and exchange '%s' with '%s'" %
              (item_to_exchange.place, item_to_exchange, item_holder.place, item_holder, item_to_exchange, item_to_fetch))

    return item_to_fetch, steps


def steal_1(elements: list, item_to_steal: element_types.Item, item_holder: element_types.NPC):
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
    print("==> Goto '%s', sneak up on '%s', and take '%s'." % (item_holder_place, item_holder, item_to_steal))

    return item_holder, steps


def spy_1(elements: list, spy_on: element_types.NPC, intel_needed: element_types.Intel, receiver: element_types.NPC):
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

    return spy_on, steps


def steal_2(elements: list, item_to_steal: element_types.Item, item_holder: element_types.NPC):
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

    return item_to_steal, steps


def kill_1(elements: list, target: element_types.NPC):
    # steps:
    # goto target
    # kill target
    steps = [
        [target.place],
        [target]
    ]

    print("==> Goto '%s' and kill '%s'." % (target.place, target))

    return target, steps
