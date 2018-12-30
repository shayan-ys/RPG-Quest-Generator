from Grammar.actions import NonTerminals as NT, Terminals as T

from World.Types.Item import Item, ItemTypes, GenericItem
from World.Types.Intel import Intel, IntelTypes, Spell
from World.Types.Place import Place
from World.Types.Person import Clan, NPC, Motivation, Player
from World.Types.BridgeModels import Need, Exchange, NPCKnowledgeBook, PlayerKnowledgeBook, ReadableKnowledgeBook
from World.Types.Names import NPCName, ItemName, PlaceName, SpellName


def create():
    alliance = Clan.create(name='alliance')
    horde = Clan.create(name='horde')

    beach = Place.create(name='beach', x=10, y=80)
    azshara = Place.create(name='azshara', x=50, y=50)
    cataclysm = Place.create(name='cataclysm', x=70, y=90)
    crystalsong = Place.create(name='crystalsong', x=10, y=60)
    forest = Place.create(name='forest', x=60, y=20)
    dalaran = Place.create(name='dalaran', x=80, y=85)
    feralas = Place.create(name='feralas', x=10, y=10)
    harbor = Place.create(name='harbor', x=80, y=10)
    shrine = Place.create(name='shrine', x=30, y=80)
    nagrand = Place.create(name='nagrand', x=70, y=40)
    acherus = Place.create(name='acherus', x=10, y=40)
    alcaz = Place.create(name='alcaz', x=90, y=60)

    PlaceName.create(name='hamilton')
    PlaceName.create(name='denver')
    PlaceName.create(name='munich')
    PlaceName.create(name='quebec')

    player = Player.create(name='player_1', place=beach, clan=alliance)

    qeynos = NPC.create(name='qeynos', place=azshara, clan=alliance)
    npc_2 = NPC.create(name='npc2', place=beach, clan=alliance)  # = adon
    steve = NPC.create(name='steve', place=forest, clan=alliance)
    tomas = NPC.create(name='tomas', place=feralas, clan=alliance)
    lempeck = NPC.create(name='lempeck', place=harbor, clan=alliance, health_meter=0.7)  # = Denros
    bixies = NPC.create(name='bixies', place=cataclysm, clan=horde)
    goblin = NPC.create(name='goblin', place=dalaran, clan=horde)

    NPCName.create(name='gabriel')
    NPCName.create(name='mariah')
    NPCName.create(name='sia')
    NPCName.create(name='silva')
    NPCName.create(name='berg')
    NPCName.create(name='jessie')
    NPCName.create(name='lizzy')
    NPCName.create(name='amanda')
    NPCName.create(name='bernard')
    NPCName.create(name='monica')
    NPCName.create(name='catrina')
    NPCName.create(name='leo')
    NPCName.create(name='richard')
    NPCName.create(name='naomi')
    NPCName.create(name='aaron')

    Motivation.create(npc=steve, action=NT.knowledge.value, motive=0.6)
    Motivation.create(npc=lempeck, action=NT.comfort.value, motive=0.9)
    Motivation.create(npc=npc_2, action=NT.reputation.value, motive=0.7)
    Motivation.create(npc=goblin, action=NT.serenity.value, motive=0.7)
    Motivation.create(npc=tomas, action=NT.protection.value, motive=0.7)
    Motivation.create(npc=qeynos, action=NT.conquest.value, motive=0.7)

    potion = Item.create(type=ItemTypes.tool.name, generic=GenericItem.get_or_create(name=ItemTypes.singleton.name)[0], name='potion', place=None, belongs_to=qeynos, usage=T.treat.value, impact_factor=0.5)
    jum = Item.create(type=ItemTypes.unknown.name, generic=GenericItem.get_or_create(name='jum')[0], name='jum', place=None, belongs_to=npc_2)
    comb = Item.create(type=ItemTypes.unknown.name, generic=GenericItem.get_or_create(name='comb')[0], name='comb', place=None, belongs_to=bixies)
    bandage = Item.create(type=ItemTypes.tool.name, generic=GenericItem.get_or_create(name='bandage')[0], name='bandage', place=crystalsong, belongs_to=None, usage=T.treat.value)
    address_book = Item.create(type=ItemTypes.readable.name, generic=GenericItem.get_or_create(name=ItemTypes.singleton.name)[0], name='address_book', belongs_to=tomas)  # address-book (goblin loc)
    coin = Item.create(type=ItemTypes.unknown.name, generic=GenericItem.get_or_create(name='coin')[0], name='coin', belongs_to_player=player)

    Need.create(npc=lempeck, item=potion)

    spell = Intel.construct(spell=Spell.create(name="needs_path",
                                               text="'Earth, grass, trees and seeds reveal the path to suit my needs'"))
    spell_2 = Intel.construct(spell=Spell.create(name="flat_earth", text="Earth is flat! LoL"))
    spell_3 = Intel.construct(spell=Spell.create(name="gravity", text="Gravity is a myth"))

    # SpellName.create()

    NPCKnowledgeBook.create(npc=goblin, intel=spell)
    NPCKnowledgeBook.create(npc=bixies, intel=spell_2)
    NPCKnowledgeBook.create(npc=steve, intel=spell_2)

    intel_bandage_loc = Intel.construct(item_place=bandage)
    intel_npc2_loc = Intel.construct(npc_place=npc_2, worth=0.6)

    intel_goblin_loc = Intel.construct(npc_place=goblin, worth=0.8)
    ReadableKnowledgeBook.create(readable=address_book, intel=intel_goblin_loc)

    intel_tomas_loc = Intel.construct(npc_place=tomas)
    NPCKnowledgeBook.create(npc=bixies, intel=intel_tomas_loc)
    NPCKnowledgeBook.create(npc=lempeck, intel=intel_tomas_loc)

    intel_lempeck_loc = Intel.construct(npc_place=lempeck)
    NPCKnowledgeBook.create(npc=qeynos, intel=intel_lempeck_loc)

    intel_qeynos_loc = Intel.construct(npc_place=qeynos)
    NPCKnowledgeBook.create(npc=npc_2, intel=intel_qeynos_loc)

    intel_comb_place = Intel.construct(item_place=comb)
    NPCKnowledgeBook.create(npc=npc_2, intel=intel_comb_place)

    intel_cataclysm = Intel.construct(npc_place=bixies)
    NPCKnowledgeBook.create(npc=npc_2, intel=intel_cataclysm)

    Exchange.create(npc=qeynos, item=potion, need=Need.get_or_create(npc=qeynos, item=jum)[0])
    Exchange.create(npc=npc_2, intel=intel_comb_place, need=Need.get_or_create(npc=npc_2, item=bandage)[0])
    Exchange.create(npc=npc_2, intel=intel_cataclysm, need=Need.get_or_create(npc=npc_2, item=bandage)[0])
    Exchange.create(npc=npc_2, item=jum, need=Need.get_or_create(npc=npc_2, item=comb)[0])
    Exchange.create(npc=tomas, item=address_book, need=Need.get_or_create(npc=tomas, item=coin)[0])

    for place in Place.select():
        intel = Intel.construct(place_location=place)
        PlayerKnowledgeBook.create(player=player, intel=intel)

    PlayerKnowledgeBook.create(player=player, intel=intel_npc2_loc)
    # PlayerKnowledgeBook.create(player=player, intel=Intel.construct(npc_place=steve))
