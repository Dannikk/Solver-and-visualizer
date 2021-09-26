from dataclasses import dataclass
from PyQt5.QtWidgets import QPushButton, QPlainTextEdit, QLabel, QTextEdit, QComboBox
from typing import Any
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
import numpy as np
from enum import Enum
# import sympy
# from sympy.parsing.sympy_parser import (parse_expr, standard_transformations, implicit_multiplication_application,
#                                         convert_xor)
# from itertools import combinations
# from sympy.parsing.sympy_parser import (parse_expr, standard_transformations, implicit_multiplication_application,
#                                         convert_xor)


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
    cb_accuracy: QComboBox = None


@dataclass
class Solution:
    start: np.ndarray


class ErrorCode(Enum):
    OK = 'Success'
    ZERO_DIVISION = 'Division by zero occurred'
    DIVERGENCE = 'Gradient norm is unlimited. Method diverges'
    EMPTY_FIELD = 'The input field is empty'
    EXTRA_VARS = 'The input field contains some variables other than x and y!'
    NOT_ENOUGH_VARS = 'The input field contains insufficient arguments for a 2D function'
    WRONG_POINT = 'Incorrect point or accuracy entered'
    WRONG_EXPRESSION = 'Expression contain prohibited characters'
    UK_ERROR = 'Unknown error has occurred'


# if __name__ == '__main__':
#     # def func(x, y):
#     #     return x**2 + y**2
#     #
#     # x, y = np.mgrid[-10: 10:100j,
#     #                 -10: 10:100j]
#     # # levels = np.array([range(1, 10)])
#     # z = func(x, y)
#     # print(type(z))
#     # print(type(x))
#     # cs = plt.contour(x, y, z, levels=[1, 4, 9])
#     # plt.clabel(cs)
#     # plt.grid()
#     # plt.show()
#     #
#     # xx = np.array([1, 2, 3])
#     # x = sympy.Symbol('x')
#     # y = sympy.Symbol('y')
#     # variables = [x, y]
#     # func = 'x^2+y^2'
#     # f = parse_expr(func, transformations=(standard_transformations + (implicit_multiplication_application,) +
#     #                                       (convert_xor,)))
#     # x_, y_ = np.mgrid[-10: 10:100j,
#     #                 -10: 10:100j]
#     # z = f.subs([(x, x_), (y, y_)])
#     # print('grsgs')
#     # print()
#     # x_ = sympy.Symbol('x')
#     # strf = 'x**4'
#     # f = parse_expr(strf, transformations=(standard_transformations + (implicit_multiplication_application,) +
#     #                                      (convert_xor,)))
#     # try:
#     #     x = np.float32(10)
#     #     while True:
#     #        # p = f(x)
#     #        p = f.subs(x_, x)
#     #        print(type(p), p, p < np.inf)
#     #        x +=p
#     # except RuntimeWarning as e:
#     #     print(e, type(e))
#     string = "x^2+yI^2"
#     f = parse_expr(string, evaluate=False, transformations=(standard_transformations + (implicit_multiplication_application,) +
#                                             (convert_xor,)))
#     print(f)