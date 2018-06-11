from Data.quests import arbitrary_quest1, arbitrary_quest2, arbitrary_quest3, cure, spy, small_goto, tiny_goto
from Grammar.serializers import write_file, deserialize_tree_json_str
from Grammar.operators import replace_node_by_path, get_node_by_path
from GA.operators import quest_generator, crossover_flatten
from GA.fitness import fitness_sum
from copy import copy, deepcopy
import random

# depths = []
#
# for i in range(1000):
#     tree = quest_generator()
#     depths.append(tree.depth)
#     if tree.depth <= 2:
#         print(tree.pretty_string())
#         print('fitness = %.2f' % fitness_sum(tree))
#
#
# print('max = %d' % max(depths))
# print('min = %d' % min(depths))
# print('avg = %.1f' % (sum(depths) / len(depths)))

parent1 = cure
parent2 = spy

result = crossover_flatten(parent1, parent2)
if result:
    print(parent1.pretty_string())
    print(parent2.pretty_string())
    print('-- children --')
    child1, child2 = result
    if child1 == parent1:
        print("= parent1")
    else:
        print(child1)
    if child2 == parent2:
        print("= parent2")
    else:
        print(child2)
else:
    print('Failed')

print('----')

# parent_t = deserialize_tree_json_str('{"action_str": "NonTerminals.quest", "rule": 5, "branches": [{"action_str": "NonTerminals.protection", "rule": 2, "branches": [{"action_str": "NonTerminals.get", "rule": 4, "branches": [{"action_str": "NonTerminals.goto", "rule": 3, "branches": [{"action_str": "NonTerminals.learn", "rule": 1, "branches": [{"action_str": "Terminals.null", "rule": null, "branches": [], "action": 1, "terminal": true}], "action": 13, "terminal": false}, {"action_str": "Terminals.goto", "rule": null, "branches": [], "action": 11, "terminal": true}], "action": 12, "terminal": false}, {"action_str": "NonTerminals.get", "rule": 4, "branches": [{"action_str": "NonTerminals.goto", "rule": 3, "branches": [{"action_str": "NonTerminals.learn", "rule": 4, "branches": [{"action_str": "NonTerminals.get", "rule": 3, "branches": [{"action_str": "NonTerminals.goto", "rule": 3, "branches": [{"action_str": "NonTerminals.learn", "rule": 1, "branches": [{"action_str": "Terminals.null", "rule": null, "branches": [], "action": 1, "terminal": true}], "action": 13, "terminal": false}, {"action_str": "Terminals.goto", "rule": null, "branches": [], "action": 11, "terminal": true}], "action": 12, "terminal": false}, {"action_str": "Terminals.gather", "rule": null, "branches": [], "action": 9, "terminal": true}], "action": 14, "terminal": false}, {"action_str": "NonTerminals.sub_quest", "rule": 1, "branches": [{"action_str": "NonTerminals.goto", "rule": 3, "branches": [{"action_str": "NonTerminals.learn", "rule": 1, "branches": [{"action_str": "Terminals.null", "rule": null, "branches": [], "action": 1, "terminal": true}], "action": 13, "terminal": false}, {"action_str": "Terminals.goto", "rule": null, "branches": [], "action": 11, "terminal": true}], "action": 12, "terminal": false}], "action": 11, "terminal": false}, {"action_str": "Terminals.give", "rule": null, "branches": [], "action": 10, "terminal": true}, {"action_str": "Terminals.listen", "rule": null, "branches": [], "action": 13, "terminal": true}], "action": 13, "terminal": false}, {"action_str": "Terminals.goto", "rule": null, "branches": [], "action": 11, "terminal": true}], "action": 12, "terminal": false}, {"action_str": "NonTerminals.get", "rule": 2, "branches": [{"action_str": "NonTerminals.steal", "rule": 2, "branches": [{"action_str": "NonTerminals.goto", "rule": 1, "branches": [{"action_str": "Terminals.null", "rule": null, "branches": [], "action": 1, "terminal": true}], "action": 12, "terminal": false}, {"action_str": "NonTerminals.kill", "rule": 1, "branches": [{"action_str": "NonTerminals.goto", "rule": 1, "branches": [{"action_str": "Terminals.null", "rule": null, "branches": [], "action": 1, "terminal": true}], "action": 12, "terminal": false}, {"action_str": "Terminals.kill", "rule": null, "branches": [], "action": 12, "terminal": true}], "action": 18, "terminal": false}, {"action_str": "Terminals.take", "rule": null, "branches": [], "action": 19, "terminal": true}], "action": 15, "terminal": false}], "action": 14, "terminal": false}, {"action_str": "NonTerminals.sub_quest", "rule": 1, "branches": [{"action_str": "NonTerminals.goto", "rule": 1, "branches": [{"action_str": "Terminals.null", "rule": null, "branches": [], "action": 1, "terminal": true}], "action": 12, "terminal": false}], "action": 11, "terminal": false}, {"action_str": "NonTerminals.goto", "rule": 3, "branches": [{"action_str": "NonTerminals.learn", "rule": 1, "branches": [{"action_str": "Terminals.null", "rule": null, "branches": [], "action": 1, "terminal": true}], "action": 13, "terminal": false}, {"action_str": "Terminals.goto", "rule": null, "branches": [], "action": 11, "terminal": true}], "action": 12, "terminal": false}, {"action_str": "Terminals.exchange", "rule": null, "branches": [], "action": 6, "terminal": true}], "action": 14, "terminal": false}, {"action_str": "NonTerminals.sub_quest", "rule": 1, "branches": [{"action_str": "NonTerminals.goto", "rule": 1, "branches": [{"action_str": "Terminals.null", "rule": null, "branches": [], "action": 1, "terminal": true}], "action": 12, "terminal": false}], "action": 11, "terminal": false}, {"action_str": "NonTerminals.goto", "rule": 3, "branches": [{"action_str": "NonTerminals.learn", "rule": 1, "branches": [{"action_str": "Terminals.null", "rule": null, "branches": [], "action": 1, "terminal": true}], "action": 13, "terminal": false}, {"action_str": "Terminals.goto", "rule": null, "branches": [], "action": 11, "terminal": true}], "action": 12, "terminal": false}, {"action_str": "Terminals.exchange", "rule": null, "branches": [], "action": 6, "terminal": true}], "action": 14, "terminal": false}, {"action_str": "NonTerminals.goto", "rule": 3, "branches": [{"action_str": "NonTerminals.learn", "rule": 1, "branches": [{"action_str": "Terminals.null", "rule": null, "branches": [], "action": 1, "terminal": true}], "action": 13, "terminal": false}, {"action_str": "Terminals.goto", "rule": null, "branches": [], "action": 11, "terminal": true}], "action": 12, "terminal": false}, {"action_str": "Terminals.use", "rule": null, "branches": [], "action": 20, "terminal": true}], "action": 6, "terminal": false}], "action": 1, "terminal": false}')
# parent_orig = deepcopy(parent_t)
# print(parent_t)
# write_file(parent_t)
# path_t = [0, 0, 3]
# replace_by = deserialize_tree_json_str('{"action_str": "NonTerminals.goto", "rule": 3, "branches": [{"action_str": "NonTerminals.learn", "rule": 2, "branches": [{"action_str": "NonTerminals.goto", "rule": 3, "branches": [{"action_str": "NonTerminals.learn", "rule": 2, "branches": [{"action_str": "NonTerminals.goto", "rule": 3, "branches": [{"action_str": "NonTerminals.learn", "rule": 2, "branches": [{"action_str": "NonTerminals.goto", "rule": 3, "branches": [{"action_str": "NonTerminals.learn", "rule": 1, "branches": [{"action_str": "Terminals.null", "rule": null, "branches": [], "action": 1, "terminal": true}], "action": 13, "terminal": false}, {"action_str": "Terminals.goto", "rule": null, "branches": [], "action": 11, "terminal": true}], "action": 12, "terminal": false}, {"action_str": "NonTerminals.sub_quest", "rule": 1, "branches": [{"action_str": "NonTerminals.goto", "rule": 1, "branches": [{"action_str": "Terminals.null", "rule": null, "branches": [], "action": 1, "terminal": true}], "action": 12, "terminal": false}], "action": 11, "terminal": false}, {"action_str": "Terminals.listen", "rule": null, "branches": [], "action": 13, "terminal": true}], "action": 13, "terminal": false}, {"action_str": "Terminals.goto", "rule": null, "branches": [], "action": 11, "terminal": true}], "action": 12, "terminal": false}, {"action_str": "NonTerminals.sub_quest", "rule": 1, "branches": [{"action_str": "NonTerminals.goto", "rule": 1, "branches": [{"action_str": "Terminals.null", "rule": null, "branches": [], "action": 1, "terminal": true}], "action": 12, "terminal": false}], "action": 11, "terminal": false}, {"action_str": "Terminals.listen", "rule": null, "branches": [], "action": 13, "terminal": true}], "action": 13, "terminal": false}, {"action_str": "Terminals.goto", "rule": null, "branches": [], "action": 11, "terminal": true}], "action": 12, "terminal": false}, {"action_str": "NonTerminals.sub_quest", "rule": 1, "branches": [{"action_str": "NonTerminals.goto", "rule": 1, "branches": [{"action_str": "Terminals.null", "rule": null, "branches": [], "action": 1, "terminal": true}], "action": 12, "terminal": false}], "action": 11, "terminal": false}, {"action_str": "Terminals.listen", "rule": null, "branches": [], "action": 13, "terminal": true}], "action": 13, "terminal": false}, {"action_str": "Terminals.goto", "rule": null, "branches": [], "action": 11, "terminal": true}], "action": 12, "terminal": false}')
#
# orig_node = get_node_by_path(parent_t, path_t)
# print(orig_node)
# print("orig_node == replace_by: %s " % str(orig_node == replace_by))
# print(replace_by)
#
# child_t = replace_node_by_path(parent_t, path_t, replace_by)
# print(child_t)
#
# print("parent_t == child_t: %s" % str(parent_t == child_t))
