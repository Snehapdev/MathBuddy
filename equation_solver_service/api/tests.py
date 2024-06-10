# equation_solver_service/api/tests.py
from django.test import TestCase
from services.equation_solver import solve_linear_equations
import sympy as sp
import re

class SolveEquationsTest(TestCase):

    def test_solve_linear_equations_valid_input(self):
        equations = ""
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