from typing import List

import numpy as np
from PyQt6 import QtCore
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *


class TableModel(QtCore.QAbstractTableModel):

    def __init__(self, data):
        super().__init__()
        self._data = data

    def headerData(self, section: int, orientation: Qt.Orientation, role: int):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return ["Account Number", "Available Balance"][section]

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            value = self._data[index.row()][index.column()]
            return str(value)

    def rowCount(self, index):
        return self._data.shape[0]

    def columnCount(self, index):
        return self._data.shape[1]

    def get_single_value(self, row: int, column: int):
        return self._data[row][column]

    def flags(self, index):
        return Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable

    # def update(self):
    #     self._data = controller.update()


class BankUI(QWidget):
    # def __init__(self, model: Model):
    def __init__(self, table_model: TableModel):
        super().__init__()
        self._table_model = table_model

        '''
        Main Window
        '''
        self.setWindowTitle("First National Bank of SCAG")
        self.setStyleSheet("background-color: darkgray")
        self.setFixedSize(QSize(500, 500))

        '''
        View Label
        '''
        self.view_label = QLabel(self)
        self.view_label.setGeometry(QRect(50, 0, 400, 20))
        view_label_font = QFont()
        view_label_font.setPointSize(12)
        self.view_label.setFont(view_label_font)
        self.view_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.view_label.setText("Accounts (View)")

        '''
        Account Table View
        '''
        box_dimension = 400
        self.account_table_view = QTableView(self)
        self.account_table_view.setGeometry(QRect(50, 20, box_dimension, box_dimension))
        self.account_table_view.verticalHeader().setVisible(False)
        header_stylesheet = "::section{Background-color: gainsboro; border: 1px solid black;}"
        self.account_table_view.horizontalHeader().setStyleSheet(header_stylesheet)
        self.account_table_view.setStyleSheet("QTableView::item {border-left: 1px solid gainsboro; "
                                              "border-bottom: 1px solid gainsboro; background-color: white}")
        self.account_table_view.setModel(self._table_model)

        for col in range(self._table_model.columnCount(0)):
            self.account_table_view.setColumnWidth(col, int(box_dimension / self._table_model.columnCount(0))-1)

        '''
        Controller Label
        '''
        self.controller_label = QLabel(self)
        self.controller_label.setGeometry(QRect(50, 430, 400, 20))
        controller_label_font = QFont()
        controller_label_font.setPointSize(12)
        self.controller_label.setFont(controller_label_font)
        self.controller_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.controller_label.setText("Actions (Controller)")

        '''
        Account Dropdown
        '''
        self.account_dropdown = QComboBox(self)
        self.account_dropdown.setGeometry(QRect(20, 460, 120, 20))
        self.account_dropdown.setEditable(False)
        self.account_dropdown.setModelColumn(0)
        self.account_dropdown.setStyleSheet("background-color: white")
        self.account_dropdown.addItem("Accounts", -1)
        for row in range(self._table_model.rowCount(0)):
            self.account_dropdown.addItem(self._table_model.get_single_value(row, 0))

        '''
        Transaction Type Dropdown
        '''
        self.transaction_dropdown = QComboBox(self)
        self.transaction_dropdown.setGeometry(QRect(150, 460, 120, 20))
        self.transaction_dropdown.setEditable(False)
        self.transaction_dropdown.setModelColumn(0)
        self.transaction_dropdown.setStyleSheet("background-color: white")
        self.transaction_dropdown.addItem("Transaction Type", -1)
        self.transaction_dropdown.addItem("Deposit", 0)
        self.transaction_dropdown.addItem("Withdraw", 1)

        '''
        Amount Line Edit Field
        '''
        self.amount_field = QLineEdit(self)
        self.amount_field.setGeometry(QRect(280, 460, 120, 20))
        self.amount_field.setInputMethodHints(Qt.InputMethodHint.ImhFormattedNumbersOnly)
        self.amount_field.setStyleSheet("background-color: white")  # ; border: 1px solid black")
        self.amount_field.setPlaceholderText("Amount")

        '''
        OK Button
        '''
        self.ok_button = QPushButton(self)
        self.ok_button.setGeometry(QRect(420, 460, 60, 20))
        self.ok_button.setStyleSheet("background-color: indianred")
        ok_button_font = QFont()
        ok_button_font.setPointSize(10)
        ok_button_font.setBold(True)
        self.ok_button.setFont(ok_button_font)
        self.ok_button.setText("OK")
        self.ok_button.clicked.connect(self.ok_clicked)

    def ok_clicked(self):
        acct = self.account_dropdown.currentText()
        trans_type = self.transaction_dropdown.currentText()
        amt = float(self.amount_field.text())
        # model.update_account(acct, -amt if trans_type == "Withdraw" else amt)
        

app = QApplication([])

data = np.array([("10", 245.87),
                 ("22", 4742.12),
                 ("34", 83226.42),
                 ("49", 10784.22)])

table_model = TableModel(data)
window = BankUI(table_model)

window.show()

app.exec()