from Grammar.actions import Terminals as T


# GA parameters
class GAParams:
    selection_factor = 0.4
    mutation_factor = 0.1
    maximum_quest_depth = 7
    generation_count = 100
    population_size = 80
    elite_group_size = 3

    print_progress_bar = True
    print_progress_split_count = 5
    record_statistics = False
    statistics_float_precision = 3

    class Fitness:
        class BellCurves:
            class Factors:
                def __init__(self, opt_value: int, scaling_value: float):
                    self.opt_value = opt_value
                    self.scaling_value = scaling_value

                def items(self) -> dict:
                    return {'opt_value': self.opt_value, 'scaling_value': self.scaling_value}

            rep_fact = Factors(opt_value=0, scaling_value=(1 / 1024))
            len_fact = Factors(opt_value=25, scaling_value=(1 / 8))
            xp_fact = Factors(opt_value=25, scaling_value=(1 / 8))


class XP:
    values = {
        0: [T.null, T.goto, T.stealth, T.take],
        1: [T.capture, T.damage, T.defend],
        2: [T.exchange, T.escort],
        3: [T.experiment, T.repair, T.report],
        4: [T.gather, T.give, T.explore, T.listen, T.read, T.spy, T.use],
        5: [T.kill]
    }
    terminal_xp_mapping = {}

    @staticmethod
    def create_map() -> None:
        for xp, terminals in XP.values.items():
            for term in terminals:
                XP.terminal_xp_mapping[term] = xp

    @staticmethod
    def terminal_map(terminal: T) -> int:

        if type(terminal) != T:
            return 0
        if not XP.terminal_xp_mapping:
            XP.create_map()
        return XP.terminal_xp_mapping[terminal]


class Playground:
    debug_mode = False
    max_level_skip_loop = 100
    default_damage_power = 0.3


class World:
    reachable_distance = 70
    minimum_distance = 10
