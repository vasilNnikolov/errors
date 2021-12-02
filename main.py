class Variable(float):
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
            pass

    def __partial_derivative(self, argument_index):

        pass


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
    function = (lambda x, y: x**y)
    params = (Variable(value=10, error=0.1), Variable(value=3, error=0.2))
    b = Variable(function=function, parameters=params)
    print(b)
