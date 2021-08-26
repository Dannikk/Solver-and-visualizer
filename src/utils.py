from dataclasses import dataclass
from PyQt5.QtWidgets import QPushButton, QPlainTextEdit, QLabel, QTextEdit
from typing import Any
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
import numpy as np
import sympy
from sympy.parsing.sympy_parser import (parse_expr, standard_transformations, implicit_multiplication_application,
                                        convert_xor)
from scipy.optimize import minimize as min
from itertools import combinations
import math
import matplotlib.pyplot as plt


@dataclass
class UIelements:
    find_btn: QPushButton = None
    func_field: QTextEdit = None
    x_field: QPlainTextEdit = None
    y_field: QPlainTextEdit = None
    result_field: QLabel = None
    res_default: str = "We will solve all your problems... almost)"
    previous: QPushButton = None
    next: QPushButton = None
    figure: Any = None
    canvas: FigureCanvasQTAgg = None


@dataclass
class Solution:
    start: np.ndarray


if __name__ == '__main__':
    def func(x, y):
        return x**2 + y**2

    x, y = np.mgrid[-10: 10:100j,
                    -10: 10:100j]
    # levels = np.array([range(1, 10)])
    z = func(x, y)
    print(type(z))
    print(type(x))
    cs = plt.contour(x, y, z, levels=[1, 4, 9])
    plt.clabel(cs)
    plt.grid()
    plt.show()
    #
    # xx = np.array([1, 2, 3])
    # x = sympy.Symbol('x')
    # y = sympy.Symbol('y')
    # variables = [x, y]
    # func = 'x^2+y^2'
    # f = parse_expr(func, transformations=(standard_transformations + (implicit_multiplication_application,) +
    #                                       (convert_xor,)))
    # x_, y_ = np.mgrid[-10: 10:100j,
    #                 -10: 10:100j]
    # z = f.subs([(x, x_), (y, y_)])
    # print('grsgs')
    # print()
    x = np.array([range(1, 12)])
    print(x.sort())