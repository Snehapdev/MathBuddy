import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
import io
import base64
import re


import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
import re
import io
import base64


def plot_linear(equation):
    try:
        # Handle implicit multiplication (e.g., 2x -> 2*x)
        equation = re.sub(r'([0-9])([a-zA-Z])', r'\1*\2', equation)
        equation = re.sub(r'√([0-9]*)', r'sqrt(\1)', equation)
        equation = re.sub(r'(sqrt\(\d+\)|sqrt\d+|\d+)([a-zA-Z])', r'\1*\2', equation)
        
        # Split the equation at '=' and sympify both sides
        lhs, rhs = equation.split('=')
        lhs = sp.sympify(lhs)
        rhs = sp.sympify(rhs)
        
        # Solve lhs - rhs = 0 for one of the symbols
        symbols = lhs.free_symbols.union(rhs.free_symbols)
        if len(symbols) == 1:
            x = list(symbols)[0]
            expr = sp.sympify(lhs - rhs)
            f = sp.lambdify(x, expr, 'numpy')
            x_vals = np.linspace(-10, 10, 400)
            y_vals = f(x_vals)
            plt.plot(x_vals, y_vals, label=f'{equation}')
            
        elif len(symbols) == 2:
            x, y = symbols
            expr = sp.solve(lhs - rhs, y)[0]
            f = sp.lambdify(x, expr, 'numpy')
            x_vals = np.linspace(-10, 10, 400)
            y_vals = f(x_vals)
            plt.plot(x_vals, y_vals, label=f'{equation}')
            plt.xlabel(str(x))
            plt.ylabel(str(y))
        else:
            raise ValueError("The equation should contain one or two variables.")
        
        plt.title('Linear Equation')
        plt.legend()
        plt.grid(True)

        # Save the plot to a buffer
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        image_base64 = base64.b64encode(buf.read()).decode('utf-8')
        plt.close()

        return image_base64
    except Exception as e:
        raise ValueError(f"Could not plot the equation: {str(e)}")


def plot_trigonometric(equation):
    try:
        x = sp.symbols('x')
        expr = sp.sympify(equation)
        f = sp.lambdify(x, expr, 'numpy')
        x_vals = np.linspace(-2 * np.pi, 2 * np.pi, 400)
        y_vals = f(x_vals)
        plt.plot(x_vals, y_vals, label=f'y = {equation}')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.title('Trigonometric Equation')
        plt.legend()
        plt.grid(True)
        plt.ylim(-10, 10)

        # Save the plot to a buffer
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        image_base64 = base64.b64encode(buf.read()).decode('utf-8')
        plt.close()

        return image_base64
    except Exception as e:
        raise ValueError(f"Could not plot the equation: {str(e)}")

def plot_complex(equation):
    try:
        x = sp.symbols('x')
        expr = sp.sympify(equation)
        f_real = sp.lambdify(x, sp.re(expr), 'numpy')
        f_imag = sp.lambdify(x, sp.im(expr), 'numpy')
        x_vals = np.linspace(-10, 10, 400)
        y_real_vals = f_real(x_vals)
        y_imag_vals = f_imag(x_vals)
        plt.plot(x_vals, y_real_vals, label='Real part')
        plt.plot(x_vals, y_imag_vals, label='Imaginary part')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.title('Complex Equation')
        plt.legend()
        plt.grid(True)

        # Save the plot to a buffer
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        image_base64 = base64.b64encode(buf.read()).decode('utf-8')
        plt.close()

        return image_base64
    except Exception as e:
        raise ValueError(f"Could not plot the equation: This feature is not supported yet")
