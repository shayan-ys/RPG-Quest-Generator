from Grammar.actions import NonTerminals as NT


def goto_1():
    """
    You are already there.
    :return:
    """
    # return or fix, the given destination is same as the player's current location
    # todo: OR the game will automatically take you to the destination!
    pass


def goto_2():
    """
    Just wander around and look.
    :return:
    """
    # place[1] is destination
    # area around location[1] is given to player to explore and find location[1]

    # steps:
    # T.explore
    pass


def goto_3():
    """
    Find out where to go and go there.
    :return:
    """
    # place[1] is destination
    # location[1] is place[1] exact location

    # steps:
    # learn: location[1]
    # T.goto: location[1]
    pass


def learn_3():
    """
    Go someplace, get something, and read what is written on it.
    :return:
    """
    # intel[1] is to be learned
    # find a book[1] (readable, it could be a sign) that has intel[1] on it
    # place[1] is where the book[1] is

    # steps:
    # goto: place[1]
    # get: book[1]
    # T.read: intel[1] from book[1]
    pass


def get_2():
    """
    Steal it from somebody.
    :return:
    """
    # item[1] is to be fetched
    # find an NPC[1] who
    #   has the item,
    #   preferably is an enemy
    #   not too far from Player's current location

    # steps:
    # steal: steal item[1] from NPC[1]
    pass


def steal_1():
    """
    Go someplace, sneak up on somebody, and take something.
    :return:
    """
    # item[1] is to be stolen from NPC[1] who has it
    # place[1] is where NPC[1] lives

    # steps:
    # goto: place[1]
    # T.stealth: stealth NPC[1]
    pass
