from GA.ga import *


pop = run(generations_count=500, pop_size=100)
for ind in pop[:7]:
    print(ind)
