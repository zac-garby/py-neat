from enum import Enum
from copy import deepcopy

class NodeType(Enum):
    inp = 1
    hidden = 2
    out = 3

class Gene(object):
    def copy(self):
        return deepcopy(self)

class Node(Gene):
    def __init__(self, type, id):
        self.type = type
        self.id = id

class Connection(Gene):
    def __init__(self, inp, out, weight, expressed, innovation):
        self.inp = inp
        self.out = out
        self.weight = weight
        self.expressed = expressed
        self.innovation = innovation
