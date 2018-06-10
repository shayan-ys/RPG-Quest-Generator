from Data.quests import arbitrary_quest1, arbitrary_quest2, cure, small_goto, tiny_goto
from Grammar.serializers import write_file
from GA.operators import quest_generator
from GA.fitness import fitness_sum

depths = []

for i in range(1000):
    tree = quest_generator()
    depths.append(tree.depth)
    if tree.depth <= 2:
        print(tree.pretty_string())
        print('fitness = %.2f' % fitness_sum(tree))


print('max = %d' % max(depths))
print('min = %d' % min(depths))
print('avg = %.1f' % (sum(depths) / len(depths)))
