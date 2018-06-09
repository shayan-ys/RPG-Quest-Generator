from Grammar.actions import Terminals as T


# GA parameters
class GAParams:
    selection_factor = 0.4
    mutation_factor = 0.1


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
