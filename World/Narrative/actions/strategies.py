from World.Types import fn, JOIN
from World.Types.Person import NPC
from World.Types.Intel import Intel
from World.Types.Item import Item
from World.Types.BridgeModels import Need, Exchange, NPCKnowledgeBook

# todo: use pre-filled favour book to choose between NPCs


def knowledge_2(NPC_knowledge_motivated: NPC):
    # find someone enemy to the given NPC who has a worthy intel that the given NPC doesn't have.
    already_known_intel_list = Intel.select()\
        .join(NPCKnowledgeBook)\
        .where(NPCKnowledgeBook.npc == NPC_knowledge_motivated)

    results = NPC.select(NPC, Intel.id.alias('intel_id'))\
        .join(NPCKnowledgeBook)\
        .join(Intel)\
        .where(NPC.clan != NPC_knowledge_motivated.clan, Intel.id.not_in(already_known_intel_list))\
        .order_by(Intel.worth.desc()).objects()

    # todo: sort by distance

    if not results:
        return []

    spy_target = results[0]
    spy_intel = Intel.get_by_id(spy_target.intel_id)
    del spy_target.intel_id

    # steps:
    # spy: on target, to get intel, then report it to knowledge_motivated NPC
    steps = [
        [spy_target, spy_intel, NPC_knowledge_motivated]
    ]

    print("==> Spy on '%s' to get the intel '%s' for '%s'." % (spy_target, spy_intel, NPC_knowledge_motivated))

    return steps


def knowledge_3(NPC_knowledge_motivated: NPC):
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
    not_interesting_intel = Intel.select().join(NPCKnowledgeBook).join(NPC).where(NPC.id == NPC_knowledge_motivated.id)

    results = NPC.select(NPC, Intel.id.alias('intel_id'))\
        .join(NPCKnowledgeBook)\
        .join(Intel)\
        .order_by(Intel.worth.desc())\
        .where(Intel.id.not_in(not_interesting_intel)).objects()

    # todo: sort by distance

    if not results:
        return []

    # for res in results:
    #     print(res.intel_id)

    NPC_knowledgeable = results[0]
    intended_intel = Intel.get_by_id(NPC_knowledgeable.intel_id)

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
    print("==> Interview '", NPC_knowledgeable, "' to get the intel '", intended_intel, "'.")

    return steps


def protection_2(NPC_protection_motivated: NPC):
    # find an NPC, who is ally to motivated_NPC and needs something, as well as an NPC who that has that thing
    results = NPC.select(NPC, Need.item_id.alias('needed_item_id'))\
        .join(Need) \
        .join(Exchange, JOIN.LEFT_OUTER)\
        .where(
            NPC.clan == NPC_protection_motivated.clan,
            Need.item.is_null(False),
        )\
        .group_by(Need)\
        .having(fn.COUNT(Exchange.id) == 0)\
        .objects()

    # todo: sort by distance

    if results:
        npc_in_need = results[0]
    else:
        return []

    needed_item = Item.get_by_id(npc_in_need.needed_item_id)
    del npc_in_need.needed_item_id

    # get
    # goto
    # use
    steps = [
        [needed_item],
        [npc_in_need.place],
        [needed_item, npc_in_need]
    ]

    print("==> Treat or repair '%s' using '%s'." % (npc_in_need, needed_item))

    return steps
