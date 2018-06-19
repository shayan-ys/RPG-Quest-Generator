class Properties:
    pass


class Locations(Properties):
    x = 0
    y = 0

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y


class Distances(Properties):
    short = None
    medium = None
    far = None
    unreachable = None

    def __init__(self, short: int, medium: int, far: int, unreachable: int):
        self.short = short
        self.medium = medium
        self.far = far
        self.unreachable = unreachable


class Name(Properties):
    name = ""

    def __init__(self, name: str):
        if len(name) < 2:
            raise Exception("Too short 'Name' chosen as property, minimum length is 2, "
                            "entered \"" + name + "\" with length: '" + str(name) + "'")
        self.name = name

    def __str__(self):
        return self.name
