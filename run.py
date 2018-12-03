from Data import quests

from World.world import World
from World.Types import *
from World.Types import Place
from World.Types import Person
from World.Types import Item
from World.Types import Intel
from World.Types import BridgeModels

from World.Instances import Everquest, Custom
from Playground.play import Play

# from GA.ga import *
#
#
# pop = run(generations_count=200, pop_size=300)
# for ind in pop[:12]:
#     print(ind)

list_of_models = Place.list_of_models + Person.list_of_models + Item.list_of_models + Intel.list_of_models \
                 + BridgeModels.list_of_models
# + Item.list_of_models + Intel.list_of_models
print(list_of_models)

db.close()
db.connect()
db.drop_tables(list_of_models)
db.create_tables(list_of_models)
Everquest.create()

# world = World()
# world.parse_quest(quest=quests.cure)

# prg = Progress(quest=quests.cure)
# prg.get_narratives(prg.quest, [])
# prg.get_narratives(prg.quest.branches[0], prg.semantics_indices[1])
# prg.mission(0)
Play(quests.cure).cmdloop()

# intel = Intel.Intel.select().join(Place.Place, on=(Intel.Intel.npc_place == Person.NPC.id))\
#     .where(Intel.Intel.type == 'npc_place', Person.NPC.name == 'bixies').get()

print(intel)
db.close()
