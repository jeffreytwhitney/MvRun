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

recent_programs_file_location = ""


def _write_recent_program_locations_to_file(recent_file_locations: list[str]):
    recent_program_list_filepath = _get_recent_program_list_file_location()
    line_count = min(len(recent_file_locations), 15)

    with open(recent_program_list_filepath, "w") as f:
        for i in range(line_count):
            f.write(f"{recent_file_locations[i].strip()}\n")


def _get_recent_program_list_file_location() -> str:
    if this.recent_programs_file_location:
        return this.recent_programs_file_location
    pattern = 'recent_files.txt'
    for root, dirs, files in os.walk(os.getcwd()):
        for file in files:
            if file == pattern:
                this.recent_programs_file_location = os.path.join(root, file)
    return this.recent_programs_file_location or ""


def _get_list_of_recent_files() -> list[str]:
    list_filepath = _get_recent_program_list_file_location()
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


def _save_recent_file_to_list(recent_file: str):
    recent_files = _get_list_of_recent_files()
    recent_files = _delete_lines_containing_text(recent_files, recent_file)
    recent_files.insert(0, recent_file)
    _write_recent_program_locations_to_file(recent_files)


class MvRun_MainWindow(QtWidgets.QMainWindow, ui_MvRun_MainWindow):
    _input_rootpath: str
    _output_path: str

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self._load_settings()
        self._load_recent_files()
        self._bind_events()
        return

    def _bind_events(self):
        self.btnFind.clicked.connect(self.btnFind_clicked)
        self.btnRunMicroVu.clicked.connect(self.btnRunMicroVu_clicked)
        self.cboRecentPrograms.currentTextChanged.connect(self.cboRecentPrograms_currentTextChanged)
        self.txtSequenceNumber.textChanged.connect(self.txtSequenceNumber_textchanged)
        self.txtJobNumber.textChanged.connect(self.txtJobNumber_textchanged)
        self.txtEmployeeID.textChanged.connect(self.txtEmployeeID_textchanged)
        self.txtMachineName.textChanged.connect(self.txtMachineName_textchanged)
        return



    def _load_settings(self):
        self._output_path = lib.Utilities.GetStoredIniValue("Paths", "outputrootpath", "Settings")
        self._input_rootpath = lib.Utilities.GetStoredIniValue("Paths", "inputrootpath", "Settings")
        return

    def _show_error_message(self, message: str, title: str) -> None:
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
        return

    def _get_filepath_via_dialog(self, title, default_directory="") -> str:
        dialog = QFileDialog()
        return dialog.getOpenFileName(self, title, default_directory, "MicroVu Files (*.iwp)")

    def _enable_process_button(self):
        if not self.txtJobNumber.text().strip():
            self.btnRunMicroVu.setEnabled(False)
            return
        if not self.txtMachineName.text().strip():
            self.btnRunMicroVu.setEnabled(False)
            return
        if not self.txtEmployeeID.text().strip():
            self.btnRunMicroVu.setEnabled(False)
            return
        if not self.txtSequenceNumber.text().strip():
            self.btnRunMicroVu.setEnabled(False)
            return
        if not self.cboRecentPrograms.currentText().strip():
            self.btnRunMicroVu.setEnabled(False)
            return
        self.btnRunMicroVu.setEnabled(True)
        return

    def _load_recent_files(self):
        recent_files = _get_list_of_recent_files()
        self.cboRecentPrograms.clear()
        self.cboRecentPrograms.addItem("", "")
        for file_path in recent_files:
            if base_name := os.path.basename(file_path).strip():
                self.cboRecentPrograms.addItem(base_name, file_path)
        return

    def _validate_form(self):
        if not self.txtJobNumber.text().strip():
            self._show_error_message("Job Number cannot be empty.", "Invalid Entry")
            return False
        if not self.txtMachineName.text().strip():
            self._show_error_message("Machine Name cannot be empty.", "Invalid Entry")
            return False
        if not self.txtEmployeeID.text().strip():
            self._show_error_message("Employee Number cannot be empty.", "Invalid Entry")
            return False
        if not self.txtSequenceNumber.text().strip():
            self._show_error_message("Sequence Number cannot be empty.", "Invalid Entry")
            return False

    def txtJobNumber_textchanged(self):
        self._enable_process_button()
        return

    def txtMachineName_textchanged(self):
        self._enable_process_button()
        return

    def txtEmployeeID_textchanged(self):
        self._enable_process_button()
        return

    def txtSequenceNumber_textchanged(self):
        self._enable_process_button()
        return

    def cboRecentPrograms_currentTextChanged(self):
        self._enable_process_button()
        return

    def btnFind_clicked(self):
        output_filepath, file_filter = self._get_filepath_via_dialog("Select MicroVu File", self._input_rootpath)
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
