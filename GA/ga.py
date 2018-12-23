from GA.crossovers import crossover
from GA.fitness import fitness
from GA.operators import quest_generator
from Grammar.tree import Node
from Grammar.actions import NonTerminals as NT
from Data.statics import GAParams
from helper import grouped

import numpy as np
from datetime import datetime, timedelta


class Individual:
    """
    GA individual in the evolving population, the quest tree and its fitness
    """
    tree = None     # type: Node
    score = 0.0   # type: float

    def __init__(self, tree: Node, score: float=None):
        self.tree = tree
        if score:
            self.score = score
        else:
            self.evaluate()

    def validate(self) -> bool:
        """
        If quest is a correct one, not too small not too big
        :return:
        """
        if self.tree.depth <= 2 or self.tree.depth >= 900:
            return False
        return True

    def evaluate(self) -> float:
        """
        If the quest is not valid, set fitness to 0, else calculate using GA.fitness
        :return: calculated fitness
        """
        if not self.validate():
            self.score = 0
        else:
            self.score = fitness(self.tree)
        return self.score

    def __str__(self):
        return 'score: %.4f' % self.score + ' | ' + str(self.tree)

    def __repr__(self):
        return self.__str__()


def init(pop_size: int=50, quest_rule_number: int=None) -> list:
    """
    Initial population of individual quests generated automatically (randomly)
    :param pop_size: desired population size
    :param quest_rule_number: rule number for quest, limiting options
    :return: list of individuals, the population
    """
    pop = []
    for i in range(pop_size):
        for depth_tries in range(100):
            tree = quest_generator(NT.quest, quest_rule_number)
            ind = Individual(tree)
            if ind.score > 0.0:
                pop.append(Individual(tree))
                break

    return pop


def generation(population: list) -> list:
    """
    Evolve one generation only, gets the population, return new population including created offspring and mutated
    individuals
    :param population: population from generation number n
    :return: population for generation number n+1
    """
    # select parents
    if not population or len(population) < 2:
        return []
    parents_pool = np.random.choice(population, max(2, int(GAParams.selection_factor * len(population))), replace=False)

    # recombine
    new_gen = []
    for parent_1, parent_2 in grouped(parents_pool, 2):
        result = crossover(parent_1.tree, parent_2.tree)
        if result:
            child_1, child_2 = result
            new_gen += [Individual(child_1), Individual(child_2)]

    population += new_gen

    # mutation
    mutant_pop_indices = np.random.choice(list(range(len(population))), int(GAParams.mutation_factor * len(population)),
                                          replace=False)
    for mute_index in mutant_pop_indices:
        result = crossover(population[mute_index].tree, quest_generator(NT.quest))
        if result:
            mutant, nothing = result
            mutant.update_metrics()
            population[mute_index].tree = mutant
            population[mute_index].evaluate()

    # evaluate
    sorted_pop = []
    for individual in population:
        insert_index = 0
        for sorted_indv in sorted_pop:
            if individual.score >= sorted_indv.score:
                break
            insert_index += 1
        sorted_pop.insert(insert_index, individual)

    return sorted_pop


def run(generations_count: int=None, pop_size: int=None, quest_rule_number: int=None) -> list:
    """
    Run GA application, creates a population of given size 'pop_size' and evolve through given number of generations
    :param generations_count: number of generations to be evolved
    :param pop_size: population size, initially through out the evolution and return
    :param quest_rule_number: quest rule number (motivation) to limit population quest types
    :return: population of given size evolved given number of times
    """
    if not generations_count:
        generations_count = GAParams.generation_count
    if not pop_size:
        pop_size = GAParams.population_size

    population = init(pop_size=pop_size, quest_rule_number=quest_rule_number)

    start_time = datetime.now()
    diff = None
    diff_i = None
    for i in range(generations_count):
        population = generation(population)[:pop_size]
        if len(population) < pop_size:
            population += init(pop_size=pop_size - len(population))

        if int(100 * i / generations_count) % 20 == 0 and i:
            if diff is None:
                diff = datetime.now() - start_time
                diff_i = i
            remaining_secs = diff.total_seconds() * ((generations_count - i) / diff_i)
            print(str(int(100 * i / generations_count)) + "% progressed | remaining time:", str(timedelta(seconds=remaining_secs)))

    print("------ finished ------ process time:", str(datetime.now() - start_time), "------")
    return population
