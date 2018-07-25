from Grammar.actions import Terminals as T
from Grammar.actions import NonTerminals as NT

rules = {
    NT.quest: {
        1: [NT.knowledge],
        2: [NT.comfort],
        3: [NT.reputation],
        4: [NT.serenity],
        5: [NT.protection],
        6: [NT.conquest],
        7: [NT.wealth],
        8: [NT.ability],
        9: [NT.equipment]
    },
    NT.knowledge: {
        1: [NT.get, NT.goto, T.give],
        2: [NT.spy],
        3: [NT.goto, T.listen, NT.goto, T.report],
        4: [NT.get, NT.goto, T.use, NT.goto, T.give]
    },
    NT.comfort: {
        1: [NT.get, NT.goto, T.give],
        2: [NT.goto, T.damage, NT.goto, T.report]
    },
    NT.reputation: {
        1: [NT.get, NT.goto, T.give],
        2: [NT.goto, NT.kill, NT.goto, T.report],
        3: [NT.goto, NT.goto, T.report]
    },
    NT.serenity: {
        1: [NT.goto, T.damage],
        2: [NT.get, NT.goto, T.use, NT.goto, T.give],
        3: [NT.get, NT.goto, T.use, T.capture, NT.goto, T.give],
        4: [NT.goto, T.listen, NT.goto, T.report],
        5: [NT.goto, T.take, NT.goto, T.give],
        6: [NT.get, NT.goto, T.give],
        7: [NT.goto, T.damage, T.escort, NT.goto, T.report]
    },
    NT.protection: {
        1: [NT.goto, T.damage, NT.goto, T.report],
        2: [NT.get, NT.goto, T.use],
        3: [NT.goto, T.repair],
        4: [NT.get, NT.goto, T.use],
        5: [NT.goto, T.damage]
    },
    NT.conquest: {
        1: [NT.goto, T.damage],
        2: [NT.goto, NT.steal, NT.goto, T.give]
    },
    NT.wealth: {
        1: [NT.goto, NT.get],
        2: [NT.goto, NT.steal],
        3: [T.repair]
    },
    NT.ability: {
        1: [T.repair, T.use],
        2: [NT.get, T.use],
        3: [T.use],
        4: [T.damage],
        5: [T.use],
        6: [NT.get, T.use],
        7: [NT.get, T.experiment]
    },
    NT.equipment: {
        1: [T.repair],
        2: [NT.get, NT.goto, T.give],
        3: [NT.steal],
        4: [NT.goto, T.exchange]
    },

    NT.sub_quest: {
        1: [NT.goto],
        2: [NT.goto, NT.quest, T.goto]
    },
    NT.goto: {
        1: [T.null],
        2: [T.explore],
        3: [NT.learn, T.goto]
    },
    NT.learn: {
        1: [T.null],
        2: [NT.sub_quest, NT.goto, T.listen],
        3: [NT.goto, NT.get, T.read],
        4: [NT.get, NT.sub_quest, T.give, T.listen]
    },
    NT.get: {
        1: [T.null],
        2: [NT.steal],
        3: [NT.goto, T.gather],
        4: [NT.goto, NT.get, NT.sub_quest, NT.goto, T.exchange]
    },
    NT.steal: {
        1: [NT.goto, T.stealth, T.take],
        2: [NT.goto, NT.kill, T.take]
    },
    NT.spy: {
        1: [NT.goto, T.spy, NT.goto, T.report]
    },
    NT.capture: {
        1: [NT.get, NT.goto, T.capture]
    },
    NT.kill: {
        1: [NT.goto, T.kill]
    }
}
