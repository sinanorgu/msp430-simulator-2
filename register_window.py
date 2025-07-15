from PyQt5.QtWidgets import (
    QWidget,QVBoxLayout
)

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QLabel
        
class RegisterWindow(QWidget):
    def __init__(self, registers: dict):
        super().__init__()
        self.registers = registers
        self.setWindowTitle("Register Görünümü")
        self.resize(300, 400)

        layout = QVBoxLayout()
        self.setLayout(layout)

        label = QLabel("Mikrodenetleyici Registerları:")
        layout.addWidget(label)

        self.table = QTableWidget()
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)

        
        self.table.setRowCount(len(registers))
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Register", "Değer"])

        for row, (reg, val) in enumerate(registers.items()):
            self.table.setItem(row, 0, QTableWidgetItem(reg))
            self.table.setItem(row, 1, QTableWidgetItem(str(val)))
        
        layout.addWidget(self.table)


    def update_table(self):
        self.table.setRowCount(len(self.registers))
        for row, (reg, val) in enumerate(self.registers.items()):
            self.table.setItem(row, 0, QTableWidgetItem(reg))
            self.table.setItem(row, 1, QTableWidgetItem(str(val)))
