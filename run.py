from data.quests import arbitrary_quest2
from Grammar.serializers import deserialize_tree_json_str, write_file


# print(serialize_tree(arbitrary_quest2))

# json_string = json.dumps(arbitrary_quest2, default=serialize_tree)
# print(json_string)

# tree_dict = serialize_tree(arbitrary_quest2)
# print(type(tree_dict))
# print(tree_dict)
#
# tree = deserialize_tree_json(tree_dict)
# print(type(tree))
# print(tree)

# tree_dict = json.loads(json_string)
# tree = deserialize_tree_json(tree_dict)
#
# print(type(tree))
# print(tree)

print(arbitrary_quest2)

write_file(arbitrary_quest2)
# tree_json_str = str(arbitrary_quest2)
#
# tree = deserialize_tree_json_str(tree_json_str)
# print(tree)
