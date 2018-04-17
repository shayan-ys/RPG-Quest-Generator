from actions import T

xp_values = {
    0: [T.null, T.goto, T.stealth, T.take],
    1: [T.capture, T.damage, T.defend],
    2: [T.exchange, T.escort],
    3: [T.experiment, T.repair, T.report],
    4: [T.gather, T.give, T.explore, T.listen, T.read, T.spy, T.use],
    5: [T.kill]
}

terminal_xp = {}


def init():
    for xp, terminals in xp_values.items():
        for term in terminals:
            terminal_xp[term] = xp


def terminal_xp_map(terminal: T):
    if type(terminal) != T:
        return 0
    if not terminal_xp:
        init()
    return terminal_xp[terminal]
