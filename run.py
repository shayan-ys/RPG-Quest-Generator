from World.Types import *
from World.Types import Place, Person, Item, Intel, BridgeModels, Log, Names

from World.Instances import Everquest
from Playground.play import Play
from GA.ga import run
from Data import quests
from Grammar.plot import export_grammar_plot

import random

list_of_models = Place.list_of_models + Person.list_of_models + Item.list_of_models + Intel.list_of_models \
                 + BridgeModels.list_of_models + Log.list_of_models + Names.list_of_models
print(list_of_models)

db.close()
db.connect()
db.drop_tables(list_of_models)
db.create_tables(list_of_models)
Everquest.create()

# random.seed(3)
#
Play().cmdloop()

# run(generations_count=200, pop_size=25)
# quest = quests.arbitrary_quest3
# quest.set_indices()
# export_grammar_plot(quest)

db.close()
