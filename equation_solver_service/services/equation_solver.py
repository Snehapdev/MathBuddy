
import sympy as sp

def solve_arithmetic_equation(equation):
   pass

def solve_linear_equation(equation):
    try:
        lhs, rhs = equation.split('=')
        x = sp.symbols('x')
        lhs_expr = sp.sympify(lhs.strip())
        rhs_expr = sp.sympify(rhs.strip())
        solution = sp.solve(lhs_expr - rhs_expr, x)
        
        # Convert SymPy objects to native Python types
        solution = [float(s) if isinstance(s, sp.Float) else int(s) if isinstance(s, sp.Integer) else s.evalf() for s in solution]
        
        return solution
    except Exception as e:
        raise ValueError(f"Could not parse or solve the equation: {str(e)}")

def solve_trigonometric_equation(equation):
    pass
