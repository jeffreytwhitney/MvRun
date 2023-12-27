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
    line_count = min(len(file_lines), 15)

    with open(list_filepath, "w") as f:
        for i in range(line_count):
            f.write(f"{file_lines[i].strip()}\n")


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
    _input_rootpath: str
    _output_path: str

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self._input_rootpath = ""
        self._output_path = ""
        self._load_settings()
        self._load_recent_files()
        self.btnFind.clicked.connect(self.btnFind_clicked)
        self.btnRunMicroVu.clicked.connect(self.btnRunMicroVu_clicked)
        self.cboRecentPrograms.currentTextChanged.connect(self.cboRecentPrograms_currentTextChanged)
        return

    def _load_settings(self):
        self._output_path = lib.Utilities.GetStoredIniValue("Paths", "outputrootpath", "Settings")
        self._input_rootpath = lib.Utilities.GetStoredIniValue("Paths", "inputrootpath", "Settings")
        return

    def _show_error_message(self, message: str, title: str):
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Icon.Critical)
        msg_box.setText(message)
        msg_box.setWindowTitle(title)
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg_box.exec()
        return

    def _show_message(self, message: str, title: str):
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Icon.Information)
        msg_box.setText(message)
        msg_box.setWindowTitle(title)
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg_box.exec()
        return

    def _get_filepath_via_dialog(self, title, default_directory="") -> str:
        dialog = QFileDialog()
        return dialog.getOpenFileName(self, title, default_directory, "MicroVu Files (*.iwp)")

    def _enable_process_button(self):
        if not self.txtJobNumber.text():
            self.btnRunMicroVu.setEnabled(False)
            return
        if not self.txtMachineName.text():
            self.btnRunMicroVu.setEnabled(False)
            return
        if not self.txtEmployeeID.text():
            self.btnRunMicroVu.setEnabled(False)
            return
        if not self.txtSequenceNumber.text():
            self.btnRunMicroVu.setEnabled(False)
            return
        if not self.cboRecentPrograms.currentText():
            self.btnRunMicroVu.setEnabled(False)
            return
        self.btnRunMicroVu.setEnabled(True)
        return

    def _load_recent_files(self):
        recent_file_lines = _get_list_of_recent_files()
        self.cboRecentPrograms.clear()
        self.cboRecentPrograms.addItem("", "")
        for line in recent_file_lines:
            if base_name := os.path.basename(line).strip():
                self.cboRecentPrograms.addItem(base_name, line)
        return

    def cboRecentPrograms_currentTextChanged(self):
        self._enable_process_button()
        return

    def btnFind_clicked(self):
        output_filepath, file_filter = self._get_filepath_via_dialog("Select Output Folder", self._input_rootpath)
        if output_filepath:
            base_name = os.path.basename(output_filepath).strip()
            self.cboRecentPrograms.insertItem(1, base_name, output_filepath)
            self.cboRecentPrograms.setCurrentIndex(1)
            self._enable_process_button()
        return

    def btnRunMicroVu_clicked(self):
        pass


def main():
    app = QtWidgets.QApplication(sys.argv)
    ui = MvRun_MainWindow()
    ui.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
