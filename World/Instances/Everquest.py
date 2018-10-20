from Grammar.actions import NonTerminals as NT, Terminals as T

from World.Types.Item import Item, ItemTypes, GenericItem
from World.Types.Intel import Intel, IntelTypes, Spell
from World.Types.Place import Place
from World.Types.Person import Clan, NPC, Motivation, Player
from World.Types.BridgeModels import Need, Exchange, NPCKnowledgeBook, PlayerKnowledgeBook, ReadableKnowledgeBook


def create():
    alliance = Clan.create(name='Alliance')
    horde = Clan.create(name='Horde')

    rivervale = Place.create(name='Rivervale', x=10, y=80)
    qeynos_place = Place.create(name='qeynos_place', x=50, y=50)
    bixies_place = Place.create(name='bixies_place', x=70, y=90)
    bandage_place = Place.create(name='bandage_place', x=10, y=60)
    steve_place = Place.create(name='steve_place', x=60, y=20)
    goblin_place = Place.create(name='goblin_place', x=80, y=85)
    tomas_place = Place.create(name='tomas_place', x=10, y=10)
    lempeck_place = Place.create(name='lempeck_place', x=80, y=10)

    player = Player.create(name='player_1', place=rivervale, clan=alliance)

    qeynos = NPC.create(name='Qeynos', place=qeynos_place, clan=alliance)
    npc_2 = NPC.create(name='NPC2', place=rivervale, clan=alliance)  # = adon
    steve = NPC.create(name='Steve', place=steve_place, clan=alliance)
    tomas = NPC.create(name='Tomas', place=tomas_place, clan=alliance)
    lempeck = NPC.create(name='Lempeck', place=lempeck_place, clan=alliance, health_meter=0.7)  # = Denros
    bixies = NPC.create(name='Bixies', place=bixies_place, clan=horde)
    goblin = NPC.create(name='Goblin', place=goblin_place, clan=horde)

    steve_motive = Motivation.create(npc=steve, action=NT.knowledge.value, motive=0.6)
    tomas_motive = Motivation.create(npc=tomas, action=NT.protection.value, motive=0.8)

    potion = Item.create(type=ItemTypes.tool.name, generic=GenericItem.get_or_create(name=ItemTypes.singleton.name)[0], name='potion', place=None, belongs_to=qeynos, usage=T.treat.value, impact_factor=0.5)
    jum = Item.create(type=ItemTypes.unknown.name, generic=GenericItem.get_or_create(name='jum')[0], name='jum', place=None, belongs_to=npc_2)
    comb = Item.create(type=ItemTypes.unknown.name, generic=GenericItem.get_or_create(name='comb')[0], name='comb', place=None, belongs_to=bixies)
    bandage = Item.create(type=ItemTypes.tool.name, generic=GenericItem.get_or_create(name='bandage')[0], name='bandage', place=bandage_place, belongs_to=None, usage=T.treat.value)
    address_book = Item.create(type=ItemTypes.readable.name, generic=GenericItem.get_or_create(name=ItemTypes.singleton.name)[0], name='address-book (goblin loc)', belongs_to=tomas)
    coin = Item.create(type=ItemTypes.unknown.name, generic=GenericItem.get_or_create(name='coin')[0], name='coin', belongs_to_player=player)

    Need.create(npc=lempeck, item=potion)

    spell = Intel.create(type=IntelTypes.spell.name, spell=Spell.create(
        name="needs_path",
        text="'Earth, grass, trees and seeds reveal the path to suit my needs'"))
    spell_2 = Intel.create(type=IntelTypes.spell.name, spell=Spell.create(name="flat_earth",
                                                                          text="Earth is flat! LoL"))
    spell_3 = Intel.create(type=IntelTypes.spell.name, spell=Spell.create(name="gravity", text="Gravity is a myth"))
    NPCKnowledgeBook.create(npc=goblin, intel=spell)
    NPCKnowledgeBook.create(npc=bixies, intel=spell_2)
    NPCKnowledgeBook.create(npc=steve, intel=spell_2)

    intel_bandage_loc = Intel.create(type=IntelTypes.place.name, place=bandage_place)
    intel_rivervale_loc = Intel.create(type=IntelTypes.place.name, place=npc_2.place, npc_place=npc_2, worth=0.6)

    intel_goblin_loc = Intel.create(type=IntelTypes.place.name, place=goblin.place, npc_place=goblin, worth=0.8)
    ReadableKnowledgeBook.create(readable=address_book, intel=intel_goblin_loc)

    intel_tomas_loc = Intel.create(type=IntelTypes.place.name, place=tomas.place, npc_place=tomas)
    NPCKnowledgeBook.create(npc=bixies, intel=intel_tomas_loc)
    NPCKnowledgeBook.create(npc=lempeck, intel=intel_tomas_loc)

    intel_lempeck_loc = Intel.create(type=IntelTypes.place.name, place=lempeck.place, npc_place=lempeck)
    NPCKnowledgeBook.create(npc=qeynos, intel=intel_lempeck_loc)

    intel_qeynos_loc = Intel.create(type=IntelTypes.place.name, place=qeynos.place, npc_place=qeynos)
    NPCKnowledgeBook.create(npc=npc_2, intel=intel_qeynos_loc)

    intel_comb_holder = Intel.create(type=IntelTypes.holding.name, holding_item=comb, holding_holder=bixies)
    NPCKnowledgeBook.create(npc=npc_2, intel=intel_comb_holder)

    intel_bixies_place = Intel.create(type=IntelTypes.place.name, place=bixies.place, npc_place=bixies)
    NPCKnowledgeBook.create(npc=npc_2, intel=intel_bixies_place)

    Exchange.create(npc=qeynos, item=potion, need=Need.get_or_create(npc=qeynos, item=jum)[0])
    Exchange.create(npc=npc_2, intel=intel_comb_holder, need=Need.get_or_create(npc=npc_2, item=bandage)[0])
    Exchange.create(npc=npc_2, intel=intel_bixies_place, need=Need.get_or_create(npc=npc_2, item=bandage)[0])
    Exchange.create(npc=npc_2, item=jum, need=Need.get_or_create(npc=npc_2, item=comb)[0])
    Exchange.create(npc=tomas, item=address_book, need=Need.get_or_create(npc=tomas, item=coin)[0])

    PlayerKnowledgeBook.create(player=player, intel=intel_qeynos_loc)
    PlayerKnowledgeBook.create(player=player, intel=intel_tomas_loc)
    PlayerKnowledgeBook.create(player=player, intel=Intel.get_or_create(
        type=IntelTypes.place.name, place=steve_place, npc_place=steve)[0])
    PlayerKnowledgeBook.create(player=player, intel=intel_bandage_loc)
    PlayerKnowledgeBook.create(player=player, intel=intel_lempeck_loc)

    # todo: remove followings
    PlayerKnowledgeBook.create(player=player, intel=intel_goblin_loc)


# elements = []
#
# # potion = Tool(name='potion', usage=T.treat)
# # jum = UnknownItem(name='jum')
# # comb = UnknownItem(name='comb')
# # bandage = Tool(name='bandage', usage=T.treat)
# #
# # rivervale = Place('Rivervale', location=Location(10, 80))
# # bandage_place = Place('bandage_place', Location(10, 60), items=[bandage])
# #
# # steve = NPC(name='Steve', motivations={NT.knowledge: 0.6}, place=Place('steve_loc', Location(60, 20)))
# #
# # intel_spell = IntelSpell('Magical Spell')
# # goblin = NPC('Goblin', motivations={}, place=Place('goblin_place', Location(80, 85)), intel=[intel_spell])
# #
# # intel_goblin_loc = IntelLocation(goblin.place)
# # intel_goblin_loc.worth = 0.8
# # letter = Readable(name='address-book (goblin)', intel=[IntelLocation(goblin.place)])
# #
# # tomas = NPC('NPC1 (Tomas)', motivations={NT.protection: 0.8}, place=Place('tomas_place', Location(10, 10)),
# #             belongings=[letter], exchange_motives={letter: Coin()})
# # intel_tomas_place = IntelLocation(tomas.place)
# # lempeck = NPC('lempeck (Denros)', motivations={}, place=Place('lempeck_hiding', location=Location(80, 10)),
# #               needs=[potion], intel=[intel_tomas_place])
# # intel_lempeck_place = IntelLocation(lempeck.place)
# # qeynos = NPC('Qeynos (Angie)', motivations={}, place=Place('qeynos_place', location=Location(50, 50)), belongings=[potion],
# #              needs=[jum], exchange_motives={potion: jum}, intel=[intel_lempeck_place])
# # intel_qeynos_place = IntelLocation(qeynos.place)
# #
# # bixies = NPC('bixies', motivations={}, place=Place('bixies_place', location=Location(70, 90)), belongings=[comb])
# #
# # bixies_place_intel = IntelLocation(bixies.place)
# # comb_holder = IntelHolding(comb, bixies)
# # npc_2 = NPC('NPC2 (adon)', motivations={}, place=rivervale, belongings=[jum], needs=[comb, bandage],
# #             intel=[comb_holder, intel_qeynos_place],
# #             exchange_motives={comb_holder: bandage, bixies_place_intel: bandage, jum: comb})
# #
# #
# # Clan([
# #     qeynos,
# #     lempeck,
# #     tomas,
# #     npc_2,
# #     steve
# # ]).set_enemy(Clan([
# #         bixies,
# #         goblin
# #     ]))
# #
# # player_pre_intel = [
# #     intel_lempeck_place,
# #     intel_qeynos_place,
# #     bixies_place_intel,
# #     IntelLocation(bandage_place),
# #     IntelLocation(rivervale),
# #     IntelLocation(steve.place)
# # ]
# #
# # player_starting_money = 4
# #
# # elements = player_pre_intel + [
# #
# #     intel_goblin_loc,
# #     intel_tomas_place,
# #
# #     potion,
# #     jum,
# #     comb,
# #     bandage,
# #     letter,
# #
# #     rivervale,
# #     bandage_place,
# #
# #     steve,
# #     tomas,
# #     goblin,
# #     lempeck,
# #     qeynos,
# #     bixies,
# #     comb_holder,
# #     npc_2
# # ]
