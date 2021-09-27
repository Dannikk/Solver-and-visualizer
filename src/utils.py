from dataclasses import dataclass
from PyQt5.QtWidgets import QPushButton, QPlainTextEdit, QLabel, QTextEdit, QComboBox
from typing import Any
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
import numpy as np
from enum import Enum

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
