from World.Types import *
from World.Types import Place, Person, Item, Intel, BridgeModels, Log, Names

from World.Instances import Everquest
from Playground.play import Play

import random

list_of_models = Place.list_of_models + Person.list_of_models + Item.list_of_models + Intel.list_of_models \
                 + BridgeModels.list_of_models + Log.list_of_models + Names.list_of_models
print(list_of_models)

db.close()
db.connect()
db.drop_tables(list_of_models)
db.create_tables(list_of_models)
Everquest.create()

random.seed(3)

Play().cmdloop()

db.close()
