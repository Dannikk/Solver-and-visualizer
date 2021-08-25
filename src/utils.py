from dataclasses import dataclass
from PyQt5.QtWidgets import QPushButton, QPlainTextEdit, QLabel, QTextEdit
from typing import Any
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
import numpy as np
from itertools import combinations


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


def all_pairs(lst):
    n = len(lst) // 4
    grps = (lst[i:i + n] for i in range(0, len(lst), n))
    cmb = combinations(grps, 2)
    for a,b in cmb:
        yield ((a.pop(),b.pop()))


if __name__ == '__main__':
    names = list(range(11))

    it = iter(names)
    print(names)
    names = [str(first_name) + " " + str(second_name) for first_name, second_name in zip(it, it)]
    print(names)
    lst = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    it = iter(lst)
    a = it.__next__()
    b = it.__next__()
    while True:
        print(a, b)
        try:
            a, b = b, it.__next__()
        except StopIteration:
            break
    it = iter(lst)
    it2 = iter(lst)
    for a, b in zip(it, it2):
        print(a, b)