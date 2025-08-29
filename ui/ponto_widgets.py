# perfect_acqua_system/ui/ponto_widgets.py

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget, QHeaderView,
    QTableWidgetItem, QComboBox, QDateEdit, QPushButton, QDialog
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt, QDateTime

class RegistrarPontoDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Registrar Ponto")
        self.setFixedSize(400, 250)

        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        title = QLabel("Registrar Ponto de Funcionário")
        title.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        layout.addWidget(title)
        layout.addWidget(QLabel("Selecione o Funcionário:"))
        self.combo_funcionarios = QComboBox()
        self.combo_funcionarios.addItems(["Maria Silva", "João Santos", "Ana Costa"])
        layout.addWidget(self.combo_funcionarios)
        horario_atual = QDateTime.currentDateTime().toString("dd/MM/yyyy hh:mm:ss")
        layout.addWidget(QLabel(f"Horário do Registro: {horario_atual}"))
        layout.addStretch()
        button_layout = QHBoxLayout()
        btn_confirmar = QPushButton("Confirmar Registro")
        btn_confirmar.setProperty("class", "success")
        btn_confirmar.clicked.connect(self.accept)
        btn_cancelar = QPushButton("Cancelar")
        btn_cancelar.setStyleSheet("background-color: #475569;")
        btn_cancelar.clicked.connect(self.reject)
        button_layout.addWidget(btn_cancelar)
        button_layout.addWidget(btn_confirmar)
        layout.addLayout(button_layout)

class FolhaDePonto(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setSpacing(15)

        title = QLabel("Folha de Ponto")
        title.setObjectName("Title")
        subtitle = QLabel("Controle de horários dos funcionários")
        subtitle.setObjectName("Subtitle")
        layout.addWidget(title)
        layout.addWidget(subtitle)

        top_layout = QHBoxLayout()
        filtros = QHBoxLayout()
        filtros.setSpacing(10)
        filtros.addWidget(QLabel("Funcionário:"))
        filtros.addWidget(QComboBox())
        filtros.addWidget(QLabel("Data Início:"))
        filtros.addWidget(QDateEdit(calendarPopup=True))
        filtros.addWidget(QLabel("Data Fim:"))
        filtros.addWidget(QDateEdit(calendarPopup=True))
        filtros.addStretch()
        top_layout.addLayout(filtros)
        
        btn_registrar = QPushButton("➕ Registrar ponto")
        btn_registrar.setProperty("class", "primary")
        btn_registrar.clicked.connect(self.abrir_dialog_registrar_ponto)
        top_layout.addWidget(btn_registrar)
        layout.addLayout(top_layout)

        tabela = QTableWidget()
        tabela.verticalHeader().setVisible(False)
        tabela.setColumnCount(5)
        tabela.setHorizontalHeaderLabels(["Funcionário", "Data", "Entrada", "Saída", "Horas"])
        tabela.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        dados = [
            ("👩‍💼 Maria Silva", "28/08/2025", "07:30", "17:30", "10h"),
            ("👨‍💼 João Santos", "28/08/2025", "08:00", "18:00", "10h"),
        ]
        tabela.setRowCount(len(dados))
        for row, data in enumerate(dados):
            for col, text in enumerate(data):
                item = QTableWidgetItem(text)
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                tabela.setItem(row, col, item)
        layout.addWidget(tabela)

    def abrir_dialog_registrar_ponto(self):
        dialog = RegistrarPontoDialog(self)
        dialog.exec()