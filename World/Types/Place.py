from World.Types import *


class Place(BaseElement, Named):
    x = IntegerField(default=0, constraints=[Check('x >= 0')])
    y = IntegerField(default=0, constraints=[Check('y >= 0')])

    class Meta:
        indexes = (
            (('x', 'y'), True),
        )


list_of_models = [Place]
