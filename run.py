from Data import quests
from Grammar.serializers import write_file

from World.world import World
from World.elements import triangle_dist_meter
from World.properties import Location

# from GA.ga import *
#
#
# pop = run(generations_count=200, pop_size=300)
# for ind in pop[:12]:
#     print(ind)

world = World()
world.parse_quest(quest=quests.cure)
