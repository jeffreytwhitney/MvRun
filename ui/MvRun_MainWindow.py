import os
import sys
from PyQt6.QtWidgets import QMessageBox, QFileDialog, QTableWidgetItem
from pathlib import Path

import lib.Utilities
import lib.MicroVuFileProcessor
from lib.MicroVuFileProcessor import ProcessorException
from ui.ui_MvRun_MainWindow import ui_MvRun_MainWindow
from PyQt6 import QtWidgets


class MvRun_MainWindow(QtWidgets.QMainWindow, ui_MvRun_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.btnFind.clicked.connect(self.btnFind_clicked)
        self.btnRunMicroVu.clicked.connect(self.btnRunMicroVu_clicked)
        self.cboRecentPrograms.currentTextChanged.connect(self.cboRecentPrograms_currentTextChanged)

    def cboRecentPrograms_currentTextChanged(self):
        pass

    def btnFind_clicked(self):
        pass

    def btnRunMicroVu_clicked(self):
        pass


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MvRun_MainWindow = QtWidgets.QMainWindow()
    ui = ui_MvRun_MainWindow()
    ui.setupUi(MvRun_MainWindow)
    MvRun_MainWindow.show()
    sys.exit(app.exec())
