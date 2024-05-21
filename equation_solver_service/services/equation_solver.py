
import sympy as sp
import re

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
            equation = re.sub(r'√([a-zA-Z0-9]*)', r'sqrt(\1)', equation)
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
        
        if len(variables) != len(equations):
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
    pass
