from World import elements as element_types


def goto_1(elements: list, destination: element_types.Place):
    """
    You are already there.
    :return:
    """
    print('==> Teleported to %s, (goto.1: already in your destination)' % destination)
    # return or fix, the given destination is same as the player's current location
    # todo: OR the game will automatically take you to the destination!
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
    destination_location = destination.location

    # steps:
    #   learn: location[1]
    #   T.goto: location[1]
    steps = [
        [destination_location],
        [destination_location]
    ]
    print("==> Find out how to get to '%s', then goto it" % destination)

    return destination, steps


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
            if required_intel == elem.value:
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


def get_2(elements: list, item_to_fetch: element_types.Object):
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


def steal_1(elements: list, item_to_steal: element_types.Object, item_holder: element_types.NPC):
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
    #   T.take: take item[1]
    steps = [
        [item_holder_place],
        [item_holder],
        [item_to_steal]
    ]
    print("==> Goto '%s', sneak up on '%s', and take '%s'." % (item_holder_place, item_holder, item_to_steal))

    return item_holder, steps
