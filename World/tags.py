from Grammar.actions import Terminals as T
from World.properties import Locations, Distances


class Tags:
    pass


class ActionTags(Tags):
    action = None

    def __init__(self, action: T):
        self.action = action


class RelativeTags(Tags):
    pass


class DistanceTags(RelativeTags):
    location = None   # type: Locations
    distances = None  # type: Distances

    def __init__(self, location: Locations, distances: Distances):
        self.location = location
        self.distances = distances
