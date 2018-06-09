from Data.quests import arbitrary_quest1, arbitrary_quest2, cure, small_goto, tiny_goto
from Grammar.operators import flat_non_terminals_subtrees, replace_node_by_path
from Grammar.serializers import write_file
# from Logger import logger
# logger.name = __name__


subtrees, node_types, paths = flat_non_terminals_subtrees(cure)

# for index in range(len(subtrees)):
#     print('================================== %d ================' % index)
#     print(node_types[index])
#     print(paths[index])
# 0010 = 6

new = replace_node_by_path(arbitrary_quest2, [0], tiny_goto)
print(new.pretty_string())

new_2 = replace_node_by_path(arbitrary_quest1, [0, 0], small_goto)
print(new_2)

prev_flatten = cure.flatten
new_cure = replace_node_by_path(cure, paths[6], tiny_goto)
print(new_cure)

after_flatten = cure.flatten

print('prev_flatten len = %d' % len(prev_flatten))
print('after_flatten len = %d' % len(after_flatten))

write_file(new_cure)
