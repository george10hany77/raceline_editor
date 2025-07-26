from path_extractor.config.config import extractor_config, State
class Node():
    def __init__(self, x, y, state:State=None, parent=None):
        self.x = x
        self.y = y
        self.state = state
        self.parent = parent

    def __hash__(self):
        return hash((self.x, self.y))
    
    def __eq__(self, other):
        return isinstance(other, Node) and self.x == other.x and self.y == other.y