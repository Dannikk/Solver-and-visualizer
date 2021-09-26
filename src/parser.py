import sympy
from sympy.tensor.array import derive_by_array
from sympy.parsing.sympy_parser import (parse_expr, standard_transformations, implicit_multiplication_application,
                                        convert_xor)
from typing import Any, Union, List, Callable, Tuple, NoReturn
import numpy as np
from src.utils import ErrorCode
# from sympy.functions.elementary.complexes import re, im
from sympy.core.numbers import ImaginaryUnit
from queue import Queue
from sympy import re, im, I, E, symbols


class WrongFieldException(ValueError):
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


def get_pretty_func(func: Union[Callable, List[Callable]], variables: list) -> Callable:
    """

    Parameters
    ----------
    func : Union[Callable, List[Callable]]
        callable function or list
    variables :

    Returns
    -------

    """
    def get_sub_value(f: Any, point_: Union[list, np.ndarray], vars: list):
        res = f.subs([(var, p) for var, p in zip(vars, point_)])
        if isinstance(res, sympy.core.numbers.ComplexInfinity):
            raise ValueError(ErrorCode.ZERO_DIVISION.value)
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
            raise e
    return inner_func


def contain_I(expr):
    queue = Queue()
    queue.put(expr)
    while not queue.empty():
        current = queue.get()
        if isinstance(current, ImaginaryUnit):
            return True
        for arg in current.args:
            queue.put(arg)
    return False


def parse_function_expression(func: str) -> Tuple[ErrorCode, Callable, Callable]:
    """

    Parameters
    ----------
    func : str
        string that contains the function

    Returns
    -------
    Union[Tuple[Callable, Callable], Exception] :
        tuple of function and gradient
        or any Exception

    """
    x = sympy.Symbol('x')
    y = sympy.Symbol('y')
    variables = [x, y]

    if func:
        try:
            f = parse_expr(func, evaluate=False,
                           transformations=(standard_transformations + (implicit_multiplication_application,) +
                                            (convert_xor,)))
        except Exception:
            return ErrorCode.UK_ERROR, NoReturn, NoReturn
        if contain_I(f):
            return ErrorCode.WRONG_EXPRESSION, NoReturn, NoReturn
    else:
        # raise WrongFieldException(ErrorCode.EMPTY_FIELD.value)
        return ErrorCode.OK, NoReturn, NoReturn


    # the case when some variables other than x and y are recognized
    if f.free_symbols - {x, y}:
        # raise WrongFieldException(ErrorCode.EXTRA_VARS.value)
        return ErrorCode.EXTRA_VARS, NoReturn, NoReturn
    elif {x, y} - f.free_symbols:
        # raise WrongFieldException(ErrorCode.NOT_ENOUGH_VARS.value)
        return ErrorCode.NOT_ENOUGH_VARS, NoReturn, NoReturn

    numerical_func = get_pretty_func(f, variables)
    gradient = derive_by_array(f, (x, y))
    numerical_gradient = get_pretty_func(gradient, variables)
    # print(f'{f}, {gradient}, {numerical_gradient}, {type(numerical_gradient)}')
    # return numerical_func, numerical_gradient
    return ErrorCode.OK, numerical_func, numerical_gradient


def is_float(x: str) -> bool:
    """

    Parameters
    ----------
    x : a string that can be assumed to be a number

    Returns
    -------
    bool :
        True if x can be a float, False otherwise

    """
    if x.isdigit():
        return True
    else:
        try:
            float(x)
            return True
        except ValueError:
            return False


def parse_float(x: str) -> Tuple[ErrorCode, float]:
    """

    Parameters
    ----------
    x : str
        a string that can be assumed to be a number

    Returns
    -------
    Union[float, WrongFieldException] :
        flaot number if string can be assumed to be a number
        or WrongFieldException otherwise

    """
    if is_float(x):
        return ErrorCode.OK, float(x)
        # return float(x)
    else:
        # raise WrongFieldException(ErrorCode.WRONG_POINT.value)
        return ErrorCode.WRONG_POINT, NoReturn
