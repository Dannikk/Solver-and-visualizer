from PyQt5 import QtWidgets
from src.ui import Window


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)

    # MainWindow = QtWidgets.QMainWindow()

    # window = Window(MainWindow)
    window = Window()
    # window.run()
    window.show()
    sys.exit(app.exec_())
