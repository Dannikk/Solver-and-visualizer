from .ui import Window
from typing import List
from PyQt5 import QtCore


ANSWER_FORMAT = '.4e'
WARNING = 'Warning!'
ERROR = 'Error!'
ANSWER = 'Answer:'
WINDOW_TITLE = 'S&V'
func = 'x^2+y^2'
hard_func = "(x + 2y - 7)^2 + (2x + y - 5)^2"
McCormic_func = "sin(x+y) + (x - y)^2 - 1.5x + 2.5y + 1"
start_point = ['20', '30']
start_point_hard = ['9', '-5']
McCormic_start = ['-4', '-2']
min_point = [0, 0]
min_point_hard = [1, 3]
McCormic_min_point = [-0.54719, -1.54719]
acc_str = '0.001'
accuracy = 0.001


def init_test_app(function: str, start: List[str]) -> Window:

    window_app = Window()
    window_app.textEdit_func.setText(function)
    window_app.plainTextEdit_X.setPlainText(start[0])
    window_app.plainTextEdit_Y.setPlainText(start[1])
    window_app.comboBox_accuracy.setCurrentText(acc_str)
    return window_app


def test_correct(qtbot):
    window_app = init_test_app(func, start_point)
    qtbot.addWidget(window_app.main_window)
    qtbot.mouseClick(window_app.btn_find, QtCore.Qt.LeftButton)
    assert sum([(x - y) ** 2 for x, y in zip(window_app.interaction.res, min_point)]) < accuracy


def test_correct_hard(qtbot):
    window_app = init_test_app(hard_func, start_point_hard)
    qtbot.addWidget(window_app.main_window)
    qtbot.mouseClick(window_app.btn_find, QtCore.Qt.LeftButton)
    print(window_app.interaction.accuracy)
    assert sum([(x - y) ** 2 for x, y in zip(window_app.interaction.res, min_point_hard)]) < accuracy
