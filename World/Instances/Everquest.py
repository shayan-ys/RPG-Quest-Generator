from Grammar.actions import NonTerminals as NT, Terminals as T

from World.properties import Location
from World.elements import NPC, Clan, IntelLocation, IntelSpell, IntelHolding, Place, UnknownItem, Tool, Readable, Coin


potion = Tool(name='potion', usage=T.treat)
jum = UnknownItem(name='jum')
comb = UnknownItem(name='comb')
# bondage = Tool(name='bondage', usage=T.treat)
bandage = UnknownItem(name='bandage')

rivervale = Place('Rivervale', location=Location(10, 80))
bandage_place = Place('bandage_place', Location(10, 60), items=[bandage])

steve = NPC(name='Steve', motivations={NT.knowledge: 0.6}, place=Place('steve_loc', Location(60, 20)))

intel_spell = IntelSpell('Magical Spell')
goblin = NPC('Goblin', motivations={}, place=Place('goblin_place', Location(80, 85)), intel=[intel_spell])

intel_goblin_loc = IntelLocation(goblin.place)
intel_goblin_loc.worth = 0.8
letter = Readable(name='address-book (goblin)', intel=[IntelLocation(goblin.place)])

tomas = NPC('NPC1 (Tomas)', motivations={NT.protection: 0.8}, place=Place('tomas_place', Location(10, 10)),
            belongings=[letter], exchange_motives={letter: Coin()})
intel_tomas_place = IntelLocation(tomas.place)
lempeck = NPC('lempeck (Denros)', motivations={}, place=Place('lempeck_hiding', location=Location(80, 10)),
              needs=[potion], intel=[intel_tomas_place])
intel_lempeck_place = IntelLocation(lempeck.place)
qeynos = NPC('Qeynos (Angie)', motivations={}, place=Place('qeynos_place', location=Location(50, 50)), belongings=[potion],
             needs=[jum], exchange_motives={potion: jum}, intel=[intel_lempeck_place])
intel_qeynos_place = IntelLocation(qeynos.place)

bixies = NPC('bixies', motivations={}, place=Place('bixies_place', location=Location(70, 90)), belongings=[comb])

bixies_place_intel = IntelLocation(bixies.place)
comb_holder = IntelHolding(comb, bixies)
npc_2 = NPC('NPC2 (adon)', motivations={}, place=rivervale, belongings=[jum], needs=[comb, bandage],
            intel=[comb_holder, intel_qeynos_place],
            exchange_motives={comb_holder: bandage, bixies_place_intel: bandage, jum: comb})


Clan([
    qeynos,
    lempeck,
    tomas,
    npc_2,
    steve
]).set_enemy(Clan([
        bixies,
        goblin
    ]))

player_pre_intel = [
    intel_lempeck_place,
    intel_qeynos_place,
    bixies_place_intel,
    IntelLocation(bandage_place),
    IntelLocation(rivervale),
    IntelLocation(steve.place)
]

player_starting_money = 4

elements = player_pre_intel + [

    intel_goblin_loc,
    intel_tomas_place,

    potion,
    jum,
    comb,
    bandage,
    letter,

    rivervale,
    bandage_place,

    steve,
    tomas,
    goblin,
    lempeck,
    qeynos,
    bixies,
    comb_holder,
    npc_2
]
