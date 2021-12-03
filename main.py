class Variable(float):
    """define a variable with value and error kwargs or function and parameters kwargs(parameters is a tuple of Variable objects)"""
    def __new__(self, **kwargs):
        _, value = self.__get_define_type_value(self, kwargs)
        return float.__new__(self, value)
    
    def __init__(self, **kwargs):
        self.__define_type, self.value = self.__get_define_type_value(kwargs)
        self.__kwargs = kwargs
    
    def get_std_error(self):
        if self.__define_type == "value":
            return float(self.__kwargs["error"])
        else:
            # compute error from standard deviations
            n_params = len(self.__kwargs["parameters"])
            parameter_errors = [self.__kwargs["parameters"][i].get_std_error() for i in range(n_params)]
            return (sum([(self.__partial_derivative(i)*parameter_errors[i])**2 for i in range(n_params)])) ** 0.5

    def __partial_derivative(self, argument_index):
        if self.__define_type != "function":
            raise Exception("cannot compute partial derivative of variable defined with value and error")
        else:
            function = self.__kwargs["function"]
            args = self.__kwargs["parameters"]
            modified_args = list(args)
            if modified_args[argument_index] != 0:
                increment = 0.001*modified_args[argument_index]
                modified_args[argument_index] += increment
                return (function(*modified_args) - function(*args))/increment
            else:
                increment = 0.001
                modified_args[argument_index] += increment
                return (function(*modified_args) - function(*args))/increment



    def __get_define_type_value(self, kwargs):
        """returns either "value" or "function", depending on the definition type"""
        # parse value and error definition
        if len(kwargs) != 2:
            raise Exception("Constructor accepts either value and error of function and its arguments as named arguments(kwargs)")

        if "value" in kwargs and "error" in kwargs:
            try:
                value = float(kwargs["value"])
                error = float(kwargs["error"])

                return ("value", value)
            except ValueError:
                raise Exception("Value or error given in wrong format")
        
        #parse function and variables definition
        elif "function" in kwargs and "parameters" in kwargs:
            if any(not isinstance(param, Variable) for param in kwargs["parameters"]):
                raise Exception("The arguments to the function must be of class Variable")
            else:
                try:
                    function = kwargs["function"]
                    value = float(function(*kwargs["parameters"]))

                    return ("function", value)
                except TypeError:
                    raise Exception("The number of variables given does not equal the number of variables the given function accepts")
                

if __name__ == "__main__":
    function = (lambda x, y: x**2*y**3)
    params = (Variable(value=10, error=0.1), Variable(value=3, error=0.1))
    b = Variable(function=function, parameters=params)
    print(b, b.get_std_error())
