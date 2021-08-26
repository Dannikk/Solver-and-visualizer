from dataclasses import dataclass
from PyQt5 import QtWidgets
from src.utils import UIelements
import numpy as np
from src.parser import parse_function_expression, VoidFieldException
from typing import Any, Union, List
from src.solver import solver
import random


ANSWER_FORMAT = '.4e'


class Interaction:
    def __init__(self, ui_elements: UIelements):
        self.ui_elements = ui_elements
        self.solved = False
        self.set_functions()
        self.function: Any = None
        self.gradient: List[Any] = []
        self.start: np.ndarray
        self.step_count: int = 0

    def set_functions(self):
        self.ui_elements.find_btn.clicked.connect(self.find)
        # self.ui_elements.previous.clicked.connect()
        # self.ui_elements.previous.clicked.connect()

    def find(self):
        # deprecated
        # self.plot()
        print('Entry field have')
        try:
            self.function, self.gradient = parse_function_expression(self.ui_elements.func_field.toPlainText())
            self.start = ...
            # print(derive_by_array(self.function, ()))
        except (SyntaxError, VoidFieldException, ValueError) as e:
            self.show_message('Warning', e, level=QtWidgets.QMessageBox.Warning)
            return None
        except Exception as e:
            print(f'is it ValueError?: {isinstance(e, ValueError)}')
            self.show_message('Error', e, level=QtWidgets.QMessageBox.Critical)
            return None

        res, points, values = solver(start=np.array([2, 11]), function=self.function, gradient=self.gradient, eps=0.001)
        self.solved = True
        print(points)
        print()
        self.ui_elements.result_field.setText(f'Answer: {res[0]:{ANSWER_FORMAT}}, {res[1]:{ANSWER_FORMAT}}')
        self.plot_solution(points, values=values)

    def plot_solution(self, data: np.ndarray = None, values: np.ndarray = None):
        # instead of ax.hold(False)
        self.ui_elements.figure.clear()

        # create an axis
        ax = self.ui_elements.figure.add_subplot(111)
        steps = len(data)
        tmp = data.transpose()
        print(tmp)
        ax.grid()
        try:
            ax.scatter(tmp[0], tmp[1], color='r', marker='*')
            for i in range(0, steps - 1):
                size = data[i+1] - data[i]
                width = np.linalg.norm(size) / 600
                ax.arrow(data[i][0], data[i][1], size[0], size[1], facecolor='b', edgecolor='black', linewidth=1,
                         width=width, length_includes_head=True)
            x_extrems = (min(data[0:steps, 0]), max(data[0:steps, 0]))
            y_extrems = (min(data[0:steps, 1]), max(data[0:steps, 1]))
            x_, y_ = np.mgrid[x_extrems[0]:x_extrems[1]:100j,
                            y_extrems[0]:y_extrems[1]:100j]
            sh = x_.shape
            xr = np.ravel(x_)
            yr = np.ravel(y_)
            ps = np.vstack([xr, yr]).transpose()
            vect = np.vectorize(self.function, signature='(2)->()')
            z = vect(ps)
            z = z.reshape(sh)

            ax.contour(x_, y_, z, levels=list(sorted(values)))
            # refresh canvas
            self.ui_elements.canvas.draw()
        except Exception as e:
            print(e)
        print('I had drawed')

    def plot(self, data: np.ndarray = None):
        ''' plot some random stuff '''
        # random data
        print('Работает plot() в Interaction')

        data = [random.random() for i in range(10)]

        # instead of ax.hold(False)
        self.ui_elements.figure.clear()

        # create an axis
        ax = self.ui_elements.figure.add_subplot(111)

        # discards the old graph
        # ax.hold(False) # deprecated, see above

        # plot data
        ax.plot(data, '*-')
        ax.grid()

        # refresh canvas
        self.ui_elements.canvas.draw()

    def show_message(self, text: str = 'Info', info: Union[str, BaseException] = 'Any info',
                     level: QtWidgets.QMessageBox.Icon = QtWidgets.QMessageBox.Information):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(level)
        msg.setText(text)
        msg.setInformativeText(info.__str__() if isinstance(info, Exception) else info)
        msg.setWindowTitle('S&V')
        msg.exec_()
