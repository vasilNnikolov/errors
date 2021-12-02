from typing import Tuple

class Variable(float):
    def __new__(self, value, error):
        return float.__new__(self, value)
    
    def __init__(self, value, error):
        float.__init__(value)
        self.error = abs(error)
        self.relative_error = self.error/self


class Expression:
    def __init__(self, function, *args: Variable):
        if any(not isinstance(argument, Variable) for argument in args):
            raise ValueError("One of the arguments is not an instance of Variable class")
        else:
            self.function = function
            self.arguments = list(args)
            self.value = function(*args)
    
    # def __get_partial_derivative(self, argument_index):
    #     increment = 0.001*self.arguments[argument_index]
    #     modified_args = self.arguments[:]
    #     modified_args[argument_index] += increment
    #     return (self.function(modified_args) - self.function(self.arguments))/increment

    # def get_error(self):
    #     errors = [self.__get_partial_derivative(i)*self.arguments[i].error for i in range(len(self.arguments))]
    #     return (sum([error ** 2 for error in errors])) ** 0.5
        
        
a = Variable(10, 0.2)

b = Variable(12, 0.4)

c = Variable(10, 0.2)

d = Variable(12, 0.4)

y = Expression(lambda a, b, c, d: (a+b+c)*d, a, b, c, d)

print(y.value)