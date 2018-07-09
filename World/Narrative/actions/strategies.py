from Grammar.actions import NonTerminals as NT

from World.elements import Element


def knowledge_3(elements: list):
    """
    Interview an NPC
    :return:
    """
    print('==> knowledge 3 called, Interview an NPC')
    # NPC[0] is from knowledge itself (parent node)

    # select an NPC[1] that:
    #   has an intel that NPC[0] doesn't have
    #   not an enemy to Player (or NPC[0])
    #   willing to tell, either intel is not expensive, or you already done a favour for the NPC[1]
    #   location is not too far from NPC[0]

    # intel[1] is the intel NPC[1] has that NPC[0] doesn't

    # place[0] is where the NPC[0] is living
    # place[1] is where the NPC[1] is living

    # steps:
    #   goto[1]: from place[0] | destination place[1]
    #   listen: get intel[1] from NPC[1]
    #   goto[2]: from place[1] | destination place[0]
    #   report: give intel[1] to NPC[0]
    pass
