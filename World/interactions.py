from Grammar.actions import Terminals

from helper import dict_pretty_str

from datetime import datetime


class Interaction:
    action = Terminals.null
    doers = []        # list of Elements, most likely of type Person who are doing the 'action'
    receivers = []    # list of Elements, most likely of type Person or Object, that the 'action' is being done on them
    timestamp = None  # timestamp of the 'action' initiated

    def __init__(self, action: Terminals, doers: list, receivers: list):
        self.action = action
        self.doers = doers
        self.receivers = receivers

        self.timestamp = datetime.now()

    def __dict__(self) -> dict:
        return {
            'action': self.action,
            'doers': self.doers,
            'receivers': self.receivers,
            'timestamp': self.timestamp
        }

    def str__pretty(self) -> str:
        return dict_pretty_str(self.__dict__())

    def __str__(self):
        return str(self.__dict__())

    def __repr__(self):
        return self.__str__()
