from dataclasses import dataclass
from PyQt5 import QtWidgets
from src.utils import UIelements
import numpy as np
from src.parser import parse_function_expression, WrongFieldException
import src.parser as parser
from typing import Union, List, Callable, NoReturn, Tuple
from src.solver import solver, ErrorCode


ANSWER_FORMAT = '.4e'
WARNING = 'Warning!'
ERROR = 'Error!'
ANSWER = 'Answer:'
WINDOW_TITLE = 'S&V'


class Interaction:
    def __init__(self, ui_elements: UIelements):
        self.ui_elements = ui_elements
        self.solved = False
        self.set_functions()
        self.function: Callable = Callable
        self.gradient: Callable = Callable
        self.start: np.ndarray = np.array([])
        self.step_count: int = 0
        self.accuracy: float = 0.01

    def set_functions(self):
        self.ui_elements.find_btn.clicked.connect(self.find)

    def find(self) -> NoReturn:

        err = self.__parse_parameters()
        if err != ErrorCode.OK:
            self.show_answer(WARNING, info=err.value)
            self.show_message(WARNING, err.value, level=QtWidgets.QMessageBox.Warning)
            return NoReturn

        err, self.res = self.__solve_plot()
        if err != ErrorCode.OK:
            self.solved = False
            self.show_answer(WARNING, info=err.value)
            self.show_message(WARNING, err.value, level=QtWidgets.QMessageBox.Warning)
            return NoReturn
        self.solved = True
        self.show_answer(ANSWER, res=self.res)

    def __parse_parameters(self) -> ErrorCode:
        """
        Parsing and obtaining method parameters: function, gradient, start point and accuracy

        Returns
        -------

        """

        err, self.function, self.gradient = parser.parse_function_expression(self.ui_elements.func_field.toPlainText())
        # another pathetic attempt to avoid using exceptions
        if err != ErrorCode.OK:
            return err
        err, x = parser.parse_float(self.ui_elements.x_field.toPlainText())
        # I agree, it looks scary
        if err != ErrorCode.OK:
            return err
        err, y = parser.parse_float(self.ui_elements.y_field.toPlainText())
        if err != ErrorCode.OK:
            return err
        self.start = np.array([x, y])
        err, self.accuracy = parser.parse_float(self.ui_elements.cb_accuracy.currentText())
        # but ... why are exceptions so bad?
        if err != ErrorCode.OK:
            return err

        return ErrorCode.OK

    def __solve_plot(self) -> Tuple[ErrorCode, np.ndarray]:
        """
        Solving and plotting

        Returns
        -------
        Union[np.ndarray, Exception] :
            the minimum that sought by minimize method if no errors occurred
            or any Exception otherwise

        """
        err, res, points, values = solver(start=self.start, function=self.function,
                                          gradient=self.gradient, eps=self.accuracy)
        if err == ErrorCode.OK:
            self.solved = True
            self.plot_solution(points)
            return ErrorCode.OK, res
        else:
            return err, NoReturn

    def plot_solution(self, data: np.ndarray):
        # instead of ax.hold(False)
        self.ui_elements.figure.clear()

        # create an axis
        ax = self.ui_elements.figure.add_subplot(111)
        steps = len(data)
        tmp = data.transpose()
        ax.grid()
        ax.scatter(tmp[0], tmp[1], color='r', marker='*')
        for i in range(0, steps - 1):
            size = data[i+1] - data[i]
            width = np.linalg.norm(size) / 600
            ax.arrow(data[i][0], data[i][1], size[0], size[1], facecolor='b', edgecolor='black', linewidth=1,
                     width=width, length_includes_head=True)
        # refresh canvas
        self.ui_elements.canvas.draw()

    def show_message(self, text: str, info: Union[str, Exception, ErrorCode],
                     level: QtWidgets.QMessageBox.Icon = QtWidgets.QMessageBox.Information):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(level)
        msg.setText(text)
        if isinstance(info, Exception):
            info = info.__str__()
        elif isinstance(info, ErrorCode):
            info = info.value
        msg.setInformativeText(info)
        msg.setWindowTitle(WINDOW_TITLE)
        msg.exec_()

    def show_answer(self, prefix: str = '', info: Union[str, Exception, ErrorCode] = '', res: np.ndarray = None):
        if prefix == ANSWER and res.all():
            self.ui_elements.result_field.setText(f'{ANSWER} {res[0]:{ANSWER_FORMAT}}, {res[1]:{ANSWER_FORMAT}}')
        else:
            if isinstance(info, Exception):
                info = info.__str__()
            elif isinstance(info, ErrorCode):
                info = info.value
            self.ui_elements.result_field.setText(prefix + ' ' + info)
