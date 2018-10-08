from Data import quests

from World.world import World
from World.Types import *
from World.Types import Place
from World.Types import Person
from World.Types import Item
from World.Types import Intel
from World.Types import BridgeModels

from World.Instances import Everquest, Custom

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

db.connect()
db.drop_tables(list_of_models)
db.create_tables(list_of_models)
Everquest.create()

world = World()
world.parse_quest(quest=quests.spy)

db.close()
