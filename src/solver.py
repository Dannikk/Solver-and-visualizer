import numpy as np
from numpy.linalg import norm
from typing import Any, List, Union


def golden_solver(func, left: float = 0, right: float = 1, epsilon=10**-8) -> float:
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
        # print(step_count)
        # step_count += 1
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


def solver(start: np.ndarray, function: Any, gradient: Any, eps: float) -> (np.ndarray, np.ndarray):
    x = start
    step_count = 0
    points = []
    values = []
    while True:
        grad = gradient(x)
        # print(f"grad: {grad}, {type(grad)}")
        # print(f"grad: {grad[0]}, {type(grad[0])}")
        points.append(x)
        values.append(function(x))
        if norm(grad) < eps:
            print("Количество шагов: ", step_count)
            return x, np.array(points), np.array(values)
        alpha = golden_solver(lambda al: function(x - al * grad))
        x = x - alpha * grad
        print(f'step: {step_count}')
        step_count += 1