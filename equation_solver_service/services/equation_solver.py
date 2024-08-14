
import sympy as sp
from sympy import Symbol, Eq, solve, pi, Interval
import re
from scipy.optimize import fsolve
import google.generativeai as genai
from django.conf import settings


def solve_arithmetic_equation(equation):
    try:
        equation = re.sub(r'√([a-zA-Z0-9]*)', r'sqrt(\1)', equation)

        # Parse the equation
        result = sp.sympify(equation)
        
        # Evaluate the result
        solution = result.evalf()
        
        # Convert SymPy object to native Python type if necessary
        if isinstance(solution, sp.Float):
            solution = float(solution)
        elif isinstance(solution, sp.Integer):
            solution = int(solution)
        
        return solution
    except Exception as e:
        raise ValueError(f"Could not parse or evaluate the equation: {str(e)}")

def solve_linear_equations(equations):
    try:
        equations = [eq.strip() for eq in equations.split(',')]
        # Preprocess the equations to replace sqrt and add * between numbers and variables
        for i, equation in enumerate(equations):
            equation = re.sub(r'√([0-9]*)', r'sqrt(\1)', equation)
            equation = re.sub(r'(sqrt\(\d+\)|sqrt\d+|\d+)([a-zA-Z])', r'\1*\2', equation)
            equations[i] = equation
        
        # Split the equations into lhs and rhs
        lhs_rhs = [equation.split('=') for equation in equations]
        
        # Create sympy expressions for lhs and rhs
        lhs_expr = [sp.sympify(lhs.strip()) for lhs, rhs in lhs_rhs]
        rhs_expr = [sp.sympify(rhs.strip()) for lhs, rhs in lhs_rhs]
        
        # Identify the variables in the equations
        variables = set()
        for lhs, rhs in zip(lhs_expr, rhs_expr):
            variables = variables.union(lhs.free_symbols).union(rhs.free_symbols)
        
        if len(variables) > len(equations):
            raise ValueError("The number of variables should be equal to the number of equations.")
        
        # Solve the equations
        solution = sp.solve((lhs - rhs for lhs, rhs in zip(lhs_expr, rhs_expr)), *variables)
        
        if not solution:
            raise ValueError("No solution found.")
        
        solution = [f"{var} = {val.evalf():.2f}" for var, val in solution.items()]
        
        return solution
    except Exception as e:
        raise ValueError(f"Could not parse or solve the equations: {str(e)}")

def solve_trigonometric_equation(equation):
    try:
        # Preprocess the equation
        equation = equation.strip()
        equation = re.sub(r'√([a-zA-Z0-9]*)', r'sqrt(\1)', equation)  # Replace sqrt with sqrt()
        equation = re.sub(r'(sqrt\(\d+\)|sqrt\d+|\d+)([a-zA-Z])', r'\1*\2', equation)  # Add * between numbers and variables
    
        # Split the equation into lhs and rhs
        lhs, rhs = equation.split('=')
        lhs_expr = sp.sympify(lhs.strip())
        rhs_expr = sp.sympify(rhs.strip())

        # Identify the variable in the equation
        variables = lhs_expr.free_symbols.union(rhs_expr.free_symbols)
        if len(variables) != 1:
            raise ValueError("Equation must have exactly one variable.")
        
        variable = variables.pop()
        
        # Check for single variable trigonometric equation
            
        # Solve the equation symbolically
        solutions = sp.solve(lhs_expr - rhs_expr, variable)
            
        # Format solutions based on trigonometric function type
        formatted_solutions = []
        for sol in solutions:
            sol = sp.simplify(sol)
            if lhs_expr.has(sp.sin):
                formatted_solutions.append(f"x = {sol} + 2πn")
                formatted_solutions.append(f"x = π - {sol} + 2πn")
            elif lhs_expr.has(sp.cos):
                formatted_solutions.append(f"x = {sol} + 2πn")
                formatted_solutions.append(f"x = -{sol} + 2πn")
            elif lhs_expr.has(sp.tan):
                formatted_solutions.append(f"x = {sol} + πn")
            elif lhs_expr.has(sp.cot):
                formatted_solutions.append(f"x = {sol} + πn")
            elif lhs_expr.has(sp.sec):
                formatted_solutions.append(f"x = {sol} + 2πn")
                formatted_solutions.append(f"x = -{sol} + 2πn")
            elif lhs_expr.has(sp.csc):
                formatted_solutions.append(f"x = {sol} + 2πn")
                formatted_solutions.append(f"x = π - {sol} + 2πn")
            else:
                raise ValueError("Unsupported trigonometric function.")
            return formatted_solutions    
    
    except Exception as e:
        raise ValueError(f"Could not solve equation: {str(e)}")
    
def solve_equation_with_imaginary_unit(equation):
    try:
        # Split the equations and preprocess them
        equations = [eq.strip() for eq in equation.split(',')]
        for i, equation in enumerate(equations):
            # Replace square roots and add * between numbers and variables
            equation = re.sub(r'√([0-9]*)', r'sqrt(\1)', equation)
            equation = re.sub(r'(sqrt\(\d+\)|sqrt\d+|\d+)([a-zA-Z])', r'\1*\2', equation)
            equations[i] = equation
        
        # Split the equations into lhs and rhs
        lhs_rhs = [equation.split('=') for equation in equations]
        
        # Create sympy expressions for lhs and rhs
        lhs_expr = [sp.sympify(lhs.strip()) for lhs, rhs in lhs_rhs]
        rhs_expr = [sp.sympify(rhs.strip()) for lhs, rhs in lhs_rhs]
        
        # Identify the variables in the equations
        variables = set()
        for lhs, rhs in zip(lhs_expr, rhs_expr):
            variables = variables.union(lhs.free_symbols).union(rhs.free_symbols)
        
        variables.discard(sp.symbols('i'))

        # Check if the number of variables matches the number of equations
        if len(variables) > len(equations):
            raise ValueError("The number of variables should be equal to the number of equations.")
        
        # Solve the equations
        solution = sp.solve((lhs - rhs for lhs, rhs in zip(lhs_expr, rhs_expr)), *variables)
        
        if not solution:
            raise ValueError("No solution found.")
        
        # Format the solutions
        formatted_solution = []
        for var, val in solution.items():
            formatted_solution.append(f"{var} = {val}")
        
        return formatted_solution
    
    except Exception as e:
        raise ValueError(f"Could not solve the equations: {str(e)}")
    
# Function to sense the type of mathematical equation
def sense_math_equation(equation):
    # Configure your API key
    genai.configure(api_key=settings.GEN_LANGUAGE_API_KEY)
    # Choose a model that's appropriate for your use case
    model = genai.GenerativeModel('gemini-1.5-flash')

    # Create the prompt with the equation
    prompt = f"Classify the following mathematical equation as one of the following types: linear, trigonometric, arithmetic, or complex. Only respond with the type. Equation: {equation}"
    response = model.generate_content(prompt)

    # List of valid types
    valid_types = {'linear', 'trigonometric', 'arithmetic', 'complex'}
    
    # Extract the response text and filter it
    if response:
        response_text = response.text.strip().lower()
        # Return the first valid type found in the response
        for valid_type in valid_types:
            if valid_type in response_text:
                return valid_type
    return "Error"