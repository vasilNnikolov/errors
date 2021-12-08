import unittest
import math
from main import Variable

class TestVariable(unittest.TestCase):
    def testLinearFunction(self):
        a = Variable(5, 0.1)
        b = Variable(7, 0.2)
        result = Variable(lambda x, y: x + y, (a, b))
        self.assertAlmostEqual(result.get_std_error(), (0.1**2 + 0.2**2)**0.5, 2, "Linear function does not match")
        self.assertAlmostEqual(result.get_max_error(), 0.1 + 0.2, 2, "Linear function does not match")
    
    def testProduct(self):
        a = Variable(5, 0.1)
        b = Variable(7, 0.2)
        result = Variable(lambda x, y: x * y, (a, b))
        self.assertAlmostEqual(result.get_std_error(), ((b*a.get_std_error())**2 + (a*b.get_std_error())**2)**0.5, 2, "Linear function does not match")

    def testExponential(self):
        a = Variable(5, 0.1)
        b = Variable(7, 0.2)
        result = Variable(lambda x, y: x ** y, (a, b))
        theoretical_error = ((b*a**(b-1)*a.get_std_error())**2 + (a**b * math.log(a)*b.get_std_error())**2) ** 0.5
        calculated_error = result.get_std_error()
        self.assertAlmostEqual((calculated_error - theoretical_error)/theoretical_error, 0, 1, "Exponent function does not match")

    def testProductExponent(self):
        a = Variable(5, 0.1)
        b = Variable(7, 0.2)
        result = Variable(lambda x, y: x**5 * y**7, (a, b))
        theoretical_error = ((a**5 * 7*b**6*b.get_std_error())**2 + (b**7 * 5*a**4*a.get_std_error())**2) ** 0.5
        calculated_error = result.get_std_error()
        self.assertAlmostEqual((calculated_error - theoretical_error)/theoretical_error, 0, 1, "Exponent product function does not match")

    def testInvalidInputs_1(self):
        a = Variable("text", 0.6)

    def testInvalidInputs_2(self):
        a = Variable(6, "a12")
    
    def testInvalidInputs_3(self):
        a = Variable("text", "more text")
    
    def testInvalidInputs_4(self):
        a = Variable(69, Variable(1, 1), Variable(2, 0.2))

    def testInvalidInputs_5(self):
        a = Variable(lambda x, y: x+y, (Variable(1, 2)))
if __name__ == "__main__":
    unittest.main()