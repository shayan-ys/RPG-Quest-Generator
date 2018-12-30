from World.Types import fn, JOIN
from World.Types.Person import NPC, Player, Clan
from World.Types.Place import Place
from World.Types.Intel import Intel, Spell
from World.Types.Item import Item, ItemTypes, GenericItem
from World.Types.BridgeModels import Need, Exchange, NPCKnowledgeBook, PlayerKnowledgeBook
from World.Types.Log import Message
from World.Types.Names import NPCName, ItemName, PlaceName, SpellName
from World.Narrative import helper

from Grammar.actions import Terminals as T
from helper import sort_by_list
from random import randint


def knowledge_1(NPC_target: NPC):
    """
    Deliver item for study
    :param NPC_target:
    :return:
    """
    player = Player.current()
    results = Item.select().where(Item.belongs_to != NPC_target, Item.belongs_to_player != player)
    if results:
        locations_scores = [player.distance(res.place_()) for res in results]
        results = sort_by_list(results, locations_scores)
        item = results[0]
    else:
        results = NPC.select().where(NPC.id != NPC_target)
        if results:
            locations_scores = [player.distance(res.place) for res in results]
            results = sort_by_list(results, locations_scores)
            new_item_holder = results[0]
        else:
            # No NPC left in the world except the target
            new_item_holder = NPC.create(place=Place.select().order_by(fn.Random()).get(),
                                         clan=Clan.select().order_by(fn.Random()).get(),
                                         name=NPCName.fetch_new())
        item = Item.create(
            type=ItemTypes.unknown.name, generic=GenericItem.get_or_create(name=ItemTypes.singleton.name)[0],
            name='arbitrary_item_unknown_' + str(randint(100, 999)),
            place=None, belongs_to=new_item_holder)

    # steps:
    #   get item
    #   goto target place
    #   give item to target
    steps = [
        [item],
        [NPC_target.place, NPC_target],
        [item, NPC_target]
    ]
    # print("==> Deliver item", item, "to", NPC_target, "for study")
    Message.instruction("%s: Get item '%s' for me, I want to study it" % (NPC_target, item))
    return steps


def knowledge_2(NPC_knowledge_motivated: NPC):
    player = Player.current()
    # find someone enemy to the given NPC who has a worthy intel that the given NPC doesn't have.
    # or player already know them
    already_known_intel_list = Intel.select(Intel.id)\
        .join(NPCKnowledgeBook)\
        .where(NPCKnowledgeBook.npc == NPC_knowledge_motivated)
    already_known_intel_list += Intel.select(Intel.id)\
        .join(PlayerKnowledgeBook)\
        .where(PlayerKnowledgeBook.player == player)

    results = NPC.select(NPC, Intel.id.alias('intel_id'))\
        .join(NPCKnowledgeBook)\
        .join(Intel)\
        .where(NPC.clan != NPC_knowledge_motivated.clan, Intel.id.not_in(already_known_intel_list))\
        .order_by(Intel.worth.desc()).group_by(NPC).objects()

    if results:
        locations_scores = [player.distance(res.place) for res in results]
        results = sort_by_list(results, locations_scores)
        spy_target = results[0]
        spy_intel = Intel.get_by_id(spy_target.intel_id)
        del spy_target.intel_id
    else:
        # enemies
        results = NPC.select().where(NPC.clan != NPC_knowledge_motivated.clan)
        if not results:
            # no enemy found, pick any NPC
            Message.debug("knowledge_2: no enemy found, pick any NPC")
            results = NPC.select()

        locations_scores = [player.distance(res.place) for res in results]
        results = sort_by_list(results, locations_scores)
        spy_target = results[0]

        new_intel_list = Intel.select().where(Intel.id.not_in(already_known_intel_list)).order_by(Intel.worth.desc())
        if new_intel_list:
            # add the most valuable intel to the NPC knowledge book
            Message.debug("knowledge_2: add the most valuable intel to the NPC knowledge book")
            spy_intel = new_intel_list[0]
        else:
            # no new intel found, create a new intel
            spy_intel = Intel.construct(spell=Spell.create(name=SpellName.fetch_new(),
                                                           text='magical arbitrary spell'))
        NPCKnowledgeBook.create(npc=spy_target, intel=spy_intel)

    # steps:
    # spy: on target, to get intel, then report it to knowledge_motivated NPC
    steps = [
        [spy_target, spy_intel, NPC_knowledge_motivated]
    ]

    # print("==> Spy on '%s' to get the intel '%s' for '%s'." % (spy_target, spy_intel, NPC_knowledge_motivated))
    Message.instruction("%s: Spy on '%s' to get the intel '%s' for me" %
                        (NPC_knowledge_motivated, spy_target, spy_intel))
    return steps


def knowledge_3(NPC_knowledge_motivated: NPC):
    """
    Interview an NPC
    :return:
    """
    player = Player.current()
    # NPC[0] is from knowledge itself (parent node)
    # NPC_knowledge_motivated = None

    # select an NPC[1] that:
    #   has an intel that NPC[0] doesn't have
    #   not an enemy to Player (or NPC[0])
    #   willing to tell, either intel is not expensive, or you already done a favour for the NPC[1]
    #   location is not too far from NPC[0]
    not_interesting_intel = Intel.select(Intel.id).join(NPCKnowledgeBook).join(NPC)\
        .where(NPC.id == NPC_knowledge_motivated)
    not_interesting_intel += Intel.select(Intel.id).join(PlayerKnowledgeBook)\
        .where(PlayerKnowledgeBook.player == player)

    results = NPC.select(NPC, Intel.id.alias('intel_id'))\
        .join(NPCKnowledgeBook)\
        .join(Intel)\
        .order_by(Intel.worth.desc())\
        .where(Intel.id.not_in(not_interesting_intel), NPC.clan == player.clan).objects()

    if results:
        locations_scores = [player.distance(res.place) for res in results]
        results = sort_by_list(results, locations_scores)
        NPC_knowledgeable = results[0]
        intended_intel = Intel.get_by_id(NPC_knowledgeable.intel_id)
        del NPC_knowledgeable.intel_id
    else:
        new_intel_list = Intel.select().where(Intel.id.not_in(not_interesting_intel)).order_by(Intel.worth.desc())
        if new_intel_list:
            intended_intel = new_intel_list[0]
        else:
            # no new intel found, create a new intel
            intended_intel = Intel.construct(spell=Spell.create(name=SpellName.fetch_new(),
                                                                text='magical arbitrary spell'))
        results = NPC.select().where(NPC.clan == player.clan)
        if not results:
            results = NPC.select()

        locations_scores = [player.distance(res.place) for res in results]
        results = sort_by_list(results, locations_scores)
        NPC_knowledgeable = results[0]
        NPCKnowledgeBook.create(npc=NPC_knowledgeable, intel=intended_intel)

    # intel[1] is the intel NPC[1] has that NPC[0] doesn't
    # place_location[0] is where the NPC[0] is living
    # place_location[1] is where the NPC[1] is living

    # steps:
    #   goto[1]: from place_location[0] | destination place_location[1]
    #   listen: get intel[1] from NPC[1]
    #   goto[2]: from place_location[1] | destination place_location[0]
    #   report: give intel[1] to NPC[0]
    steps = [
        [NPC_knowledgeable.place],
        [intended_intel, NPC_knowledgeable],
        [NPC_knowledge_motivated.place],
        [intended_intel, NPC_knowledge_motivated]
    ]
    # print("==> Interview '", NPC_knowledgeable, "' to get the intel '", intended_intel, "'.")
    Message.instruction("%s: Ask '%s' about '%s'" % (NPC_knowledge_motivated, NPC_knowledgeable, intended_intel))
    return steps


def comfort_1(motivated: NPC) -> list:
    """
    Obtain luxuries for the motivated NPC
    :param motivated:
    :return:
    """
    # get item useful for motivated

    needed_item = Item.select().join(Need).where(Need.npc == motivated, Item.belongs_to_player.is_null())\
        .order_by(fn.Random()).limit(1)
    if needed_item:
        # motivated NPC need some items
        item = needed_item[0]
    else:
        # motivated NPC doesn't have any needs
        items_in_world = Item.select().where(Item.belongs_to_player.is_null()).order_by(Item.worth.desc()).limit(1)
        if items_in_world:
            item = items_in_world[0]
        else:
            # item not found in the world
            place = Place.select().order_by(fn.Random()).limit(1)
            if place:
                place = place[0]
            else:
                Message.debug("No place found in the World!")
                place = helper.create_place(known_to_player=False)
            item = Item.create(
                type=ItemTypes.unknown.name, generic=GenericItem.get_or_create(name=ItemTypes.singleton.name)[0],
                name='arbitrary_item_' + str(randint(100, 999)),
                place=place, worth=1)
            Message.debug("No Item found in the world, item created: %s" % item)

    # steps:
    #   get
    #   goto
    #   give
    steps = [
        [item],
        [motivated.place, motivated],
        [item, motivated]
    ]

    Message.instruction("%s: Get luxury item '%s' for me" % (motivated, item))
    return steps


def comfort_2(motivated: NPC) -> list:
    """
    Kill pests
    :param motivated:
    :return:
    """
    # find enemy of motivated, or create one
    results = NPC.select().where(NPC.clan != motivated.clan).order_by(fn.Random()).limit(1)
    if results:
        enemy = results.get()
    else:
        # No NPC left in the world except the motivated
        enemies_clan = Clan.select().where(Clan.id != motivated.clan).order_by(fn.Random()).get()
        enemy = NPC.create(place=Place.select().order_by(fn.Random()).get(),
                           clan=enemies_clan,
                           name=NPCName.fetch_new())

    player = Player.current()
    damage_report_intel = Intel.construct(other='arbitrary_pest_damage_report_' + str(randint(100, 999)))
    PlayerKnowledgeBook.create(player=player, intel=damage_report_intel)

    # steps:
    #   goto enemies place
    #   kill enemies
    #   goto motivated place
    #   T.report intel(?) to motivated
    steps = [
        [enemy.place, enemy],
        [enemy],
        [motivated.place, motivated],
        [damage_report_intel, motivated]
    ]

    Message.instruction("%s: Take care of that pest '%s' for me" % (motivated, enemy))
    return steps


def reputation_1(motivated: NPC) -> list:
    """
    Obtain rare items
    :param motivated:
    :return:
    """
    # find high worth item

    worthy_item = Item.select().where(Item.belongs_to_player.is_null()).order_by(Item.worth.desc()).limit(1)
    if worthy_item:
        # item found for NPC
        item = worthy_item[0]
    else:
        # item not found in the world
        place = Place.select().order_by(fn.Random()).limit(1)
        if place:
            place = place[0]
        else:
            Message.debug("No place found in the World!")
            place = helper.create_place(known_to_player=False)
        item = Item.create(
            type=ItemTypes.unknown.name, generic=GenericItem.get_or_create(name=ItemTypes.singleton.name)[0],
            name='arbitrary_item_' + str(randint(100, 999)),
            place=place, worth=1)
        Message.debug("No Item found in the world, item created: %s" % item)

    # steps:
    #   get
    #   goto
    #   give
    steps = [
        [item],
        [motivated.place, motivated],
        [item, motivated]
    ]

    Message.instruction("%s: Get the rare item '%s' for me" % (motivated, item))
    return steps


def reputation_2(motivated: NPC) -> list:
    """
    Kill enemies of motivated
    :param motivated: given from higher level nodes
    :return:
    """
    results = NPC.select().where(NPC.clan != motivated.clan).order_by(fn.Random()).limit(1)
    if results:
        enemy = results.get()
    else:
        # No NPC left in the world except the motivated
        enemies_clan = Clan.select().where(Clan.id != motivated.clan).order_by(fn.Random()).get()
        enemy = NPC.create(place=Place.select().order_by(fn.Random()).get(),
                           clan=enemies_clan,
                           name=NPCName.fetch_new())

    player = Player.current()
    killing_report_intel = Intel.construct(other='arbitrary_killing_report_' + str(randint(100, 999)))
    PlayerKnowledgeBook.create(player=player, intel=killing_report_intel)

    # steps:
    #   goto enemies place
    #   kill enemies
    #   goto motivated place
    #   T.report intel(?) to motivated
    steps = [
        [enemy.place, enemy],
        [enemy],
        [motivated.place, motivated],
        [killing_report_intel, motivated]
    ]
    # print("==> Kill enemies", enemy, "and report it back to", motivated)
    Message.instruction("%s: Kill my enemy '%s', and report it" % (motivated, enemy))
    return steps


def reputation_3(motivated: NPC) -> list:
    """
    Visit a dangerous place
    :param motivated:
    :return:
    """
    # goto an enemies place
    enemies = NPC.select().where(NPC.clan != motivated.clan).order_by(fn.Random()).limit(1)
    if enemies:
        place = enemies[0].place
    else:
        place = Place.select().order_by(fn.Random()).limit(1)
        if place:
            place = place[0]
        else:
            Message.debug("No place found in the World!")
            place = helper.create_place(known_to_player=False)

    player = Player.current()
    danger_report_intel = Intel.construct(other='arbitrary_danger_report_' + str(randint(100, 999)))
    PlayerKnowledgeBook.create(player=player, intel=danger_report_intel)

    # steps
    #   goto
    #   goto
    #   report
    steps = [
        [place],
        [motivated.place, motivated],
        [danger_report_intel, motivated]
    ]
    Message.instruction("%s: Goto the dangerous '%s' and report what you've seen there" % (motivated, place))
    return steps


def serenity_1(motivated: NPC):
    """
    Revenge, Justice
    :param motivated:
    :return:
    """
    enemies = NPC.select().where(NPC.clan != motivated.clan).order_by(fn.Random()).limit(1)
    if enemies:
        target = enemies[0]
    else:
        place = Place.select().order_by(fn.Random()).limit(1)
        if place:
            place = place[0]
        else:
            Message.debug("No place found in the World!")
            place = helper.create_place(known_to_player=False)
        enemy_clan = Clan.select().where(Clan.id != motivated.clan).order_by(fn.Random()).limit(1).get()
        target = NPC.create(clan=enemy_clan, name=NPCName.fetch_new(), place=place)

    # steps
    #   goto
    #   damage
    steps = [
        [target.place, target],
        [target]
    ]
    Message.instruction("%s: Get my revenge from '%s'" % (motivated, target))
    return steps


def serenity_4(motivated: NPC) -> list:
    """
    Check on NPC(1)
    :param motivated:
    :return:
    """
    # find ally NPC to motivated get generated intel about health and well being
    allies = NPC.select().where(NPC.clan == motivated.clan, NPC.id != motivated).order_by(fn.Random()).limit(1)
    if allies:
        target = allies[0]
    else:
        place = Place.select().order_by(fn.Random()).limit(1)
        if place:
            place = place[0]
        else:
            Message.debug("No place found in the World!")
            place = helper.create_place(known_to_player=False)
        target = NPC.create(clan=motivated.clan, name=NPCName.fetch_new(), place=place)

    well_being_intel = Intel.construct(other='arbitrary_well_being_report_' + str(randint(100, 999)))
    NPCKnowledgeBook.create(npc=target, intel=well_being_intel)
    # steps
    #   goto
    #   listen
    #   goto
    #   report
    steps = [
        [target.place, target],
        [well_being_intel, target],
        [motivated.place, motivated],
        [well_being_intel, motivated]
    ]
    Message.instruction("%s: Check on my friend, '%s' ask how he's doing for me" % (motivated, target))
    return steps


def serenity_5(motivated: NPC) -> list:
    """
    Check on NPC(2)
    :param motivated:
    :return:
    """
    # find ally NPC to motivated get an item from he/she
    allies = NPC.select().where(NPC.clan == motivated.clan, NPC.id != motivated).order_by(fn.Random()).limit(1)
    if allies:
        target = allies[0]
    else:
        place = Place.select().order_by(fn.Random()).limit(1)
        if place:
            place = place[0]
        else:
            Message.debug("No place found in the World!")
            place = helper.create_place(known_to_player=False)
        target = NPC.create(clan=motivated.clan, name=NPCName.fetch_new(), place=place)

    belongings = Item.select().where(Item.belongs_to == target.id).order_by(fn.Random()).limit(1)
    if belongings:
        item = belongings[0]
    else:
        item = Item.create(
            type=ItemTypes.singleton.name, generic=GenericItem.get_or_create(name=ItemTypes.singleton.name)[0],
            name='arbitrary_item_' + str(randint(100, 999)),
            belongs_to=target)
    # steps
    #   goto
    #   take
    #   goto
    #   give
    steps = [
        [target.place, target],
        [item, target],
        [motivated.place, motivated],
        [item, motivated]
    ]
    Message.instruction("%s: Get item '%s' from my friend, '%s' for me" % (motivated, item, target))
    return steps


def conquest_1(motivated: NPC) -> list:
    """
    Attack enemy
    :param motivated:
    :return:
    """
    # find enemy of motivated, or create one
    results = NPC.select().where(NPC.clan != motivated.clan).order_by(fn.Random()).limit(1)
    if results:
        enemy = results.get()
    else:
        # No NPC left in the world except the motivated
        enemies_clan = Clan.select().where(Clan.id != motivated.clan).order_by(fn.Random()).get()
        enemy = NPC.create(place=Place.select().order_by(fn.Random()).get(),
                           clan=enemies_clan,
                           name=NPCName.fetch_new())

    # steps:
    #   goto enemies place
    #   damage enemies
    steps = [
        [enemy.place, enemy],
        [enemy]
    ]

    Message.instruction("%s: Damage my enemy '%s' or me" % (motivated, enemy))
    return steps


def conquest_2(motivated: NPC) -> list:
    """
    Steal stuff
    :param motivated:
    :return:
    """
    # find something an enemy to motivated has
    item = None
    enemy_ids = NPC.select(NPC.id).where(NPC.clan != motivated.clan)
    if enemy_ids:
        items = Item.select().where(Item.belongs_to.in_(enemy_ids)).order_by(fn.Random()).limit(1)
        if items:
            item = items[0]

    if not item:
        place = Place.select().order_by(fn.Random()).limit(1)
        if place:
            place = place[0]
        else:
            Message.debug("No place found in the World!")
            place = helper.create_place(known_to_player=False)
        enemy_clan = Clan.select().where(Clan.id != motivated.clan).order_by(fn.Random()).limit(1).get()
        target = NPC.create(clan=enemy_clan, name=NPCName.fetch_new(), place=place)
        item = Item.create(
            type=ItemTypes.singleton.name, generic=GenericItem.get_or_create(name=ItemTypes.singleton.name)[0],
            name='arbitrary_item_' + str(randint(100, 999)),
            belongs_to=target)

    # steps
    #   goto
    #   steal
    #   goto
    #   give
    steps = [
        [item.place_(), None, item],
        [item, item.belongs_to],
        [motivated.place, motivated],
        [item, motivated]
    ]
    Message.instruction("%s: Steal item '%s' from '%s' for me" % (motivated, item, item.belongs_to))
    return steps


def protection_1(motivated: NPC) -> list:
    """
    Attack threatening entities
    :param motivated:
    :return:
    """
    # find enemy of motivated, or create one
    results = NPC.select().where(NPC.clan != motivated.clan).order_by(fn.Random()).limit(1)
    if results:
        enemy = results.get()
    else:
        # No NPC left in the world except the motivated
        enemies_clan = Clan.select().where(Clan.id != motivated.clan).order_by(fn.Random()).get()
        enemy = NPC.create(place=Place.select().order_by(fn.Random()).get(),
                           clan=enemies_clan,
                           name=NPCName.fetch_new())

    player = Player.current()
    threat_report_intel = Intel.construct(other='arbitrary_threat_damage_report_' + str(randint(100, 999)))
    PlayerKnowledgeBook.create(player=player, intel=threat_report_intel)

    # steps:
    #   goto enemies place
    #   kill enemies
    #   goto motivated place
    #   T.report intel(?) to motivated
    steps = [
        [enemy.place, enemy],
        [enemy],
        [motivated.place, motivated],
        [threat_report_intel, motivated]
    ]

    Message.instruction("%s: Relieve me of '%s' threats, then report it" % (motivated, enemy))
    return steps


def protection_2(NPC_protection_motivated: NPC) -> list:
    # find an NPC, who is ally to motivated_NPC and needs something, as well as an NPC who has that thing
    # and that need is not part of an exchange
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

    if not results:
        # select any kind of need including an exchange need
        results = NPC.select(NPC, Need.item_id.alias('needed_item_id'))\
            .join(Need) \
            .where(
                NPC.clan == NPC_protection_motivated.clan,
                Need.item.is_null(False),
            )\
            .objects()

    player = Player.current()

    if results:
        # sort by distance
        locations_scores = [player.distance(res.place) for res in results]
        results = sort_by_list(results, locations_scores)
        npc_in_need = results[0]

        needed_item = Item.get_by_id(npc_in_need.needed_item_id)
        del npc_in_need.needed_item_id

    else:
        # no need found, have to create one
        # just select an ally, create a need for him
        results = NPC.select().where(NPC.clan == NPC_protection_motivated.clan)
        if not results:
            # just select an NPC, including enemies
            results = NPC.select()

        # sort by distance
        locations_scores = [player.distance(res.place) for res in results]
        results = sort_by_list(results, locations_scores)
        npc_in_need = results[0]

        # select an NPC to hold the item, enemies preferred
        holders = NPC.select().where(NPC.id != npc_in_need, NPC.clan != player.clan)
        if not holders:
            holders = NPC.select().where(NPC.id != npc_in_need)
        # sort by distance
        locations_scores = [player.distance(res.place) for res in holders]
        holders = sort_by_list(holders, locations_scores)
        holder = holders[0]

        needed_item = Item.create(
            type=ItemTypes.tool.name, generic=GenericItem.get_or_create(name=ItemTypes.singleton.name)[0],
            name='arbitrary_item_potion_' + str(randint(100, 999)),
            place=None, belongs_to=holder,
            usage=T.treat.value, impact_factor=0.5)
        Need.create(npc=npc_in_need, item=needed_item)

    # get
    # goto NPC in need
    # use
    steps = [
        [needed_item],
        [npc_in_need.place, npc_in_need],
        [needed_item, npc_in_need]
    ]

    # print("==> Treat or repair '%s' using '%s'." % (npc_in_need, needed_item))
    Message.instruction("%s: Treat my friend '%s' using '%s'" % (NPC_protection_motivated, npc_in_need, needed_item))
    return steps
