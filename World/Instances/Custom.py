from Grammar.actions import NonTerminals as NT

from World.Types.Place import Place
from World.Types.Person import Clan, NPC, Motivation, Player
from World.Types.Intel import Intel, IntelTypes
from World.Types.Item import Item, ItemTypes
from World.Types.BridgeModels import NPCKnowledgeBook, ReadableKnowledgeBook, FavoursBook


def create():
    good_clan = Clan.create(name='good boys')
    bad_clan = Clan.create(name='bad boys')

    place_1 = Place.create(name='place_1', x=10, y=10)
    good_1 = NPC.create(name='good_1', place=place_1, clan=good_clan)
    good_1_motive = Motivation.create(npc=good_1, action=NT.knowledge.value, motive=0.7)

    intel_1 = Intel.create(type=IntelTypes.place.name, place=good_1.place)

    place_2 = Place.create(name='place_2', x=10, y=90)
    good_2 = NPC.create(name='good_2', place=place_2, clan=good_clan)
    intel_2 = Intel.create(type=IntelTypes.spell.name, spell='spell!')
    intel_npc_1 = NPCKnowledgeBook.create(intel=intel_2, npc=good_2)

    intel_3 = Intel.create(type=IntelTypes.place.name, place=good_2.place)

    place_3 = Place.create(name='place_3', x=90, y=90)

    bad_1 = NPC.create(name='bad_1', place=place_3, clan=bad_clan)

    book_1 = Item.create(type=ItemTypes.readable.name, name='book_1', belongs_to=bad_1)
    intel_readable_1 = ReadableKnowledgeBook.create(intel=intel_3, readable=book_1)

    intel_4 = Intel.create(type=IntelTypes.place.name, place=bad_1.place)
    # TODO: redundant
    intel_npc_2 = NPCKnowledgeBook.create(intel=intel_4, npc=good_1)

    player = Player.create(name='player_1', place=place_1)
