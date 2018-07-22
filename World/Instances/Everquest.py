from Grammar.actions import NonTerminals as NT, Terminals as T

from World.properties import Location
from World.elements import NPC, Clan, IntelLocation, IntelHolding, Place, UnknownObject, Tool


potion = Tool(name='potion', usage=T.treat)
jum = UnknownObject(name='jum')
comb = UnknownObject(name='comb')
# bondage = Tool(name='bondage', usage=T.treat)
bandage = UnknownObject(name='bandage')

rivervale = Place('Rivervale', location=Location(10, 80))
bandage_place = Place('bandage_place', Location(10, 60), items=[bandage])

npc_1 = NPC('NPC1', motivations={NT.protection: 0.8}, place=Place('npc_1_place', Location(10, 10)))
lempeck = NPC('lempeck', motivations={}, place=Place('lempeck_hiding', location=Location(80, 10)), needs=[potion])
qeynos = NPC('Qeynos', motivations={}, place=Place('qeynos_place', location=Location(50, 50)), belongings=[potion],
             needs=[jum], exchange_motives={potion: jum})

bixies = NPC('bixies', motivations={}, place=Place('bixies_place', location=Location(70, 90)), belongings=[comb])

bixies_place_intel = IntelLocation(bixies.place)
comb_holder = IntelHolding(comb, bixies)
npc_2 = NPC('NPC2', motivations={}, place=rivervale, belongings=[jum], needs=[comb, bandage], intel=[comb_holder],
            exchange_motives={comb_holder: bandage, bixies_place_intel: bandage, jum: comb})


Clan([
    qeynos,
    lempeck,
    npc_1,
    npc_2
]).set_enemy(Clan([
        bixies
    ]))

player_pre_intel = [
    IntelLocation(lempeck.place),
    IntelLocation(qeynos.place),
    bixies_place_intel,
    IntelLocation(bandage_place),
    IntelLocation(rivervale)
]

elements = player_pre_intel + [
    potion,
    jum,
    comb,
    bandage,

    rivervale,
    bandage_place,

    npc_1,
    lempeck,
    qeynos,
    bixies,
    comb_holder,
    npc_2
]
