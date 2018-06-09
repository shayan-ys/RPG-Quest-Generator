from Grammar.tree import Node
from Data.statics import GAParams, XP
from helper import nwise, bell_curve

from collections import Counter


def pattern_finder(items: list, pat_length: int=2, min_repeat: int=2, in_order: bool=True) -> (int, int):
    """
    Finds number of patterns with the given length, as described in Prof Winter paper, section III part A (Fitness)
    :param items: flatten quest nodes: look into Grammar/tree.py , flat()
    :param pat_length: length of pattern to look for
    :param min_repeat: minimum number of repeats to consider a repetition pattern, default=2
    :param in_order: (a, b) and (b, a) is not a pattern, if 'in_order' is set to True
    :return: (r, s): number of different patterns 's' that occur 'r'-times within the event sequence of the quest
    """

    repeats_list = []
    found_indices = []

    for index, comp_base in enumerate(nwise(items, n=pat_length)):

        if index in found_indices:
            """ this pattern is already counted, nothing new will be found here. => skip """
            continue
        repeats = 1

        for index_needle, comp_needle in enumerate(nwise(items[index+1:], n=pat_length)):
            if (in_order and comp_base == comp_needle) or (not in_order and set(comp_base) == set(comp_needle)):
                repeats += 1
                found_indices.append(index_needle)

        if repeats >= min_repeat:
            repeats_list.append(repeats)

    return [(r, s) for r, s in Counter(repeats_list).items()]


def repetition_factor(flatten_events: list, pattern_min_length: int=2, pattern_max_length: int=None) -> float:
    """
    Calculating repetition factor as described in Prof Winter paper, section III part A (Fitness)
    By calling 'pattern_finder' function looking for patterns with length from 'pattern_min_length'
    to 'pattern_max_length', summing up the results. sum (n * r * s)
    :param flatten_events: flatten quest nodes: look into Grammar/tree.py , flat()
    :param pattern_min_length: start of n
    :param pattern_max_length: end of n
    :return: repetition factor: sum (n * r * s)
    """
    if not pattern_max_length:
        pattern_max_length = int(len(flatten_events) / 2)

    q = 0
    for n in range(pattern_min_length, pattern_max_length):
        for r, s in pattern_finder(flatten_events, pat_length=n, min_repeat=2):
            q += n * r * s

    return q


def length_event(event) -> int:
    """
    Every event has same length of 1
    :param event:
    :return: 1
    """
    return 1


def fitness_sum(quest: Node, bell_curve_enabled: bool=True) -> float:
    """
    Calculates fitness based on average of 3 factors
    - Repetition factor: calculates using 'repetition_factor' function
    - Length factor: sum of lengths of each event using 'length_event'
    - XP factor: experience valud of each event, based on the chart in 'statics.py' , 'XP' class
    :param quest: the quest, which fitness is being calculated for
    :param bell_curve_enabled: to apply bell-curve-like function on results of each factor or not
    :return: quest's fitness
    """

    bell = GAParams.Fitness.BellCurves

    rep_fact = repetition_factor(quest.flatten, pattern_max_length=4)
    len_fact = sum(map(length_event, quest.flatten))
    xp_fact = sum(map(XP.terminal_map, quest.flatten))

    if bell_curve_enabled:
        rep_fact = bell_curve(rep_fact, **bell.rep_fact.items())
        len_fact = bell_curve(len_fact, **bell.len_fact.items())
        xp_fact = bell_curve(xp_fact, **bell.xp_fact.items())

    return (rep_fact + len_fact + xp_fact) / 3
