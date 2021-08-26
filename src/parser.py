import sympy
from sympy.tensor.array import derive_by_array
from sympy.parsing.sympy_parser import (parse_expr, standard_transformations, implicit_multiplication_application,
                                        convert_xor)
from typing import Any, Union, List
import numpy as np


class VoidFieldException(ValueError):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return f'Wrong value have been found: {self.message}!'
        else:
            return 'Wrong value have been found!'


def get_pretty_func(func: Union[Any, List[Any]], variables: list):
    def get_sub_value(f: Any, point_: Union[list, np.ndarray], vars: list):
        res = f.subs([(var, p) for var, p in zip(vars, point_)])
        if isinstance(res, sympy.core.numbers.ComplexInfinity):
            raise ValueError('Division by zero occured')
        elif res.has(sympy.core.numbers.ImaginaryUnit):
            raise ValueError('The root argument turned out to be negative')
        return res

    def inner_func(point: Union[list, np.ndarray]) -> Union[np.ndarray, float]:
        try:
            if isinstance(func, (list, np.ndarray, sympy.tensor.array.dense_ndim_array.ImmutableDenseNDimArray)):
                result = [float(get_sub_value(f, point, variables)) for f in func]
                return np.array(result)
            else:
                return float(get_sub_value(func, point, variables))
        except Exception as e:
            print('pizdaaaa')
            raise e
    return inner_func


def parse_function_expression(func: str = "sqrt(x) / y"):
    x = sympy.Symbol('x')
    y = sympy.Symbol('y')
    variables = [x, y]
    if func:
        try:
            # print(f"before parsing: '{func}'")
            f = parse_expr(func, transformations=(standard_transformations + (implicit_multiplication_application,) +
                                                  (convert_xor,)))
            # print('after parsing')
        except SyntaxError:
            raise SyntaxError('Syntax error occur')
        except Exception as e:
            raise e
    else:
        raise VoidFieldException('dibil bleat')
    if f.free_symbols - {x, y}:
        raise SyntaxError('Invalid characters encountered')

    numerical_func = get_pretty_func(f, variables)
    gradient = derive_by_array(f, (x, y))
    numerical_gradient = get_pretty_func(gradient, variables)

    # print(f'{f}, {gradient}, {numerical_gradient}, {type(numerical_gradient)}')

    return numerical_func, numerical_gradient


if __name__ == '__main__':
    str_func = input('Enter func')
    func = get_function(str_func)
    print(func)
    print(type(func))
    res = func(0, 0).evalf()
    print(res)
    print(type(res))
