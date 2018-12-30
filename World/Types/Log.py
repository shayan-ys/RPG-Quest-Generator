from World.Types import *

from enum import Enum, auto
from datetime import datetime


class MessageLevels(Enum):
    debug = auto()
    event = auto()
    instruction = auto()
    achievement = auto()
    error = auto()


class Message(BaseElement):
    level = CharField(choices=[(lvl.value, lvl.name) for lvl in MessageLevels])
    text = CharField()
    created = DateTimeField(default=datetime.now)

    @staticmethod
    def construct(level: MessageLevels, text: str) -> 'Message':
        msg, created = Message.get_or_create(level=level.name, text=text.capitalize())
        return msg

    @staticmethod
    def debug(msg: str) -> 'Message':
        return Message.construct(level=MessageLevels.debug, text=msg)

    @staticmethod
    def event(msg: str) -> 'Message':
        return Message.construct(level=MessageLevels.event, text=msg)

    @staticmethod
    def instruction(msg: str) -> 'Message':
        return Message.construct(level=MessageLevels.instruction, text=msg)

    @staticmethod
    def achievement(msg: str) -> 'Message':
        return Message.construct(level=MessageLevels.achievement, text=msg)

    @staticmethod
    def error(msg: str) -> 'Message':
        return Message.construct(level=MessageLevels.error, text=msg)

    class Meta:
        indexes = (
            (('level', 'text'), True),
        )

    @staticmethod
    def print_queue(debug_mode: bool=False) -> None:
        msgs = Message.select()
        if not debug_mode:
            msgs = Message.select().where(Message.level != MessageLevels.debug.name)

        msgs = msgs.order_by(Message.created.asc())
        for m in msgs:
            if m.level == MessageLevels.debug.name:
                print("##> %s." % m.text)
            elif m.level == MessageLevels.event.name:
                print("!~> %s." % m.text)
            elif m.level == MessageLevels.instruction.name:
                print("--> %s." % m.text)
            elif m.level == MessageLevels.achievement.name:
                print("++> %s." % m.text)
            elif m.level == MessageLevels.error.name:
                print("!!> Error: %s!" % m.text)
            else:
                print("??> %s." % m.text)

        # delete messages
        if debug_mode:
            query = Message.delete()
        else:
            query = Message.delete().where(Message.level != MessageLevels.debug.name)
        query.execute()


list_of_models = [Message]
