
from enum import Enum, auto


class SIBaseUnit(Enum):
    m = auto()      # meter
    kg = auto()     # kilo gram
    s = auto()      # second
    A = auto()      # Ampere
    K = auto()      # Kelbin
    mol = auto()    # mol
    cd = auto()     # candela
    
    
class Unit:
    pass
