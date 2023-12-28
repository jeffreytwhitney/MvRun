import sys
from PyQt6 import QtWidgets
from ui.MvRun_MainWindow import MvRun_MainWindow


def main():
    app = QtWidgets.QApplication(sys.argv)
    ui = MvRun_MainWindow()
    ui.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
