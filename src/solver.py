import numpy as np
from numpy.linalg import norm
from typing import Any, List, Union, Callable, Tuple, NoReturn
from src.utils import ErrorCode


GRADNORM_MAX = 2**32
ITERATION_MAX = 1000


def golden_solver(func: Callable, left: float = 0, right: float = 1, epsilon=10**-8) -> Union[float, Exception]:
    """
    A function that finds the minimum of a one-dimensional function

    Parameters
    ----------
    func : Callable
        the one-dimensional function
    left : float
        the left boundary of the segment on which the minimum is sought
    right : float
        the right boundary of the segment on which the minimum is sought
    epsilon : float
        the accuracy with which the minimum is sought

    Returns
    -------
    float :
        the value of the argument at which the minimum is reached

    """
    phi = (1 + 5 ** 0.5) / 2

    if right - left < epsilon:
        return (right - left) / 2

    a = left + (right - left) * (2 - phi)
    b = left + (right - left) * (1 / phi)
    f_1 = func(a)
    f_2 = func(b)

    # step_count = 0
    while True:
        if right - left < epsilon:
            return (right + left) / 2
        if f_1 < f_2:
            right = b
            b = a
            a = left + (right - left) * (2 - phi)
            f_1, f_2 = func(a), f_1
        else:
            left = a
            a = b
            b = left + (right - left) * (1 / phi)
            f_1, f_2 = f_2, func(b)


def solver(start: np.ndarray, function: Callable, gradient: Callable, eps: float) \
        -> Tuple[ErrorCode, float, np.ndarray, np.ndarray]:
    """

    Parameters
    ----------
    start : np.array
        start point
    function : Callable
        the function whose minimum is sought
    gradient : Callable
        the gradient of function
    eps : float
        the accuracy with which the minimum is sought

    Returns
    -------
    Union[Tuple[np.ndarray, np.ndarray, np.ndarray], Exception]
        return tuple of minimum point and two np.ndarray's that are points and values of each step
        or any Exception that must be processed in calling method

    """
    x = start
    step_count = 0
    points = []
    values = []
    while True:
        grad = gradient(x)
        points.append(x)
        values.append(function(x))
        grad_norm = norm(grad)
        if grad_norm > GRADNORM_MAX or step_count > ITERATION_MAX:
            return ErrorCode.DIVERGENCE, NoReturn, NoReturn, NoReturn
        elif norm(grad) < eps:
            print(x)
            return ErrorCode.OK, x, np.array(points), np.array(values)
        alpha = golden_solver(lambda al: function(x - al * grad))
        x = x - alpha * grad
        print(f'step: {step_count}')
        step_count += 1