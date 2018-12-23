from Data import quests

from GA import ga

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

import random

list_of_models = Place.list_of_models + Person.list_of_models + Item.list_of_models + Intel.list_of_models \
                 + BridgeModels.list_of_models
print(list_of_models)

db.close()
db.connect()
db.drop_tables(list_of_models)
db.create_tables(list_of_models)
Everquest.create()

random.seed(3)

Play().cmdloop()

db.close()
