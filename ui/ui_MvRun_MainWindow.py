from PyQt6 import QtCore, QtWidgets


class ui_MvRun_MainWindow(object):
    def setupUi(self, MvRun_MainWindow):
        MvRun_MainWindow.setObjectName("MvRun_MainWindow")
        MvRun_MainWindow.resize(600, 250)
        MvRun_MainWindow.setMinimumSize(QtCore.QSize(600, 250))
        MvRun_MainWindow.setMaximumSize(QtCore.QSize(600, 250))
        self.centralwidget = QtWidgets.QWidget(MvRun_MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 10, 201, 81))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")

        self.lblEmployeeID = QtWidgets.QLabel(self.gridLayoutWidget)
        self.lblEmployeeID.setObjectName("lblEmployeeID")
        self.gridLayout.addWidget(self.lblEmployeeID, 0, 0, 1, 1)
        self.txtEmployeeID = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.txtEmployeeID.setObjectName("txtEmployeeID")
        self.gridLayout.addWidget(self.txtEmployeeID, 0, 1, 1, 1)

        self.lblJobNumber = QtWidgets.QLabel(self.gridLayoutWidget)
        self.lblJobNumber.setObjectName("lblJobNumber")
        self.gridLayout.addWidget(self.lblJobNumber, 1, 0, 1, 1)
        self.txtJobNumber = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.txtJobNumber.setObjectName("txtJobNumber")
        self.gridLayout.addWidget(self.txtJobNumber, 1, 1, 1, 1)

        self.lblMachineName = QtWidgets.QLabel(self.gridLayoutWidget)
        self.lblMachineName.setObjectName("lblMachineName")
        self.gridLayout.addWidget(self.lblMachineName, 2, 0, 1, 1)
        self.txtMachineName = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.txtMachineName.setObjectName("txtMachineName")
        self.gridLayout.addWidget(self.txtMachineName, 2, 1, 1, 1)

        self.lblSequenceNumber = QtWidgets.QLabel(self.gridLayoutWidget)
        self.lblSequenceNumber.setObjectName("lblSequenceNumber")
        self.gridLayout.addWidget(self.lblSequenceNumber, 3, 0, 1, 1)
        self.txtSequenceNumber = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.txtSequenceNumber.setObjectName("txtSequenceNumber")
        self.gridLayout.addWidget(self.txtSequenceNumber, 3, 1, 1, 1)

        self.gridLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(10, 100, 571, 41))
        self.gridLayoutWidget_2.setObjectName("gridLayoutWidget_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")

        self.cboRecentPrograms = QtWidgets.QComboBox(self.gridLayoutWidget_2)
        self.cboRecentPrograms.setObjectName("cboRecentPrograms")
        self.gridLayout_2.addWidget(self.cboRecentPrograms, 1, 0, 1, 1)
        self.btnFind = QtWidgets.QToolButton(self.gridLayoutWidget_2)
        self.btnFind.setObjectName("btnFind")
        self.gridLayout_2.addWidget(self.btnFind, 1, 1, 1, 1)

        self.label = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.btnRunMicroVu = QtWidgets.QPushButton(self.centralwidget)
        self.btnRunMicroVu.setGeometry(QtCore.QRect(510, 190, 75, 23))
        self.btnRunMicroVu.setObjectName("btnRunMicroVu")
        self.btnRunMicroVu.setEnabled(False)

        MvRun_MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MvRun_MainWindow)
        self.statusbar.setObjectName("statusbar")
        MvRun_MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MvRun_MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MvRun_MainWindow)

    def retranslateUi(self, MvRun_MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MvRun_MainWindow.setWindowTitle(_translate("MvRun_MainWindow", "MvRun"))
        self.lblMachineName.setText(_translate("MvRun_MainWindow", "Machine Name:"))
        self.lblJobNumber.setText(_translate("MvRun_MainWindow", "Job Number:"))
        self.lblEmployeeID.setText(_translate("MvRun_MainWindow", "Employee ID:"))
        self.lblSequenceNumber.setText(_translate("MvRun_MainWindow", "Sequence Number:"))
        self.btnFind.setText(_translate("MvRun_MainWindow", "..."))
        self.label.setText(_translate("MvRun_MainWindow", "MicroVu File:"))
        self.btnRunMicroVu.setText(_translate("MvRun_MainWindow", "Run MicroVu"))



