from GA.ga import *


pop = run(generations_count=300, pop_size=200)
for ind in pop[:12]:
    print(ind)
