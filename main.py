from typing import Tuple

class Variable(float):
    def __new__(self, **kwargs):
        return float.__new__(self, value, error=None)
    
    def __init__(self, **kwargs):
        pass

    def __parse_args(self, **kwargs):
        pass 
        
a = Variable(10, 0.2)

b = Variable(12, 0.4)

c = Variable(10, 0.2)

d = Variable(12, 0.4)

