from ga import ga_run

# print("----- cure -----")
# print(list_to_str(cure.flatten))
#
# print("repr_factor= " + str(repetition_factor(cure.flatten, pattern_max_length=3)))
# print("length_factor= " + str(sum(map(length_event, cure.flatten))))
# print("xp_factor= " + str(sum(map(terminal_xp_map, cure.flatten))))
# print("occurrence_factor= " + str(cure.flatten.count(T.kill)))
#
# f_cure = (
#              bell_curve(repetition_factor(cure.flatten, pattern_max_length=4), opt_value=0, scaling_value=(1/1024)) +
#              bell_curve(sum(map(length_event, cure.flatten)), opt_value=24, scaling_value=(1/8)) +
#              bell_curve(sum(map(terminal_xp_map, cure.flatten)), opt_value=25, scaling_value=(1/8))
#          ) / 3
#
# print("fitness: cure= " + str(f_cure))
#
# print("----- spy -----")
# print(list_to_str(spy.flatten))
# print("repr_factor= " + str(repetition_factor(spy.flatten, pattern_max_length=3)))
# print("length_factor= " + str(sum(map(length_event, spy.flatten))))
# print("xp_factor= " + str(sum(map(terminal_xp_map, spy.flatten))))
# print("occurrence_factor= " + str(spy.flatten.count(T.kill)))
#
# f_spy = (
#              bell_curve(repetition_factor(spy.flatten, pattern_max_length=4), opt_value=0, scaling_value=(1/1024)) +
#              bell_curve(sum(map(length_event, spy.flatten)), opt_value=27, scaling_value=(1/8)) +
#              bell_curve(sum(map(terminal_xp_map, spy.flatten)), opt_value=25, scaling_value=(1/8))
#          ) / 3
#
# print("fitness: spy= " + str(f_spy))
#
# print("------- flat non_terminals subtree - arbitrary quest 2 ------")
# flatten_subtrees_arbitrary_2, flatten_types_arbitrary_2, path_nodes_arbitrary_2 = flat_non_terminals_subtrees(arbitrary_quest2)
# print(flatten_types_arbitrary_2)
# print(["".join(map(str, path_ls)) for path_ls in path_nodes_arbitrary_2])
# for subtree in flatten_subtrees_arbitrary_2:
#     print(subtree)
#
# print("------- flat non_terminals subtree - arbitrary quest 1 ------")
# flatten_subtrees_arbitrary_1, flatten_types_arbitrary_1, path_nodes_arbitrary_1 = flat_non_terminals_subtrees(arbitrary_quest1)
# print(flatten_types_arbitrary_1)
# print(["".join(map(str, path_ls)) for path_ls in path_nodes_arbitrary_1])
# for subtree in flatten_subtrees_arbitrary_1:
#     print(subtree)
#
# print("------- find sub-tree - arbitrary quest 1 ------")
# steal_type_2 = Node(NT.steal, 2,
#                     Node(NT.goto, 1,
#                          Leaf(T.null)),
#                     Node(NT.kill, 1,
#                          Node(NT.goto, 1,
#                               Leaf(T.null)),
#                          Leaf(T.kill)),
#                     Leaf(T.take))
# subtree_arbitrary_1 = replace_node_by_path(arbitrary_quest1, [0, 0, 0, 1, 0], steal_type_2)
# print(subtree_arbitrary_1)
#
# # NonTerminals.quest(1):{NonTerminals.knowledge(3):{NonTerminals.goto(3):{NonTerminals.learn(3):{NonTerminals.goto(1):{Terminals.null}, NonTerminals.get(2):{NonTerminals.steal(1):{NonTerminals.goto(2):{Terminals.explore}, Terminals.stealth, Terminals.take}}, Terminals.read}, Terminals.goto}, Terminals.listen, NonTerminals.goto(1):{Terminals.null}, Terminals.report}}
# # NonTerminals.quest(1):{NonTerminals.knowledge(3):{NonTerminals.goto(3):{NonTerminals.learn(3):{NonTerminals.goto(1):{Terminals.null}, NonTerminals.get(2):{NonTerminals.steal(2):{NonTerminals.goto(1):{Terminals.null}, NonTerminals.kill(1):{NonTerminals.goto(1):{Terminals.null}, Terminals.kill}, Terminals.take}}, Terminals.read}, Terminals.goto}, Terminals.listen, NonTerminals.goto(1):{Terminals.null}, Terminals.report}}
#
# print("------- Crossover - arbitrary quest 1 & 2 ----------")
# spy_cure_child1, spy_cure_child2 = crossover_flatten(spy, cure)
# print(spy_cure_child1)
# print(spy_cure_child2)

# print("------- Random Generated Quest Tree --------")
# for i in range(500):
#     print("+++++ Quest " + str(i) + " +++++")
#     qs_rand_1 = quest_generator(NT.quest)
#     print(qs_rand_1)

# print("----- cure -----")
# f_cure_new = fitness_sum(cure, bell_curve_dict={
#     'rep_fact': {'opt_value': 0, 'scaling_value': (1/1024)},
#     'len_fact': {'opt_value': 24, 'scaling_value': (1/8)},
#     'xp_fact': {'opt_value': 25, 'scaling_value': (1/8)}
# })
# print("fitness (new): cure= " + str(f_cure_new))
#
# print("----- spy -----")
# f_spy_new = fitness_sum(spy, bell_curve_dict={
#     'rep_fact': {'opt_value': 0, 'scaling_value': (1/1024)},
#     'len_fact': {'opt_value': 27, 'scaling_value': (1/8)},
#     'xp_fact': {'opt_value': 25, 'scaling_value': (1/8)}
# })
# print("fitness (new): spy= " + str(f_spy_new))

# pop_0 = init(10)
# pop_1 = generation(pop_0)
pop = ga_run(generations_count=200, pop_size=50)

# for indv in pop:
#     print(indv)

print(pop[0])
print("len(" + str(len(pop)) + ")")

# a = [4, 1, 2, 5, 3, 6]
# sorted_a = []
#
# for aa in a:
#     i = 0
#     for sorted_aa in sorted_a:
#         if aa > sorted_aa:
#             break
#         i += 1
#     sorted_a.insert(i, aa)
#
# print(sorted_a)
