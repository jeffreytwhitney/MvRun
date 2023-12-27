import os
import sys
from PyQt6.QtWidgets import QMessageBox, QFileDialog
from pathlib import Path

import lib.Utilities
import lib.MicroVuFileProcessor
from lib.MicroVuFileProcessor import ProcessorException
from ui.ui_MvRun_MainWindow import ui_MvRun_MainWindow
from PyQt6 import QtWidgets

this = sys.modules[__name__]

recent_files_filepath = ""


def _write_recent_files(file_lines: list[str]):
    list_filepath = _get_recentfiles_filepath()
    with open(list_filepath, "w") as f:
        for file in file_lines:
            f.write(f"{file.strip()}\n")


def _get_recentfiles_filepath() -> str:
    if this.recent_files_filepath:
        return this.recent_files_filepath
    pattern = 'recent_files.txt'
    for root, dirs, files in os.walk(os.getcwd()):
        for file in files:
            if file == pattern:
                this.recent_files_filepath = os.path.join(root, file)
    return this.recent_files_filepath or ""


def _get_list_of_recent_files() -> list[str]:
    list_filepath = _get_recentfiles_filepath()
    if not list_filepath:
        return []

    with open(list_filepath, "r") as f:
        return f.readlines()


def _get_index_containing_text(file_lines: list[str], text_to_find: str) -> int:
    return next(
        (
            i
            for i, l in enumerate(file_lines)
            if l.upper().find(text_to_find.upper()) > -1
        ),
        -1,
    )


def _delete_lines_containing_text(file_lines: list[str], text_to_find: str) -> list[str]:
    idx_to_delete = _get_index_containing_text(file_lines, text_to_find)
    while idx_to_delete > -1:
        del file_lines[idx_to_delete]
        idx_to_delete = _get_index_containing_text(file_lines, text_to_find)
    return file_lines


def _save_recent_file(recent_file: str):
    recent_file_lines = _get_list_of_recent_files()
    recent_file_lines = _delete_lines_containing_text(recent_file_lines, recent_file)
    recent_file_lines.insert(0, recent_file)
    _write_recent_files(recent_file_lines)


class MvRun_MainWindow(QtWidgets.QMainWindow, ui_MvRun_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.recent_files_filepath = ""
        self.btnFind.clicked.connect(self.btnFind_clicked)
        self.btnRunMicroVu.clicked.connect(self.btnRunMicroVu_clicked)
        self.cboRecentPrograms.currentTextChanged.connect(self.cboRecentPrograms_currentTextChanged)
        self._load_recent_files()
        self.cboRecentPrograms.setEnabled(True)

    def _show_error_message(self, message: str, title: str):
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Icon.Critical)
        msg_box.setText(message)
        msg_box.setWindowTitle(title)
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg_box.exec()

    def _show_message(self, message: str, title: str):
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Icon.Information)
        msg_box.setText(message)
        msg_box.setWindowTitle(title)
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg_box.exec()

    def _get_directory_via_dialog(self, title, default_directory=""):
        dialog = QFileDialog()
        return_path = dialog.getExistingDirectory(self, title, default_directory)
        return str(Path(return_path).absolute()) + "\\"

    def cboRecentPrograms_currentTextChanged(self):
        pass

    def btnFind_clicked(self):
        pass

    def btnRunMicroVu_clicked(self):
        pass

    def _load_recent_files(self):
        recent_file_lines = _get_list_of_recent_files()
        self.cboRecentPrograms.clear()
        self.cboRecentPrograms.addItem("", "")
        for line in recent_file_lines:
            base_name = os.path.basename(line).strip()
            self.cboRecentPrograms.addItem(base_name, line)


def main():
    app = QtWidgets.QApplication(sys.argv)
    ui = MvRun_MainWindow()
    ui.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
