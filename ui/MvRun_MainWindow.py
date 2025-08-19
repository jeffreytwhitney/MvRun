import os
import sys
from datetime import datetime
from typing import List

from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QMessageBox, QFileDialog
import lib
from lib import Utilities, MicroVuFileProcessor
from lib.MicroVuProgram import MicroVuProgram
from ui.ui_MvRun_MainWindow import Ui_MvRun_MainWindow

this = sys.modules[__name__]

recent_program_list = ""


def _delete_lines_containing_text(file_lines: list[str], text_to_find: str) -> list[str]:
    idx_to_delete = _get_index_containing_text(file_lines, text_to_find)
    while idx_to_delete > -1:
        del file_lines[idx_to_delete]
        idx_to_delete = _get_index_containing_text(file_lines, text_to_find)
    return file_lines


def _get_index_containing_text(file_lines: list[str], text_to_find: str) -> int:
    return next(
        (
            i
            for i, l in enumerate(file_lines)
            if l.upper().find(text_to_find.upper()) > -1
        ),
        -1,
    )


def _get_micro_vu_sequence_count(program_filepath: str) -> int:
    if not os.path.exists(program_filepath):
        return 0
    micro_vu_program = MicroVuProgram(program_filepath)
    return micro_vu_program.sequence_count


def _get_list_of_recent_folders() -> list[str]:
    list_filepath = _get_recent_program_list()
    if not list_filepath:
        return []

    with open(list_filepath, "r") as f:
        return f.readlines()


def _get_recent_program_list():
    if this.recent_program_list:
        return this.recent_program_list
    pattern = 'recent_folders.txt'
    for root, dirs, files in os.walk(os.getcwd()):
        for file in files:
            if file == pattern:
                this.recent_program_list = os.path.join(root, file)
    return this.recent_program_list or ""


def _save_recent_folder_to_list(recent_folder: str):
    recent_folders = _get_list_of_recent_folders()
    recent_folders = _delete_lines_containing_text(recent_folders, recent_folder)
    recent_folders.insert(0, recent_folder)
    _write_recent_program_list_to_file(recent_folders)


def _write_recent_program_list_to_file(recent_folder_locations: list[str]):
    recent_program_list_filepath = _get_recent_program_list()
    line_count = min(len(recent_folder_locations), 15)

    with open(recent_program_list_filepath, "w") as f:
        for i in range(line_count):
            f.write(f"{recent_folder_locations[i].strip()}\n")


class MvRun_MainWindow(QtWidgets.QMainWindow, Ui_MvRun_MainWindow):
    _input_rootpath: str
    _output_path: str
    _min_employee_number: int
    _max_employee_number: int
    _min_job_number_length: int
    _max_machine_name_length: int
    _max_sequence_number: int
    _inspec_exe_name: str
    _iscmd_filepath: str
    _inspec_filename: str
    _inspec_filepath: str
    _sequence_number_fields: List[QtWidgets.QLineEdit] = []
    _sequence_number_error_labels: List[QtWidgets.QLabel] = []
    _input_dirpath: str
    _input_filepath: str
    _output_filepath: str
    _sequence_count: int

    # Dunder Methods
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self._load_settings()
        self._load_recent_folders()
        self._bind_events()
        self._createSequenceField(4)
        return

    # Protected Methods
    def _bind_events(self):
        self.btnFind.clicked.connect(self.btnFind_clicked)
        self.btnRunMicroVu.clicked.connect(self.btnRunMicroVu_clicked)
        self.cboRecentPrograms.currentTextChanged.connect(self.cboRecentPrograms_currentTextChanged)
        self.cboRunSetup.currentTextChanged.connect(self.cboRunSetup_currentTextChanged)
        self.txtJobNumber.textChanged.connect(self.txtJobNumber_textchanged)
        self.txtEmployeeID.textChanged.connect(self.txtEmployeeID_textchanged)
        self.txtMachineName.textChanged.connect(self.txtMachineName_textchanged)
        self.lstPrograms.currentItemChanged.connect(self.lstPrograms_currentItemChanged)
        return

    def _clear_form(self):
        self.txtEmployeeID.setText("")
        self.txtJobNumber.setText("")
        self.txtMachineName.setText("")
        self._reset_sequence_number_fields()

    def _createSequenceField(self, index):
        txtMultiSequenceNumber = QtWidgets.QLineEdit(parent=self.user_fields_widget)
        txtMultiSequenceNumber.setMaximumWidth(50)
        self.user_fields_layout.addWidget(txtMultiSequenceNumber, index, 1)
        txtMultiSequenceNumber.textChanged.connect(self.txtSequenceNumberMulti_textchanged)

        errorLabel_MultiSequenceNumber = QtWidgets.QLabel(parent=self.user_fields_widget)
        errorLabel_MultiSequenceNumber.setText("")
        errorLabel_MultiSequenceNumber.setStyleSheet("color: red;")
        self.user_fields_layout.addWidget(errorLabel_MultiSequenceNumber, index, 2)

        self._sequence_number_fields.append(txtMultiSequenceNumber)
        self._sequence_number_error_labels.append(errorLabel_MultiSequenceNumber)

    def _enable_process_button(self):
        if len(self.txtJobNumber.text().strip()) < self._min_job_number_length:
            self.btnRunMicroVu.setEnabled(False)
            return

        if len(self.txtMachineName.text().strip()) < self._min_machine_name_length:
            self.btnRunMicroVu.setEnabled(False)
            return

        if (not self.txtEmployeeID.text().strip().isdecimal()
                or int(self.txtEmployeeID.text().strip()) < self._min_employee_number
                or int(self.txtEmployeeID.text().strip()) > self._max_employee_number):
            self.btnRunMicroVu.setEnabled(False)
            return

        for _ in self._sequence_number_fields:
            if not _.text().strip().isdecimal():
                self.btnRunMicroVu.setEnabled(False)
                return

        if not self.lstPrograms.currentItem().text().strip():
            self.btnRunMicroVu.setEnabled(False)
            return
        self.btnRunMicroVu.setEnabled(True)
        return

    def _generate_output_filename(self, program_filename):
        program_name = os.path.splitext(program_filename)[0]
        current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{program_name}_{current_datetime}.iwp"

    def _generate_sequence_number_fields(self):
        self._reset_sequence_number_fields()
        if self._is_setup():
            self.main_window.resize(600, 500)
            self.lblSequenceNumber.setText("")
            self._enable_process_button()
            return

        if self._sequence_count == 1:
            self.lblSequenceNumber.setText("Sequence Number:")
        elif self._sequence_count > 1:
            self.lblSequenceNumber.setText("Sequence Numbers:")

        if self._sequence_count == 1:
            return

        for i in range(1, self._sequence_count):
            self._createSequenceField(i + 4)
            current_size = self.main_window.size()
            self.main_window.resize(current_size.width(), current_size.height() + 25)

        self.user_fields_widget.setLayout(self.user_fields_layout)
        self._enable_process_button()
        return

    def _get_sequence_number_values(self) -> list[int]:
        if self._is_setup():
            return [0] * self._sequence_count
        sequence_numbers = []
        for i in range(len(self._sequence_number_fields)):
            sequence_number_field = self._sequence_number_fields[i]
            sequence_numbers.append(int(sequence_number_field.text()))
        return sequence_numbers

    def _get_dirpath_via_dialog(self, title, default_directory="") -> str:
        dialog = QFileDialog()
        return dialog.getExistingDirectory(self, title, default_directory)

    def _is_setup(self) -> bool:
        selected_value = self.cboRunSetup.currentText()
        return selected_value == "Setup"

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
        self._min_job_number_length = int(Utilities.get_stored_ini_value("MinMaxValues", "min_job_number_length", "Settings"))
        self._min_machine_name_length = int(Utilities.get_stored_ini_value("MinMaxValues", "min_machine_name_length", "Settings"))
        self._max_sequence_number = int(Utilities.get_stored_ini_value("MinMaxValues", "max_sequence_number", "Settings"))
        self._inspec_filepath = Utilities.get_stored_ini_value("Paths", "inspec_filepath", "Settings")
        self._inspec_filename = Utilities.get_stored_ini_value("Paths", "inspec_filename", "Settings")
        self._iscmd_filepath = Utilities.get_stored_ini_value("Paths", "iscmd_filepath", "Settings")
        return

    def _remove_sequence_number_field(self, i):
        sequence_number_field = self._sequence_number_fields[i]
        sequence_number_error_label = self._sequence_number_error_labels[i]
        self.user_fields_layout.removeWidget(sequence_number_field)
        sequence_number_field.deleteLater()
        self.user_fields_layout.removeWidget(sequence_number_error_label)
        sequence_number_error_label.deleteLater()
        return

    def _reset_form_errors(self):
        self.txtEmployeeID.setStyleSheet("border : 1px solid black;")
        self.txtJobNumber.setStyleSheet("border : 1px solid black;")
        self.txtMachineName.setStyleSheet("border : 1px solid black;")
        for i in self._sequence_number_fields:
            i.setStyleSheet("border : 1px solid black;")
        self.lblError_EmployeeID.setText("")
        self.lblError_JobNumber.setText("")
        self.lblError_MachineName.setText("")
        for i in self._sequence_number_error_labels:
            i.setText("")
            i.setStyleSheet("color: black;")

    def _reset_sequence_number_fields(self):
        if self._is_setup():
            for i in range(len(self._sequence_number_fields)):
                self._remove_sequence_number_field(i)
            self._sequence_number_fields.clear()
            self._sequence_number_error_labels.clear()
            return

        if len(self._sequence_number_fields) == 0:
            self._createSequenceField(4)
            return

        for i in range(1, len(self._sequence_number_fields)):
            self._remove_sequence_number_field(i)

        self._sequence_number_fields = self._sequence_number_fields[:1]
        self._sequence_number_error_labels = self._sequence_number_error_labels[:1]
        self._sequence_number_fields[0].setText("")
        self._sequence_number_error_labels[0].setText("")
        self.main_window.resize(600, 500)
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

    def _validate_form(self):
        form_is_valid = True
        self._reset_form_errors()

        if len(self.txtJobNumber.text().strip()) < self._min_job_number_length:
            self.lblError_JobNumber.setText(f"Job Number less than {self._min_job_number_length} characters long.")
            self.txtJobNumber.setStyleSheet("border : 1px solid red;")
            form_is_valid = False

        if len(self.txtMachineName.text().strip()) < self._min_machine_name_length:
            self.lblError_MachineName.setText(f"Machine Name less than {self._min_machine_name_length} characters long.")
            self.txtMachineName.setStyleSheet("border : 1px solid red;")
            form_is_valid = False

        if (not self.txtEmployeeID.text().strip().isdecimal()
                or int(self.txtEmployeeID.text().strip()) < self._min_employee_number
                or int(self.txtEmployeeID.text().strip()) > self._max_employee_number):
            self.txtEmployeeID.setStyleSheet("border : 1px solid red;")
            self.lblError_EmployeeID.setText(f"Employee Number must be between {self._min_employee_number} and {self._max_employee_number}.")
            form_is_valid = False

        if not self._is_setup():
            # Check for valid sequence numbers
            for idx, s in enumerate(self._sequence_number_fields):
                if (not s.text().strip().isdecimal()
                        or int(s.text()) < 1
                        or int(s.text()) > self._max_sequence_number):
                    self._sequence_number_error_labels[
                        idx].setText(f"Sequence Number must be between 1 and {self._max_sequence_number}.")
                    self._sequence_number_error_labels[idx].setStyleSheet("border : 1px solid red;")
                    form_is_valid = False

            # Check for duplicate sequence numbers
            if self._sequence_count > 1:
                for idx, s in enumerate(self._sequence_number_fields):
                    current_sequence_number = int(s.text())
                    for dup_idx in range(idx + 1, len(self._sequence_number_fields)):
                        if current_sequence_number == int(self._sequence_number_fields[dup_idx].text()):
                            if self._sequence_number_error_labels[idx].text() == "":
                                self._sequence_number_error_labels[idx].setText("Sequence Numbers must be unique.")
                                self._sequence_number_fields[idx].setStyleSheet("border : 1px solid red;")
                            if self._sequence_number_error_labels[dup_idx].text() == "":
                                self._sequence_number_error_labels[dup_idx].setText("Sequence Numbers must be unique.")
                                self._sequence_number_fields[dup_idx].setStyleSheet("border : 1px solid red;")
                            form_is_valid = False

        return form_is_valid

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
        if not self._validate_form():
            return
        try:
            output_filename = self._generate_output_filename(self.lstPrograms.currentItem().text().strip())
            self._output_filepath = os.path.join(self._output_path, output_filename)
            sequence_numbers = self._get_sequence_number_values()
            micro_vu_processor = MicroVuFileProcessor.get_processor(self._input_filepath, self._is_setup(),
                                                                    self.txtMachineName.text().strip(),
                                                                    self.txtEmployeeID.text().strip(),
                                                                    self.txtJobNumber.text().strip(),
                                                                    sequence_numbers,
                                                                    self._output_filepath)

            micro_vu_processor.process_file()
        except Exception as e:
            self._show_error_message(f"Error occurred:'{e.args[0]}'.", "Runtime Error")
            return
        _save_recent_folder_to_list(self._input_dirpath)
        Utilities.execute_micro_vu_program(self._iscmd_filepath, self._inspec_filepath, self._inspec_filename, self._output_filepath)

    def cboRecentPrograms_currentTextChanged(self, new_text):
        self._input_dirpath = str(self.cboRecentPrograms.currentData().strip())
        self._clear_form()
        self._load_program_list()
        return

    def cboRunSetup_currentTextChanged(self):
        self._generate_sequence_number_fields()

    def lstPrograms_currentItemChanged(self):
        if self.lstPrograms.currentItem() is not None:
            self._input_filepath = os.path.join(self._input_dirpath, self.lstPrograms.currentItem().text().strip())
            if not os.path.exists(self._input_filepath):
                self._show_error_message(f"File '{self._input_filepath}' does not exist.", "File Not Found")
                return
            self._sequence_count = _get_micro_vu_sequence_count(self._input_filepath)
            self._generate_sequence_number_fields()
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

    def txtSequenceNumberMulti_textchanged(self):
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
