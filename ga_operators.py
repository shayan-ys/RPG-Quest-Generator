from statics import terminal_xp_map
from helper import list_to_str, nwise, bell_curve
from quests import *
from collections import Counter


def pattern_finder(items: list, pat_length: int=2, min_repeat: int=2, in_order: bool=True) -> (int, int):

    repeats_list = []
    found_indices = []

    for index, comp_base in enumerate(nwise(items, n=pat_length)):

        if index in found_indices:
            # this pattern is already counted, nothing new will be found here. => skip!
            continue
        repeats = 1

        for index_needle, comp_needle in enumerate(nwise(items[index+1:], n=pat_length)):
            if (in_order and comp_base == comp_needle) or (not in_order and set(comp_base) == set(comp_needle)):
                # print(str(list(x.name for x in comp_base)) + " == " + str(list(x.name for x in comp_needle)))
                repeats += 1
                found_indices.append(index_needle)

        if repeats >= min_repeat:
            repeats_list.append(repeats)

    return [(r, s) for r, s in Counter(repeats_list).items()]


def repetition_factor(flatten_events: list, pattern_min_length: int=2, pattern_max_length: int=None) -> float:
    if not pattern_max_length:
        pattern_max_length = int(len(flatten_events) / 2)

    q = 0
    for n in range(pattern_min_length, pattern_max_length):
        for r, s in pattern_finder(flatten_events, pat_length=n, min_repeat=2):
            q += n * r * s

    return q


print(list_to_str(cure.flatten))

# patterns = pattern_finder(cure.flatten, pat_length=2, in_order=True)
# print(patterns)

print("repr_factor= " + str(repetition_factor(cure.flatten, pattern_max_length=3)))


def length_event(event) -> int:
    return 1


print("length_factor= " + str(sum(map(length_event, cure.flatten))))
print("xp_factor= " + str(sum(map(terminal_xp_map, cure.flatten))))
print("occurrence_factor= " + str(cure.flatten.count(T.kill)))
