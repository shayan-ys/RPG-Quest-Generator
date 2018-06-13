from GA.ga import *


pop = run(generations_count=200, pop_size=300)
for ind in pop[:12]:
    print(ind)
