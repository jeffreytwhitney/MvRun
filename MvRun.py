import sys
from PyQt6 import QtWidgets

from lib import Utilities
from ui.MvRun_MainWindow import MvRun_MainWindow


def main():
    stylesheet_filepath = Utilities.get_filepath_by_name("MacOS.qss")
    styleSheet = Utilities.get_file_as_string(stylesheet_filepath)
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(styleSheet)
    ui = MvRun_MainWindow()
    ui.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
