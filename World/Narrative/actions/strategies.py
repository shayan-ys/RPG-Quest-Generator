from World.elements import BaseElement
from World import elements as element_types


def knowledge_2(elements: list, NPC_knowledge_motivated: element_types.NPC):
    # find someone enemy to the given NPC who has a worthy intel the ally NPC doesn't.
    spy_target = None  # type: element_types.NPC
    spy_intel = None   # type: element_types.Intel
    for elem in elements:
        if isinstance(elem, element_types.NPC):
            if elem in NPC_knowledge_motivated.enemies:
                for worthy_intel in elem.intel:
                    if worthy_intel.worth > 0.5:
                        if worthy_intel not in NPC_knowledge_motivated.intel:
                            spy_target = elem
                            spy_intel = worthy_intel

    steps = [
        [spy_target, spy_intel, NPC_knowledge_motivated]
    ]

    print("==> Spy on '%s' to get the intel '%s' for '%s'." % (spy_target, spy_intel, NPC_knowledge_motivated))

    return spy_target, steps


def knowledge_3(elements: list, NPC_knowledge_motivated: element_types.NPC):
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
        elem = elem  # type: BaseElement
        if isinstance(elem, element_types.NPC):
            useful_intel = None
            if not NPC_knowledge_motivated and elem.intel:
                useful_intel = elem.intel[0]
            else:
                for intel in elem.intel:
                    if intel not in NPC_knowledge_motivated.intel:
                        useful_intel = intel
                        break
            if useful_intel:
                intended_intel = useful_intel
                if not NPC_knowledge_motivated or elem not in NPC_knowledge_motivated.enemies:
                    # if location not too far
                    results.append(elem)

    if results:
        NPC_knowledgeable = results[0]  # type: element_types.NPC
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
        [NPC_knowledgeable.place],
        [intended_intel, NPC_knowledgeable],
        [NPC_knowledge_motivated.place],
        [intended_intel, NPC_knowledge_motivated]
    ]
    print("==> Interview '%s' to get the intel '%s', which is about '%s'." % (NPC_knowledgeable, intended_intel, intended_intel.value))

    return NPC_knowledgeable, steps


def protection_2(elements: list, NPC_protection_motivated: element_types.NPC):
    # find an NPC, ally to motivated_NPC who needs something, and who that has it
    needed_item = None  # type: element_types.Tool
    npc_in_need = None  # type: element_types.NPC
    holder_item = None  # type: element_types.NPC
    for elem in elements:
        if isinstance(elem, element_types.NPC):
            if elem in NPC_protection_motivated.allies:
                if elem.needs and len(elem.needs) > 0:
                    needed_item = elem.needs[0]
                    npc_in_need = elem
                    break

    if not needed_item or not npc_in_need:
        return None, []

    # get
    # goto
    # use
    steps = [
        [needed_item],
        [npc_in_need.place],
        [needed_item, npc_in_need]
    ]

    print("==> Treat or repair '%s' using '%s'." % (npc_in_need, needed_item))

    return npc_in_need, steps
