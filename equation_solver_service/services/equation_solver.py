
import sympy as sp
from sympy import Symbol, Eq, solve, pi, Interval
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

def solve_trigonometric_equation(equation, range_start=-2*pi, range_end=2*pi):
  try:
    # Preprocess the equation
    equation = equation.strip()
    equation = re.sub(r'√([a-zA-Z0-9]*)', r'sqrt(\1)', equation)  # Replace sqrt with sqrt()
    equation = re.sub(r'(sqrt\(\d+\)|sqrt\d+|\d+)([a-zA-Z])', r'\1*\2', equation)  # Add * between numbers and variables

    # Split the equation into lhs and rhs
    lhs, rhs = equation.split('=')

    # Create sympy expressions for lhs and rhs
    lhs_expr = sp.sympify(lhs.strip())
    rhs_expr = sp.sympify(rhs.strip())

    # Identify the variables in the equation
    variables = lhs_expr.free_symbols.union(rhs_expr.free_symbols)

    # Check if number of variables is acceptable
    if len(variables) > 1:
      # Allow for multiple trig functions of the same variable
      all_trig_funcs = True
      for var in variables:
        if not (sp.is_Function(var) and sp.trigify(var) == var):
          all_trig_funcs = False
          break
      if not all_trig_funcs:
        raise ValueError("Only single-variable equations or equations with multiple trig functions of the same variable are supported.")

    # Solve the equation (assuming single variable or multiple trig functions of the same variable)
    variable = variables.pop()  # Extract a variable (might be the only one or representative)
    solution = sp.solve(Eq(lhs_expr, rhs_expr), variable, domain=Interval(range_start, range_end))

    # Convert SymPy objects to native Python types (consider real solutions)
    solution_list = []
    for sol in solution:
      if sol.is_real:
        solution_list.append(float(sol.evalf(10)))  # Evaluate with 10 digits precision

    return solution_list

  except Exception as e:
    raise ValueError(f"Could not parse or solve the equation: {str(e)}")
