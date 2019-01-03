import Grammar.tree
from Data import quests, statics

import anytree
from anytree.exporter import DotExporter

from copy import copy


def build_anytree(grammar_root: Grammar.tree.Node, parent: anytree.Node = None,
                  semantics_indices: dict={}, current_level_index: int=None):

    if grammar_root.branches:
        name = "-%s-\nNT.%s[%s]" % (grammar_root.index, grammar_root.action.name, grammar_root.rule)
    else:
        name = "-%s-\nT.%s" % (grammar_root.index, grammar_root.action.name)

    if semantics_indices:
        semantic_index = grammar_root.index
        if semantic_index == current_level_index:
            prefix = ">> "
        elif semantic_index < current_level_index:
            prefix = "* "
        else:
            prefix = ""
        try:
            name += "\n%s%s" % (prefix, semantics_indices[semantic_index])
        except (KeyError, IndexError) as e:
            pass

    anytree_node = anytree.Node(name, parent=parent)

    if grammar_root.branches:
        for i, branch in enumerate(grammar_root.branches):
            build_anytree(grammar_root=branch, parent=anytree_node,
                          semantics_indices=semantics_indices, current_level_index=current_level_index)

    return anytree_node


def export_grammar_plot(quest: Grammar.tree.Node=None):

    if not quest:
        quest = quests.spy
        quest.set_indices()
    grammar = build_anytree(grammar_root=quest)

    if statics.Playground.debug_mode:
        for pre, fill, node in anytree.RenderTree(grammar):
            print("%s%s" % (pre, str(node.name).replace("\n", " ")))

    DotExporter(grammar).to_picture("Results/Trees/grammar.png")


def export_semantics_plot(quest: Grammar.tree.Node=None, semantics_indices: dict={}, current_level_index: int=None):

    if not quest:
        quest = quests.spy
        quest.set_indices()
    semantics_indices_copy = copy(semantics_indices)
    semantics = build_anytree(grammar_root=quest, semantics_indices=semantics_indices_copy,
                              current_level_index=current_level_index)

    DotExporter(semantics).to_picture("Results/Trees/semantics.png")
