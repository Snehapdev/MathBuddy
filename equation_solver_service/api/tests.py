# equation_solver_service/api/tests.py
from django.test import TestCase
from services.equation_solver import solve_linear_equations, solve_trigonometric_equation, solve_equation_with_imaginary_unit, solve_arithmetic_equation
from unittest.mock import patch

import sympy as sp
import re

class SolveEquationsTest(TestCase):

    def test_solve_linear_equations_valid_input(self):
        equations = "2x + 3y = 5, 4x - y = 3"
        expected_output = {"x": 1.00, "y": 1.00}  # Define expected output as a dictionary
        result = solve_linear_equations(equations)
        
        # Parse the result and convert it to a dictionary
        parsed_result = {}
        for item in result:
            variable, value = item.split("=")
            variable = variable.strip()  # Remove any leading or trailing spaces
            value = float(value.strip())  # Convert value to float
            parsed_result[variable] = value
        
        # Validate the solution
        self.assertDictEqual(parsed_result, expected_output)

    def test_solve_linear_equations_no_solution(self):
        equations = "x + y = 1, x + y = 2"
        with self.assertRaises(ValueError) as context:
            solve_linear_equations(equations)
        self.assertIn("No solution found.", str(context.exception))

    def test_solve_linear_equations_invalid_input(self):
        equations = "2x + = 5, 4x - y = 3"
        with self.assertRaises(ValueError) as context:
            solve_linear_equations(equations)
        self.assertIn("Could not parse or solve the equations", str(context.exception))

    def test_solve_linear_equations_non_matching_variables(self):
        equations = "2x + 3y = 5, 4a - y = 3"
        with self.assertRaises(ValueError) as context:
            solve_linear_equations(equations)
        self.assertIn("The number of variables should be equal to the number of equations.", str(context.exception))
    

    def test_sin_equation(self):
        # Test equation: sin(x) = 0.5
        equation = "sin(x) = 0.5"
        solutions = solve_trigonometric_equation(equation)
        self.assertEqual(solutions, ["x = 0.523598775598299 + 2πn", "x = π - 0.523598775598299 + 2πn"])
    
    def test_cos_equation(self):
        # Test equation: cos(x) = -1
        equation = "cos(x) = -1"
        solutions = solve_trigonometric_equation(equation)
        self.assertEqual(solutions, ["x = pi + 2πn", "x = -pi + 2πn"])
    
    def test_tan_equation(self):
        # Test equation: tan(x) = 1
        equation = "tan(x) = 1"
        solutions = solve_trigonometric_equation(equation)
        self.assertEqual(solutions, ["x = pi/4 + πn"])
    
    def test_invalid_equation(self):
        # Test an invalid equation
        equation = "sin(x) + cos(y) = 0.8"
        with self.assertRaises(ValueError):
            solve_trigonometric_equation(equation)
    
    def test_solve_equations_with_imaginary_unit(self):
        equations = "2z - 3i = 5"
        expected_solution = ["z = 3*i/2 + 5/2"]
        solution = solve_equation_with_imaginary_unit(equations)
        self.assertEqual(solution, expected_solution)
    
    def test_solve_arithmetic_equation_invalid_equation(self):
        invalid_equation = "2 +"
        with self.assertRaises(ValueError) as context:
            solve_arithmetic_equation(invalid_equation)
        self.assertIn("Could not parse or evaluate the equatio", str(context.exception))

    def test_solve_arithmetic_equation(self):
        # Test cases with expected results
        test_cases = [
            ("2 + 2", 4),
            ("5 - 3", 2),
            ("2 * 3", 6),
            ("8 / 4", 2.0),
            ("√16", 4),
            ("2**3", 8),
            ("(2 + 3) * 4", 20),
            ("2 + √9", 5)
        ]

        for equation, expected in test_cases:
            with self.subTest(equation=equation):
                result = solve_arithmetic_equation(equation)
                self.assertEqual(result, expected)

    