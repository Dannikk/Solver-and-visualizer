from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys


def application():
    app = QApplication(sys.argv)
    window = QMainWindow()

    window.setWindowTitle('xyu pizda')
    window.setGeometry(300, 250, 350, 200)

    main_text = QtWidgets.QLabel(window)
    main_text.setText('pizda xyu pizda xyu pizda xyu pizda xyu')
    main_text.adjustSize()

    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    # application()
    e = ValueError()
    e1 = ValueError('hueta')
    print(isinstance(e, ValueError))
    print(isinstance(e1, ValueError))