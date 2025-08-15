import os
import subprocess
import sys
from typing import List

from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QMessageBox, QFileDialog
import pywinctl
import lib
from lib import Utilities, MicroVuFileProcessor
from ui.ui_MvRun_MainWindow import Ui_MvRun_MainWindow

this = sys.modules[__name__]

recent_program_list = ""


def _write_recent_program_list_to_file(recent_folder_locations: list[str]):
    recent_program_list_filepath = _get_recent_program_list()
    line_count = min(len(recent_folder_locations), 15)

    with open(recent_program_list_filepath, "w") as f:
        for i in range(line_count):
            f.write(f"{recent_folder_locations[i].strip()}\n")


def _get_recent_program_list() -> str:
    if this.recent_program_list:
        return this.recent_program_list
    pattern = 'recent_folders.txt'
    for root, dirs, files in os.walk(os.getcwd()):
        for file in files:
            if file == pattern:
                this.recent_program_list = os.path.join(root, file)
    return this.recent_program_list or ""


def _get_list_of_recent_folders() -> list[str]:
    list_filepath = _get_recent_program_list()
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


def _save_recent_folder_to_list(recent_folder: str):
    recent_folders = _get_list_of_recent_folders()
    recent_folders = _delete_lines_containing_text(recent_folders, recent_folder)
    recent_folders.insert(0, recent_folder)
    _write_recent_program_list_to_file(recent_folders)


class MvRun_MainWindow(QtWidgets.QMainWindow, Ui_MvRun_MainWindow):
    _input_rootpath: str
    _output_path: str
    _min_employee_number: int
    _max_employee_number: int
    _inspec_directory: str
    _inspec_exe_name: str
    _inspec_iscmd_exe_name: str
    _inspec_filepath: str
    _inspec_iscmd_filepath: str
    _multi_sequence_numbers: List[QtWidgets.QLineEdit] = []
    _micro_vu_processor: MicroVuFileProcessor.Processor
    _input_dirpath: str
    _input_filepath: str
    _output_filepath: str

    # Dunder Methods
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self._load_settings()
        self._load_recent_folders()
        self._bind_events()
        return

    # Protected Methods
    def _add_sequence_number_fields(self):
        self.txtSequenceNumber2 = QtWidgets.QLineEdit(parent=self.user_fields_widget)
        self.txtSequenceNumber2.setMaximumWidth(50)
        self.user_fields_layout.addWidget(self.txtSequenceNumber2, 5, 1)
        self.user_fields_widget.setLayout(self.user_fields_layout)
        current_size = self.main_window.size()
        self.main_window.resize(current_size.width(), current_size.height() + 25)
        return

    def _bind_events(self):
        self.btnFind.clicked.connect(self.btnFind_clicked)
        self.btnRunMicroVu.clicked.connect(self.btnRunMicroVu_clicked)
        self.cboRecentPrograms.currentTextChanged.connect(self.cboRecentPrograms_currentTextChanged)
        self.txtSequenceNumber.textChanged.connect(self.txtSequenceNumber_textchanged)
        self.txtJobNumber.textChanged.connect(self.txtJobNumber_textchanged)
        self.txtEmployeeID.textChanged.connect(self.txtEmployeeID_textchanged)
        self.txtMachineName.textChanged.connect(self.txtMachineName_textchanged)
        self.lstPrograms.itemSelectionChanged.connect(self.program_list_item_selected)

        return

    def _clear_form(self):
        self.txtEmployeeID.setText("")
        self.txtJobNumber.setText("")
        self.txtMachineName.setText("")
        self.txtSequenceNumber.setText("")

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
        if not self.lstPrograms.currentItem().text().strip():
            self.btnRunMicroVu.setEnabled(False)
            return
        self.btnRunMicroVu.setEnabled(True)
        return

    def _execute_microvu_program(self, microvu_program_path: str):
        win = pywinctl.getWindowsWithTitle('InSpec', condition=pywinctl.Re.CONTAINS)[0]
        win.activate()
        run_text = f"\"{self._inspec_iscmd_filepath}\" /run \"{microvu_program_path}\" /nowait"
        subprocess.Popen(run_text, stderr=subprocess.DEVNULL, shell=True)

    def _get_dirpath_via_dialog(self, title, default_directory="") -> str:
        dialog = QFileDialog()
        return dialog.getExistingDirectory(self, title, default_directory)

    def _load_program_list(self):
        selected_program_path = str(self.cboRecentPrograms.currentData().strip())
        self.lstPrograms.clear()

        if not selected_program_path:
            return

        if not os.path.exists(selected_program_path):
            self._show_error_message(f"Directory '{self.cboRecentPrograms.currentText().strip()}' does not exist.", "File Not Found")
            return
        else:
            files = files = [file for file in os.listdir(selected_program_path) if file.lower().endswith('.iwp')]
            for file in files:
                if file.endswith(".iwp"):
                    self.lstPrograms.addItem(file)
        return

    def _load_recent_folders(self):
        recent_folders = _get_list_of_recent_folders()
        self.cboRecentPrograms.clear()
        self.cboRecentPrograms.addItem("", "")
        for dir_path in recent_folders:
            dir_path = dir_path.rstrip('\r\n').rstrip('\\')
            if dir_name := os.path.split(dir_path)[-1]:
                self.cboRecentPrograms.addItem(dir_name, dir_path)
        return

    def _load_settings(self):
        self._output_path = Utilities.get_stored_ini_value("Paths", "output_rootpath", "Settings")
        self._input_rootpath = Utilities.get_stored_ini_value("Paths", "input_rootpath", "Settings")
        self._min_employee_number = int(Utilities.get_stored_ini_value("MinMaxValues", "min_employee_number", "Settings"))
        self._max_employee_number = int(Utilities.get_stored_ini_value("MinMaxValues", "max_employee_number", "Settings"))
        self._inspec_directory = Utilities.get_stored_ini_value("Paths", "inspec_directory", "Settings")
        self._inspec_exe_name = Utilities.get_stored_ini_value("Paths", "inspec_exe_name", "Settings")
        self._inspec_iscmd_exe_name = Utilities.get_stored_ini_value("Paths", "iscmd_exe_name", "Settings")
        self._inspec_filepath = os.path.join(self._inspec_directory, self._inspec_exe_name)
        self._inspec_iscmd_filepath = os.path.join(self._inspec_directory, self._inspec_iscmd_exe_name)
        return

    def _start_inspec_application(self):
        Utilities.start_application(self._inspec_filepath)

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

    def _validate_form(self):
        self.txtEmployeeID.setStyleSheet("border : 1px solid black;")
        self.txtJobNumber.setStyleSheet("border : 1px solid black;")
        self.txtMachineName.setStyleSheet("border : 1px solid black;")
        self.txtSequenceNumber.setStyleSheet("border : 1px solid black;")

        if not self.txtJobNumber.text().strip():
            self._show_error_message("Job Number cannot be empty.", "Invalid Entry")
            self.txtJobNumber.setStyleSheet("border : 1px solid red;")
            return False
        if not self.txtMachineName.text().strip():
            self._show_error_message("Machine Name cannot be empty.", "Invalid Entry")
            self.txtMachineName.setStyleSheet("border : 1px solid red;")
            return False
        if not self.txtEmployeeID.text().strip():
            self.txtEmployeeID.setStyleSheet("border : 1px solid red;")
            self._show_error_message("Employee Number cannot be empty.", "Invalid Entry")
            return False
        if not self.txtSequenceNumber.text().strip():
            self.txtSequenceNumber.setStyleSheet("border : 1px solid red;")
            self._show_error_message("Sequence Number cannot be empty.", "Invalid Entry")
            return False
        if not self.txtSequenceNumber.text().strip().isdecimal() or int(self.txtSequenceNumber.text()) < 1:
            self.txtSequenceNumber.setStyleSheet("border : 1px solid red;")
            self._show_error_message("Invalid Sequence Number.", "Invalid Entry")
            return False
        if (not self.txtEmployeeID.text().strip().isdecimal()
                or int(self.txtEmployeeID.text()) < self._min_employee_number
                or int(self.txtEmployeeID.text()) > self._max_employee_number):
            self.txtEmployeeID.setStyleSheet("border : 1px solid red;")
            self._show_error_message("Invalid Employee Number.", "Invalid Entry")
            return False
        return True

    def _start_inspec_software(self):
        if not Utilities.is_process_running(self._inspec_exe_name):
            self._start_inspec_application()

    # Event Handlers
    def btnFind_clicked(self):
        if input_dirpath := self._get_dirpath_via_dialog(
                "Select Part Number Folder", self._input_rootpath
        ):
            input_dirpath = input_dirpath.rstrip('\r\n').rstrip('\\')
            dir_name = os.path.split(input_dirpath)[-1]
            exists = self.cboRecentPrograms.findText(dir_name) != -1
            if not exists:
                self.cboRecentPrograms.insertItem(1, dir_name, input_dirpath)
                self.cboRecentPrograms.setCurrentIndex(1)
            else:
                idx = self.cboRecentPrograms.findText(dir_name)
                self.cboRecentPrograms.setCurrentIndex(idx)
        self._enable_process_button()
        return

    def btnRunMicroVu_clicked(self):

        try:
            self._micro_vu_processor.process_file()
            self._clear_form()
        except Exception as e:
            self._show_error_message(f"Error occurred:'{e.args[0]}'.", "Runtime Error")
            return
        _save_recent_folder_to_list(self._input_filepath)
        self._start_inspec_software()
        self._execute_microvu_program(self._output_filepath)

    def cboRecentPrograms_currentTextChanged(self):
        self._load_program_list()

        # self._enable_process_button()
        return

    def program_list_item_selected(self):

        self._input_dirpath = str(self.cboRecentPrograms.currentData().strip())
        self._input_filepath = os.path.join(self._input_dirpath, self.lstPrograms.currentItem().text().strip())
        if not os.path.exists(self._input_dirpath):
            self._show_error_message(f"File '{self.cboRecentPrograms.currentText().strip()}' does not exist.", "File Not Found")
            return
        self._output_filepath = os.path.join(self._output_path, self.cboRecentPrograms.currentText().strip())
        self._micro_vu_processor = MicroVuFileProcessor.get_processor(self._input_filepath, self._output_filepath)
        self._add_sequence_number_fields()
        return

    def txtEmployeeID_textchanged(self):
        self._enable_process_button()
        return

    def txtJobNumber_textchanged(self):
        self._enable_process_button()
        return

    def txtMachineName_textchanged(self):
        self._enable_process_button()
        return

    def txtSequenceNumber_textchanged(self):
        self._enable_process_button()
        return


def main():
    stylesheet_filepath = lib.Utilities.get_filepath_by_name("MacOS.qss")
    styleSheet = lib.Utilities.get_file_as_string(stylesheet_filepath)
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(styleSheet)
    ui = MvRun_MainWindow()
    ui.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
