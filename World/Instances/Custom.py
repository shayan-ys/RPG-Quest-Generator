from Grammar.actions import NonTerminals as NT

from World.elements import Element as Elem
from World.properties import Location
from World.types import NPC, IntelLocation, IntelSpell, Place, Readable


location_1 = Location(10, 10)

place_1 = Elem(Place, 'place_1')
place_1.type.location = location_1

good_1 = Elem(NPC, 'good_1')
good_1.type.motivations = {
    NT.knowledge: 0.7
}
good_1.type.place = place_1

intel_1 = Elem(IntelLocation, 'intel_1')
intel_1.type.value = location_1

intel_2 = Elem(IntelSpell, 'intel_2')
intel_2.type.value = "Spell!"

location_2 = Location(10, 90)

place_2 = Elem(Place, 'place_2')
place_2.type.location = location_2

good_2 = Elem(NPC, 'good_2')
good_2.type.intel = [
    intel_2
]
good_2.type.place = place_2

intel_3 = Elem(IntelLocation, 'intel_3')
intel_3.type.value = location_2

book_1 = Elem(Readable, 'book_1')
book_1.type.intel = [
    intel_3
]

location_3 = Location(90, 90)

place_3 = Elem(Place, 'place_3')
place_3.type.location = location_3

intel_4 = Elem(IntelLocation, 'intel_4')
intel_4.type.value = location_3

bad_1 = Elem(NPC, 'bad_1')
bad_1.type.place = place_3
bad_1.type.belongings = [
    book_1
]

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
