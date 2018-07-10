from World.elements import Element
from World import types


def knowledge_3(elements: list, NPC_knowledge_motivated: types.NPC):
    """
    Interview an NPC
    :return:
    """
    # NPC[0] is from knowledge itself (parent node)
    # NPC_knowledge_motivated = None

    # select an NPC[1] that:
    #   has an intel that NPC[0] doesn't have
    #   not an enemy to Player (or NPC[0])
    #   willing to tell, either intel is not expensive, or you already done a favour for the NPC[1]
    #   location is not too far from NPC[0]
    results = []
    intended_intel = None
    for elem in elements:
        elem = elem  # type: Element
        if isinstance(elem.type, types.NPC):
            useful_intel = None
            if not NPC_knowledge_motivated and elem.type.intel:
                useful_intel = elem.type.intel[0]
            else:
                for intel in elem.type.intel:
                    if intel not in NPC_knowledge_motivated.type.intel:
                        useful_intel = intel
                        break
            if useful_intel:
                intended_intel = useful_intel
                if not NPC_knowledge_motivated or elem not in NPC_knowledge_motivated.type.enemies:
                    # if location not too far
                    results.append(elem)

    if results:
        NPC_knowledgeable = results[0]  # type: Element
    else:
        return None

    # intel[1] is the intel NPC[1] has that NPC[0] doesn't

    # place[0] is where the NPC[0] is living
    # place[1] is where the NPC[1] is living

    # steps:
    #   goto[1]: from place[0] | destination place[1]
    #   listen: get intel[1] from NPC[1]
    #   goto[2]: from place[1] | destination place[0]
    #   report: give intel[1] to NPC[0]
    steps = [
        [NPC_knowledgeable.type.place],
        [intended_intel, NPC_knowledgeable],
        [NPC_knowledge_motivated.type.place],
        [intended_intel, NPC_knowledge_motivated]
    ]
    print("==> Interview '%s' to get the intel '%s', which is about '%s'." % (NPC_knowledgeable, intended_intel, intended_intel.type.value))

    return NPC_knowledgeable, steps
