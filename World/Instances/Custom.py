from Grammar.actions import NonTerminals as NT

from World.properties import Location
from World.elements import NPC, Clan, IntelLocation, IntelSpell, Place, Readable


place_1 = Place('place_1', Location(10, 10))

good_1 = NPC('good_1', motivations={NT.knowledge: 0.7}, place=place_1)

intel_1 = IntelLocation(good_1.place)

intel_2 = IntelSpell("Spell!")

place_2 = Place('place_2', Location(10, 90))

good_2 = NPC('good_2', motivations={}, place=place_2, intel=[intel_2])

intel_3 = IntelLocation(good_2.place)

book_1 = Readable('book_1', intel=[
    IntelLocation(good_2.place)
])

place_3 = Place('place_3', Location(90, 90))

bad_1 = NPC('bad_1', motivations={}, place=place_3, belongings=[book_1])

intel_4 = IntelLocation(bad_1.place)

Clan([
    good_1,
    good_2
]).set_enemy(Clan([
        bad_1
    ]))

player_pre_intel = [
    intel_1,
    intel_4
]

elements = [
    place_1,
    place_2,
    place_3,

    good_1,
    good_2,
    bad_1,

    intel_1,
    intel_2,
    intel_3,
    intel_4,

    book_1
]
