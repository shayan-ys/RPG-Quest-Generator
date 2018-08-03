from Data import quests
from Grammar.serializers import write_file

from World.world import World
from World.elements import triangle_dist_meter
from World.properties import Location

from math import acos, cos, degrees, radians
# from GA.ga import *
#
#
# pop = run(generations_count=200, pop_size=300)
# for ind in pop[:12]:
#     print(ind)

# world = World()
# world.parse_quest(quest=quests.spy)

source = Location(0, 0)
candid = Location(-1, -2)
laterd = Location(10, 0)

meter = triangle_dist_meter(src=source, dest=candid, later=laterd)
print(meter)
