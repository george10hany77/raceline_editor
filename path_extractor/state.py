from enum import Enum

class State(Enum):
    """
    Enum representing the state of a node in a pathfinding algorithm.
    """
    START = "#ff0000"  # Example hex color for start
    END = "#94367b"  # Example hex color for end
    PATH = "#ff0000"  # Example hex color for path

    def __str__(self):
        return self.name.lower()
