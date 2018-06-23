from helper import camel_case_to_underscore


class Status:
    name = ''

    def __init__(self):
        self.name = camel_case_to_underscore(str(self.__class__))


class Belongings(Status):
    items = []  # list of object Elements


class VitalStat(Status):
    alive = True


class Inhabitants(Status):
    people = []  # list of Person type Elements
