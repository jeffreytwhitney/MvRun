from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QSizePolicy

import lib.Utilities


class Ui_MvRun_MainWindow(object):
    main_window: QtWidgets.QMainWindow
    centralwidget: QtWidgets.QWidget
    centrallayout: QtWidgets.QGridLayout
    part_number_selection_widget: QtWidgets.QWidget
    part_number_selection_layout: QtWidgets.QGridLayout
    btnFind: QtWidgets.QToolButton
    lblPartNumber: QtWidgets.QLabel
    cboRecentPrograms: QtWidgets.QComboBox
    program_list_widget: QtWidgets.QWidget
    program_list_layout: QtWidgets.QGridLayout
    lblProgramList: QtWidgets.QLabel
    lstPrograms: QtWidgets.QListWidget
    placeholder_widget: QtWidgets.QWidget
    user_fields_widget: QtWidgets.QWidget
    user_fields_layout: QtWidgets.QGridLayout
    lblRunSetup: QtWidgets.QLabel
    cboRunSetup: QtWidgets.QComboBox
    ue_placeholder_widget: QtWidgets.QWidget
    lblEmployeeID: QtWidgets.QLabel
    txtEmployeeID: QtWidgets.QLineEdit
    lblJobNumber: QtWidgets.QLabel
    txtJobNumber: QtWidgets.QLineEdit
    lblMachineName: QtWidgets.QLabel
    txtMachineName: QtWidgets.QLineEdit
    lblSequenceNumber: QtWidgets.QLabel
    txtSequenceNumber: QtWidgets.QLineEdit
    btnRunMicroVu: QtWidgets.QPushButton
    statusbar: QtWidgets.QStatusBar

    def setupUi(self, main_window):
        icon_filepath: str = lib.Utilities.get_filepath_by_name("MvRun.ico")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(icon_filepath), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.main_window = main_window
        self.main_window.resize(600, 500)
        self.main_window.setMinimumSize(QtCore.QSize(600, 500))
        self.main_window.setMaximumSize(QtCore.QSize(600, 800))
        self.main_window.setWindowTitle("MvRun")

        self.centralwidget = QtWidgets.QWidget(parent=self.main_window)
        self.centralwidget.setObjectName("centralwidget")
        self.centralwidget.setWindowIcon(icon)
        self.centrallayout = QtWidgets.QGridLayout(self.centralwidget)

        # Program Search And Selection ------------------------------------------------
        self.part_number_selection_widget = QtWidgets.QWidget(parent=self.centralwidget)
        self.part_number_selection_widget.setMaximumHeight(70)

        self.part_number_selection_layout = QtWidgets.QGridLayout(self.part_number_selection_widget)
        self.part_number_selection_layout.setContentsMargins(0, 0, 0, 0)

        self.btnFind = QtWidgets.QToolButton(parent=self.part_number_selection_widget)
        self.btnFind.setText("...")
        self.part_number_selection_layout.addWidget(self.btnFind, 1, 1)

        self.lblPartNumber = QtWidgets.QLabel(parent=self.part_number_selection_widget)
        self.lblPartNumber.setText("Part Number:")
        self.part_number_selection_layout.addWidget(self.lblPartNumber, 0, 0)

        self.cboRecentPrograms = QtWidgets.QComboBox(parent=self.part_number_selection_widget)
        self.part_number_selection_layout.addWidget(self.cboRecentPrograms, 1, 0)

        self.part_number_selection_widget.setLayout(self.part_number_selection_layout)
        self.centrallayout.addWidget(self.part_number_selection_widget, 0, 0)
        # -----------------------------------------------------------------------------

        # Program List-----------------------------------------------------------------
        self.program_list_widget = QtWidgets.QWidget(parent=self.centralwidget)
        self.program_list_widget.setMaximumHeight(150)
        self.program_list_layout = QtWidgets.QGridLayout(self.program_list_widget)
        self.program_list_layout.setContentsMargins(0, 0, 0, 0)

        self.lblProgramList = QtWidgets.QLabel(parent=self.program_list_widget)
        self.lblProgramList.setText("Programs:")
        self.program_list_layout.addWidget(self.lblProgramList, 0, 0)

        self.lstPrograms = QtWidgets.QListWidget(parent=self.program_list_widget)
        self.lstPrograms.setMaximumHeight(175)
        self.lstPrograms.setMaximumWidth(200)
        self.program_list_layout.addWidget(self.lstPrograms, 1, 0)

        self.placeholder_widget = QtWidgets.QWidget(parent=self.program_list_widget)
        self.program_list_layout.addWidget(self.placeholder_widget, 1, 1)

        self.program_list_widget.setLayout(self.program_list_layout)
        self.centrallayout.addWidget(self.program_list_widget, 1, 0)
        # -----------------------------------------------------------------------------

        # User-Entered Fields----------------------------------------------------------
        self.user_fields_widget = QtWidgets.QWidget(parent=self.centralwidget)
        self.user_fields_widget.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.user_fields_layout = QtWidgets.QGridLayout(self.user_fields_widget)
        self.user_fields_layout.setContentsMargins(0, 0, 0, 0)

        self.lblRunSetup = QtWidgets.QLabel(parent=self.centralwidget)
        self.lblRunSetup.setText("Run/Setup:")
        self.user_fields_layout.addWidget(self.lblRunSetup, 0, 0)

        self.cboRunSetup = QtWidgets.QComboBox(parent=self.centralwidget)
        self.cboRunSetup.addItem("Run")
        self.cboRunSetup.addItem("Setup")
        self.user_fields_layout.addWidget(self.cboRunSetup, 0, 1)

        # hack to get the grid to look right
        self.ue_placeholder_widget = QtWidgets.QWidget(parent=self.user_fields_widget)
        self.ue_placeholder_widget.setMinimumWidth(370)
        self.user_fields_layout.addWidget(self.ue_placeholder_widget, 0, 2)

        self.lblEmployeeID = QtWidgets.QLabel(parent=self.user_fields_widget)
        self.lblEmployeeID.setText("Employee ID:")
        self.user_fields_layout.addWidget(self.lblEmployeeID, 1, 0)

        self.txtEmployeeID = QtWidgets.QLineEdit(parent=self.user_fields_widget)
        self.txtEmployeeID.setMaximumWidth(50)
        self.txtEmployeeID.setMaxLength(20)
        self.user_fields_layout.addWidget(self.txtEmployeeID, 1, 1)

        self.lblJobNumber = QtWidgets.QLabel(parent=self.user_fields_widget)
        self.lblJobNumber.setText("Job Number:")
        self.user_fields_layout.addWidget(self.lblJobNumber, 2, 0)

        self.txtJobNumber = QtWidgets.QLineEdit(parent=self.user_fields_widget)
        self.txtJobNumber.setMaximumWidth(100)
        self.txtJobNumber.setMaxLength(20)
        self.user_fields_layout.addWidget(self.txtJobNumber, 2, 1)

        self.lblMachineName = QtWidgets.QLabel(parent=self.user_fields_widget)
        self.lblMachineName.setText("Machine Name:")
        self.user_fields_layout.addWidget(self.lblMachineName, 3, 0)

        self.txtMachineName = QtWidgets.QLineEdit(parent=self.user_fields_widget)
        self.txtMachineName.setMaximumWidth(100)
        self.user_fields_layout.addWidget(self.txtMachineName, 3, 1)

        self.lblSequenceNumber = QtWidgets.QLabel(parent=self.user_fields_widget)
        self.lblSequenceNumber.setText("Sequence Number(s):")
        self.user_fields_layout.addWidget(self.lblSequenceNumber, 4, 0)

        self.txtSequenceNumber = QtWidgets.QLineEdit(parent=self.user_fields_widget)
        self.txtSequenceNumber.setMaximumWidth(50)
        self.user_fields_layout.addWidget(self.txtSequenceNumber, 4, 1)

        self.user_fields_widget.setLayout(self.user_fields_layout)
        self.centrallayout.addWidget(self.user_fields_widget, 2, 0)
        # -----------------------------------------------------------------------------

        # Run Button-------------------------------------------------------------------
        self.btnRunMicroVu = QtWidgets.QPushButton(parent=self.centralwidget)
        self.btnRunMicroVu.setObjectName("btnRunMicroVu")
        self.btnRunMicroVu.setText("Run MicroVu")
        self.btnRunMicroVu.setEnabled(False)
        self.centrallayout.addWidget(self.btnRunMicroVu, 3, 0, QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignBottom)
        # -----------------------------------------------------------------------------

        self.centralwidget.setLayout(self.centrallayout)

        # Status Bar-------------------------------------------------------------------
        main_window.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(parent=main_window)
        main_window.setStatusBar(self.statusbar)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MvRun_MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MvRun_MainWindow()
    ui.setupUi(MvRun_MainWindow)
    MvRun_MainWindow.show()
    sys.exit(app.exec())
