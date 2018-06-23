from World import properties
from World.types import *
from World.elements import Element


# class WorldElements(WorldElementsBase):

elements = [
    Element(Person(), properties=[properties.Name('NPC1')]),
    Element(Person(), properties=[properties.Name('NPC2')]),

    Element(Tool(), properties=[properties.Name('potion')]),
    Element(UnknownObject(), properties=[properties.Name('honeyjum')]),
    Element(UnknownObject(), properties=[properties.Name('honeycomb')]),
    Element(Territory(), properties=[properties.Name('rivervale')]),
    Element(Tool(), properties=[properties.Name('bondage')]),
    Element(Territory(), properties=[properties.Name('bixies territory')]),
    Element(Person(), properties=[properties.Name('bixies')]),
    Element(Territory(), properties=[properties.Name('qeynos')]),
    Element(Place(), properties=[properties.Name('lempeck\'s location')])
]
