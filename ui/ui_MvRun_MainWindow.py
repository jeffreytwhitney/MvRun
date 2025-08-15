from PyQt6 import QtCore, QtGui, QtWidgets

import lib.Utilities


class Ui_MvRun_MainWindow(object):
    def __init__(self):
        self.centrallayout = None
        self.lblSequenceNumber = None
        self.txtSequenceNumber = None
        self.txtMachineName = None
        self.txtJobNumber = None
        self.lblJobNumber = None
        self.lblMachineName = None
        self.txtEmployeeID = None
        self.lblEmployeeID = None
        self.user_fields_layout = None
        self.user_fields_widget = None
        self.lstPrograms = None
        self.statusbar = None
        self.lblProgramList = None
        self.program_list_layout = None
        self.lblPartNumber = None
        self.program_list_widget = None
        self.cboRecentPrograms = None
        self.btnFind = None
        self.btnRunMicroVu = None
        self.part_number_selection_layout = None
        self.centralwidget = None
        self.part_number_selection_widget = None

    def setupUi(self, main_window):
        icon_filepath: str = lib.Utilities.get_filepath_by_name("MvRun.ico")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(icon_filepath), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)

        main_window.setObjectName("main_window")
        main_window.resize(600, 500)
        main_window.setMinimumSize(QtCore.QSize(600, 500))
        main_window.setMaximumSize(QtCore.QSize(600, 800))

        main_window.setWindowTitle("MvRun")
        self.centralwidget = QtWidgets.QWidget(parent=main_window)
        self.centralwidget.setObjectName("centralwidget")
        self.centralwidget.setWindowIcon(icon)
        self.centrallayout = QtWidgets.QGridLayout(self.centralwidget)

        # ---------------------------------------------------------
        # Program Search And Selection Layout
        self.part_number_selection_widget = QtWidgets.QWidget(parent=self.centralwidget)
        self.part_number_selection_widget.setGeometry(QtCore.QRect(10, 10, 571, 41))
        self.part_number_selection_widget.setObjectName("part_number_selection_widget")

        self.part_number_selection_layout = QtWidgets.QGridLayout(self.part_number_selection_widget)
        self.part_number_selection_layout.setContentsMargins(0, 0, 0, 0)
        self.part_number_selection_layout.setObjectName("part_number_selection_layout")

        self.btnFind = QtWidgets.QToolButton(parent=self.part_number_selection_widget)
        self.btnFind.setObjectName("btnFind")
        self.btnFind.setText("...")
        self.part_number_selection_layout.addWidget(self.btnFind, 1, 1, 1, 1)

        self.cboRecentPrograms = QtWidgets.QComboBox(parent=self.part_number_selection_widget)
        self.cboRecentPrograms.setObjectName("cboRecentPrograms")
        self.part_number_selection_layout.addWidget(self.cboRecentPrograms, 1, 0, 1, 1)

        self.lblPartNumber = QtWidgets.QLabel(parent=self.part_number_selection_widget)
        self.lblPartNumber.setObjectName("lblPartNumber")
        self.lblPartNumber.setText("Part Number:")
        self.part_number_selection_layout.addWidget(self.lblPartNumber, 0, 0, 1, 1)
        self.part_number_selection_widget.setLayout(self.part_number_selection_layout)

        # ---------------------------------------------------------
        # Program List Layout
        self.program_list_widget = QtWidgets.QWidget(parent=self.centralwidget)
        self.program_list_widget.setGeometry(QtCore.QRect(10, 54, 261, 121))
        self.program_list_widget.setObjectName("program_list_widget")

        self.program_list_layout = QtWidgets.QGridLayout(self.program_list_widget)
        self.program_list_layout.setContentsMargins(0, 0, 0, 0)
        self.program_list_layout.setObjectName("program_list_layout")

        self.lblProgramList = QtWidgets.QLabel(parent=self.program_list_widget)
        self.lblProgramList.setObjectName("lblProgramList")
        self.lblProgramList.setText("Programs:")
        self.program_list_layout.addWidget(self.lblProgramList, 0, 0, 1, 1)

        self.lstPrograms = QtWidgets.QListWidget(parent=self.program_list_widget)
        self.lstPrograms.setObjectName("lstPrograms")
        self.program_list_layout.addWidget(self.lstPrograms, 1, 0, 1, 1)

        # ---------------------------------------------------------
        # User-Entered Fields Layout
        self.user_fields_widget = QtWidgets.QWidget(parent=self.centralwidget)
        self.user_fields_widget.setGeometry(QtCore.QRect(10, 178, 315, 100))
        self.user_fields_widget.setObjectName("user_fields_widget")

        self.user_fields_layout = QtWidgets.QGridLayout(self.user_fields_widget)
        self.user_fields_layout.setContentsMargins(0, 0, 0, 0)
        self.user_fields_layout.setObjectName("user_fields_layout")

        # Employee ID Label
        self.lblEmployeeID = QtWidgets.QLabel(parent=self.user_fields_widget)
        self.lblEmployeeID.setObjectName("lblEmployeeID")
        self.lblEmployeeID.setText("Employee ID:")
        self.user_fields_layout.addWidget(self.lblEmployeeID, 0, 0, 1, 1)

        # Employee ID Textbox
        self.txtEmployeeID = QtWidgets.QLineEdit(parent=self.user_fields_widget)
        self.txtEmployeeID.setMinimumSize(QtCore.QSize(100, 20))
        self.txtEmployeeID.setObjectName("txtEmployeeID")
        self.user_fields_layout.addWidget(self.txtEmployeeID, 0, 1, 1, 1)

        # Job Number Label
        self.lblJobNumber = QtWidgets.QLabel(parent=self.user_fields_widget)
        self.lblJobNumber.setObjectName("lblJobNumber")
        self.lblJobNumber.setText("Job Number:")
        self.user_fields_layout.addWidget(self.lblJobNumber, 1, 0, 1, 1)

        # Job Number Textbox
        self.txtJobNumber = QtWidgets.QLineEdit(parent=self.user_fields_widget)
        self.txtJobNumber.setMinimumSize(QtCore.QSize(100, 20))
        self.txtJobNumber.setObjectName("txtJobNumber")
        self.user_fields_layout.addWidget(self.txtJobNumber, 1, 1, 1, 1)

        # Machine Name Label
        self.lblMachineName = QtWidgets.QLabel(parent=self.user_fields_widget)
        self.lblMachineName.setObjectName("lblMachineName")
        self.lblMachineName.setText("Machine Name:")
        self.user_fields_layout.addWidget(self.lblMachineName, 2, 0, 1, 1)

        # Machine Name Textbox
        self.txtMachineName = QtWidgets.QLineEdit(parent=self.user_fields_widget)
        self.txtMachineName.setMinimumSize(QtCore.QSize(100, 20))
        self.txtMachineName.setObjectName("txtMachineName")
        self.user_fields_layout.addWidget(self.txtMachineName, 2, 1, 1, 1)

        # Sequence Number Label
        self.lblSequenceNumber = QtWidgets.QLabel(parent=self.user_fields_widget)
        self.lblSequenceNumber.setObjectName("lblSequenceNumber")
        self.lblSequenceNumber.setText("Sequence Number:")
        self.user_fields_layout.addWidget(self.lblSequenceNumber, 3, 0, 1, 1)

        # Sequence Number Textbox
        self.txtSequenceNumber = QtWidgets.QLineEdit(parent=self.user_fields_widget)
        self.txtSequenceNumber.setMinimumSize(QtCore.QSize(100, 20))
        self.txtSequenceNumber.setObjectName("txtSequenceNumber")
        self.user_fields_layout.addWidget(self.txtSequenceNumber, 3, 1, 1, 1)

        # ---------------------------------------------------------
        # Run Button
        self.btnRunMicroVu = QtWidgets.QPushButton(parent=self.centralwidget)
        grid.addWidget(self.button2, 0, 1, QtCore.Qt.AlignRight | QtCore.Qt.AlignBottom)
        self.btnRunMicroVu.setGeometry(QtCore.QRect(470, 450, 121, 23))
        self.btnRunMicroVu.setObjectName("btnRunMicroVu")
        self.btnRunMicroVu.setText("Run MicroVu")

        # ---------------------------------------------------------
        # Status Bar
        main_window.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(parent=main_window)
        self.statusbar.setObjectName("statusbar")
        main_window.setStatusBar(self.statusbar)

        # self.retranslateUi(main_window)
        # QtCore.QMetaObject.connectSlotsByName(main_window)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MvRun_MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MvRun_MainWindow()
    ui.setupUi(MvRun_MainWindow)
    MvRun_MainWindow.show()
    sys.exit(app.exec())
