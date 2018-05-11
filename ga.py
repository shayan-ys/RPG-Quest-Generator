from ga_operators import quest_generator, fitness_sum, crossover_flatten
from helper import grouped
from actions import NT, Node
from statics import ga_params as ga

import numpy as np


class Individual:
    tree = None     # type: Node
    fitness = 0.0   # type: float

    def __init__(self, tree: Node, fitness: float=None):
        if fitness is None:
            fitness = fitness_sum(tree)
        self.tree = tree
        self.fitness = fitness

    def evaluate(self):
        self.fitness = fitness_sum(self.tree)

    def __str__(self):
        return 'fitness: %.4f' % self.fitness + ' | ' + str(self.tree)

    def __repr__(self):
        return self.__str__()


def init(pop_size: 50):
    pop = []
    for i in range(pop_size):
        tree = quest_generator(NT.quest, depth=10)
        pop.append(Individual(tree))

    return pop


def generation(population: list):
    # select parents
    parents_pool = np.random.choice(population, int(ga['selection_factor']*len(population)), replace=False)

    # recombine
    new_gen = []
    for parent_1, parent_2 in grouped(parents_pool, 2):
        parent_1_tree = parent_1.tree
        parent_2_tree = parent_2.tree
        child_1, child_2 = crossover_flatten(parent_1_tree, parent_2_tree)
        new_gen += [Individual(child_1, 0), Individual(child_2, 0)]

    population += new_gen

    # mutation
    mutant_pop_indices = np.random.choice(list(range(len(population))), int(ga['mutation_factor']*len(population)),
                                          replace=False)
    for mute_index in mutant_pop_indices:
        population[mute_index].tree, nothing = crossover_flatten(population[mute_index].tree,
                                                                 quest_generator(NT.quest, depth=5))

    # evaluate
    sorted_pop = []
    for individual in population:
        individual.evaluate()
        insert_index = 0
        for sorted_indv in sorted_pop:
            if individual.fitness >= sorted_indv.fitness:
                break
            insert_index += 1
        sorted_pop.insert(insert_index, individual)

    return sorted_pop


def ga_run(generations_count: int=100, pop_size: int=50):
    population = init(pop_size=pop_size)

    for i in range(generations_count):
        population = generation(population)[:pop_size]

    return population
