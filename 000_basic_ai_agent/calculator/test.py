import unittest
from pkg.calculator import Calculator

class TestCalculator(unittest.TestCase):
    def setUp(self):
        self.calculator = Calculator()

    def test_addition(self):
        result = self.calculator.evaluate("2 + 3")
        self.assertEqual(result, 5)
    
    def test_subtraction(self):
        result = self.calculator.evaluate("5 - 2")
        self.assertEqual(result, 3)
    
    def test_multiplication(self):
        result = self.calculator.evaluate("2 * 3")
        self.assertEqual(result, 6)

    def test_division(self):
        result = self.calculator.evaluate("6 / 2")
        self.assertEqual(result, 3)

    def test_nested_expressions(self):
        result = self.calculator.evaluate("2 + 3 * 4")
        self.assertEqual(result, 14)

    def test_complex_expression(self):
        result = self.calculator.evaluate("2 + 3 * (4 - 1)")
        self.assertEqual(result, 11)
    
    def test_negative_numbers(self):
        result = self.calculator.evaluate("-2 + 3")
        self.assertEqual(result, 1)

    def test_invalid_expression(self):
        with self.assertRaises(ValueError):
            self.calculator.evaluate("2 +")

    def test_division_by_zero(self):
        with self.assertRaises(ZeroDivisionError):
            self.calculator.evaluate("5 / 0")

    def test_float_operations(self):
        result = self.calculator.evaluate("2.5 + 3.1")
        self.assertAlmostEqual(result, 5.6)

if __name__ == '__main__':
    unittest.main()
