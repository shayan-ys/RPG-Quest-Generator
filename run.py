from Data import quests

from World.world import World
from World.Types import *
from World.Types import Place
from World.Types import Person
from World.Types import Item
from World.Types import Intel
from World.Types import BridgeModels

from World.Narrative.actions import non_terminals
from World.Instances import Everquest, Custom
from Playground.play import Play
from Playground.info import print_player_intel

list_of_models = Place.list_of_models + Person.list_of_models + Item.list_of_models + Intel.list_of_models \
                 + BridgeModels.list_of_models
print(list_of_models)

db.close()
db.connect()
db.drop_tables(list_of_models)
db.create_tables(list_of_models)
Everquest.create()

# for i in range(1, 10):
#     print('running:', i)
#     non_terminals.capture_1(Item.Item.get_by_id(i))

Play().cmdloop()

db.close()
