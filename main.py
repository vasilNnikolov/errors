class Variable(float):
    """define a variable with value and error kwargs or function and parameters kwargs(parameters is a tuple of Variable objects)"""
    def __new__(self, *args):
        _, value = self.__get_define_type_value(self, args)
        return float.__new__(self, value)

    def __init__(self, *args):
        define_type, value = self.__get_define_type_value(args)
        self.__define_type = define_type
        self.value = value
        if self.__define_type == "value":
            self.__error = abs(float(args[1]))
        elif self.__define_type == "function":
            self.__function = args[0]
            self.__parameters = args[1]

    def get_std_error(self):
        if self.__define_type == "value":
            return self.__error 
        else:
            # compute error from standard deviations
            n_params = len(self.__parameters)
            parameter_errors = [self.__parameters[i].get_std_error() for i in range(n_params)]
            return (sum([(self.__partial_derivative(i)*parameter_errors[i])**2 for i in range(n_params)])) ** 0.5

    def get_max_error(self):
        if self.__define_type == "value":
            return self.__error 
        else:
            # compute error from standard deviations
            n_params = len(self.__parameters)
            parameter_errors = [self.__parameters[i].get_std_error() for i in range(n_params)]
            return sum([self.__partial_derivative(i)*parameter_errors[i] for i in range(n_params)])

    def __partial_derivative(self, argument_index):
        if self.__define_type != "function":
            raise Exception("cannot compute partial derivative of variable defined with value and error")
        else:
            function = self.__function
            args = self.__parameters
            modified_args = list(args)
            if modified_args[argument_index] != 0:
                increment = 0.001*modified_args[argument_index]
                modified_args[argument_index] += increment
                return (function(*modified_args) - function(*args))/increment
            else:
                increment = 0.001
                modified_args[argument_index] += increment
                return (function(*modified_args) - function(*args))/increment

    def __get_define_type_value(self, args):
        """returns either "value" or "function", depending on the definition type"""
        if len(args) != 2:
            raise Exception("Constructor accepts either value and error of function and its arguments as args")

        # parse value and error definition
        def is_float(v):
            try:
                v = float(v)
                return True
            except Exception:
                return False
        
        if is_float(args[0]) and is_float(args[1]):
            value = float(args[0])
            error = float(args[1])

            return ("value", value)

        #parse function and variables definition
        elif callable(args[0]) and type(args[1]) is tuple:
            if any(not isinstance(param, Variable) for param in args[1]):
                raise Exception("The arguments to the function must be of class Variable")
            else:
                try:
                    function = args[0] 
                    value = float(function(*args[1]))

                    return ("function", value)
                except TypeError:
                    raise Exception("The number of variables given does not equal the number of variables the given function accepts")
        
        else:
            raise Exception("Pass either two floats(value and error) or callable function and its arguments in a tuple")
                

if __name__ == "__main__":
    a = Variable(10, 0.1)
    b = Variable(10, 5)
    c = Variable(30, 0.75)

    d = Variable(lambda x, y, z: (x**2 * y**5)/z, (a, b, c))
    print(d, d.value, d.get_std_error())
