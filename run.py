from World.world import World
from Data import quests

# from GA.ga import *
#
#
# pop = run(generations_count=200, pop_size=300)
# for ind in pop[:12]:
#     print(ind)

world = World()
# print(world.str__actions_map())
world.parse_quest(quest=quests.arbitrary_quest1)
