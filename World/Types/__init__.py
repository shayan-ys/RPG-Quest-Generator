from peewee import *
from enum import Enum


db = SqliteDatabase('Databases/world.db', pragmas={
    'journal_mode': 'wal',
    'cache_size': -1024 * 64})


class BaseElement(Model):
    class Meta:
        database = db


class Named(Model):
    name = CharField(unique=True)

    def __str__(self):
        return self.name


class Worthy(Model):
    worth = FloatField(null=True)    # general worth (price)
    default_worth = 0.1     # defined by type, used if general worth is None

    def worth_(self):
        return self.worth if self.worth else self.default_worth


list_of_models = []
